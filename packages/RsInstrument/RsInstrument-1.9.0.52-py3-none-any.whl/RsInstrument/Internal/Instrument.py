import re
import threading
from enum import Enum
from typing import List, Callable, Tuple, Dict

from . import Utilities, InstrumentSettings, InstrumentOptions, InstrumentErrors, Conversions as Conv
from .ArgSingleSuppressed import ArgSingleSuppressed
from .ArgStructList import ArgStructList
from .InternalLinker import InternalLinker
from .IoTransferEventArgs import IoTransferEventArgs
from .StreamReader import StreamReader
from .StreamWriter import StreamWriter
from .Utilities import trim_str_response
from .VisaSession import VisaSession, EventArgsChunk
from .VisaSessionSim import VisaSessionSim
from .RepeatedCapability import RepeatedCapability


class Instrument(object):
	"""Model of an Instrument with VISA interface."""

	def __init__(self, resource_name: str, simulate: bool, settings: InstrumentSettings, direct_session=None):
		"""Opening an instrument session.
		If simulate is true, it cannot be later switched to false anymore."""
		self._simulating: bool = simulate
		self._session = None
		self._global_repcaps: Dict[str, RepeatedCapability] = {}
		self._linker = InternalLinker()
		# noinspection PyTypeChecker
		self.on_write_handler: Callable = None
		# noinspection PyTypeChecker
		self.on_read_handler: Callable = None
		self._io_events_include_data: bool = False
		self._lock = None

		# Fixed settings
		self.selftest_timeout = 100000 if settings.selftest_timeout == 0 else settings.selftest_timeout
		self.idn_model_full_name = settings.idn_model_full_name
		self.instr_options_parse_mode = settings.instr_options_parse_mode

		# Changeable settings
		self.resource_name: str = resource_name
		self._instr_options: InstrumentOptions = None  # Internal private property for the lazy property self.instr_options - see the getter for self.instr_options. Initialized by the first access
		self.query_instr_status: bool = True
		self.opc_query_after_write: bool = False
		self.bin_float_numbers_format = settings.bin_float_numbers_format
		self.bin_int_numbers_format = settings.bin_int_numbers_format
		self.opc_query_after_write: bool = settings.opc_query_after_write
		self.stb_in_error_check: bool = settings.stb_in_error_check

		self.manufacturer: str = 'Rohde&Schwarz'
		self.model: str = 'R&S Instrument'
		self.serial_number: str = '100001'
		self.firmware_version: str = '1.00'

		if self._simulating:
			self._session = VisaSessionSim(resource_name, settings, direct_session)
			self._lock = self._session.get_lock()
			self._instr_options = InstrumentOptions.Options('K0', InstrumentOptions.ParseMode.KeepOriginal)
			self._session.write("*OPT K0")
			return

		self._session = VisaSession(resource_name, settings, direct_session)
		self._lock = self._session.get_lock()
		with self._lock:
			self._session.clear_before_read()
			self.idn_string = Utilities.trim_str_response(self._session.query_str('*IDN?')).strip()

			# NRP-Z session coercing
			if self._session.is_rsnrp_session():
				settings.instr_options_parse_mode = InstrumentOptions.ParseMode.Skip
				self.stb_in_error_check = False
			self.instr_options_parse_mode = settings.instr_options_parse_mode

	def __str__(self):
		if self._simulating:
			return f"Simulated, Model: '{self.model}', ResourceName: '{self.resource_name}'"
		else:
			return f"Instrument Model: '{self.model}', ResourceName: '{self.resource_name}'"

	def set_simulating_cmds(self) -> None:
		"""Updated cached values in the simulating VISA session to properly respond to *IDN? or *OPT?"""
		if self._simulating:
			self.write(f'*idn {self.idn_string}')
			self.write(f'*opt {Conv.list_to_csv_str(self.instr_options.get_all())}')
			self.write(f'*opc 1')
			self.write(f'*stb 0')
			self.write(f'*tst 0,"Passed"')
			self.write(f'syst:err 0,"No Error"')
			self.write(f'system:error 0,"No Error"')

	def get_last_sent_cmd(self) -> str:
		"""Returns the last commands sent to the instrument. Only works in simulation mode"""
		if self._simulating:
			# noinspection PyUnresolvedReferences
			return self._session.get_last_sent_cmd()
		raise Exception("get_last_sent_cmd() can only be used in simulation mode")

	def assign_lock(self, lock: threading.RLock) -> None:
		"""Assigns the thread lock provided from by the user. Trickles down to the VisaSession."""
		self._lock = lock
		self._session.assign_lock(lock)

	def get_lock(self) -> threading.RLock:
		"""Returns the current RLock object."""
		return self._lock

	def clear_lock(self):
		"""Clears the existing thread lock, making the current session thread-independent from others that might share the current thread lock."""
		self.assign_lock(threading.RLock())

	@property
	def visa_manufacturer(self) -> str:
		"""Returns the visa manufacturer of the current session."""
		return self._session.manufacturer

	def set_link_handler(self, link_name: str, handler: Callable) -> Callable:
		"""Adds / Updates link handler for the entered link_name.
		Handler API: handler(event_args: ArgLinkedEventArgs)
		Returns the previous registered handler, or None if no handler was registered before."""
		return self._linker.set_handler(link_name, handler)

	def del_link_handler(self, link_name: str) -> Callable:
		"""Deletes link handler for the link_name.
		Returns the deleted handler, or None if none existed."""
		return self._linker.del_handler(link_name)

	def del_all_link_handlers(self) -> int:
		"""Deletes all the link handlers.
		Returns number of deleted links."""
		return self._linker.del_all_handlers()

	@property
	def idn_string(self) -> str:
		return self._idn_string

	@idn_string.setter
	def idn_string(self, value: str) -> None:
		"""IDN string. Set it to force a different IDN string than the default *IDN? response."""
		self._idn_string = value
		self._parse_idn_string(self._idn_string)

	@property
	def instr_options(self) -> InstrumentOptions:
		"""Public getter for the lazy property instr_options"""
		if self._instr_options is None:
			self._query_options_and_parse(self.instr_options_parse_mode)
		return self._instr_options

	@property
	def opc_timeout(self) -> int:
		"""See the opc_timeout.setter."""
		return self._session.opc_timeout

	@opc_timeout.setter
	def opc_timeout(self, value: int) -> None:
		"""Sets / Gets timeout in milliseconds for all the operations that use OPC synchronization."""
		self._session.opc_timeout = value

	@property
	def visa_timeout(self) -> int:
		"""See the visa_timeout.setter."""
		return self._session.visa_timeout

	@visa_timeout.setter
	def visa_timeout(self, value: int) -> None:
		"""Sets / Gets visa IO timeout in milliseconds."""
		self._session.visa_timeout = value

	@property
	def data_chunk_size(self) -> int:
		"""Returns max chunk size of one data block."""
		return self._session.data_chunk_size

	@data_chunk_size.setter
	def data_chunk_size(self, chunk_size: int) -> None:
		"""Sets the maximum size of one block transferred during write/read operations."""
		self._session.data_chunk_size = int(chunk_size)

	# noinspection PyMethodMayBeStatic
	def _sim_cached_value_found(self, value) -> bool:
		return value != 'Simulating'

	# noinspection PyMethodMayBeStatic
	def _sim_cached_value_not_found(self, value) -> bool:
		return value == 'Simulating'

	def _parse_idn_string(self, idn_string: str) -> None:
		"""Parse the *IDN? response to:
		- Manufacturer
		- Model
		- SerialNumber
		- FirmwareRevision"""
		idn_string = idn_string.strip()
		m = re.search(r'([\w& ]+),([a-zA-Z ]+)([\-0-9a-zA-Z ]*),([^,]+),([\w .\-/]+)', idn_string)
		if not m:
			raise Exception(f"The instrument *IDN? string parsing failed. Parsed *IDN? response: '{idn_string}'")
		self.manufacturer = m.group(1).strip()
		self.model = m.group(2).strip()
		self.full_model_name = self.model + m.group(3).strip()
		self.serial_number = m.group(4).strip()
		self.firmware_version = m.group(5).strip()
		if self.idn_model_full_name:
			self.model = self.full_model_name

	def fits_idn_pattern(self, patterns: List[str], supported_models: List[str]) -> None:
		"""Throws exception if the current instrument model does not fit  any of the patterns.
		The supported_models argument is only used for exception messages"""
		matches = False
		assert self._idn_string, f'*IDN? was not assigned yet.'
		for x in patterns:
			matches = re.search(x, self.idn_string, re.IGNORECASE)
			if matches:
				break
		if not matches:
			message = f"Instrument is not supported.\n*IDN? string: '{self.idn_string}'"
			if len(supported_models) > 0:
				message += f"\nSupported models: '{', '.join(supported_models)}'"
			if len(patterns) == 1:
				message += f"\nSupported IDN pattern: '{patterns[0]}'"
			if len(patterns) > 1:
				message += "\nSupported IDN patterns:\n" + '\n'.join(patterns)
			raise InstrumentErrors.UnexpectedResponseException(self.resource_name, message)

	def _query_options_and_parse(self, mode: InstrumentOptions.ParseMode) -> None:
		"""Queries *OPT? and parses it based on the ParseMode."""
		if mode == InstrumentOptions.ParseMode.Skip:
			self._instr_options = InstrumentOptions.Options('', mode)
			return
		if self._simulating is False:
			with self._lock:
				opts = self._session.query_str_no_tout_err('*OPT?', 1000)
				if opts is None:
					opts = 'Cannot read the instrument options - *OPT? query is not supported'
				self._instr_options = InstrumentOptions.Options(opts, mode)

	@staticmethod
	def _parse_err_query_response(response: str) -> str:
		"""Parses entered response string to string error message without the error code.
		E.g.: response = '-110,"Command error"' returns: 'Command error'."""
		m = re.match(r'(-?[\d]+).*?"(.*)"', response)
		if m:
			return m.group(2)
		else:
			return response

	def add_global_repcap(self, name: str, rep_cap: RepeatedCapability) -> None:
		"""Adds the global repcap name to the list of global repcaps
		and sets its value to the provided default value."""
		if name in self._global_repcaps:
			raise Exception(f"Error adding new global repcap: '{name}' already exists in the list.")
		self._global_repcaps[name] = rep_cap

	def set_global_repcap_value(self, name: str, enum_value: Enum) -> None:
		"""Updates the existing global repcap value as enum"""
		if name not in self._global_repcaps:
			raise Exception(f"Error updating global repcap: '{name}' does not exist in the list.")
		self._global_repcaps[name].set_enum_value(enum_value)

	def get_global_repcap_value(self, name: str) -> Enum:
		"""Returns the current global repcap value as enum"""
		if name not in self._global_repcaps:
			raise Exception(f"Error retrieving global repcap: '{name}' does not exist in the list.")
		return self._global_repcaps[name].get_enum_value()

	def _replace_global_repcaps(self, cmd: str) -> str:
		"""Replaces all the global repcaps in the command: e.g. '<instance>' => '1'.
		Returns the replaced command."""
		for name, value in self._global_repcaps.items():
			cmd_value = value.get_cmd_string_value()
			cmd = cmd.replace(name, cmd_value)
		return cmd

	def query_opc(self) -> bool:
		"""Sends *OPC? query and returns the result."""
		with self._lock:
			self.start_send_read_event('*OPC?', False)
			opc: bool = self._session.query_opc()
			self.end_send_read_event()
			return opc

	def query_all_syst_errors(self, include_codes=True) -> List[str]:
		"""Returns all errors in the instrument's error queue.
		If include_codes is False, you only get the error messages without the error codes."""
		with self._lock:
			self.start_send_read_event('SYST:ERROR?', False)
			errors = self._session.query_all_syst_errors()
			if include_codes is False and errors is not None:
				errors = [self._parse_err_query_response(x) for x in errors]
			self.end_send_read_event()
			return errors

	def check_status(self) -> None:
		"""Throws InstrumentStatusException in case of an error in the instrument's error queue.
		The procedure is skipped, if the QueryInstrumentStatus is set to false."""
		with self._lock:
			if not self.query_instr_status:
				return
			call_syst_error = self._session.error_in_error_queue() if self.stb_in_error_check else True
			if call_syst_error:
				errors = self.query_all_syst_errors(False)
				InstrumentErrors.assert_no_instrument_status_errors(self.resource_name, errors)

	def clear_status(self) -> None:
		"""Clears instrument's status subsystem."""
		with self._lock:
			self._session.clear()
			self._session.clear_before_read()

	def reset(self) -> None:
		"""Resets the instrument and clears its status."""
		with self._lock:
			self.write("*RST")
			self.query_opc()
			self.clear_status()
			self.check_status()

	def write(self, cmd: str) -> None:
		"""Writes string command to the instrument."""
		with self._lock:
			cmd = self._replace_global_repcaps(cmd)
			self._session.write(cmd)
			if self.opc_query_after_write:
				self._session.query_opc()
			if self.on_write_handler:
				self.send_write_str_event(cmd, False)
			self.check_status()

	def write_with_opc(self, cmd: str, timeout: int = None) -> None:
		"""Writes a OPC-synced command.
		Also performs error checking if the property self.query_instr_status is set to True.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			cmd = self._replace_global_repcaps(cmd)
			self._session.write_with_opc(cmd, timeout)
			self._session.query_and_clear_esr()
			if self.on_write_handler:
				self.send_write_str_event(cmd, True)
			self.check_status()

	def write_struct(self, cmd: str, struct: object) -> None:
		"""Writes command to the instrument with the parameter composed from the entered structure."""
		with self._lock:
			worker = ArgStructList(struct)
			param = worker.compose_cmd_string()
			cmd += f' {param}'.rstrip()
			self.write(cmd)

	def write_struct_with_opc(self, cmd: str, struct: object, timeout: int = None) -> None:
		"""Writes OPC-synced command to the instrument with the parameter composed from the entered structure.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			worker = ArgStructList(struct)
			param = worker.compose_cmd_string()
			cmd += f' {param}'.rstrip()
			self.write_with_opc(cmd, timeout)

	def query_str(self, query: str) -> str:
		"""Sends a query and reads response from the instrument.
		The response is trimmed of any trailing LF characters and has no length limit."""
		with self._lock:
			query = self._replace_global_repcaps(query)
			self.start_send_read_event(query, False)
			response = self._session.query_str(query)
			self.end_send_read_event()
			self.check_status()
			return response

	def query_str_with_opc(self, query: str, timeout: int = None) -> str:
		"""Sends a OPC-synced query.
		Also performs error checking if the self.query_instr_status is true.
		The response is trimmed of any trailing LF characters and has no length limit.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			query = self._replace_global_repcaps(query)
			self.start_send_read_event(query, True)
			response = self._session.query_str_with_opc(query, timeout)
			self.end_send_read_event()
			self._session.query_and_clear_esr()
			self.check_status()
			return response

	def query_bin_block_to_stream(self, query: str, stream: StreamWriter) -> None:
		"""Queries binary data block to the provided stream.
		Use it for querying data from instrument to a variable or a file.
		Throws an exception if the returned data was not a binary data."""
		with self._lock:
			query = self._replace_global_repcaps(query)
			self.start_send_read_event(query, False)
			self._session.query_bin_block(query, stream, True)
			self.end_send_read_event()
			self.check_status()

	def query_bin_block(self, query: str) -> bytes:
		"""Queries binary data block to bytes and returns data as bytes.
		Throws an exception if the returned data was not a binary data."""
		with self._lock:
			writer = StreamWriter.as_bin_var()
			self.query_bin_block_to_stream(query, writer)
			return writer.content

	def query_bin_block_to_file(self, cmd: str, file_path: str, append: bool = False) -> None:
		"""Queries binary data block to the provided file.
		If append is False, any existing file content is discarded.
		If append is True, the new content is added to the end of the existing file, or if the file does not exit, it is created.
		Throws an exception if the returned data was not a binary data."""
		with self._lock:
			with StreamWriter.as_bin_file(file_path, append) as writer:
				self.query_bin_block_to_stream(cmd, writer)

	def query_bin_block_to_stream_with_opc(self, query: str, stream: StreamWriter, timeout: int = None) -> None:
		"""Sends a OPC-synced query and returns data the provided stream.
		Use it for querying data from instrument to a variable or a file.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			query = self._replace_global_repcaps(query)
			self.start_send_read_event(query, True)
			self._session.query_bin_block_with_opc(query, stream, True, timeout)
			self.end_send_read_event()
			self._session.query_and_clear_esr()
			self.check_status()

	def query_bin_block_with_opc(self, query: str, timeout: int = None) -> bytes:
		"""Sends a OPC-synced query and returns data as bytes.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			with StreamWriter.as_bin_var() as stream:
				self.query_bin_block_to_stream_with_opc(query, stream, timeout)
				return stream.content

	def query_bin_block_to_file_with_opc(self, cmd: str, file_path: str, append: bool = False, timeout: int = None) -> None:
		"""Sends a OPC-synced query and writes the returned data to the provided file.
		If append is False, any existing file content is discarded.
		If append is True, the new content is added to the end of the existing file, or if the file does not exit, it is created.
		Throws an exception if the returned data was not a binary data."""
		with self._lock:
			with StreamWriter.as_bin_file(file_path, append) as writer:
				self.query_bin_block_to_stream_with_opc(cmd, writer, timeout)

	def query_int(self, query: str) -> int:
		"""Sends a query and reads response from the instrument as integer."""
		with self._lock:
			string = self.query_str(query)
			if self._simulating and self._sim_cached_value_not_found(string):
				return 0
			return Conv.str_to_int(string)

	def query_int_with_opc(self, query: str, timeout: int = None) -> int:
		"""Sends a OPC-synced query and reads response from the instrument as integer number.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			string = self.query_str_with_opc(query, timeout)
			if self._simulating and self._sim_cached_value_not_found(string):
				return 0
			return Conv.str_to_int(string)

	def query_float(self, query: str) -> float:
		"""Sends a query and reads response from the instrument as float number."""
		with self._lock:
			string = self.query_str(query)
			if self._simulating and self._sim_cached_value_not_found(string):
				return 0.0
			return Conv.str_to_float(string)

	def query_float_with_opc(self, query: str, timeout: int = None) -> float:
		"""Sends a OPC-synced query and reads response from the instrument as float number.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			string = self.query_str_with_opc(query, timeout)
			if self._simulating and self._sim_cached_value_not_found(string):
				return 0.0
			return Conv.str_to_float(string)

	def query_bool(self, query: str) -> bool:
		"""Sends a query and reads response from the instrument as boolean value."""
		with self._lock:
			string = self.query_str(query)
			if self._simulating and self._sim_cached_value_not_found(string):
				return False
			return Conv.str_to_bool(string)

	def query_bool_with_opc(self, query: str, timeout: int = None) -> bool:
		"""Sends a OPC-synced query and reads response from the instrument as boolean value.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			string = self.query_str_with_opc(query, timeout)
			if self._simulating and self._sim_cached_value_not_found(string):
				return False
			return Conv.str_to_bool(string)

	def query_str_list(self, query: str) -> List[str]:
		"""Sends a query and reads response from the instrument as csv-list."""
		with self._lock:
			string = self.query_str(query)
			if self._simulating and self._sim_cached_value_not_found(string):
				string = 'AAA,BBB,CCC,DDD,EEE,FFF,GGG,HHH,III,JJJ'
			response = [trim_str_response(x) for x in string.split(',')]
			return response

	def query_str_list_with_opc(self, query: str, timeout: int = None) -> List[str]:
		"""Sends a OPC-synced query and reads response from the instrument as csv-list.
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			string = self.query_str_with_opc(query, timeout)
			if self._simulating and self._sim_cached_value_not_found(string):
				string = 'AAA,BBB,CCC,DDD,EEE,FFF,GGG,HHH,III,JJJ'
			response = [trim_str_response(x) for x in string.split(',')]
			return response

	def write_bin_block_from_stream(self, cmd: str, stream: StreamReader) -> None:
		"""Writes all the stream content as binary data block to the instrument.
		Use it for writing data to instrument from a variable or a file.
		The binary data header is added at the beginning of the transmission automatically, do not include it in the payload!!!"""
		with self._lock:
			if self.on_write_handler:
				self.start_send_write_bin_event(cmd)
			self._session.write_bin_block(cmd, stream)
			self.end_send_write_bin_event()
			self.check_status()

	def write_bin_block(self, cmd: str, payload: bytes) -> None:
		"""Writes all the payload as binary data block to the instrument.
		The binary data header is added at the beginning of the transmission automatically, do not include it in the payload!!!"""
		self.write_bin_block_from_stream(cmd, StreamReader.as_bin_var(payload))

	def write_bin_block_from_file(self, cmd: str, file_path: str) -> None:
		"""Writes all the file content as binary data block to the instrument.
		The binary data header is added at the beginning of the transmission automatically, do not include it in the file content!!!"""
		with StreamReader.as_bin_file(file_path) as reader:
			self.write_bin_block_from_stream(cmd, reader)

	def query_bin_or_ascii_float_list(self, query: str) -> List[float]:
		"""Queries a list of floating-point numbers that can be returned in ASCII format or in binary format.
		- For ASCII format, the list numbers are decoded as comma-separated values.
		- For Binary Format, the numbers are decoded based on the property BinFloatFormat, usually float 32-bit (FORM REAL,32)."""
		with self._lock:
			query = self._replace_global_repcaps(query)
			self.start_send_read_event(query, False)
			stream = StreamWriter.as_bin_var()
			self._session.query_bin_block(query, stream, False)
			self.end_send_read_event()
			if self._simulating and not self._session.cached_to_stream:
				return [0.1, 1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9, 9.1, 10.2]
			if stream.binary:
				result = Conv.bytes_to_list_of_floats(stream.content, self.bin_float_numbers_format)
			else:
				result = Conv.str_to_float_list(stream.content)
			self.check_status()
			return result

	def query_bin_or_ascii_float_list_with_opc(self, query: str, timeout: int = None) -> List[float]:
		"""Sends a OPC-synced query and reads a list of floating-point numbers that can be returned in ASCII format or in binary format.
		- For ASCII format, the list numbers are decoded as comma-separated values.
		- For Binary Format, the numbers are decoded based on the property BinFloatFormat, usually float 32-bit (FORM REAL,32).
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			query = self._replace_global_repcaps(query)
			self.start_send_read_event(query, True)
			stream = StreamWriter.as_bin_var()
			self._session.query_bin_block_with_opc(query, stream, False, timeout)
			self.end_send_read_event()
			if self._simulating and not self._session.cached_to_stream:
				return [0.1, 1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9, 9.1, 10.2]
			if stream.binary:
				result = Conv.bytes_to_list_of_floats(stream.content, self.bin_float_numbers_format)
			else:
				result = Conv.str_to_float_list(stream.content)
			self._session.query_and_clear_esr()
			self.check_status()
			return result

	def query_bin_or_ascii_float_list_suppressed(self, query: str, suppressed: ArgSingleSuppressed) -> List[float]:
		"""Queries string of unknown size from instrument, and returns the part without the suppressed argument as list of floats.
		The current implementation allows for the rest of the string to be only ASCII format."""
		with self._lock:
			string = self.query_str(query)
			if self._simulating and self._sim_cached_value_not_found(string):
				return [0.1, 1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9, 9.1, 10.2]
			response = self._linker.cut_from_response_string(suppressed, string, query)
			return Conv.str_to_float_list(response)

	def query_bin_or_ascii_float_list_suppressed_with_opc(self, query: str, suppressed: ArgSingleSuppressed, timeout: int = None) -> List[float]:
		"""Queries string of unknown size from instrument, and returns the part without the suppressed argument as list of floats.
		If you do not provide timeout, the method uses current opc_timeout.
		The current implementation allows for the rest of the string to be only ASCII format."""
		with self._lock:
			string = self.query_str_with_opc(query, timeout)
			if self._simulating and self._sim_cached_value_not_found(string):
				return [0.1, 1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9, 9.1, 10.2]
			response = self._linker.cut_from_response_string(suppressed, string, query)
			return Conv.str_to_float_list(response)

	def query_bin_or_ascii_int_list(self, query: str) -> List[int]:
		"""Queries a list of integer numbers that can be returned in ASCII format or in binary format.
		- For ASCII format, the list numbers are decoded as comma-separated values.
		- For Binary Format, the numbers are decoded based on the property BinIntFormat, usually int 32-bit (FORM REAL,32)."""
		with self._lock:
			query = self._replace_global_repcaps(query)
			self.start_send_read_event(query, False)
			stream = StreamWriter.as_bin_var()
			self._session.query_bin_block(query, stream, False)
			self.end_send_read_event()
			if self._simulating and not self._session.cached_to_stream:
				return [1, 2, 3, 5, 10, 15, 20, 30, 50, 100]
			if stream.binary:
				result = Conv.bytes_to_list_of_integers(stream.content, self.bin_int_numbers_format)
			else:
				result = Conv.str_to_int_list(stream.content)
			self.check_status()
			return result

	def query_bin_or_ascii_int_list_with_opc(self, query: str, timeout: int = None) -> List[int]:
		"""Sends a OPC-synced query and reads a list of integer numbers that can be returned in ASCII format or in binary format.
		- For ASCII format, the list numbers are decoded as comma-separated values.
		- For Binary Format, the numbers are decoded based on the property BinIntFormat, usually int 32-bit (FORM REAL,32).
		If you do not provide timeout, the method uses current opc_timeout."""
		with self._lock:
			query = self._replace_global_repcaps(query)
			self.start_send_read_event(query, True)
			stream = StreamWriter.as_bin_var()
			self._session.query_bin_block_with_opc(query, stream, False, timeout)
			self.end_send_read_event()
			if self._simulating and not self._session.cached_to_stream:
				return [1, 2, 3, 5, 10, 15, 20, 30, 50, 100]
			if stream.binary:
				result = Conv.bytes_to_list_of_integers(stream.content, self.bin_int_numbers_format)
			else:
				result = Conv.str_to_int_list(stream.content)
			self._session.query_and_clear_esr()
			self.check_status()
			return result

	def query_bin_or_ascii_int_list_suppressed(self, query: str, suppressed: ArgSingleSuppressed) -> List[int]:
		"""Queries string of unknown size from instrument, and returns the part without the suppressed argument as list of integers.
		The current implementation allows for the rest of the string to be only ASCII format."""
		with self._lock:
			response = self.query_str(query)
			if self._simulating:
				return [1, 2, 3, 5, 10, 15, 20, 30, 50, 100]
			response = self._linker.cut_from_response_string(suppressed, response, query)
			return Conv.str_to_int_list(response)

	def query_bin_or_ascii_int_list_suppressed_with_opc(self, query: str, suppressed: ArgSingleSuppressed, timeout: int = None) -> List[int]:
		"""Queries string of unknown size from instrument, and returns the part without the suppressed argument as list of integers.
		If you do not provide timeout, the method uses current opc_timeout.
		The current implementation allows for the rest of the string to be only ASCII format."""
		with self._lock:
			response = self.query_str_with_opc(query, timeout)
			if self._simulating:
				return [1, 2, 3, 5, 10, 15, 20, 30, 50, 100]
			response = self._linker.cut_from_response_string(suppressed, response, query)
			return Conv.str_to_int_list(response)

	def query_struct(self, query: str, struct: object) -> object:
		"""Queries string of from instrument, and parses it based on the provided structure object.
		THe method returns the copy of the entered object that it had modified."""
		with self._lock:
			string = self.query_str(query)
			if self._simulating and self._sim_cached_value_not_found(string):
				return struct
			struct_list = ArgStructList(struct)
			struct_list.parse_from_cmd_response(string)
			self._linker.invoke_struct_intern_links(struct, struct_list.args, query)
			return struct

	def query_str_suppressed(self, query: str, suppressed: ArgSingleSuppressed) -> str:
		"""Queries string of unknown size from instrument, and returns the part without the suppressed argument."""
		with self._lock:
			string = self.query_str(query)
			if self._simulating and self._sim_cached_value_not_found(string):
				return string
			response = self._linker.cut_from_response_string(suppressed, string, query)
			return response

	def self_test(self, timeout: int = None) -> Tuple[int, str]:
		"""Performs instrument's selftest (*TST?).
		Returns tuple (code:int, message: str). . Code 0 means the self-test passed.
		You can define the custom timeout in milliseconds. If you do not define it, the default selftest timeout is used (usually 60 secs)."""
		with self._lock:
			if timeout is None or timeout == 0:
				timeout = self.selftest_timeout
			response = self.query_str_with_opc('*TST?', timeout)
			m = re.search(r'^(-?[\d]+)(,(.*))?', response)
			if not m:
				raise InstrumentErrors.UnexpectedResponseException(self.resource_name, f"Unexpected response to a '*TST?' self-test query: '{response}'")
			code = Conv.str_to_int(m.group(1))
			msg = Utilities.trim_str_response(m.group(3))
			self.check_status()
			return code, msg

	def get_session_handle(self) -> object:
		"""Returns the underlying pyvisa session."""
		return self._session.get_session_handle()

	def close(self) -> None:
		"""Closes the Instrument session."""
		with self._lock:
			self._session.close()
			self._session = None

	# Events part

	@property
	def io_events_include_data(self) -> bool:
		"""If true, the read and write handlers also include read and written data."""
		return self._io_events_include_data

	@io_events_include_data.setter
	def io_events_include_data(self, value: bool) -> None:
		"""If true, the read and write handlers also include read and written data."""
		self._io_events_include_data = value
		self._session.io_events_include_data = value

	def event_args_append_instr_info(self, args: IoTransferEventArgs) -> IoTransferEventArgs:
		"""Appends instrument-related information to the read/write event argument"""
		args.chunk_size = self.data_chunk_size
		args.resource_name = self.resource_name
		return args

	def send_write_str_event(self, cmd: str, opc_sync: bool) -> None:
		"""Creates and sends write string event. The transfer is marked as done (end_of_transfer = True)."""
		args = IoTransferEventArgs.write_str(opc_sync, len(cmd), cmd)
		args.transferred_size = args.total_size
		args.chunk_ix = 0
		args.end_of_transfer = True
		args = self.event_args_append_instr_info(args)
		if self._io_events_include_data:
			args.data = cmd
		self.on_write_handler(args)

	def start_send_read_event(self, query: str, opc_sync: bool) -> None:
		"""Registers VisaSession.on_read_chunk_handler() which then generates events with each chunk transfer.
		Event handler for these events is the local function of this method, which sends IoTransferEventArgs further up to the Instrument.on_read_handler()"""
		if not self.on_read_handler:
			return

		def _read_chunk_handler(visa_args: EventArgsChunk) -> None:
			"""Receives events from VisaSession on read chunk transfers, and sends them as IoTransferEventArgs to the Instrument.on_read_handler()"""
			args.end_of_transfer = visa_args.end_of_transfer
			args.chunk_ix = visa_args.chunk_ix
			args.total_chunks = visa_args.total_chunks
			args.chunk_size = visa_args.chunk_size
			args.transferred_size = visa_args.transferred_size
			args.total_size = visa_args.total_size
			args.data = visa_args.data
			args.binary = visa_args.binary
			self.on_read_handler(args)

		args = IoTransferEventArgs.read_chunk(opc_sync, query)
		args = self.event_args_append_instr_info(args)
		self._session.on_read_chunk_handler = _read_chunk_handler

	def end_send_read_event(self):
		"""Unregisters VisaSession.on_read_chunk_handler()"""
		self._session.on_read_chunk_handler = None

	def start_send_write_bin_event(self, cmd: str) -> None:
		"""Registers VisaSession.on_write_chunk_handler() which then generates events with each chunk transfer.
		Event handler for these events is the local function of this method, which sends IoTransferEventArgs further up to the Instrument.on_write_handler()"""
		if not self.on_write_handler:
			return

		def _write_chunk_handler(visa_args: EventArgsChunk) -> None:
			"""Receives events from VisaSession on write chunk transfers, and sends them as IoTransferEventArgs to the Instrument.on_write_handler()"""
			args.end_of_transfer = visa_args.end_of_transfer
			args.chunk_ix = visa_args.chunk_ix
			args.total_chunks = visa_args.total_chunks
			args.chunk_size = visa_args.chunk_size
			args.transferred_size = visa_args.transferred_size
			args.total_size = visa_args.total_size
			args.data = visa_args.data
			args.binary = visa_args.binary
			self.on_write_handler(args)

		args = IoTransferEventArgs.write_bin(cmd)
		args = self.event_args_append_instr_info(args)
		self._session.on_write_chunk_handler = _write_chunk_handler

	def end_send_write_bin_event(self):
		"""Unregisters VisaSession.on_write_chunk_handler()"""
		self._session.on_write_chunk_handler = None
