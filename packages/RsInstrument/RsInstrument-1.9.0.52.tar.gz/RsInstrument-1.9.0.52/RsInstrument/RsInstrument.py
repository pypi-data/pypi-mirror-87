import threading
from typing import List, Tuple

from .Fixed_Files import Events
from .Internal.Core import Core
from .Internal.Conversions import BinFloatFormat, BinIntFormat
from .Internal import Conversions as Conv
from .Internal.VisaSession import VisaSession


class RsInstrument:
	_driver_version_const = '1.9.0.52'
	_driver_options_const = "SupportedInstrModels = All Rohde & Schwarz Instruments, SupportedIdnPatterns = Rohde(-|&)Schwarz/Hameg, SimulationIdnString = Rohde&Schwarz*SimulationDevice*100001*" + _driver_version_const

	def __init__(
			self, resource_name: str, id_query: bool = True, reset: bool = False, options: str = None, direct_session: object = None):
		"""Initializes new RsInstrument session. \n
		Parameter options tokens examples:
			- 'Simulate=True' - starts the session in simulation mode. Default: False
			- 'SelectVisa=socket' - uses no VISA implementation for socket connections - you do not need any VISA-C installation
			- 'SelectVisa=rs' - forces usage of RohdeSchwarz Visa
			- 'SelectVisa=ni' - forces usage of National Instruments Visa
			- 'QueryInstrumentStatus = False' - same as driver.utilities.instrument_status_checking = False. Default: True.
			- 'DriverSetup=(WriteDelay = 20, ReadDelay = 5)' - Introduces delay of 20ms before each write and 5ms before each read. Default: 0ms for both
			- 'DriverSetup=(OpcWaitMode = OpcQuery)' - mode for all the opc-synchronised write/reads. Other modes: StbPolling, StbPollingSlow, StbPollingSuperSlow. Default: StbPolling
			- 'DriverSetup=(AddTermCharToWriteBinBLock = True)' - Adds one additional LF to the end of the binary data (some instruments require that). Default: False
			- 'DriverSetup=(AssureWriteWithTermChar = True)' - Makes sure each command/query is terminated with termination character. Default: Interface dependent
			- 'DriverSetup=(TerminationCharacter = '\n')' - Sets the termination character for reading. Default: '\n' (LineFeed)
			- 'DriverSetup=(IoSegmentSize = 10E3)' - Maximum size of one write/read segment. If transferred data is bigger, it is split to more segments. Default: 1E6 bytes
			- 'DriverSetup=(OpcTimeout = 10000)' - same as driver.utilities.opc_timeout = 10000. Default: 30000ms
			- 'DriverSetup=(VisaTimeout = 5000)' - same as driver.utilities.visa_timeout = 5000. Default: 10000ms
			- 'DriverSetup=(ViClearExeMode = 255)' - Binary combination where 1 means performing viClear() on a certain interface as the very first command in init
			- 'DriverSetup=(OpcQueryAfterWrite = True)' - same as driver.utilities.opc_query_after_write = True. Default: False
		:param resource_name: VISA resource name, e.g. 'TCPIP::192.168.2.1::INSTR'
		:param id_query: if True: the instrument's model name is verified against the models supported by the driver and eventually throws an exception
		:param reset: Resets the instrument (sends *RST) command and clears its status syb-system
		:param options: string tokens alternating the driver settings
		:param direct_session: Another driver object or pyVisa object to reuse the session instead of opening a new session"""

		self._core = Core(resource_name, id_query, reset, RsInstrument._driver_options_const, options, direct_session)
		self._core.driver_version = RsInstrument._driver_version_const
		self._custom_properties_init()

	@classmethod
	def from_existing_session(cls, session: object, options: str = None) -> 'RsInstrument':
		"""Creates a new RsInstrument object with the entered 'session' reused.
		:param session: can be an another driver or a direct pyvisa session.
		:param options: string tokens alternating the driver settings."""
		# noinspection PyTypeChecker
		return cls(None, False, False, options, session)

	def __str__(self):
		if self._core.io:
			return f"RsInstrument session '{self._core.io.resource_name}'"
		else:
			return f"RsInstrument with session closed"

	def close(self) -> None:
		"""Closes the active RsInstrument session"""
		self._core.io.close()

	@staticmethod
	def list_resources(expression: str = '?*::INSTR', visa_select: str = None) -> List[str]:
		"""Finds all the resources defined by the expression
			- '?*' - matches all the available instruments
			- 'USB::?*' - matches all the USB instruments
			- "TCPIP::192?*' - matches all the LAN instruments with the IP address starting with 192
		:param expression: see the examples in the function
		:param visa_select: optional parameter selecting a specific VISA. Examples: '@ni', '@rs'
		"""
		rm = VisaSession.get_resource_manager(visa_select)
		resources = rm.list_resources(expression)
		rm.close()
		return resources

	def get_session_handle(self):
		"""Returns the underlying pyvisa session"""
		return self._core.get_session_handle()

	def _custom_properties_init(self) -> None:
		"""Adds all the interfaces that are custom for the driver"""
		self.events = Events.Events(self._core)

	# Utilities part follows - copy it manually fro  the Utilities.py file
	@property
	def driver_version(self) -> str:
		"""Returns the instrument driver version"""
		return self._core.driver_version

	@property
	def idn_string(self) -> str:
		"""SCPI Command: *IDN?
		Returns instrument's Identification string"""
		return self._core.io.idn_string

	@property
	def manufacturer(self) -> str:
		"""Returns manufacturer of the instrument"""
		return self._core.io.manufacturer

	@property
	def full_instrument_model_name(self) -> str:
		"""Returns the current instrument's full name e.g. 'FSW26'"""
		return self._core.io.full_model_name

	@property
	def instrument_model_name(self) -> str:
		"""Returns the current instrument's family name e.g. 'FSW'"""
		return self._core.io.model

	@property
	def supported_models(self) -> List[str]:
		"""Returns a list of the instrument models supported by this instrument driver"""
		return self._core.supported_instr_models

	@property
	def instrument_firmware_version(self) -> str:
		"""Returns instrument's firmware version"""
		return self._core.io.firmware_version

	@property
	def instrument_serial_number(self) -> str:
		"""Returns instrument's serial_number"""
		return self._core.io.serial_number

	def query_opc(self) -> int:
		"""SCPI command: *OPC?
		Queries the instrument's OPC bit and hence it waits until the instrument reports operation complete"""
		return self._core.io.query_opc()

	@property
	def instrument_status_checking(self) -> bool:
		"""See the instrument_status_checking.setter"""
		return self._core.io.query_instr_status

	@instrument_status_checking.setter
	def instrument_status_checking(self, value) -> None:
		"""Sets / Gets Instrument Status Checking.
		When True (default is True), all the driver methods and properties are sending "SYST:ERR?"
		at the end to immediately react on error that might have occurred.
		We recommend to keep the state checking ON all the time. Switch it OFF only in rare cases when you require maximum speed.
		The default state after initializing the session is ON."""
		self._core.io.query_instr_status = value

	@property
	def opc_query_after_write(self) -> bool:
		"""See the opc_query_after_write.setter"""
		return self._core.io.opc_query_after_write

	@opc_query_after_write.setter
	def opc_query_after_write(self, value) -> None:
		"""Sets / Gets Instrument *OPC? query sending after each command write.
		When True, (default is False) the driver sends *OPC? every time a write command is performed.
		Use this if you want to make sure your sequence is performed command-after-command."""
		self._core.io.opc_query_after_write = value

	@property
	def bin_float_numbers_format(self) -> BinFloatFormat:
		"""Sets / Gets format of float numbers when transferred as binary data"""
		return self._core.io.bin_float_numbers_format

	@bin_float_numbers_format.setter
	def bin_float_numbers_format(self, value: BinFloatFormat) -> None:
		"""Sets / Gets format of float numbers when transferred as binary data"""
		self._core.io.bin_float_numbers_format = value

	@property
	def bin_int_numbers_format(self) -> BinIntFormat:
		"""Sets / Gets format of integer numbers when transferred as binary data"""
		return self._core.io.bin_int_numbers_format

	@bin_int_numbers_format.setter
	def bin_int_numbers_format(self, value: BinIntFormat) -> None:
		"""Sets / Gets format of integer numbers when transferred as binary data"""
		self._core.io.bin_int_numbers_format = value

	def clear_status(self) -> None:
		"""Clears instrument's status system, the session's I/O buffers and the instrument's error queue"""
		return self._core.io.clear_status()

	def query_all_errors(self) -> List[str]:
		"""Queries and clears all the errors from the instrument's error queue.
		The method queries 'SYSTem:ERRor?' in a loop until the error queue is empty."""
		return self._core.io.query_all_syst_errors(False)

	@property
	def instrument_options(self) -> List[str]:
		"""Returns all the instrument options.
		The options are sorted in the ascending order starting with K-options and continuing with B-options"""
		return self._core.io.instr_options.get_all()

	def reset(self) -> None:
		"""SCPI command: *RST
		Sends *RST command + calls the clear_status()"""
		return self._core.io.reset()

	def self_test(self, timeout: int = None) -> Tuple[int, str]:
		"""SCPI command: *TST?
		Performs instrument's selftest.
		Returns tuple (code:int, message: str). Code 0 means the self-test passed.
		You can define the custom timeout in milliseconds. If you do not define it, the default selftest timeout is used (usually 60 secs)."""
		return self._core.io.self_test(timeout)

	@property
	def resource_name(self) -> int:
		"""Returns the resource name used in the constructor"""
		return self._core.io.resource_name

	@property
	def opc_timeout(self) -> int:
		"""See the opc_timeout.setter"""
		return self._core.io.opc_timeout

	@opc_timeout.setter
	def opc_timeout(self, value: int) -> None:
		"""Sets / Gets timeout in milliseconds for all the operations that use OPC synchronization"""
		self._core.io.opc_timeout = value

	@property
	def visa_timeout(self) -> int:
		"""See the visa_timeout.setter"""
		return self._core.io.visa_timeout

	@visa_timeout.setter
	def visa_timeout(self, value) -> None:
		"""Sets / Gets visa IO timeout in milliseconds"""
		self._core.io.visa_timeout = value

	@property
	def data_chunk_size(self) -> int:
		"""Returns max chunk size of one data block"""
		return self._core.io.data_chunk_size

	@data_chunk_size.setter
	def data_chunk_size(self, chunk_size: int) -> None:
		"""Sets the maximum size of one block transferred during write/read operations"""
		self._core.io.data_chunk_size = chunk_size

	@property
	def visa_manufacturer(self) -> int:
		"""Returns the manufacturer of the current VISA session"""
		return self._core.io.visa_manufacturer

	def process_all_commands(self) -> None:
		"""SCPI command: *WAI
		Stops further commands processing until all commands sent before *WAI have been executed"""
		return self._core.io.write('*WAI')

	def write_str(self, cmd: str) -> None:
		"""Writes the command to the instrument"""
		self._core.io.write(cmd)

	def write_int(self, cmd: str, param: int) -> None:
		"""Writes the command to the instrument followed by the integer parameter:
		e.g.: cmd = 'SELECT:INPUT' param = '2', result command = 'SELECT:INPUT 2'"""
		self._core.io.write(f'{cmd} {param}')

	def write_int_with_opc(self, cmd: str, param: int, timeout: int = None) -> None:
		"""Writes the command with OPC to the instrument followed by the integer parameter:
		e.g.: cmd = 'SELECT:INPUT' param = '2', result command = 'SELECT:INPUT 2'
		If you do not provide timeout, the method uses current opc_timeout."""
		self._core.io.write_with_opc(f'{cmd} {param}', timeout)

	def write_float(self, cmd: str, param: float) -> None:
		"""Writes the command to the instrument followed by the boolean parameter:
		e.g.: cmd = 'CENTER:FREQ' param = '10E6', result command = 'CENTER:FREQ 10E6'"""
		self._core.io.write(f'{cmd} {Conv.float_to_str(param)}')

	def write_float_with_opc(self, cmd: str, param: float, timeout: int = None) -> None:
		"""Writes the command with OPC to the instrument followed by the boolean parameter:
		e.g.: cmd = 'CENTER:FREQ' param = '10E6', result command = 'CENTER:FREQ 10E6'
		If you do not provide timeout, the method uses current opc_timeout."""
		self._core.io.write_with_opc(f'{cmd} {Conv.float_to_str(param)}', timeout)

	def write_bool(self, cmd: str, param: bool) -> None:
		"""Writes the command to the instrument followed by the boolean parameter:
		e.g.: cmd = 'OUTPUT' param = 'True', result command = 'OUTPUT ON'"""
		self._core.io.write(f'{cmd} {Conv.bool_to_str(param)}')

	def write_bool_with_opc(self, cmd: str, param: bool, timeout: int = None) -> None:
		"""Writes the command with OPC to the instrument followed by the boolean parameter:
		e.g.: cmd = 'OUTPUT' param = 'True', result command = 'OUTPUT ON'
		If you do not provide timeout, the method uses current opc_timeout."""
		self._core.io.write_with_opc(f'{cmd} {Conv.bool_to_str(param)}', timeout)

	def query_str(self, query: str) -> str:
		"""Sends the query to the instrument and returns the response as string.
		The response is trimmed of any trailing LF characters and has no length limit."""
		return self._core.io.query_str(query)

	def query_bool(self, query: str) -> bool:
		"""Sends the query to the instrument and returns the response as boolean"""
		return self._core.io.query_bool(query)

	def query_int(self, query: str) -> int:
		"""Sends the query to the instrument and returns the response as integer"""
		return self._core.io.query_int(query)

	def query_float(self, query: str) -> float:
		"""Sends the query to the instrument and returns the response as float"""
		return self._core.io.query_float(query)

	def write_str_with_opc(self, cmd: str, timeout: int = None) -> None:
		"""Writes the opc-synced command to the instrument.
		If you do not provide timeout, the method uses current opc_timeout."""
		self._core.io.write_with_opc(cmd, timeout)

	def query_str_with_opc(self, query: str, timeout: int = None) -> str:
		"""Sends the opc-synced query to the instrument and returns the response as string.
		The response is trimmed of any trailing LF characters and has no length limit.
		If you do not provide timeout, the method uses current opc_timeout."""
		return self._core.io.query_str_with_opc(query, timeout)

	def query_bool_with_opc(self, query: str, timeout: int = None) -> bool:
		"""Sends the opc-synced query to the instrument and returns the response as boolean.
		If you do not provide timeout, the method uses current opc_timeout."""
		return self._core.io.query_bool_with_opc(query, timeout)

	def query_int_with_opc(self, query: str, timeout: int = None) -> int:
		"""Sends the opc-synced query to the instrument and returns the response as integer.
		If you do not provide timeout, the method uses current opc_timeout."""
		return self._core.io.query_int_with_opc(query, timeout)

	def query_float_with_opc(self, query: str, timeout: int = None) -> float:
		"""Sends the opc-synced query to the instrument and returns the response as float.
		If you do not provide timeout, the method uses current opc_timeout."""
		return self._core.io.query_float_with_opc(query, timeout)

	def write_bin_block(self, cmd: str, payload: bytes) -> None:
		"""Writes all the payload as binary data block to the instrument.
		The binary data header is added at the beginning of the transmission automatically, do not include it in the payload!!!"""
		self._core.io.write_bin_block(cmd, payload)

	def query_bin_block(self, query: str) -> bytes:
		"""Queries binary data block to bytes.
		Throws an exception if the returned data was not a binary data.
		Returns data:bytes"""
		return self._core.io.query_bin_block(query)

	def query_bin_block_with_opc(self, query: str, timeout: int = None) -> bytes:
		"""Sends a OPC-synced query and returns binary data block to bytes.
		If you do not provide timeout, the method uses current opc_timeout."""
		return self._core.io.query_bin_block_with_opc(query, timeout)

	def query_bin_or_ascii_float_list(self, query: str) -> List[float]:
		"""Queries a list of floating-point numbers that can be returned in ASCII format or in binary format.
		- For ASCII format, the list numbers are decoded as comma-separated values.
		- For Binary Format, the numbers are decoded based on the property BinFloatFormat, usually float 32-bit (FORM REAL,32)."""
		return self._core.io.query_bin_or_ascii_float_list(query)

	def query_bin_or_ascii_float_list_with_opc(self, query: str, timeout: int = None) -> List[float]:
		"""Sends a OPC-synced query and reads an list of floating-point numbers that can be returned in ASCII format or in binary format.
		- For ASCII format, the list numbers are decoded as comma-separated values.
		- For Binary Format, the numbers are decoded based on the property BinFloatFormat, usually float 32-bit (FORM REAL,32).
		If you do not provide timeout, the method uses current opc_timeout."""
		return self._core.io.query_bin_or_ascii_float_list_with_opc(query, timeout)

	def query_bin_or_ascii_int_list(self, query: str) -> List[int]:
		"""Queries a list of floating-point numbers that can be returned in ASCII format or in binary format.
		- For ASCII format, the list numbers are decoded as comma-separated values.
		- For Binary Format, the numbers are decoded based on the property BinFloatFormat, usually float 32-bit (FORM REAL,32)."""
		return self._core.io.query_bin_or_ascii_int_list(query)

	def query_bin_or_ascii_int_list_with_opc(self, query: str, timeout: int = None) -> List[int]:
		"""Sends a OPC-synced query and reads an list of floating-point numbers that can be returned in ASCII format or in binary format.
		- For ASCII format, the list numbers are decoded as comma-separated values.
		- For Binary Format, the numbers are decoded based on the property BinFloatFormat, usually float 32-bit (FORM REAL,32).
		If you do not provide timeout, the method uses current opc_timeout."""
		return self._core.io.query_bin_or_ascii_int_list_with_opc(query, timeout)

	# Write / Read to file
	def query_bin_block_to_file(self, cmd: str, file_path: str, append: bool = False) -> None:
		"""Queries binary data block to the provided file.
		If append is False, any existing file content is discarded.
		If append is True, the new content is added to the end of the existing file, or if the file does not exit, it is created.
		Throws an exception if the returned data was not a binary data.
		Example for transferring a file from Instrument -> PC:
		cmd = f"MMEM:DATA? '{INSTR_FILE_PATH}'".
		Alternatively, use the dedicated methods for this purpose:
		- send_file_from_pc_to_instrument ()
		- read_file_from_instrument_to_pc ()"""
		self._core.io.query_bin_block_to_file(cmd, file_path, append)

	def query_bin_block_to_file_with_opc(self, cmd: str, file_path: str, append: bool = False, timeout: int = None) -> None:
		"""Sends a OPC-synced query and writes the returned data to the provided file.
		If append is False, any existing file content is discarded.
		If append is True, the new content is added to the end of the existing file, or if the file does not exit, it is created.
		Throws an exception if the returned data was not a binary data."""
		self._core.io.query_bin_block_to_file_with_opc(cmd, file_path, append, timeout)

	def write_bin_block_from_file(self, cmd: str, file_path: str) -> None:
		"""Writes data from the file as binary data block to the instrument using the provided command.
		Example for transferring a file from PC -> Instrument:
		cmd = f"MMEM:DATA '{INSTR_FILE_PATH}',".
		Alternatively, use the dedicated methods for this purpose:
		- send_file_from_pc_to_instrument ()
		- read_file_from_instrument_to_pc ()"""
		self._core.io.write_bin_block_from_file(cmd, file_path)

	def send_file_from_pc_to_instrument(self, source_pc_file: str, target_instr_file: str) -> None:
		"""SCPI Command: MMEM:DATA \n
		Sends file from PC to the instrument"""
		cmd = f"MMEM:DATA '{target_instr_file}',"
		self.write_bin_block_from_file(cmd, source_pc_file)

	def read_file_from_instrument_to_pc(self, source_instr_file: str, target_pc_file: str, append_to_pc_file: bool = False) -> None:
		"""SCPI Command: MMEM:DATA? \n
		Reads file from instrument to the PC. \n
		Set the append_to_pc_file to True if you want to append the read content to the end of the existing PC file"""
		cmd = f"MMEM:DATA? '{source_instr_file}'"
		self.query_bin_block_to_file(cmd, target_pc_file, append_to_pc_file)

	def get_last_sent_cmd(self) -> str:
		"""Returns the last commands sent to the instrument. Only works in simulation mode"""
		return self._core.get_last_sent_cmd()

	def get_lock(self) -> threading.RLock:
		"""Returns the thread lock for the current session. By default:
			- If you create standard new RsInstrument instance with new VISA session, the session gets a new thread lock.
				You can assign it to other RsInstrument sessions in order to share one physical instrument with a multi-thread access.
			- If you create new RsInstrument from an existing session, the thread lock is shared automatically making both instances multi-thread safe.
			You can always assign new thread lock by calling RsInstrument.assign_lock()
		"""
		return self._core.io.get_lock()

	def assign_lock(self, lock: threading.RLock) -> None:
		"""Assigns the provided thread lock."""
		self._core.io.assign_lock(lock)

	def clear_lock(self):
		"""Clears the existing thread lock, making the current session thread-independent from others that might share the current thread lock."""
		self._core.io.clear_lock()

	@staticmethod
	def assert_minimum_version(min_version: str) -> None:
		"""Asserts that the driver version fulfills the minimum required version you have entered.
		This way you make sure your installed driver is of the entered version or newer."""
		min_version_list = min_version.split('.')
		curr_version_list = RsInstrument._driver_version_const.split('.')
		count_min = len(min_version_list)
		count_curr = len(curr_version_list)
		count = count_min if count_min < count_curr else count_curr
		for i in range(count):
			minimum = int(min_version_list[i])
			curr = int(curr_version_list[i])
			if curr > minimum:
				break
			if curr < minimum:
				raise Exception(f"Assertion for minimum RsInstrument version failed. Current version: '{RsInstrument._driver_version_const}', minimum required version: '{min_version}'")
