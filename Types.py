from enum import Enum

class file(Enum):
    DWG = r"..\AutoCAD CSharp plug-in Get Text From Drawings\AutoCAD CSharp plug-in Get Text From Drawings\bin\Release\extractDWG.json"
    IPT = r"..\ConsoleApplication Get Inventor\ConsoleApplication Get Inventor\bin\Release\extractIPT.json"
    IDW = r"..\ConsoleApplication Get Inventor\ConsoleApplication Get Inventor\bin\Release\extractIDW.json"
    IAM = r"..\ConsoleApplication Get Inventor\ConsoleApplication Get Inventor\bin\Release\extractIAM.json"
    PDFDocuments = r"..\ConsoleApplication Get PDFs\ConsoleApplication Get PDFs\bin\Release\extractPDFDocuments.json"
    PDFDrawings = r"..\ConsoleApplication Get PDFs\ConsoleApplication Get PDFs\bin\Release\extractPDFDrawings.json"
    ServiceRequests = r"..\ConsoleApplication Get SharePoint\ConsoleApplication Get SharePoint\bin\Release\extractServiceRequests.json"



class fileType(Enum):
    DWG = "DWG"
    INVENTOR = "INVENTOR"
    PDFDocuments = "PDFDOCUMENTS"
    PDFDrawings = "PDFDRAWINGS"
    ServiceRequests = "SERVICEREQUESTS"


class searchType(Enum):
    NonApprovedCLSIDrawings = "NON-APPROVED CLSI DRAWINGS"
    ApprovedCLSIDrawings = "APPROVED CLSI DRAWINGS"
    ApprovedCLSIDocuments = "APPROVED CLSI DOCUMENTS"
    ServiceRequests = "SERVICE REQUESTS"


class boolType(Enum):
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
