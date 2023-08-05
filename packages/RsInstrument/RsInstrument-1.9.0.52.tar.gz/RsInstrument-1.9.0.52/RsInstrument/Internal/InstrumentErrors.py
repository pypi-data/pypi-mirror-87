class RsInstrException(Exception):
	"""Exception base class for all the RsInstrument exceptions."""
	def __init__(self, message: str):
		super(RsInstrException, self).__init__(message)


class TimeoutException(RsInstrException):
	"""Exception for timeout errors."""
	def __init__(self, message: str):
		super(TimeoutException, self).__init__(message)


class StatusException(RsInstrException):
	"""Exception for instrument status errors."""
	def __init__(self, rsrc_name: str, message: str):
		self.rsrc_name = rsrc_name
		super(StatusException, self).__init__(message)


class UnexpectedResponseException(RsInstrException):
	"""Exception for instrument unexpected responses."""
	def __init__(self, rsrc_name: str, message: str):
		self.rsrc_name = rsrc_name
		super(UnexpectedResponseException, self).__init__(message)


class ResourceError(RsInstrException):
	"""Exception for resource name - e.g. resource not found."""
	def __init__(self, rsrc_name: str, message: str):
		self.rsrc_name = rsrc_name
		super(ResourceError, self).__init__(message)


class DriverValueError(RsInstrException):
	"""Exception for different driver value settings e.g. RepCap values or Enum values."""
	def __init__(self, rsrc_name: str, message: str):
		self.rsrc_name = rsrc_name
		super(DriverValueError, self).__init__(message)


def assert_no_instrument_status_errors(rsrc_name: str, errors: list, context: str = '') -> None:
	"""Checks the errors list and of it contains at least one element, it throws StatusException."""
	if errors is None:
		return
	if len(errors) == 0:
		return
	if context:
		message = f"'{rsrc_name}': {context} "
	else:
		message = f"'{rsrc_name}': "
	if len(errors) == 1:
		message += f'Instrument error detected: {errors[0]}'
		raise StatusException(rsrc_name, message)
	if len(errors) > 1:
		message += '{} Instrument errors detected:\n{}'.format(len(errors), '\n'.join(errors))
		raise StatusException(rsrc_name, message)


def throw_opc_tout_exception(opc_tout: int, used_tout: int, context: str = '') -> None:
	"""Throws TimeoutException - use it for any timeout error."""
	if not context:
		message = ''
	else:
		message = f'{context} '
	if used_tout < 0 or used_tout == opc_tout:
		message = message + f"Timeout expired before the operation completed. Current OPC timeout is set to {opc_tout} milliseconds. " \
							"Change it with the property '_driver.UtilityFunctions.opc_timeout'. " \
							"Optionally, if the method API contains an optional timeout parameter, set it there."
	else:
		message = message + f"Timeout expired before the operation completed. Used timeout: {used_tout} ms"
	raise TimeoutException(message)


def throw_bin_block_unexp_resp_exception(rsrc_name: str, received_data: str) -> None:
	"""Throws InvalidDataException - use it in case an instrument response is not a binary block."""
	if received_data.endswith('\n'):
		raise UnexpectedResponseException(
			rsrc_name, "Expected binary data header starting with #(hash), received data '{}'".format(received_data.replace('\n', '\\n')))
	else:
		raise UnexpectedResponseException(
			rsrc_name, f"Expected binary data header starting with #(hash), received data starting with '{received_data}'...")


def assert_query_has_qmark(query: str, context: str = '') -> None:
	"""Throws Exception if the query does not contain any question marks."""
	if '?' in query:
		return
	message = ''
	if context:
		message = ' ' + context
	message = message + "Query commands must contain question-marks. Sent query: '{0}'".format(query.strip('\n'))
	raise Exception(message)


def assert_cmd_has_no_qmark(command: str, context: str = '') -> None:
	"""Throws Exception if the query contains a question marks."""
	if '?' not in command:
		return
	message = ''
	if context:
		message = ' ' + context
	message = message + "Set commands must not contain question-marks. Sent command: '{0}'".format(command.strip('\n'))
	raise Exception(message)
