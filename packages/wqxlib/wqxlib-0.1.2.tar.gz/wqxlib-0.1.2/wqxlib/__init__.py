from enum import Enum, IntEnum
from hashlib import sha256
import base64
import datetime
import hmac
import re
import requests

class FileType( Enum ):

  CSV = 'CSV'
  TAB = 'TAB'
  TILDE = 'TILDE'
  PIPE = 'PIPE'
  XLS = 'XLS'
  XLSX = 'XLSX'

class NewOrExistingData( IntEnum ):

  CONTAINS_NEW_OR_EXISTING = 0
  CONTAINS_NEW_ONLY = 1
  CONTAINS_EXISTING_ONLY = 2

class UponImportCompletion( IntEnum ):

  DO_NOT_EXPORT = 0
  EXPORT_IMPORT = 1
  SUBMIT_IMPORT = 2

class UponCompletionCondition( IntEnum ):

  NOT_APPLICABLE = 0
  EXPORT_IF_NO_ERROR = 1
  EXPORT_IF_NO_WARNING = 2
  EXPORT_ALWAYS = 3

class UponExportCompletion( IntEnum ):

  DO_NOT_SUBMIT = 0
  SUBMIT_EXPORT = 1

class WQXException( Exception ):

  def __init__( self, arg ):

    super(WQXException, self).__init__(arg)

class WQX():

  CSV = FileType.CSV
  TAB = FileType.TAB
  TILDE = FileType.TILDE
  PIPE = FileType.PIPE
  XLS = FileType.XLS
  XLSX = FileType.XLSX

  CONTAINS_NEW_OR_EXISTING = NewOrExistingData.CONTAINS_NEW_OR_EXISTING
  CONTAINS_NEW_ONLY = NewOrExistingData.CONTAINS_NEW_ONLY
  CONTAINS_EXISTING_ONLY = NewOrExistingData.CONTAINS_EXISTING_ONLY

  DO_NOT_EXPORT = UponImportCompletion.DO_NOT_EXPORT
  EXPORT_IMPORT = UponImportCompletion.EXPORT_IMPORT
  SUBMIT_IMPORT = UponImportCompletion.SUBMIT_IMPORT

  NOT_APPLICABLE = UponCompletionCondition.NOT_APPLICABLE
  EXPORT_IF_NO_ERROR = UponCompletionCondition.EXPORT_IF_NO_ERROR
  EXPORT_IF_NO_WARNING = UponCompletionCondition.EXPORT_IF_NO_WARNING
  EXPORT_ALWAYS = UponCompletionCondition.EXPORT_ALWAYS

  DO_NOT_IMPORT = UponExportCompletion.DO_NOT_SUBMIT
  SUBMIT_EXPORT = UponExportCompletion.SUBMIT_EXPORT

  def __init__(self,
    userID,
    privateKey
  ):

    # Test parameter types
    if not isinstance( userID, str ):
      raise TypeError( "Parameter 'userID' must be a string." )
    if not isinstance( privateKey, str ):
      raise TypeError( "Parameter 'privateKey' must be a string." )

    self.userID = userID

    try:
      self.privateKey = base64.b64decode( privateKey )
    except:
      self.privateKey = None
    if ( self.privateKey == None ):
      raise ValueError( "The provided privateKey is not valid." )

    self.session = requests.Session()

  def queryWQX(self,
    method,
    endpoint,
    data = None,
    filename = None,
    parameters = None
  ):

    # Test parameter types
    if not isinstance( self.userID, str ):
      raise TypeError( "A valid userID must be provided when initializing this module." )
    if not isinstance( self.privateKey, bytes ):
      raise TypeError( "A valid privateKey must be provided when initializing this module." )
    if not isinstance( method, str ):
      raise TypeError( "Parameter 'method' must be a string." )
    if not isinstance( endpoint, str ):
      raise TypeError( "Parameter 'endpoint' must be a string." )
    if data is not None or filename is not None:
      if not isinstance( data, object ):
        raise TypeError( "Parameter 'data' must be a set, if filename is provided." )
      if not isinstance( filename, str ):
        raise TypeError( "Parameter 'filename' must be a string, if data is provided." )
    if parameters is not None and not isinstance( parameters, object ):
      raise TypeError( "Parameter 'parameters' must be a set, if provided." )

    validEndpoints = {
      'Upload',
      'UploadAttachment',
      'StartImport',
      'StartXmlExport',
      'SubmitDatasetToCdx',
      'SubmitFileToCdx',
      'GetStatus',
      'GetDocumentList',
      'Projects',
      'MonitoringLocations'
    }

    # Test parameter values
    if method not in ( 'GET', 'POST' ):
      raise ValueError( "Parameter 'method' must be one of 'GET' or 'POST'" )
    if endpoint not in validEndpoints:
      raise ValueError( "Parameter 'endpoint' must match a WQX endpoint name.")
    
    # Prepare some intermediate values
    timeStamp = datetime.datetime.utcnow().strftime( "%m/%d/%Y %I:%M:%S %p" )
    if filename is not None:
      addr = f"https://cdx.epa.gov/WQXWeb/api/{endpoint}/{filename}"
    else:
      addr = f"https://cdx.epa.gov/WQXWeb/api/{endpoint}"

    req = requests.Request( method, addr, data=data, params=parameters )

    print( f"Requesting {req.prepare().url}" )

    signature = f"{self.userID}{timeStamp}{req.prepare().url}{method}"
    digest = hmac.digest( self.privateKey, bytes(signature,'utf-8'), sha256 )

    req.headers = {
      "Content-Type": "application/json",
      "X-UserID": self.userID,
      "X-Stamp": timeStamp,
      "X-Signature": base64.b64encode( digest ).decode()
    }

    res = self.session.send( req.prepare() )

    if res.status_code == 403:
      self.userID = None
      self.privateKey = None
      raise PermissionError( "The provided credentials are invalid. No further API calls will be honored." )

    if not isinstance( res.text, str ):
      raise RuntimeError( f"API endpoint gave status code {res.status_code} with no text." )

    return res

  def Upload(self,
    filename,
    contents
  ):

    # Test parameter types
    if not isinstance( filename, str ):
      raise TypeError( "Parameter 'filename' must be a string." )
    if not isinstance( contents, bytes ):
      raise TypeError( "Parameter 'contents' must be a bytes array." )

    # Test parameter values
    if not re.match( "^[\w\-. ]+\.(txt|csv|xlsx|xls|xml|zip)$", filename, re.IGNORECASE ):
      raise ValueError( "Parameter 'filename' must be a filename with an allowed file extension." )

    res = self.queryWQX( 'POST', 'Upload', filename=filename, data=contents )
    
    if res.text[0] != '"':
      raise WQXException( res.text )

    return res.text.strip( '"' )

  def UploadAttachment(self,
    filename,
    contents
  ):

    # Test parameter types
    if not isinstance( filename, str ):
      raise TypeError( "Parameter 'filename' must be a string." )
    if not isinstance( contents, bytes ):
      raise TypeError( "Parameter 'contents' must be a bytes array." )

    # Test parameter values
    if not re.match( "^[\w\-. ]+\.zip$", filename, re.IGNORECASE ):
      raise ValueError( "Parameter 'filename' must be a filename with a 'zip' file extension." )

    res = self.queryWQX( 'POST', 'UploadAttachment', filename=filename, data=contents )
    
    if res.text[0] != '"':
      raise WQXException( res.text )

    return res.text.strip( '"' )

  def StartImport(self,
    importConfigurationId,
    fileId,
    attachmentFileId = None,
    fileType = None,
    newOrExistingData = None,
    uponCompletion = None,
    uponCompletionCondition = None,
    worksheetsToImport = None,
    ignoreFirstRowOfFile = None,
    generatedElementName1 = None,
    generatedElementValue1 = None,
    generatedElementName2 = None,
    generatedElementValue2 = None,
    generatedElementName3 = None,
    generatedElementValue3 = None,
    generatedElementName4 = None,
    generatedElementValue4 = None,
    generatedElementName5 = None,
    generatedElementValue5 = None
  ):

    # Test parameter types
    if not isinstance( importConfigurationId, str ):
      raise TypeError( "Parameter 'importConfigurationId' must be a string." )
    if not isinstance( fileId, str ):
      raise TypeError( "Parameter 'fileId' must be a string." )
    if attachmentFileId is not None and not isinstance( attachmentFileId, str ):
      raise TypeError( "Parameter 'attachmentFileId' must be a string, if provided." )
    if not isinstance( fileType, str ) and not isinstance( fileType, FileType ):
      raise TypeError( "Parameter 'fileType' must be an enum member or string." )
    if not isinstance( newOrExistingData, int ) and not isinstance( newOrExistingData, NewOrExistingData ):
      raise TypeError( "Parameter 'newOrExistingData' must be an enum member or integer." )
    if not isinstance( uponCompletion, int ) and not isinstance( uponCompletion, UponImportCompletion ):
      raise TypeError( "Parameter 'uponCompletion' must be an enum member or integer." )
    if uponCompletionCondition is not None and not isinstance( uponCompletionCondition, int ) and not isinstance( uponCompletionCondition, UponCompletionCondition ):
      raise TypeError( "Parameter 'uponCompletionCondition' must be an enum member or integer, if provided." )
    if worksheetsToImport is not None and not isinstance( worksheetsToImport, str ):
      raise TypeError( "Parameter 'worksheetsToImport' must be a string, if provided." )
    if ignoreFirstRowOfFile is not None and not isinstance( ignoreFirstRowOfFile, bool ):
      raise TypeError( "Parameter 'ignoreFirstRowOfFile' must be a boolean, if provided." )
    if generatedElementName1 is not None or generatedElementValue1 is not None:
      if not isinstance( generatedElementName1, str ):
          raise TypeError( "Parameter 'generatedElementName1' must be a string, if 'generatedElementValue1' is provided." )
      if not isinstance( generatedElementValue1, str ):
          raise TypeError( "Parameter 'generatedElementValue1' must be a string, if 'generatedElementName1' is provided." )
    if generatedElementName2 is not None or generatedElementValue2 is not None:
      if not isinstance( generatedElementName2, str ):
          raise TypeError( "Parameter 'generatedElementName2' must be a string, if 'generatedElementValue2' is provided." )
      if not isinstance( generatedElementValue2, str ):
          raise TypeError( "Parameter 'generatedElementValue2' must be a string, if 'generatedElementName2' is provided." )
    if generatedElementName3 is not None or generatedElementValue3 is not None:
      if not isinstance( generatedElementName3, str ):
          raise TypeError( "Parameter 'generatedElementName3' must be a string, if 'generatedElementValue3' is provided." )
      if not isinstance( generatedElementValue3, str ):
          raise TypeError( "Parameter 'generatedElementValue3' must be a string, if 'generatedElementName3' is provided." )
    if generatedElementName4 is not None or generatedElementValue4 is not None:
      if not isinstance( generatedElementName4, str ):
          raise TypeError( "Parameter 'generatedElementName4' must be a string, if 'generatedElementValue4' is provided." )
      if not isinstance( generatedElementValue4, str ):
          raise TypeError( "Parameter 'generatedElementValue4' must be a string, if 'generatedElementName4' is provided." )
    if generatedElementName5 is not None or generatedElementValue5 is not None:
      if not isinstance( generatedElementName5, str ):
          raise TypeError( "Parameter 'generatedElementName5' must be a string, if 'generatedElementValue5' is provided." )
      if not isinstance( generatedElementValue5, str ):
          raise TypeError( "Parameter 'generatedElementValue5' must be a string, if 'generatedElementName5' is provided." )

    # Test parameter values
    if fileType not in [v.value for v in FileType.__members__.values()]:
      raise ValueError( "Parameter: 'fileType' is not one of the allowed values.")
    if newOrExistingData not in NewOrExistingData.__members__.values():
      raise ValueError( "Parameter: 'newOrExistingData' is not one of the allowed values.")
    if uponCompletion not in UponImportCompletion.__members__.values():
      raise ValueError( "Parameter: 'uponCompletion' is not one of the allowed values.")
    if uponCompletionCondition not in UponCompletionCondition.__members__.values():
      raise ValueError( "Parameter: 'uponCompletionCondition' is not one of the allowed values.")
    if uponCompletion == self.EXPORT_IMPORT or uponCompletion == self.SUBMIT_IMPORT:
      if uponCompletionCondition == None or uponCompletionCondition == self.NOT_APPLICABLE:
        raise ValueError( "Parameter: 'uponCompletionCondition' is required because of 'uponCompletion' value.")
    if worksheetsToImport is not None and not re.match( '^([1-9]\d*)(,[1-9]\d*)*$', worksheetsToImport ):
      raise ValueError( "Parameter: 'worksheetsToImport' must be a comma separated list of numbers." )

    # Prepare some intermediate values
    fileTypeStr = fileType.value if fileType is not None else None
    newOrExistingDataStr = str(newOrExistingData.value) if newOrExistingData is not None else None
    uponCompletionStr = str(uponCompletion.value) if uponCompletion is not None else None
    uponCompletionConditionStr = str(uponCompletionCondition.value) if uponCompletionCondition is not None else None

    params={
      "importConfigurationId": importConfigurationId,
      "fileId": fileId,
      "attachmentFileId": attachmentFileId,
      "fileType": fileTypeStr,
      "newOrExistingData": newOrExistingDataStr,
      "uponCompletion": uponCompletionStr,
      "uponCompletionCondition": uponCompletionConditionStr,
      "worksheetsToImport": worksheetsToImport,
      "ignoreFirstRowOfFile": 'true' if ignoreFirstRowOfFile else 'false',
      "generatedElementName1": generatedElementName1,
      "generatedElementValue1": generatedElementValue1,
      "generatedElementName2": generatedElementName2,
      "generatedElementValue2": generatedElementValue2,
      "generatedElementName3": generatedElementName3,
      "generatedElementValue3": generatedElementValue3,
      "generatedElementName4": generatedElementName4,
      "generatedElementValue4": generatedElementValue4,
      "generatedElementName5": generatedElementName5,
      "generatedElementValue5": generatedElementValue5
    }
    
    res = self.queryWQX( 'GET', 'StartImport', parameters=params )
    
    if res.text[0] != '"':
      raise WQXException( res.text )

    return res.text.strip( '"' )

  def StartXmlExport(self,
    datasetId,
    uponCompletion = None
  ):

    # Test parameter types
    if not isinstance( datasetId, str ):
      raise TypeError( "Parameter 'datasetId' must be an str." )
    if not isinstance( uponCompletion, int ) and not isinstance( uponCompletion, UponExportCompletion ):
      raise TypeError( "Parameter 'uponCompletion' must be an enum member or an integer." )

    # Test parameter values
    if uponCompletion not in UponExportCompletion.__members__.values():
      raise ValueError( "Parameter: 'uponCompletion' is not one of the allowed values." )

    # Prepare intermediate values
    if isinstance( uponCompletion, UponExportCompletion ):
      uponCompletionStr = uponCompletion.value
    else:
      uponCompletionStr = str(uponCompletion)

    params={
      "datasetId": datasetId,
      "uponCompletion": uponCompletionStr
    }
    res = self.queryWQX( 'GET', 'StartXmlExport', parameters=params )

    if res.text[0] != '{':
      raise WQXException( res.text )

    try:
      return res.json()
    except:
      raise WQXException( res.text )

  def SubmitDatasetToCdx(self,
    datasetId
  ):

    # Test parameter types
    if not isinstance( datasetId, str ):
      raise TypeError( "Parameter 'datasetId' must be an str." )

    params={
      "datasetId": datasetId
    }

    res = self.queryWQX( 'GET', 'SubmitDatasetToCdx', parameters=params )

    if res.text[0] != '{':
      raise WQXException( res.text )

    try:
      return res.json()
    except:
      raise WQXException( res.text )

  def SubmitFileToCdx(self,
    fileId
  ):

    # Test parameter types
    if not isinstance( fileId, str ):
      raise TypeError( "Parameter 'fileId' must be an str." )

    params={
      "fileId": fileId
    }

    res = self.queryWQX( 'GET', 'SubmitDatasetToCdx', parameters=params )

    if res.text[0] != '{':
      raise WQXException( res.text )

    try:
      return res.json()
    except:
      raise WQXException( res.text )

  def GetStatus(self,
    datasetId
  ):

    # Test parameter types
    if not isinstance( datasetId, str ):
      raise TypeError( "Parameter 'datasetId' must be an str." )

    params={
      "datasetId": datasetId
    }

    res = self.queryWQX( 'GET', 'GetStatus', parameters=params )

    if res.text[0] != '{':
      raise WQXException( res.text )

    try:
      return res.json()
    except:
      raise WQXException( res.text )

  def GetDocumentList(self,
    datasetId
  ):

    # Test parameter types
    if not isinstance( datasetId, str ):
      raise TypeError( "Parameter 'datasetId' must be an str." )

    params={
      "datasetId": datasetId
    }

    res = self.queryWQX( 'GET', 'GetDocumentList', parameters=params )

    if res.text[0] != '[':
      raise WQXException( res.text )

    try:
      return res.json()
    except:
      raise WQXException( res.text )

  def Projects(self,
    organizationIdentifiersCsv,
    projectIdentifiersCsv = None,
    transactionIdentifier = None,
    lastChangeDateMin = None,
    lastChangeDateMax = None,
    startRow = 0,
    rowsToRetrieve = 100
  ):

    # Test parameter types
    if not isinstance( organizationIdentifiersCsv, str ):
      raise TypeError( "Parameter 'organizationIdentifiersCsv' must be an str." )
    if projectIdentifiersCsv is not None and not isinstance( projectIdentifiersCsv, str ):
      raise TypeError( "Parameter 'projectIdentifiersCsv' must be an str, if provided." )
    if transactionIdentifier is not None and not isinstance( transactionIdentifier, str ):
      raise TypeError( "Parameter 'transactionIdentifier' must be an str, if provided." )
    if lastChangeDateMin is not None and not isinstance( lastChangeDateMin, datetime.date ):
      raise TypeError( "Parameter 'lastChangeDateMin' must be a date object, if provided." )
    if lastChangeDateMax is not None and not isinstance( lastChangeDateMax, datetime.date ):
      raise TypeError( "Parameter 'lastChangeDateMax' must be a date object, if provided." )
    if startRow is not None and not isinstance( startRow, int ):
      raise TypeError( "Parameter 'startRow' must be an int, if provided." )
    if rowsToRetrieve is not None and not isinstance( rowsToRetrieve, int ):
      raise TypeError( "Parameter 'rowsToRetrieve' must be an int, if provided." )

    # Test parameter values
    if ' ' in organizationIdentifiersCsv:
      raise ValueError( "Parameter 'organizationIdentifiersCsv' must not contain spaces." )
    if ' ' in projectIdentifiersCsv:
      raise ValueError( "Parameter 'projectIdentifiersCsv' must not contain spaces." )
    if startRow < 0:
      raise ValueError( "Parameter 'startRow' must be a non-negative integer, if provided." )
    if rowsToRetrieve <= 0 or rowsToRetrieve >= 25000:
      raise ValueError( "Parameter 'rowsToRetrieve' must be a positive integer less than 25000, if provided." )

    # Format dates, if present
    lastChangeDateMinStr = lastChangeDateMin.strftime( "%m-%d-%Y" ) if lastChangeDateMin is not None else None
    lastChangeDateMaxStr = lastChangeDateMax.strftime( "%m-%d-%Y" ) if lastChangeDateMax is not None else None

    params={
      "OrganizationIdentifiersCsv": organizationIdentifiersCsv,
      "ProjectIdentifiersCsv": projectIdentifiersCsv,
      "TransactionIdentifier": transactionIdentifier,
      "LastChangeDateMin": lastChangeDateMinStr,
      "LastChangeDateMax": lastChangeDateMaxStr,
      "StartRow": startRow,
      "RowsToRetrieve": rowsToRetrieve
    }

    res = self.queryWQX( 'GET', 'Projects', parameters=params )

    if res.text[0] != '[':
      raise WQXException( res.text )

    try:
      return res.json()
    except:
      raise WQXException( res.text )

  def MonitoringLocations(self,
    organizationIdentifiersCsv,
    monitoringLocationIdentifiersCsv = None,
    monitoringLocationName = None,
    monitoringLocationType = None,
    transactionIdentifier = None,
    lastChangeDateMin = None,
    lastChangeDateMax = None,
    startRow = 0,
    rowsToRetrieve = 100
  ):

    # Test parameter types
    if not isinstance( organizationIdentifiersCsv, str ):
      raise TypeError( "Parameter 'organizationIdentifiersCsv' must be an str." )
    if monitoringLocationIdentifiersCsv is not None and not isinstance( monitoringLocationIdentifiersCsv, str ):
      raise TypeError( "Parameter 'monitoringLocationIdentifiersCsv' must be an str, if provided." )
    if monitoringLocationName is not None and not isinstance( monitoringLocationName, str ):
      raise TypeError( "Parameter 'monitoringLocationName' must be an str, if provided.")
    if monitoringLocationType is not None and not isinstance( monitoringLocationType, str ):
      raise TypeError( "Parameter 'monitoringLocationType' must be an str, if provided." )
    if transactionIdentifier is not None and not isinstance( transactionIdentifier, str ):
      raise TypeError( "Parameter 'transactionIdentifier' must be an str, if provided." )
    if lastChangeDateMin is not None and not isinstance( lastChangeDateMin, datetime.date ):
      raise TypeError( "Parameter 'lastChangeDateMin' must be a date object, if provided." )
    if lastChangeDateMax is not None and not isinstance( lastChangeDateMax, datetime.date ):
      raise TypeError( "Parameter 'lastChangeDateMax' must be a date object, if provided." )
    if startRow is not None and not isinstance( startRow, int ):
      raise TypeError( "Parameter 'startRow' must be an int, if provided." )
    if rowsToRetrieve is not None and not isinstance( rowsToRetrieve, int ):
      raise TypeError( "Parameter 'rowsToRetrieve' must be an int, if provided." )

    # Test parameter value ranges
    if ' ' in organizationIdentifiersCsv:
      raise ValueError( "Parameter 'organizationIdentifiersCsv' must not contain spaces." )
    if monitoringLocationIdentifiersCsv is not None and ' ' in monitoringLocationIdentifiersCsv:
      raise ValueError( "Parameter 'monitoringLocationIdentifiersCsv' must not contain spaces, if provided." )
    if startRow < 0:
      raise ValueError( "startRow must be a non-negative integer." )
    if rowsToRetrieve <= 0 or rowsToRetrieve >= 25000:
      raise ValueError( "rowsToRetrieve must be a positive integer less than 25000." )

    # Format dates, if present
    lastChangeDateMinStr = lastChangeDateMin.strftime( "%m-%d-%Y" ) if lastChangeDateMin is not None else None
    lastChangeDateMaxStr = lastChangeDateMax.strftime( "%m-%d-%Y" ) if lastChangeDateMax is not None else None

    params={
      "OrganizationIdentifiersCsv": organizationIdentifiersCsv,
      "MonitoringLocationIdentifiersCsv": monitoringLocationIdentifiersCsv,
      "MonitoringLocationName": monitoringLocationName,
      "MonitoringLocationType": monitoringLocationType,
      "TransactionIdentifier": transactionIdentifier,
      "LastChangeDateMin": lastChangeDateMinStr,
      "LastChangeDateMax": lastChangeDateMaxStr,
      "StartRow": startRow,
      "RowsToRetrieve": rowsToRetrieve
    }

    res = self.queryWQX( 'GET', 'MonitoringLocations', parameters=params )
    
    if res.text[0] != '[':
      raise WQXException( res.text )

    try:
      return res.json()
    except:
      raise WQXException( res.text )
