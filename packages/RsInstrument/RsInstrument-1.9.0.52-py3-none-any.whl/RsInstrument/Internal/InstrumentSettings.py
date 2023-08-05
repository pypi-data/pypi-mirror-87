from enum import Enum
from enum import Flag

from . import InstrumentOptions as Opts, Conversions as Conv


class InstrViClearMode(Flag):
	disabled = 0x00
	ignore_error = 0x01
	execute_on_all = 0x02
	execute_on_socket = 0x04
	execute_on_serial = 0x08
	execute_on_usb = 0x10
	execute_on_gpib = 0x20
	execute_on_tcpvxi = 0x40


class WaitForOpcMode(Enum):
	"""Mode that is used for OPC-sync commands/queries"""
	stb_poll = 1
	stb_poll_slow = 2
	stb_poll_superslow = 3
	opc_query = 4


class InstrumentSettings(object):
	"""Defines settings of the instrument."""

	def __init__(
			self,
			viclear_exe_mode: InstrViClearMode,
			idn_model_full_name: bool,
			write_delay: int,
			read_delay: int,
			io_segment_size: int,
			opc_wait_mode: WaitForOpcMode,
			opc_timeout: int,
			visa_timeout: int,
			self_test_timeout: int,
			instr_options_parse_mode: Opts.ParseMode,
			bin_float_numbers_format: Conv.BinFloatFormat,
			bin_int_numbers_format: Conv.BinIntFormat,
			opc_query_after_write: bool):

		self.viclear_exe_mode = viclear_exe_mode
		self.idn_model_full_name = idn_model_full_name
		self.write_delay = write_delay
		self.read_delay = read_delay
		self.io_segment_size = io_segment_size
		self.opc_wait_mode = opc_wait_mode
		self.opc_timeout = opc_timeout
		self.visa_timeout = visa_timeout
		self.selftest_timeout = self_test_timeout
		self.instr_options_parse_mode = instr_options_parse_mode
		self.bin_float_numbers_format = bin_float_numbers_format
		self.bin_int_numbers_format = bin_int_numbers_format
		self.opc_query_after_write = opc_query_after_write

		self.assure_write_with_tc = False
		self.term_char = '\n'
		self.add_term_char_to_write_bin_block = False

		self.stb_in_error_check = True
		self.disable_opc_query = False
		self.visa_select = None

	def apply_option_settings(self, settings: dict) -> None:

		value = settings.get('SELECTVISA')
		if value is not None:
			self.visa_select = value

		value = settings.get('DRIVERSETUP_WRITEDELAY')
		if value is not None:
			self.write_delay = Conv.str_to_int(value)

		value = settings.get('DRIVERSETUP_READDELAY')
		if value is not None:
			self.read_delay = Conv.str_to_int(value)

		value = settings.get('DRIVERSETUP_OPCWAITMODE')
		if value is not None:
			value = value.upper()
			if value == 'STBPOLLING':
				self.opc_wait_mode = WaitForOpcMode.stb_poll
			elif value == 'STBPOLLINGSLOW':
				self.opc_wait_mode = WaitForOpcMode.stb_poll_slow
			elif value == 'STBPOLLINGSUPERSLOW':
				self.opc_wait_mode = WaitForOpcMode.stb_poll_superslow
			elif value == 'OPCQUERY':
				self.opc_wait_mode = WaitForOpcMode.opc_query
			else:
				raise ValueError(
					f"Unknown value in InitWithOptions string DriverSetup key 'WaitForOPC'. Value '{value}' is not recognized. "
					"Valid values: 'StbPolling', 'StbPollingSlow', 'StbPollingSuperSlow', 'OpcQuery'")

		value = settings.get('DRIVERSETUP_ADDTERMCHARTOWRITEBINBLOCK')
		if value is not None:
			self.add_term_char_to_write_bin_block = Conv.str_to_bool(value)

		# Obsolete, use the DRIVERSETUP_ASSUREWRITEWITHTERMCHAR
		value = settings.get('DRIVERSETUP_ASSUREWRITEWITHLF')
		if value is not None:
			self.assure_write_with_tc = Conv.str_to_bool(value)
		value = settings.get('DRIVERSETUP_ASSUREWRITEWITHTERMCHAR')
		if value is not None:
			self.assure_write_with_tc = Conv.str_to_bool(value)

		value = settings.get('DRIVERSETUP_TERMINATIONCHARACTER')
		if value is not None:
			self.term_char = value

		value = settings.get('DRIVERSETUP_IOSEGMENTSIZE')
		if value is not None:
			self.io_segment_size = Conv.str_to_int(value)

		value = settings.get('DRIVERSETUP_OPCTIMEOUT')
		if value is not None:
			self.opc_timeout = Conv.str_to_int(value)

		value = settings.get('DRIVERSETUP_VISATIMEOUT')
		if value is not None:
			self.visa_timeout = Conv.str_to_int(value)

		value = settings.get('DRIVERSETUP_VICLEAREXEMODE')
		if value is not None:
			self.viclear_exe_mode = value

		value = settings.get('DRIVERSETUP_OPCQUERYAFTERWRITE')
		if value is not None:
			self.opc_query_after_write = Conv.str_to_bool(value)

		value = settings.get('DRIVERSETUP_STBINERRORCHECK')
		if value is not None:
			self.stb_in_error_check = Conv.str_to_bool(value)

		value = settings.get('DRIVERSETUP_DISABLEOPCQUERY')
		if value is not None:
			self.disable_opc_query = Conv.str_to_bool(value)

		value = settings.get('DRIVERSETUP_QUERYOPT')
		if value is not None:
			value = value.upper()
			if value == 'SKIP':
				self.instr_options_parse_mode = Opts.ParseMode.Skip
			elif value == 'AUTO':
				self.instr_options_parse_mode = Opts.ParseMode.Auto
			elif value == 'KEEPORIGINAL':
				self.instr_options_parse_mode = Opts.ParseMode.KeepOriginal
			elif value == 'KEEPBEFOREDASH':
				self.instr_options_parse_mode = Opts.ParseMode.KeepBeforeDash
			elif value == 'KEEPAFTERDASH':
				self.instr_options_parse_mode = Opts.ParseMode.KeepAfterDash
			else:
				raise ValueError(
					f"Unknown value in InitWithOptions string DriverSetup key 'QueryOpt'. Value '{value}' is not recognized. "
					"Valid values: 'Skip', 'Auto', 'KeepOriginal', 'KeepBeforeDash', 'KeepAfterDash'")
