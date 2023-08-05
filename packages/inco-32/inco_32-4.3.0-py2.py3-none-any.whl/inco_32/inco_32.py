#*******************************************************************************
#
#	\file
#	\author			R. Zulliger, &copy; INDEL AG
#
#	\remarks
#	\verbatim
#	project			: python inco_32.dll and libinco_32.dll binding
#	language		: python
#	system			: Windows, Linux
#	\endverbatim
#
#	\brief
#
#*******************************************************************************

from __future__ import print_function
from ctypes import *


#-------------------------------------------------------------------------------
# constants
#-------------------------------------------------------------------------------

# inco types
DF_INCO_TYPE_UINT64 = 0x0101		# type uint32
DF_INCO_TYPE_INT64 = 0x0102			# type int32
DF_INCO_TYPE_UINT32 = 0x0103		# type uint32
DF_INCO_TYPE_INT32 = 0x0104			# type int32
DF_INCO_TYPE_UINT16 = 0x0105		# type uint16
DF_INCO_TYPE_INT16 = 0x0106			# type int16
DF_INCO_TYPE_UINT8 = 0x0107			# type uint8
DF_INCO_TYPE_INT8 = 0x0108			# type int8
DF_INCO_TYPE_DOUBLE = 0x0109		# type double
DF_INCO_TYPE_FLOAT = 0x010A			# type float, single

# Types with prefix 0x02?? are non-scalar types (multy value variables/buffers/arrays)
DF_INCO_TYPE_STRING = 0x0200		# type string
DF_INCO_TYPE_FILE = 0x0201			# type file (path/filename)
DF_INCO_TYPE_BINARY = 0x0202		# type binary (file data)


#-------------------------------------------------------------------------------
# functions
#-------------------------------------------------------------------------------

if bytes is str:
	# nothing to convert in Python 2
	def _stringFromInco(bytestring):
		return bytestring
	def _stringToInco(string):
		return string
	def _binaryToInco(data):
		return data
else:
	# Convert bytes to str in the usual INCO way: UTF-8 if valid, else 
	# Windows-1252 for compatibility with old nonconformant systems.
	def _stringFromInco(bytestring):
		try:
			return str(bytestring, 'utf-8')
		except UnicodeError:
			return str(bytestring, 'windows-1252', 'ignore')
	# Convert anything suitable to bytes or None (the only things ctypes accepts
	# for a c_char_p argument): str as UTF-8, bytes-like objects unmodified, None
	# unmodified. Other types may raise TypeError, ValueError, or give unexpected
	# results.
	def _stringToInco(string):
		try:
			return bytes(string, 'utf-8')
		except TypeError: # "encoding without a string argument"
			# this accepts bytes, bytearray, memoryview, array.array
			return bytes(string) if string is not None else None
	# Convert bytes-like objects to something ctypes accepts for a c_char_p
	# argument. TODO: Check if the C functions can be declared differently so
	# that they can take such objects without requiring a copy.
	def _binaryToInco(data):
		return bytes(data) if data is not None else None

def RplIdDescription(aRplId):
	try:
		return [
		 	'Ok',
		 	'Skipped',
		 	'InComplete',
		 	'Ignored',
		 	'Paused',
		 	'Stopped',
		 	'Canceled',
		 	'Rejected',
		 	'Failed',
		 	'Error',
		 	'Fatal',
			'Timeout'
		][aRplId if aRplId >= 0 else None]
	except (IndexError, TypeError):
		return str(aRplId)

class INCOError (Exception):
	def __init__(self, auError, aErrorMessage=None, aPathInformation=None, aTarget=None):
		if not aErrorMessage:
			if auError < 0:
				aErrorMessage = 'ticket'
			elif auError == 0:
				aErrorMessage = 'OK'
			else:
				if (auError & 0xC0000000) and aTarget:
					try:
						aErrorMessage = GetMcMessage(aTarget, auError=auError)
					except INCOError:
						pass
				if not aErrorMessage:
					aErrorMessage = GetErrorDescription(auError)
		self.m_uError = auError
		self.m_ErrorMessage = aErrorMessage
		self.m_PathInformation = aPathInformation
	def __str__(self):
		return 'INCO-Error: 0x%x (%serror: %s, path information: %s)' % (self.m_uError, 'reply: %s, ' % RplIdDescription((self.m_uError >> 24) & 0xF) if self.m_uError & 0xC0000000 else '', self.m_ErrorMessage, self.m_PathInformation)


def HandleError( auError, auResult, aPathInformation = "{additional path information}", aTarget=None ):
	if auError > 0:
		raise INCOError(auError, aPathInformation=aPathInformation, aTarget=aTarget)
	return auResult


def GetErrorDescription( auError ):
	uMaxLength = 1024
	cBuffer = create_string_buffer( uMaxLength )
	_GetErrorDescription( b"", auError, cBuffer, uMaxLength )
	return _stringFromInco(cBuffer.value)

def GetMcMessage(aTargetName, aMessageHandlerPath='Target.message', auError=0):
	buffer = create_string_buffer(1024)
	error = _GetMcMessage(_stringToInco(aTargetName), _stringToInco(aMessageHandlerPath), auError, buffer, len(buffer))
	return HandleError(error, _stringFromInco(buffer.value), '%s 0x%X' % (aMessageHandlerPath, auError), aTargetName)


#-------------------------------------------------------------------------------
# API functions
#-------------------------------------------------------------------------------
#
#  V a r i a b l e
#
def GetVariable( aTargetName, aVarName, aSize = 0 ):
	if aSize != 0:
		# It's a string
		cBuffer = create_string_buffer( aSize )
		uError = _GetVariable( _stringToInco(aTargetName), _stringToInco(aVarName), cBuffer, aSize )
		return HandleError( uError, _stringFromInco(cBuffer.value), aVarName, aTargetName )
	else:
		dResult = c_double()
		uError = _GetVariable( _stringToInco(aTargetName), _stringToInco(aVarName), byref(dResult), 0 )
		return HandleError( uError, dResult.value, aVarName, aTargetName )


def GetVariableBin( aTargetName, aVarName, aSize = 0 ):
	if aSize != 0:
		# It's a string with embedded zeroes
		cBuffer = create_string_buffer( aSize )
		uError = _GetVariable( _stringToInco(aTargetName), _stringToInco(aVarName), cBuffer, aSize )
		return HandleError( uError, cBuffer.raw, aVarName, aTargetName )
	else:
		dResult = c_double()
		uError = _GetVariable( _stringToInco(aTargetName), _stringToInco(aVarName), byref(dResult), 0 )
		return HandleError( uError, dResult.value, aVarName, aTargetName )


def PutVariable( aTargetName, aVarName, aData ):
	uError = 0
	try:
		dDouble = c_double(aData)
		uError = _PutVariable( _stringToInco(aTargetName), _stringToInco(aVarName), byref(dDouble), 0 )
	except TypeError:
		aData = _stringToInco(aData)
		uError = _PutVariable( _stringToInco(aTargetName), _stringToInco(aVarName), c_char_p(aData), len(aData) + 1 )
	return HandleError( uError, None, aVarName, aTargetName )


incoTypes={DF_INCO_TYPE_UINT64:[8, c_uint64()],
		DF_INCO_TYPE_INT64:[8, c_int64()],
		DF_INCO_TYPE_UINT32:[4, c_uint32()],
		DF_INCO_TYPE_INT32:[4, c_int32()],
		DF_INCO_TYPE_UINT16:[2, c_uint16()],
		DF_INCO_TYPE_INT16:[2, c_int16()],
		DF_INCO_TYPE_UINT8:[1, c_uint8()],
		DF_INCO_TYPE_INT8:[1, c_int8()],
		DF_INCO_TYPE_DOUBLE:[8, c_double()],
		DF_INCO_TYPE_FLOAT:[4, c_float()]
		}

def GetVariableEx( aTargetName, aVarName, aIncoType, aSize = 0 ):
	if aSize != 0:
		# It's a string
		cBuffer = create_string_buffer( aSize )
		uError = _GetVariableEx( _stringToInco(aTargetName), _stringToInco(aVarName), aIncoType, cBuffer, aSize )
		return HandleError( uError, _stringFromInco(cBuffer.value), aVarName, aTargetName )
	else:
		if aIncoType in incoTypes:
			aSize, tResult = incoTypes[aIncoType]
		else:
			# ER_INCO_VAR_UNSUPPORTED_TYPE
			return HandleError( 0x00050210, 0, aVarName, aTargetName )
		# end else
		uError = _GetVariableEx( _stringToInco(aTargetName), _stringToInco(aVarName), aIncoType, byref(tResult), aSize )
		return HandleError( uError, tResult.value, aVarName, aTargetName )


def PutVariableEx( aTargetName, aVarName, aIncoType, aData ):
	uError = 0
	try:
		if aIncoType in incoTypes:
			aSize, tValue = incoTypes[aIncoType]
			tValue.value = aData
		else:
			# ER_INCO_VAR_UNSUPPORTED_TYPE
			return HandleError( 0x00050210, 0, aVarName, aTargetName )
		# end else
		uError = _PutVariableEx( _stringToInco(aTargetName), _stringToInco(aVarName), aIncoType, byref(tValue), aSize )
	except TypeError:
		aData = _stringToInco(aData)
		uError = _PutVariableEx( _stringToInco(aTargetName), _stringToInco(aVarName), aIncoType, c_char_p(aData), len(aData) + 1 )
	return HandleError( uError, None, aVarName, aTargetName )


#
#  P r o c e d u r e
#	
def CallProcedure( aTargetName, aFctName ):
	dResult = c_double(0.0)
	uError = _CallProcedure( _stringToInco(aTargetName), _stringToInco(aFctName), byref(dResult) )
	return HandleError( uError, dResult.value, aFctName, aTargetName )

def CallProcedureEx( aTargetName, aFctName ):
	dResult = c_double(0.0)
	ticketOrError = _CallProcedureEx( _stringToInco(aTargetName), _stringToInco(aFctName), byref(dResult) )
	return (HandleError( ticketOrError, dResult.value, aFctName, aTargetName ), ticketOrError)
	
CallAsyncProcedure = CallProcedureEx # for backwards compatibility

def CallProcedureExWait( aTargetName, aTicket, aTimeout = -1 ):
	iTicket = c_int32(int(aTicket))
	return _CallProcedureExWait(_stringToInco(aTargetName), iTicket, aTimeout)

def CallProcedureExResult(aTargetName, aTicket, aDefaultValue = None):
	(value, error) = _CallProcedureExResultCommon(aTargetName, aDefaultValue, lambda aRes, aSiz, aTyF:
		_CallProcedureExResult(_stringToInco(aTargetName), c_int32(int(aTicket)), aRes, aSiz, aTyF, None, 0))
	return value
	
def CallProcedureExResultByName(aTargetName, aTicket, aResultName, aDefaultValue = None):
	(value, error) = _CallProcedureExResultCommon(aTargetName, aDefaultValue, lambda aRes, aSiz, aTyF:
		_CallProcedureExResultByName(_stringToInco(aTargetName), c_int32(int(aTicket)), _stringToInco(aResultName), aRes, aSiz, aTyF))
	return value

def _CallProcedureExResultCommon(aTarget, aDefaultValue, aExResultFunction):
	uType = c_uint32(0)
	error = aExResultFunction(byref(uType), sizeof(uType), 0x00010000) #DF_INCO_FLAG_GET_RESULT_TYPE
	if error == 0x5040E or error == 0x5040C: #ER_INCO_RPC_UNKNOWN_TICKET, ER_INCO_RPC_NO_RETURN_VALUE
		return (aDefaultValue, error)
	elif error != 0:
		raise INCOError(error, aPathInformation="{CallProcedureExResult type}", aTarget=aTarget)
	elif uType.value == 0x200: #DF_INCO_TYPE_STRING
		uLength = c_uint32(0)	
		error = aExResultFunction(byref(uLength), sizeof(uLength), 0x00020000) #DF_INCO_FLAG_GET_RESULT_LENGTH
		if error != 0: # I don't think this should happen
			raise INCOError(error, aPathInformation="{CallProcedureExResult string length}", aTarget=aTarget)
		cBuffer = create_string_buffer(uLength.value)
		error = aExResultFunction(cBuffer, uLength, uType)
		if error != 0: # I don't think this should happen
			raise INCOError(error, aPathInformation="{CallProcedureExResult string value}", aTarget=aTarget)
		return (_stringFromInco(cBuffer.value), error)
	else:
		if uType.value == 0x101: #DF_INCO_TYPE_UINT64
			ctype = c_uint64
			incotype = 0x101
			pytype = int
		elif uType.value == 0x102: #DF_INCO_TYPE_INT64
			ctype = c_int64
			incotype = 0x102
			pytype = int
		elif uType.value >= 0x103 and uType.value <= 0x108: #DF_INCO_TYPE_UINT32 ... DF_INCO_TYPE_INT8
			ctype = c_double
			incotype = 0x0112 #DF_INCO_TYPE_NUMBER_VALUE
			pytype = int
		else: # try double
			ctype = c_double
			incotype = 0x0112 #DF_INCO_TYPE_NUMBER_VALUE
			pytype = float
		cResult = ctype()
		error = aExResultFunction(byref(cResult), sizeof(cResult), incotype)
		if error == 0x50411: # ER_INCO_RPC_NOT_CONVERTABLE_TO_DOUBLE
			raise INCOError(error, aPathInformation="{Getting result of type 0x%X is not implemented in the Python binding}" % uType.value, aTarget=aTarget)
		elif error != 0:
			raise INCOError(error, aPathInformation="{CallProcedureExResult value}", aTarget=aTarget)
		else:
			return (pytype(cResult.value), error)

def GetAsyncCallResult(aTargetName, aTicket, aDefaultValue = None): # for backwards compatibility
	if aTicket >= 0:
		return aDefaultValue
	else:
		return CallProcedureExResult(aTargetName, aTicket, aDefaultValue)

def CallProcedureExSync( aTargetName, aFctName ):
	dResult = c_double(0.0)
	ticketOrError = _CallProcedureEx( _stringToInco(aTargetName), _stringToInco(aFctName), byref(dResult) )
	if ticketOrError > 0:
		raise INCOError(ticketOrError, aPathInformation=aFctName, aTarget=aTargetName)
	elif ticketOrError == 0:
		return dResult.value
	else:
		return CallProcedureExResult(aTargetName, ticketOrError, dResult.value)

CallProcedureSync = CallProcedureExSync # for backwards compatibility

# Helper function to get all results and their names from the async results. 
# This function exists in Python only (no such C-binding is available).
# It returns a list of tuples containing the (value, name) of the result.
# E.g. 
#   []
# or
#   [(0.0, 'Inp.DI1'), (0.0, 'Inp.DI2'), (1.0, 'Out.DO1'), (0.0, 'Out.DO2'),
#   (0.0, 'Adc.AI1'), (0.0, 'Adc.AI2'), (0.0, 'Dac.AO1'), (0.0, 'Dac.AO2'), 
#   (0.0, 'X.Zero'), (0.0, 'Y.Zero')]
def CallProcedureExResultAll(aTargetName, aTicket):
	results = []
	# The result name can't excee 1024, as that's the maximum pay load for 
	# all results in an async result UDP frame.
	bufSize = 1024;
	cBuffer = create_string_buffer(bufSize)
	result = 0
	rcount = 0

	# try to get results as long as no error occurs.
	while True:
		(result, error) = _CallProcedureExResultCommon(aTargetName, 0, lambda aRes, aSiz, aTyF:
			_CallProcedureExResult(_stringToInco(aTargetName), c_int32(int(aTicket)), aRes, aSiz, aTyF, cBuffer, bufSize))
		if (error == 0x5040E) and (rcount > 0):		# ER_INCO_RPC_UNKNOWN_TICKET
			# finished reading results
			break
		if error != 0:
			raise INCOError(error, aPathInformation="CallProcedureExResultAll", aTarget=aTargetName)
		# add the result and the name to the list
		results.append((result, _stringFromInco(cBuffer.value)))
		rcount = rcount + 1
	return results


#
#  G e t B l o c k x
#	
def GetBlock8( aTargetName, aAddress, aDataLength ):
	RetValue = create_string_buffer( aDataLength )
	uError = _GetBlock8( _stringToInco(aTargetName), aAddress, RetValue, aDataLength )
	return HandleError( uError, RetValue.raw, aTarget=aTargetName )

def GetBlock16( aTargetName, aAddress, aDataLength ):
	RetValue = create_string_buffer( aDataLength*2 )
	uError = _GetBlock16( _stringToInco(aTargetName), aAddress, RetValue, aDataLength )
	return HandleError( uError, RetValue.raw, aTarget=aTargetName )

def GetBlock32( aTargetName, aAddress, aDataLength ):
	RetValue = create_string_buffer( aDataLength*4 )
	uError = _GetBlock32( _stringToInco(aTargetName), aAddress, RetValue, aDataLength )
	return HandleError( uError, RetValue.raw, aTarget=aTargetName )

def GetBlock64( aTargetName, aAddress, aDataLength ):
	RetValue = create_string_buffer( aDataLength*8 )
	uError = _GetBlock64( _stringToInco(aTargetName), aAddress, RetValue, aDataLength )
	return HandleError( uError, RetValue.raw, aTarget=aTargetName )

#
#  P u t B l o c k x
#
def PutBlock8( aTargetName, aAddress, aData, aDataLength ):
	uError = _PutBlock8( _stringToInco(aTargetName), aAddress, _binaryToInco(aData), aDataLength )
	return HandleError( uError, None, aTarget=aTargetName )
	
def PutBlock16( aTargetName, aAddress, aData, aDataLength ):
	uError = _PutBlock16( _stringToInco(aTargetName), aAddress, _binaryToInco(aData), aDataLength )
	return HandleError( uError, None, aTarget=aTargetName )
	
def PutBlock32( aTargetName, aAddress, aData, aDataLength ):
	uError = _PutBlock32( _stringToInco(aTargetName), aAddress, _binaryToInco(aData), aDataLength )
	return HandleError( uError, None, aTarget=aTargetName )
	
def PutBlock64( aTargetName, aAddress, aData, aDataLength ):
	uError = _PutBlock64( _stringToInco(aTargetName), aAddress, _binaryToInco(aData), aDataLength )
	return HandleError( uError, None, aTarget=aTargetName )

#
#  D a t a T r a n s f e r
#
def DTOpen( aTargetName, aEndpointName ):
	uFileDescriptor = c_void_p(0)
	uError = _DTOpen( _stringToInco(aTargetName), _stringToInco(aEndpointName), byref(uFileDescriptor) )
	return HandleError( uError, uFileDescriptor, aEndpointName, aTargetName )

def DTClose( aFileDescriptor ):
	_DTClose( aFileDescriptor )

def DTSend( aFileDescriptor, aData, aDataLength ):
	uError = _DTSend( aFileDescriptor, _binaryToInco(aData), aDataLength )
	return HandleError( uError, None )

def DTReceive( aFileDescriptor, aDataBufferSize, aTimeout ):
	DataLength = c_uint32(0)
	RetValue = create_string_buffer(0)
	resize( RetValue, aDataBufferSize )
	uError = _DTReceive( aFileDescriptor, RetValue, aDataBufferSize, byref(DataLength), aTimeout )
	resize( RetValue, DataLength.value )
	return HandleError( uError, RetValue.raw )
	
def DTControl( aTargetName, aRequest, aData, aDataLength ):
	uError = _DTControl( _stringToInco(aTargetName), aRequest, aData, aDataLength )
	return HandleError( uError, None )

def DTGetBufferSizes( aFileDescriptor ):
	LocalBufferSize = c_uint32(0)
	TargetBufferSize = c_uint32(0)
	uError = _DTGetBufferSizes( aFileDescriptor, byref(LocalBufferSize), byref(TargetBufferSize) )
	return HandleError( uError, {'LocalBufferSize':LocalBufferSize.value, 'TargetBufferSize':TargetBufferSize.value} )

#
#  D e b u g
#
# Historically these have not raised INCOError but returned an INCO error code
# (because they were directly reexported from C). Is that a bug or a feature?
def DbgOsReset(aTargetName, aFlags):
	return _DbgOsReset(_stringToInco(aTargetName), aFlags)

def DbgOsPrepareLoad(aTargetName):
	return _DbgOsPrepareLoad(_stringToInco(aTargetName))

#
#  D a t a b a s e
#
def CreateTable( aTargetName, aTableName, aDatabaseName, aNumberRecords, aRecordSize, aFlags ):
	uError = _CreateTable( _stringToInco(aTargetName), _stringToInco(aTableName), _stringToInco(aDatabaseName), aNumberRecords, aRecordSize, aFlags )
	return HandleError( uError, None, aTarget=aTargetName )
	
def DeleteTable( aTargetName, aTableName ):
	uError = _DeleteTable( _stringToInco(aTargetName), _stringToInco(aTableName) )
	return HandleError( uError, None, aTarget=aTargetName )	

def PutRecord( aTargetName, aTableName, aRecord, aData, aDataLength ):
	uError = _PutRecord( _stringToInco(aTargetName), _stringToInco(aTableName), _stringToInco(aRecord), _binaryToInco(aData), aDataLength )
	return HandleError( uError, None, aTarget=aTargetName )

def GetRecord( aTargetName, aTableName, aRecord, aDataLength ):
	RetValue = create_string_buffer( aDataLength )
	uError = _GetRecord( _stringToInco(aTargetName), _stringToInco(aTableName), _stringToInco(aRecord), RetValue, aDataLength )
	return HandleError( uError, RetValue.raw, aTarget=aTargetName )
	
#
#  I n c o C o n t r o l
#
def IncoCtlSetTcpServerAddress(aAddress):
	return HandleError(IncoControl(None, 0, _stringToInco(aAddress), 0), None)


def IsDebugVersionRunning():
	# try a way that only works on Windows (other platforms don't load special C modules in the debug build):
	try:
		# Python 3
		import importlib.machinery
		if '_d.pyd' in importlib.machinery.EXTENSION_SUFFIXES:
			return True
	except ImportError:
		# Python 2
		import imp
		for suffix in imp.get_suffixes():
			if suffix[0] == '_d.pyd':
				return True
	# try a way that only works when embedded in INIX, not in the standard interpreter:
	try:
		import INIXOutputRedirector
		return INIXOutputRedirector.is_debug()
	except ImportError:
		pass
	return False

def RunStreamFile( aTargetName, aStreamFilePath ):
	try:
		Streams = open(aStreamFilePath).readlines()
		for Stream in Streams:
			if len(Stream.strip()) > 0:
				if Stream.strip().find('//') != 0 and Stream.strip().find('#') != 0:
					#print("Processing stream '" + Stream.strip() + "'", end=' ')
					if Stream.find('=') >= 0:
						#print("which is a PutVariable,", end=' ')
						VarName = Stream.split('=')[0].strip()
						VarValue = Stream.split('=')[1].strip() 
						#print("Varname:", VarName, "Value:", VarValue, end=' ')
	
						# 'try to' convert the value to its python object, like int, float, str
						def int16(Val):
							if Val.strip().lower().find('0x') != 0:
								raise(ValueError)
							return int(Val, 16)
						def toString(Val):
							if Val[0] == '"' and Val[-1] == '"':
								return Val[1:-1]
							raise(ValueError)
						ConvertFcts = (int16, int, float, toString)
						bConverted = False
						for ConvertFct in ConvertFcts:
							try:
								ConvertedValue = ConvertFct(VarValue)
								bConverted = True
								break
							except ValueError:
								pass
						if bConverted:
							#print('DEBUG: found type:', type(ConvertedValue), ConvertedValue)
							try:
								PutVariable(aTargetName, VarName, ConvertedValue)
							except INCOError as error:
								print('Executing PutVariable for:')
								print(VarName, 'with value:', str(ConvertedValue), 'from file:', aStreamFilePath, 'failed with error:')
								print(error)
						else:
							print("Stream '", Stream, "' from file: '", aStreamFilePath, "' has invalid format! Skipping it.")
					else:
						# must be a callprocedure
						#print('which is a CallProcedure')
						CallProcedure(aTargetName, Stream)
	except IOError:
		print("Couldn't open stream file '" + aStreamFilePath + "'.")

# Note for linux:
# Due to some reason I don't understand, we have to provide the full path to 
# the library file. I thought it should be found if /opt/indel/lib is listed
# in /etc/ld.so.conf or when providing the LD_LIBRARY_PATH env var - but it
# didn't work for me. Thats why we load the lib by calling:
# 	_GetVariable = cdll.__getattr__('/opt/indel/lib/libinco_32.so').GetVariable;
# instead of:
#	_GetVariable = cdll.libinco_32.GetVariable;
#
import sys
if sys.platform == 'win32':
	if IsDebugVersionRunning():
		print('Importing debug version of inco_32 (inco_32d.dll)')
		LibraryLocation = 'inco_32d'
	else:
		LibraryLocation = 'inco_32'
	import os
	if hasattr(os, 'add_dll_directory'):
		# since Python 3.8, not explicitly adding a DLL path results in not finding
		# the inco_32.dll at all.
		indel_root = os.environ['INDEL_ROOT']
		if sys.maxsize > 2**32: # as recommended by https://docs.python.org/3/library/platform.html#platform.architecture
			os.add_dll_directory(os.path.join(indel_root, 'lib64'))
		else:
			os.add_dll_directory(os.path.join(indel_root, 'lib'))
		os.add_dll_directory(os.path.join(indel_root, 'bin'))
	UseClass = windll
elif sys.platform == 'darwin':
	if IsDebugVersionRunning():
		print('Importing debug version of libinco_32 (libinco_32d.dylib)')
		LibraryLocation = '/opt/indel/lib/libinco_32d.dylib'
	else:
		LibraryLocation = '/opt/indel/lib/libinco_32.dylib'
	UseClass = cdll
else:
	if IsDebugVersionRunning():
		print('Importing debug version of libinco_32 (libinco_32d.so)')
		LibraryLocation = '/opt/indel/lib/libinco_32d.so'
	else:
		LibraryLocation = '/opt/indel/lib/libinco_32.so'
	UseClass = cdll
	try:
		UseClass.__getattr__(LibraryLocation).GetVariable;
	except OSError as err:
		print(err)
		if str(err).find("ELFCLASS64") > -1:
			LibraryLocation = '/opt/indel/lib32/libinco_32.so'

INIXInitialize = UseClass.__getattr__(LibraryLocation).IncoInitialize;
INIXUninitialize = UseClass.__getattr__(LibraryLocation).IncoUninitialize;

#
# GetVariable
_GetVariable = UseClass.__getattr__(LibraryLocation).GetVariable;
_GetVariable.argtypes = [ c_char_p, c_char_p, c_void_p, c_uint32 ]
#
# PutVariable
_PutVariable = UseClass.__getattr__(LibraryLocation).PutVariable;
_PutVariable.argtypes = [ c_char_p, c_char_p, c_void_p, c_uint32 ]
#
# GetVariableEx
_GetVariableEx = UseClass.__getattr__(LibraryLocation).GetVariableEx;
_GetVariableEx.argtypes = [ c_char_p, c_char_p, c_uint32, c_void_p, c_uint32 ]
#
# PutVariableEx
_PutVariableEx = UseClass.__getattr__(LibraryLocation).PutVariableEx;
_PutVariableEx.argtypes = [ c_char_p, c_char_p, c_uint32, c_void_p, c_uint32 ]
#
# CallProcedure
_CallProcedure = UseClass.__getattr__(LibraryLocation).CallProcedure
_CallProcedure.argtypes = [ c_char_p, c_char_p, POINTER(c_double) ]
_CallProcedure.restype = c_uint32
_CallProcedureEx = UseClass.__getattr__(LibraryLocation).CallProcedureEx
_CallProcedureEx.argtypes = [ c_char_p, c_char_p, POINTER(c_double) ]
_CallProcedureEx.restype = c_int32
#
# Synchronous Calling of Asynchronous Procedures
_CallProcedureExWait = UseClass.__getattr__(LibraryLocation).CallProcedureExWait
_CallProcedureExWait.argtypes = [ c_char_p, c_int32, c_int32 ]
_CallProcedureExWait.restype = c_uint32
_CallProcedureExResult = UseClass.__getattr__(LibraryLocation).CallProcedureExResult
_CallProcedureExResult.argtypes = [ c_char_p, c_int32, c_void_p, c_uint32, c_uint32, c_char_p, c_uint32 ]
_CallProcedureExResult.restype = c_uint32
_CallProcedureExResultByName = UseClass.__getattr__(LibraryLocation).CallProcedureExResultByName
_CallProcedureExResultByName.argtypes = [ c_char_p, c_int32, c_char_p, c_void_p, c_uint32, c_uint32 ]
_CallProcedureExResultByName.restype = c_uint32
#
# Error Messages
_GetErrorDescription = UseClass.__getattr__(LibraryLocation).GetErrorDescription;
_GetErrorDescription.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
_GetMcMessage = UseClass.__getattr__(LibraryLocation).GetMcMessage;
_GetMcMessage.argtypes = [ c_char_p, c_char_p, c_uint32, c_char_p, c_uint32 ]
#
# GetBlock
_GetBlock8 = UseClass.__getattr__(LibraryLocation).GetBlock8
_GetBlock8.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
_GetBlock16 = UseClass.__getattr__(LibraryLocation).GetBlock16
_GetBlock16.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
_GetBlock32 = UseClass.__getattr__(LibraryLocation).GetBlock32
_GetBlock32.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
_GetBlock64 = UseClass.__getattr__(LibraryLocation).GetBlock64
_GetBlock64.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
#
# PutBlock
_PutBlock8 = UseClass.__getattr__(LibraryLocation).PutBlock8
_PutBlock8.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
_PutBlock16 = UseClass.__getattr__(LibraryLocation).PutBlock16
_PutBlock16.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
_PutBlock32 = UseClass.__getattr__(LibraryLocation).PutBlock32
_PutBlock32.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
_PutBlock64 = UseClass.__getattr__(LibraryLocation).PutBlock64
_PutBlock64.argtypes = [ c_char_p, c_uint32, c_char_p, c_uint32 ]
#
# DataTransfer
# tLDTFileDescriptor is actually uintptr, but that doesn't exist in ctypes. c_void_p should be close enough.
_DTOpen = UseClass.__getattr__(LibraryLocation).DTOpen
_DTOpen.argtypes = [ c_char_p, c_char_p, POINTER(c_void_p) ]
_DTClose = UseClass.__getattr__(LibraryLocation).DTClose
_DTClose.argtypes = [ c_void_p ]
_DTClose.restype = None
_DTSend = UseClass.__getattr__(LibraryLocation).DTSend
_DTSend.argtypes = [ c_void_p, c_char_p, c_uint32 ]
_DTReceive = UseClass.__getattr__(LibraryLocation).DTReceive
_DTReceive.argtypes = [ c_void_p, c_char_p, c_uint32, POINTER(c_uint32), c_int32 ]
_DTControl = UseClass.__getattr__(LibraryLocation).DTControl
_DTControl.argtypes = [ c_char_p, c_int32, c_char_p, c_uint32 ]
_DTGetBufferSizes = UseClass.__getattr__(LibraryLocation).DTGetBufferSizes
_DTGetBufferSizes.argtypes = [ c_void_p, POINTER(c_uint32), POINTER(c_uint32) ]
#
# Debug
_DbgOsReset = UseClass.__getattr__(LibraryLocation).DbgOsReset
_DbgOsReset.argtypes = [ c_char_p, c_uint32 ]
_DbgOsPrepareLoad = UseClass.__getattr__(LibraryLocation).DbgOsPrepareLoad
_DbgOsPrepareLoad.argtypes = [ c_char_p ]
#
# Database functions (for Indel internal use)
_CreateTable = UseClass.__getattr__(LibraryLocation).CreateTable
_CreateTable.argtypes = [ c_char_p, c_char_p, c_char_p, c_uint32, c_uint32, c_uint32 ]
_DeleteTable = UseClass.__getattr__(LibraryLocation).DeleteTable
_DeleteTable.argtypes = [ c_char_p, c_char_p ]
_PutRecord = UseClass.__getattr__(LibraryLocation).PutRecord
_PutRecord.argtypes = [ c_char_p, c_char_p, c_char_p, c_char_p, c_uint32 ]
_GetRecord = UseClass.__getattr__(LibraryLocation).GetRecord
_GetRecord.argtypes = [ c_char_p, c_char_p, c_char_p, c_char_p, c_uint32 ]
#
# IncoControl
try:
	IncoControl = UseClass.__getattr__(LibraryLocation).IncoControl
	IncoControl.argtypes = [ c_char_p, c_int32, c_void_p, c_uint32 ]
	IncoControl.restype = c_uint32
except AttributeError:
	# version too old
	def IncoControl(*args):
		print("warning: function IncoControl() not found in this version of libinco_32, please update")
		return 0x00010100 # ER_INCO_CTL_UNKNOWN_REQUEST				

