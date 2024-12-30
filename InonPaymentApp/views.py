from django.shortcuts import render,redirect
from KttApp.models import *
from django.http import JsonResponse
from django .http import HttpResponse
import pandas as pd
import json
from rest_framework import viewsets,filters 
from .serializers import InNonSeralizer
from .models import *
from django.views import View
from KttApp.views import SqlDb
from django_filters.rest_framework  import DjangoFilterBackend
from reportlab.pdfgen import canvas
import io
from reportlab.graphics.barcode import code39
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
from decimal import *
from reportlab.platypus import Table, TableStyle,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import xml.etree.ElementTree as ET
import zipfile
import xlwt

def InonoList(request):
    return render(request, 'InonPayment/InonPaymentList.html',{
        'CustomiseReport': CustomiseReport.objects.filter(ReportName="IPT", UserName=request.session['Username']).exclude(FiledName='id'),
        'ManageUserMail': ManageUser.objects.filter(Status='Active').order_by('MailBoxId').values_list('MailBoxId', flat=True).distinct(),
        'UserName':request.session['Username']
        })
      
class InonPayment(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
       
    def get(self,request):
        Username = request.session['Username'] 

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")
        currentDate = datetime.now().strftime("%d/%m/%Y")

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))
       
        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) + 1  FROM InNonHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'INPDEC' ".format(refDate))
        self.RefId = ("%03d" % self.cursor.fetchone()[0])

        self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 

        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"

        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='" + Username + "'")
        InNonHeadData = self.cursor.fetchone()

        context = { 
            "UserName" : Username,
            "PermitIdInNon":self.PermitIdInNon,
            "JobId" : self.JobId,
            "RefId" : self.RefId,
            "MsgId" : self.MsgId,
            "AccountId" : AccountId,
            "LoginStatus" : InNonHeadData[0],
            "DateLastUpdated" : InNonHeadData[1],
            "MailBoxId" : InNonHeadData[2],
            "SeqPool" : InNonHeadData[3],
            "StartSequence" : InNonHeadData[4],
            "TradeNetMailboxID" : InNonHeadData[5],
            "DeclarantName" : InNonHeadData[6],
            "DeclarantCode" : InNonHeadData[7],
            "DeclarantTel" : InNonHeadData[8],
            "CRUEI" : InNonHeadData[9],
            "Code" : InNonHeadData[10],
            "name" : InNonHeadData[11],
            "name1" : InNonHeadData[12],
            'DeclarationType':CommonMaster.objects.filter(TypeId=13, StatusId=1).order_by("Name"),
            'CargoType': CommonMaster.objects.filter(TypeId=2, StatusId=1),
            'InwardTransportMode': CommonMaster.objects.filter(TypeId=3, StatusId=1).order_by('Name'),
            'DeclaringFor': CommonMaster.objects.filter(TypeId=80, StatusId=1).order_by('Name'),
            'BgIndicator': CommonMaster.objects.filter(TypeId=4, StatusId=1).order_by('Name'),
            'DocumentAttachmentType': CommonMaster.objects.filter(TypeId=5, StatusId=1).order_by('Name'),
            'ContainerSizeDrop': CommonMaster.objects.filter(TypeId=6, StatusId=1).order_by('Name'),
            "currentDate": currentDate 
        }
        return render(request, 'InonPayment/InonPaymentNew.html',context)

class InonPaymentEdit(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
       
    def get(self,request):
        if not request.GET.get('InNonId'):
            InNonId = request.session['InNonId']
            print("innonid:",InNonId)

            self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(request.session['Username'] ))
            AccountId = self.cursor.fetchone()[0]

            self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='" + request.session['Username'] + "'")
            InNonHeadData = self.cursor.fetchone()

            self.cursor.execute("SELECT Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime FROM InNonHeaderTbl WHERE Id = '{}' ".format(InNonId))

            InNonHeaderData = self.cursor.fetchall()


            self.RefId = InNonHeaderData[0][0]
            self.JobId = InNonHeaderData[0][1]
            self.MsgId = InNonHeaderData[0][2]
            self.PermitIdInNon = InNonHeaderData[0][3]
            prmtStatus = InNonHeaderData[0][-9]
            PermitNumber = InNonHeaderData[0][-10]

            context = { 
                "UserName" : request.session['Username'] ,
                "PermitIdInNon":self.PermitIdInNon,
                "JobId" : self.JobId,
                "RefId" : self.RefId,
                "MsgId" : self.MsgId,
                "AccountId" : AccountId,
                "LoginStatus" : InNonHeadData[0],
                "DateLastUpdated" : InNonHeadData[1],
                "MailBoxId" : InNonHeadData[2],
                "SeqPool" : InNonHeadData[3],
                "StartSequence" : InNonHeadData[4],
                "TradeNetMailboxID" : InNonHeadData[5],
                "DeclarantName" : InNonHeadData[6],
                "DeclarantCode" : InNonHeadData[7],
                "DeclarantTel" : InNonHeadData[8],
                "CRUEI" : InNonHeadData[9],
                "Code" : InNonHeadData[10],
                "name" : InNonHeadData[11],
                "name1" : InNonHeadData[12],
                'DeclarationType':CommonMaster.objects.filter(TypeId=13, StatusId=1).order_by("Name"),
                'CargoType': CommonMaster.objects.filter(TypeId=2, StatusId=1),
                'InwardTransportMode': CommonMaster.objects.filter(TypeId=3, StatusId=1).order_by('Name'),
                'DeclaringFor': CommonMaster.objects.filter(TypeId=80, StatusId=1).order_by('Name'),
                'BgIndicator': CommonMaster.objects.filter(TypeId=4, StatusId=1).order_by('Name'),
                'DocumentAttachmentType': CommonMaster.objects.filter(TypeId=5, StatusId=1).order_by('Name'),
                'ContainerSizeDrop': CommonMaster.objects.filter(TypeId=6, StatusId=1).order_by('Name'),
                'InNonHeaderData' : (pd.DataFrame(list(InNonHeaderData), columns=['Refid','JobId','MSGId','PermitId','TradeNetMailboxID','MessageType','DeclarationType','PreviousPermit','CargoPackType','InwardTransportMode','OutwardTransportMode','BGIndicator','SupplyIndicator','ReferenceDocuments','License','Recipient','DeclarantCompanyCode','ImporterCompanyCode','ExporterCompanyCode','InwardCarrierAgentCode','OutwardCarrierAgentCode','ConsigneeCode','FreightForwarderCode','ClaimantPartyCode','ArrivalDate','LoadingPortCode','VoyageNumber','VesselName','OceanBillofLadingNo','ConveyanceRefNo','TransportId','FlightNO','AircraftRegNo','MasterAirwayBill','ReleaseLocation','RecepitLocation','RecepilocaName','StorageLocation','ExhibitionSDate','ExhibitionEDate','BlanketStartDate','TradeRemarks','InternalRemarks','CustomerRemarks','DepartureDate','DischargePort','FinalDestinationCountry','OutVoyageNumber','OutVesselName','OutOceanBillofLadingNo','VesselType','VesselNetRegTon','VesselNationality','TowingVesselID','TowingVesselName','NextPort','LastPort','OutConveyanceRefNo','OutTransportId','OutFlightNO','OutAircraftRegNo','OutMasterAirwayBill','TotalOuterPack','TotalOuterPackUOM','TotalGrossWeight','TotalGrossWeightUOM','GrossReference','DeclareIndicator','NumberOfItems','TotalCIFFOBValue','TotalGSTTaxAmt','TotalExDutyAmt','TotalCusDutyAmt','TotalODutyAmt','TotalAmtPay','Status','TouchUser','TouchTime','PermitNumber','prmtStatus','ReleaseLocaName','Inhabl','outhbl','seastore','Cnb','DeclarningFor','MRDate','MRTime'])).to_dict('records'),
            }
            print("InNonHeaderData:",InNonHeaderData)

            if prmtStatus == "AME":
                self.cursor.execute(f"select Count(PermitNumber) from InNonHeaderTbl where Id='" + str(InNonId) + "' and (Status='APR' or Status='AME') and prmtStatus='AME'")
                AMendData = self.cursor.fetchone()

                self.cursor.execute(f"SELECT Permitno,AmendmentCount,UpdateIndicator,ReplacementPermitno,DescriptionOfReason,PermitExtension,ExtendImportPeriod,DeclarationIndigator,AmendType FROM InNonAmend WHERE MSGId = '{self.MsgId}' ") 
                AmendEditdata = (pd.DataFrame(list(self.cursor.fetchall()), columns=["Permitno", "AmendmentCount", "UpdateIndicator","ReplacementPermitno","DescriptionOfReason", "PermitExtension", "ExtendImportPeriod","DeclarationIndigator","AmendType"])).to_dict('records')
                
                context.update({
                    "AmendPages" : True,
                    "AmendCount" : int(AMendData[0])+1,
                    "PermitNumber" : PermitNumber,
                    "AmendEditdata" : AmendEditdata,
                    })
                
            elif prmtStatus == "CNL":
                self.cursor.execute("SELECT Name,Description FROM CommonMaster WHERE TypeId=75 AND StatusId=1 ORDER BY Name")
                self.RFCancel = self.cursor.fetchall()

                self.cursor.execute(f"SELECT Permitno,UpdateIndicator,ReplacementPermitno,ResonForCancel,DescriptionOfReason,DeclarationIndigator,MSGId,CancelType FROM InNonCancel WHERE MSGId = '{self.MsgId}' AND Permitno= '{PermitNumber}' ")                               
                context.update({
                    "CancelPages" : True,
                    "PermitNumber" : PermitNumber,
                    "CancelData"  : (pd.DataFrame(list(self.cursor.fetchall()),columns=['Permitno','UpdateIndicator','ReplacementPermitno','ResonForCancel','DescriptionOfReason','DeclarationIndigator','MSGId','CancelType']).to_dict('records')),
                    "ReasonForCancel" : (pd.DataFrame(list(self.RFCancel), columns=["Name","Description"])).to_dict('records'),
                    })
                
            return render(request, 'InonPayment/InonPaymentNew.html',context)
    
        else:
            request.session['InNonId'] = request.GET.get('InNonId')
            return JsonResponse({"url" : '/InonPayementEdit/'}) 
        


class InonPaymentShow(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
       
    def get(self,request,id):
        Username = request.session["Username"]
        self.cursor.execute(f"SELECT * FROM InNonHeaderTbl WHERE id = {id}")
        headers = [i[0] for i in self.cursor.description]
        innonALL = list(self.cursor.fetchall())

        for i in innonALL:
            print("test ans :",i)

        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate, AccountId))
        

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"+ Username+ "'")
        InNonHeadData = self.cursor.fetchone()
    #     if not request.GET.get('InNonId'):
    #         Id = request.session['InNonId']

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(request.session['Username'] ))
        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='" + request.session['Username'] + "'")
        InNonHeadData = self.cursor.fetchone()
   

        context = { 
                "UserName" : Username,
                "PermitIdInNon":innonALL[0][4],
                "JobId" : innonALL[0][2],
                "RefId" : innonALL[0][1],
                "MsgId" : innonALL[0][3],
                "AccountId" : AccountId,
                "LoginStatus" : InNonHeadData[0],
                "DateLastUpdated" : InNonHeadData[1],
                "MailBoxId" : InNonHeadData[2],
                "SeqPool" : InNonHeadData[3],
                "StartSequence" : InNonHeadData[4],
                "TradeNetMailboxID" : InNonHeadData[5],
                "DeclarantName" : InNonHeadData[6],
                "DeclarantCode" : InNonHeadData[7],
                "DeclarantTel" : InNonHeadData[8],
                "CRUEI" : InNonHeadData[9],
                "Code" : InNonHeadData[10],
                "name" : InNonHeadData[11],
                "name1" : InNonHeadData[12],
                'DeclarationType':CommonMaster.objects.filter(TypeId=13, StatusId=1).order_by("Name"),
                'CargoType': CommonMaster.objects.filter(TypeId=2, StatusId=1),
                'InwardTransportMode': CommonMaster.objects.filter(TypeId=3, StatusId=1).order_by('Name'),
                'DeclaringFor': CommonMaster.objects.filter(TypeId=80, StatusId=1).order_by('Name'),
                'BgIndicator': CommonMaster.objects.filter(TypeId=4, StatusId=1).order_by('Name'),
                'DocumentAttachmentType': CommonMaster.objects.filter(TypeId=5, StatusId=1).order_by('Name'),
                'ContainerSizeDrop': CommonMaster.objects.filter(TypeId=6, StatusId=1).order_by('Name'),

            }


        context.update({
            "Show" : (pd.DataFrame(innonALL, columns=headers)).to_dict("records"),
 
        }) 

        status = innonALL[0][76]
        print('status:',status)

        if status == 'REJ':
        
            msgid = innonALL[0][3]  
            print('msgid:',msgid)
            chkMailId = InNonHeadData[2]  
            print('chkMailId:',chkMailId)

            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ErrorID as Code, 
                    ErrorDescription as Description 
                FROM InnonRejectStatus 
                WHERE MsgID = %s 
                AND MailBoxId = %s 
                AND RType = 'REJ' 
                ORDER BY Sno
            """, [msgid, chkMailId])

            apr_data = self.cursor.fetchall()

            apr_data_dict = []  # This will store rejection data
            if apr_data:
                for row in apr_data:
                    apr_data_dict.append({
                        'SNo': row[0],
                        'Code': row[1],
                        'Description': row[2]
                    })
            else:
                apr_data_dict.append({
                    'SNo': 'No Data',
                    'Code': 'No Data',
                    'Description': 'No Data'
                })

            context['APRData'] = apr_data_dict

            print("Rejection Data:", context['APRData'])

        elif status == 'QRY':
            msgid = innonALL[0][3]  
            chkMailId = InNonHeadData[2] 
        
            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ErrorID as Code, 
                    ErrorDescription as Description 
                FROM InnonRejectStatus 
                WHERE MsgID = %s 
                AND MailBoxId = %s 
                AND RType = 'QRY' 
                ORDER BY Sno
            """, [msgid, chkMailId])
            apr_data = self.cursor.fetchall()

            apr_data_dict = []  
            if apr_data:
                for row in apr_data:
                    apr_data_dict.append({
                        'SNo': row[0],
                        'Code': row[1],
                        'Description': row[2]
                    })
            else:
                apr_data_dict.append({
                    'SNo': 'No Data',
                    'Code': 'No Data',
                    'Description': 'No Data'
                })

            context['APRData'] = apr_data_dict

            print("Rejection Data:", context['APRData'])

        elif status == 'APR':
            self.cursor.execute("""
                    SELECT Sno as SNo, ConditionCode as Code, ConditionDescription as Description 
                    FROM Innonpmt 
                    WHERE permitnumber = %s 
                    ORDER BY Sno
                """, [innonALL[0][75]])
            apr_data = self.cursor.fetchall()

            apr_data_dict = []  # This will store APR data
            if apr_data:
                for row in apr_data:
                    apr_data_dict.append({
                        'SNo': row[0],
                        'Code': row[1],
                        'Description': row[2]
                    })
            else:
                apr_data_dict.append({
                    'SNo': 'No Data',
                    'Code': 'No Data',
                    'Description': 'No Data'
                })

            context['APRData'] = apr_data_dict

        elif status == 'ERR':
        
            msgid = innonALL[0][3]  
            chkMailId = InNonHeadData[2]  

            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ErrorCode  as Code, 
                    ErrorDescription+' '+ErrorTrace as Description 
                FROM InnonErrorStatus 
                WHERE MsgID = %s 
                AND MailBoxId = %s 
                ORDER BY Sno
            """, [msgid, chkMailId])

            apr_data = self.cursor.fetchall()

            apr_data_dict = []  # This will store rejection data
            if apr_data:
                for row in apr_data:
                    apr_data_dict.append({
                        'SNo': row[0],
                        'Code': row[1],
                        'Description': row[2]
                    })
            else:
                apr_data_dict.append({
                    'SNo': 'No Data',
                    'Code': 'No Data',
                    'Description': 'No Data'
                })

            context['APRData'] = apr_data_dict

            print("Rejection Data:", context['APRData'])


        
        elif status == 'CNL':
        
            msgid = innonALL[0][3]  
            chkMailId = InNonHeadData[2]  

            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ConditionCde  as Code, 
                    ConditionDes as Description 
                FROM InnonCancelPermit 
                WHERE permitnumber = %s
                AND MsgID = %s 
                AND MailBoxId = %s  
                ORDER BY Sno
            """, [innonALL[0][75],msgid, chkMailId])

            apr_data = self.cursor.fetchall()

            apr_data_dict = []  # This will store rejection data
            if apr_data:
                for row in apr_data:
                    apr_data_dict.append({
                        'SNo': row[0],
                        'Code': row[1],
                        'Description': row[2]
                    })
            else:
                apr_data_dict.append({
                    'SNo': 'No Data',
                    'Code': 'No Data',
                    'Description': 'No Data'
                })

            context['APRData'] = apr_data_dict

            print("Rejection Data:", context['APRData'])

        elif status == 'AME':
        
            msgid = innonALL[0][3]  
            chkMailId = InNonHeadData[2]  

            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ConditionCode as Code, 
                    ConditionDescription as Description 
                FROM InnonAMDPMT 
                 WHERE permitnumber = %s
                AND MsgID = %s 
                AND MailBoxId = %s  
                ORDER BY Sno
            """, [innonALL[0][75],msgid, chkMailId])

            apr_data = self.cursor.fetchall()

            apr_data_dict = []  # This will store rejection data
            if apr_data:
                for row in apr_data:
                    apr_data_dict.append({
                        'SNo': row[0],
                        'Code': row[1],
                        'Description': row[2]
                    })
            else:
                apr_data_dict.append({
                    'SNo': 'No Data',
                    'Code': 'No Data',
                    'Description': 'No Data'
                })

            context['APRData'] = apr_data_dict

            print("Rejection Data:", context['APRData'])
        
        else:
            context['APRData'] =[]


        # Debugging: Print out the APR Data
        print("APR Data:", context['APRData'])
        for item in context["Show"]:
            print("Row:")
            for key, value in item.items():
                print(f"  {key}: {value}")
        return render(request,"InonPayment/InonPaymentNew.html", context)
           

class InNonList(View,SqlDb):
    def __init__(self): 
        SqlDb.__init__(self)
       
    def get(self,request):
        Username = request.session['Username'] 

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        AccountId = self.cursor.fetchone()[0]

        nowdata = datetime.now()-timedelta(days=60)
        self.cursor.execute("SELECT   t1.Id as 'ID', t1.JobId as 'JOB ID', t1.MSGId as 'MSG ID', CONVERT(varchar, t1.TouchTime, 105) AS 'DEC DATE',SUBSTRING(t1.DeclarationType , 1, CHARINDEX(':', t1.DeclarationType) - 1) AS 'DEC TYPE',t1.TouchUser AS 'CREATE', t2.TradeNetMailboxID AS 'DEC ID', CONVERT(varchar, t1.ArrivalDate, 105) AS ETA, t1.PermitNumber AS 'PERMIT NO', t3.Name +' '+t3.Name1 AS 'IMPORTER',  t1.Inhabl as 'HAWB', CASE  WHEN  t1.InwardTransportMode = '4 : Air' THEN t1.MasterAirwayBill  WHEN t1.InwardTransportMode = '1 : Sea' THEN t1.OceanBillofLadingNo   ELSE '' END AS 'MAWB/OBL',t1.LoadingPortCode as POL, t1.MessageType as 'MSG TYPE', t1.InwardTransportMode as TPT, t1.PreviousPermit as 'PRE PMT',t1.GrossReference as 'X REF', t1.InternalRemarks as 'INT REM',  SUM(t1.TotalGSTTaxAmt) AS 'GST AMT', t1.Status as 'STATUS',case  when  t1.Status='APR' then (case when (select top 1 ConditionCode from InnonPMT where ConditionCode='Z02' and t1.PermitNumber=InnonPMT.PermitNumber)='Z02' or (select top 1 ConditionCode from InnonPMT where ConditionCode='Z18' and t1.PermitNumber=InnonPMT.PermitNumber)='Z18' or (select top 1 ConditionCode from InnonPMT where ConditionCode='Z06' and t1.PermitNumber=InnonPMT.PermitNumber)='Z06' then 'RED' when (select top 1 ConditionCode from InnonPMT where ConditionCode='D6' and t1.PermitNumber=InnonPMT.PermitNumber)='D6' or (select top 1 ConditionCode from InnonPMT where ConditionCode='D3' and t1.PermitNumber=InnonPMT.PermitNumber)='D3' then 'Maroon' else 'Default'  end)  else 'default' end as 'COLOR'  FROM  InNonHeaderTbl AS t1 left JOIN   DeclarantCompany AS t2 ON t1.DeclarantCompanyCode = t2.Code left JOIN InNonImporter AS t3 ON t1.ImporterCompanyCode = t3.Code  left JOIN ManageUser AS t6 ON t6.UserId=t1.TouchUser  where   t6.AccountId='" + AccountId + "' and convert(varchar,t1.TouchTime,111)>='"+ nowdata.strftime("%Y/%m/%d")+ "'  GROUP BY t1.Id, t1.JobId, t1.MSGId, t1.TouchTime, t1.TouchUser,t1.DeclarationType,t1.ArrivalDate, t1.PermitId,	t1.PermitNumber, t1.InwardTransportMode,t1.OutwardTransportMode,t1.MasterAirwayBill,t1.OceanBillofLadingNo, t1.LoadingPortCode, t1.MessageType, t1.InwardTransportMode,t1.PreviousPermit,t1.Inhabl, t1.InternalRemarks, t1.Status, t2.TradeNetMailboxID, 	t3.Name,t3.Name1, t6.AccountId,t1.OutMasterAirwayBill, t1.OutOceanBillofLadingNo,t1.outhbl,t1.OutwardTransportMode,t2.DeclarantName,t1.DepartureDate , t1.DischargePort, t1.GrossReference ,t1.License ,t1.ReleaseLocation ,t1.RecepitLocation ,t1.DeclarningFor,t1.ExporterCompanyCode ORDER BY ID DESC")
    
        self.HeaderInNon = self.cursor.fetchall()#t1.Status != 'DEL'

        result = (pd.DataFrame(list(self.HeaderInNon), columns=["id","JobId","MSGId","DECDATE","DECTYPE","CREATE","DECID","ETA","PERMITNO","IMPORTER","HAWB","MAWBOBL","POL","MSGTYPE","TPT","PREPMT","XREF","INTREM","GSTAMT","STATUS","PermitId"])).to_dict('records')

        return JsonResponse(result, safe=False)

class InNonViewSet(viewsets.ModelViewSet):
    serializer_class = InNonSeralizer
    queryset = InNonImporter.objects.filter(Status = "Active")
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ["Code","Name"]
    search_fields = ["Code","Name"]
    ordering_fields = "__all__"
    ordering = ['Name']

def ImporterInon(request):
    data = request.GET.get("Name")
    data_list = []
    if data:
        val = InNonImporter.objects.filter(Code__icontains = data,Name__icontains = data,Status = "Active")[:10]
        data_list = [[item.Code,item.CRUEI,item.Name,item.Name1] for item in val]

    return JsonResponse({"status":200,"data":data_list})

class PartyLoad(View,SqlDb): 
    def __init__(self):
        SqlDb.__init__(self)

        self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM InNonImporter WHERE status = 'Active' ORDER BY Name ")
        self.importer = self.cursor.fetchall()

        self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM InnonExporter WHERE status = 'Active' ORDER BY Name")
        self.exporter = self.cursor.fetchall()

        self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM InnonInwardCarrierAgent WHERE status = 'Active' ORDER BY Name")
        self.inward = self.cursor.fetchall()

        self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM InnonOutwardCarrierAgent WHERE status = 'Active' ORDER BY Name") 
        self.outward = self.cursor.fetchall()

        self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM FreightForwarder WHERE status = 'Active' ORDER BY Name")
        self.fright = self.cursor.fetchall()

        self.cursor.execute("SELECT ConsigneeCode,ConsigneeName,ConsigneeName1,ConsigneeCRUEI,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSub,ConsigneeSubDivi,ConsigneePostal,ConsigneeCountry FROM InnonConsignee ORDER BY ConsigneeName")
        self.consign = self.cursor.fetchall() 

        self.cursor.execute("SELECT Name,Name1,Name2,CRUEI,ClaimantName,ClaimantName1 FROM InnonClaimantParty WHERE status = 'Active' ORDER BY Name")
        self.claimant = self.cursor.fetchall() 

    def get(self,request):
        try:
            self.cursor.execute("SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime FROM InNonInvoiceDtl WHERE PermitId = '{}' ORDER BY SNO ".format(request.GET.get("PermitId")))
            self.invoice  = self.cursor.fetchall()

            self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))
            self.item  = self.cursor.fetchall()

            self.cursor.execute("SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,CASCId FROM INNONCASCDtl  WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))
            self.casc = self.cursor.fetchall()

            self.cursor.execute("SELECT Id,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3 FROM InNonCPCDtl  WHERE PermitId = '{}'".format(request.GET.get('PermitId')))
            self.cpc = self.cursor.fetchall()
            
            return JsonResponse(
                {
                    "Importer" : (pd.DataFrame(list(self.importer), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                    "Exporter" : (pd.DataFrame(list(self.exporter), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                    "Inward" : (pd.DataFrame(list(self.inward), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                    "Outward" : (pd.DataFrame(list(self.outward), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                    "fright" : (pd.DataFrame(list(self.fright), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                    "Cpc" : (pd.DataFrame(list(self.cpc), columns=["Id","RowNo", "CPCType", "ProcessingCode1","ProcessingCode2","ProcessingCode3"])).to_dict('records'),
                    "consign" : (pd.DataFrame(list(self.consign), columns=["ConsigneeCode", "ConsigneeName", "ConsigneeName1","ConsigneeCRUEI","ConsigneeAddress", "ConsigneeAddress1", "ConsigneeCity","ConsigneeSub","ConsigneeSubDivi","ConsigneePostal","ConsigneeCountry"])).to_dict('records'),
                    "Claimant" : (pd.DataFrame(list(self.claimant), columns=["Name","Name1","Name2","CRUEI","ClaimantName","ClaimantName1"])).to_dict('records'),
                    "invoice" : (pd.DataFrame(list(self.invoice), columns=['SNo' , 'InvoiceNo' , 'InvoiceDate' , 'TermType' , 'AdValoremIndicator' , 'PreDutyRateIndicator' , 'SupplierImporterRelationship' , 'SupplierCode' , 'ImportPartyCode' , 'TICurrency' , 'TIExRate' , 'TIAmount' , 'TISAmount' , 'OTCCharge' , 'OTCCurrency' , 'OTCExRate' , 'OTCAmount' , 'OTCSAmount' , 'FCCharge' , 'FCCurrency' , 'FCExRate' , 'FCAmount' , 'FCSAmount' , 'ICCharge' , 'ICCurrency' , 'ICExRate' , 'ICAmount' , 'ICSAmount' , 'CIFSUMAmount' , 'GSTPercentage' , 'GSTSUMAmount' , 'MessageType' , 'PermitId' , 'TouchUser' , 'TouchTime'])).to_dict('records'),
                    "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records'),
                    "casc" : (pd.DataFrame(list(self.casc), columns=['ItemNo','ProductCode','Quantity','ProductUOM','RowNo','CascCode1','CascCode2','CascCode3','CASCId'])).to_dict('records'),
                }
            )
        except:
            return JsonResponse(
                {
                    "Error" : "SOMTHING ITS WRONG SO PLEASE PAGE REFRESH"
                }
            )

    def post(self,request):
        DbName = request.POST.get("MODEL")  
        if DbName == "IMPORTER":
            ImpQry = ("SELECT Code FROM InNonImporter where Code = %s ")
            self.cursor.execute(ImpQry,(request.POST.get("Code"),))
            val = self.cursor.fetchone()
            if val:
                return JsonResponse({"Result" : "THIS CODE IS ALREADY EXISTS ...!", "Importer" : (pd.DataFrame(list(self.importer), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records')})
            else:
                Qry = "INSERT INTO InNonImporter (Code,Name,Name1,CRUEI,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val = (request.POST.get("Code").upper(),request.POST.get("Name").upper(),request.POST.get("Name1").upper(),request.POST.get("CRUEI").upper(),request.POST.get("TouchUser"),request.POST.get("TouchTime"),'Active')
                self.cursor.execute(Qry,val)
                self.conn.commit()
                self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM InNonImporter WHERE status = 'Active' ORDER BY Name")
                self.importer = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                    "Importer" : (pd.DataFrame(list(self.importer), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                })
            
        elif DbName == "EXPORTER":
            ExpQry = "SELECT Code FROM InnonExporter where Code=%s"
            self.cursor.execute(ExpQry,(request.POST.get("Code"),))
            val = self.cursor.fetchone()
            if val:
                return JsonResponse({"Result" : "THIS CODE IS ALREADY EXISTS ...!", "Exporter" : (pd.DataFrame(list(self.exporter), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),})
            else:
                Qry = "INSERT INTO InnonExporter (Code,Name,Name1,CRUEI,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val = (request.POST.get("Code"),request.POST.get("Name"),request.POST.get("Name1"),request.POST.get("CRUEI"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),'Active')
                self.cursor.execute(Qry,val)
                self.conn.commit()
                self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM InnonExporter WHERE status = 'Active' ORDER BY Name" )
                self.exporter = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                    "Exporter" : (pd.DataFrame(list(self.exporter), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                })
            
        elif DbName == "INWARD":
            InWard = "SELECT Code FROM InnonInwardCarrierAgent where Code=%s"
            self.cursor.execute(InWard,(request.POST.get("Code"),))
            val = self.cursor.fetchone()
            if val:
                return JsonResponse({"Result" : "THIS CODE IS ALREADY EXISTS ...!", "Inward" : (pd.DataFrame(list(self.inward), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),})
            else:
                Qry = "INSERT INTO InnonInwardCarrierAgent (Code,Name,Name1,CRUEI,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val = (request.POST.get("Code"),request.POST.get("Name"),request.POST.get("Name1"),request.POST.get("CRUEI"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),'Active')
                self.cursor.execute(Qry,val)
                self.conn.commit()
                self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM InnonInwardCarrierAgent WHERE status = 'Active' ORDER BY Name")
                self.inward = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                    "Inward" : (pd.DataFrame(list(self.inward), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                })
            
        elif DbName == "OUTWARD":
            OutQry = "SELECT Code FROM InnonOutwardCarrierAgent where Code = %s"
            self.cursor.execute(OutQry,(request.POST.get("Code"),))
            val = self.cursor.fetchone()
            if val:
                return JsonResponse({"Result" : "THIS CODE IS ALREADY EXISTS ...!", "Outward" : (pd.DataFrame(list(self.outward), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),})
            else:
                Qry = "INSERT INTO InnonOutwardCarrierAgent (Code,Name,Name1,CRUEI,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val = (request.POST.get("Code"),request.POST.get("Name"),request.POST.get("Name1"),request.POST.get("CRUEI"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),'Active')
                self.cursor.execute(Qry,val)
                self.conn.commit()
                self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM InnonOutwardCarrierAgent WHERE status = 'Active' ORDER BY Name")
                self.outward = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                    "Outward" : (pd.DataFrame(list(self.outward), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                })
            
        elif DbName == "FRIGHT":
            FriQry = "SELECT Code FROM FreightForwarder where Code=%s"
            self.cursor.execute(FriQry,(request.POST.get("Code"),))
            val = self.cursor.fetchone()
            if val:
                return JsonResponse({"Result" : "THIS CODE IS ALREADY EXISTS ...!", "Outward" : (pd.DataFrame(list(self.fright), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),})
            else:
                Qry = "INSERT INTO FreightForwarder (Code,Name,Name1,CRUEI,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val = (request.POST.get("Code"),request.POST.get("Name"),request.POST.get("Name1"),request.POST.get("CRUEI"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),'Active')
                self.cursor.execute(Qry,val)
                self.conn.commit()
                self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM FreightForwarder WHERE status = 'Active' ORDER BY Name")
                self.fright = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                    "fright" : (pd.DataFrame(list(self.fright), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                })

        elif DbName == "CONSIGNE":
            ConQry = "SELECT ConsigneeCode FROM InnonConsignee where ConsigneeCode=%s"
            self.cursor.execute(ConQry,(request.POST.get("ConsigneeCode"),))
            val = self.cursor.fetchone()
            if val:
                return JsonResponse({"Result" : "THIS CODE IS ALREADY EXISTS ...!",  "consign" : (pd.DataFrame(list(self.consign), columns=["ConsigneeCode", "ConsigneeName", "ConsigneeName1","ConsigneeCRUEI","ConsigneeAddress", "ConsigneeAddress1", "ConsigneeCity","ConsigneeSub","ConsigneeSubDivi","ConsigneePostal","ConsigneeCountry"])).to_dict('records'),})
            else:
                Qry = ("INSERT INTO InnonConsignee (ConsigneeCode,ConsigneeName,ConsigneeName1,ConsigneeCRUEI,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSub,ConsigneeSubDivi,ConsigneePostal,ConsigneeCountry,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                val = (request.POST.get("ConsigneeCode"),request.POST.get("ConsigneeName"),request.POST.get("ConsigneeName1"),request.POST.get("ConsigneeCRUEI"),request.POST.get("ConsigneeAddress"),request.POST.get("ConsigneeAddress1"),request.POST.get("ConsigneeCity"),
                        request.POST.get("ConsigneeSub"),request.POST.get("ConsigneeSubDivi"),request.POST.get("ConsigneePostal"),request.POST.get("ConsigneeCountry"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),"Active")
                self.cursor.execute(Qry,val)
                self.conn.commit()
                self.cursor.execute("SELECT ConsigneeCode,ConsigneeName,ConsigneeName1,ConsigneeCRUEI,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSub,ConsigneeSubDivi,ConsigneePostal,ConsigneeCountry FROM InnonConsignee ORDER BY ConsigneeName")
                self.consign = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                     "consign" : (pd.DataFrame(list(self.consign), columns=["ConsigneeCode", "ConsigneeName", "ConsigneeName1","ConsigneeCRUEI","ConsigneeAddress", "ConsigneeAddress1", "ConsigneeCity","ConsigneeSub","ConsigneeSubDivi","ConsigneePostal","ConsigneeCountry"])).to_dict('records'),
                })
            
        elif DbName == "CLAIMANT":
            ClaiQry = "SELECT Name  FROM InnonClaimantParty Where  Name=%s"
            self.cursor.execute(ClaiQry,(request.POST.get("Name"),))
            val = self.cursor.fetchone()
            if val:
                return JsonResponse({"Result" : "THIS CODE IS ALREADY EXISTS ...!", "Claimant" : (pd.DataFrame(list(self.claimant), columns=["Name","Name1","Name2","CRUEI","ClaimantName","ClaimantName1"])).to_dict('records'),})
            else:
                Qry = "INSERT INTO InnonClaimantParty (Name,Name1,Name2,CRUEI,ClaimantName,ClaimantName1,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (request.POST.get("Name"),request.POST.get("Name1"),request.POST.get("Name2"),request.POST.get("CRUEI"),request.POST.get("ClaimantName"),request.POST.get("ClaimantName1"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),'Active')
                self.cursor.execute(Qry,val)
                self.conn.commit()
                self.cursor.execute("SELECT Name,Name1,Name2,CRUEI,ClaimantName,ClaimantName1 FROM InnonClaimantParty WHERE status = 'Active' ORDER BY Name")
                self.claimant = self.cursor.fetchall() 
                return JsonResponse({
                    "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                    "Claimant" : (pd.DataFrame(list(self.claimant), columns=["Name","Name1","Name2","CRUEI","ClaimantName","ClaimantName1"])).to_dict('records'),
                })
            
        


            
        



class ItemCodeSave(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def post(self,request):
        DbName = request.POST.get("ModelName")
        if DbName == "InNonhouseItemCodeModel":
            Qry = "select InhouseCode from InNonhouseItemCode where InhouseCode = %s"
            print("QryItemCode:",Qry)
            Val = (request.POST.get("InhouseCode"),)
            self.cursor.execute(Qry, Val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO InNonhouseItemCode(InhouseCode,HSCode,Description,Brand,Model,DGIndicator,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
                Val = (
                    request.POST.get("InhouseCode"),
                    request.POST.get("Hscode"),
                    request.POST.get("Description"),
                    request.POST.get("Brand"),
                    request.POST.get("Model"),
                    request.POST.get("DGIndicator"),
                    request.POST.get("TouchUser"),
                    request.POST.get("TouchTime"),
                )
                self.cursor.execute(Qry, Val)
                self.conn.commit()
                return JsonResponse({"Result": "InNonhouseItemCode Saved ...!"})
            else:
                return JsonResponse(
                    {"Result": "InNonhouseItemCode Code Already Exists ...!"}
                ) 
    
class InNonCargoLoad(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

        self.cursor.execute("SELECT Name FROM CommonMaster WHERE TypeId=10 AND StatusId=1 ORDER BY Name")
        self.outepack = self.cursor.fetchall()

        self.cursor.execute("SELECT code,locationCode , description FROM ReleaseLocation ORDER BY locationCode")
        self.relese = self.cursor.fetchall()

        self.cursor.execute("SELECT code,locationCode , description FROM ReceiptLocation ORDER BY locationCode")
        self.recipt = self.cursor.fetchall()

        self.cursor.execute("SELECT code,StorageCode,description FROM StorageLocation ORDER BY Code")
        self.storage = self.cursor.fetchall()

        self.cursor.execute("SELECT PortCode,PortName,Country FROM LoadingPort ORDER BY PortCode")
        self.loadingPort = self.cursor.fetchall()

        self.cursor.execute("SELECT Top 245 CountryCode,Description FROM COUNTRY ORDER BY CountryCode")
        self.country = self.cursor.fetchall()

        self.cursor.execute("SELECT Name FROM CommonMaster WHERE TypeId = 14 AND StatusID = 1 ORDER BY Name")
        self.vessel = self.cursor.fetchall()


    def get(self,request):
       
        return JsonResponse({ 
            "TotOuterPack" : (pd.DataFrame(list(self.outepack), columns=["Name"])).to_dict('records'),
            "releaseLoc" : (pd.DataFrame(list(self.relese), columns=["code","locationCode","description"])).to_dict('records'),
            "reciptLoc" : (pd.DataFrame(list(self.recipt), columns=["code","locationCode","description"])).to_dict('records'),
            "storageLoc" : (pd.DataFrame(list(self.storage), columns=["code","StorageCode","description"])).to_dict('records'),
            "loadingPort" : (pd.DataFrame(list(self.loadingPort), columns=["PortCode","PortName","Country"])).to_dict('records'),
            "country" : (pd.DataFrame(list(self.country), columns=["CountryCode","Description"])).to_dict('records'),
            "vessel" : (pd.DataFrame(list(self.vessel), columns=["Name"])).to_dict('records'),
            })
    
class InNonInvoiceLoad(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.cursor.execute("SELECT  Code,Name,Name1,CRUEI FROM INNONSUPPLIERMANUFACTURERPARTY where Status='ACTIVE' order by Id")
        self.supply = self.cursor.fetchall()

        self.cursor.execute("SELECT Name FROM CommonMaster WHERE TypeId = 7 AND StatusID = 1 ORDER BY Name")
        self.term = self.cursor.fetchall()

        self.cursor.execute("SELECT  Currency,CurrencyRate FROM Currency ORDER BY Currency")
        self.currency = self.cursor.fetchall()

        self.cursor.execute("SELECT Name FROM CommonMaster WHERE TypeId = 20 AND StatusID = 1 ORDER BY Name")
        self.vehical = self.cursor.fetchall()

        self.cursor.execute("SELECT Name FROM CommonMaster WHERE TypeId = 21 AND StatusID = 1 ORDER BY Name")
        self.engine = self.cursor.fetchall()

        self.cursor.execute("SELECT Name FROM CommonMaster WHERE TypeId = 11 AND StatusID = 1 ORDER BY Name")
        self.preferntial = self.cursor.fetchall()

        self.cursor.execute("SELECT Name FROM CommonMaster WHERE TypeId = 12 AND StatusID = 1 ORDER BY Name")
        self.making = self.cursor.fetchall()

    def get(self,request):
        return JsonResponse({
            "supply" : (pd.DataFrame(list(self.supply), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
            "termType" : (pd.DataFrame(list(self.term), columns=["Name"])).to_dict('records'),
            "vehical" : (pd.DataFrame(list(self.vehical), columns=["Name"])).to_dict('records'),
            "engine" : (pd.DataFrame(list(self.engine), columns=["Name"])).to_dict('records'),
            "making" : (pd.DataFrame(list(self.making), columns=["Name"])).to_dict('records'),
            "preferntial" : (pd.DataFrame(list(self.preferntial), columns=["Name"])).to_dict('records'),
            "currency" : (pd.DataFrame(list(self.currency), columns=["Currency", "CurrencyRate"])).to_dict('records'), 
                
        })
    
    def post(self,request):
        DbName = request.POST.get("MODEL") 
        if DbName == "SUPPLIER":
            self.cursor.execute("SELECT Code FROM INNONSUPPLIERMANUFACTURERPARTY where Code='" + request.POST.get("Code")+ "'")
            val = self.cursor.fetchone()
            if val:
                return JsonResponse({"Result" : "THIS CODE IS ALREADY EXISTS ...!", "supply" : (pd.DataFrame(list(self.supply), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records')})
            else:
                Qry = "INSERT INTO INNONSUPPLIERMANUFACTURERPARTY (Code,Name,Name1,CRUEI,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val = (request.POST.get("Code"),request.POST.get("Name"),request.POST.get("Name1"),request.POST.get("CRUEI"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),'Active')
                self.cursor.execute(Qry,val)
                self.conn.commit()
                self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM INNONSUPPLIERMANUFACTURERPARTY WHERE status = 'Active' ORDER BY Name")
                self.supply = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                    "supply" : (pd.DataFrame(list(self.supply), columns=["Code", "Name", "Name1","CRUEI"])).to_dict('records'),
                })
            
        elif DbName == "INVOICE":

            self.cursor.execute("SELECT PermitId,SNo FROM InNonInvoiceDtl WHERE PermitId = '{}' AND SNo = {}".format(request.POST.get("PermitId"),request.POST.get("SNo")))

            if self.cursor.fetchall():
        
                Qry = "UPDATE InNonInvoiceDtl SET InvoiceNo = %s,InvoiceDate = %s,TermType = %s,AdValoremIndicator = %s,PreDutyRateIndicator = %s,SupplierImporterRelationship = %s,SupplierCode = %s,ImportPartyCode = %s,TICurrency = %s,TIExRate = %s,TIAmount = %s,TISAmount = %s,OTCCharge = %s,OTCCurrency = %s,OTCExRate = %s,OTCAmount = %s,OTCSAmount = %s,FCCharge = %s,FCCurrency = %s,FCExRate = %s,FCAmount = %s,FCSAmount = %s,ICCharge = %s,ICCurrency = %s,ICExRate = %s,ICAmount = %s,ICSAmount = %s,CIFSUMAmount = %s,GSTPercentage = %s,GSTSUMAmount = %s,MessageType = %s,TouchUser = %s,TouchTime = %s WHERE PermitId = '{}' AND SNo = {}".format(request.POST.get("PermitId"),request.POST.get("SNo"))
                Val = (request.POST.get('InvoiceNo'), request.POST.get('InvoiceDate'), request.POST.get('TermType'), request.POST.get('AdValoremIndicator'), request.POST.get('PreDutyRateIndicator'), request.POST.get('SupplierImporterRelationship'), request.POST.get('SupplierCode'), request.POST.get('ImportPartyCode'), request.POST.get('TICurrency'), request.POST.get('TIExRate'), request.POST.get('TIAmount'), request.POST.get('TISAmount'), request.POST.get('OTCCharge'), request.POST.get('OTCCurrency'), request.POST.get('OTCExRate'), request.POST.get('OTCAmount'), request.POST.get('OTCSAmount'), request.POST.get('FCCharge'), request.POST.get('FCCurrency'), request.POST.get('FCExRate'), request.POST.get('FCAmount'), request.POST.get('FCSAmount'), request.POST.get('ICCharge'), request.POST.get('ICCurrency'), request.POST.get('ICExRate'), request.POST.get('ICAmount'), request.POST.get('ICSAmount'), request.POST.get('CIFSUMAmount'), request.POST.get('GSTPercentage'), request.POST.get('GSTSUMAmount'), request.POST.get('MessageType'), request.POST.get('TouchUser'), request.POST.get('TouchTime'))
                self.cursor.execute(Qry,Val)
                self.conn.commit()

                self.cursor.execute("SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime FROM InNonInvoiceDtl WHERE PermitId = '{}' ORDER BY SNo".format(request.POST.get("PermitId")))
                self.invoice  = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "INVOICE UPDATED SUCCESSFULLY ...!",
                    "invoice" : (pd.DataFrame(list(self.invoice), columns=['SNo' , 'InvoiceNo' , 'InvoiceDate' , 'TermType' , 'AdValoremIndicator' , 'PreDutyRateIndicator' , 'SupplierImporterRelationship' , 'SupplierCode' , 'ImportPartyCode' , 'TICurrency' , 'TIExRate' , 'TIAmount' , 'TISAmount' , 'OTCCharge' , 'OTCCurrency' , 'OTCExRate' , 'OTCAmount' , 'OTCSAmount' , 'FCCharge' , 'FCCurrency' , 'FCExRate' , 'FCAmount' , 'FCSAmount' , 'ICCharge' , 'ICCurrency' , 'ICExRate' , 'ICAmount' , 'ICSAmount' , 'CIFSUMAmount' , 'GSTPercentage' , 'GSTSUMAmount' , 'MessageType' , 'PermitId' , 'TouchUser' , 'TouchTime'])).to_dict('records'),
                })
            else:
                Qry = "INSERT INTO InNonInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) VALUES (%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s)"
                Val = (request.POST.get('SNo'), request.POST.get('InvoiceNo'), request.POST.get('InvoiceDate'), request.POST.get('TermType'), request.POST.get('AdValoremIndicator'), request.POST.get('PreDutyRateIndicator'), request.POST.get('SupplierImporterRelationship'), request.POST.get('SupplierCode'), request.POST.get('ImportPartyCode'), request.POST.get('TICurrency'), request.POST.get('TIExRate'), request.POST.get('TIAmount'), request.POST.get('TISAmount'), request.POST.get('OTCCharge'), request.POST.get('OTCCurrency'), request.POST.get('OTCExRate'), request.POST.get('OTCAmount'), request.POST.get('OTCSAmount'), request.POST.get('FCCharge'), request.POST.get('FCCurrency'), request.POST.get('FCExRate'), request.POST.get('FCAmount'), request.POST.get('FCSAmount'), request.POST.get('ICCharge'), request.POST.get('ICCurrency'), request.POST.get('ICExRate'), request.POST.get('ICAmount'), request.POST.get('ICSAmount'), request.POST.get('CIFSUMAmount'), request.POST.get('GSTPercentage'), request.POST.get('GSTSUMAmount'), request.POST.get('MessageType'), request.POST.get('PermitId'), request.POST.get('TouchUser'), request.POST.get('TouchTime'))
                self.cursor.execute(Qry,Val)
                self.conn.commit()

                self.cursor.execute("SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime FROM InNonInvoiceDtl WHERE PermitId = '{}' ORDER BY SNo".format(request.POST.get("PermitId")))
                self.invoice  = self.cursor.fetchall()
                return JsonResponse({
                    "Result" : "INVOICE SAVED SUCCESSFULLY ...!",
                    "invoice" : (pd.DataFrame(list(self.invoice), columns=['SNo' , 'InvoiceNo' , 'InvoiceDate' , 'TermType' , 'AdValoremIndicator' , 'PreDutyRateIndicator' , 'SupplierImporterRelationship' , 'SupplierCode' , 'ImportPartyCode' , 'TICurrency' , 'TIExRate' , 'TIAmount' , 'TISAmount' , 'OTCCharge' , 'OTCCurrency' , 'OTCExRate' , 'OTCAmount' , 'OTCSAmount' , 'FCCharge' , 'FCCurrency' , 'FCExRate' , 'FCAmount' , 'FCSAmount' , 'ICCharge' , 'ICCurrency' , 'ICExRate' , 'ICAmount' , 'ICSAmount' , 'CIFSUMAmount' , 'GSTPercentage' , 'GSTSUMAmount' , 'MessageType' , 'PermitId' , 'TouchUser' , 'TouchTime'])).to_dict('records'),
                })
        elif DbName == "DELETE":
            self.cursor.execute("DELETE FROM InNonInvoiceDtl WHERE PermitId = '{}' AND SNo = {}".format(request.POST.get("PermitId"),request.POST.get("SNo")))
            self.conn.commit()

            self.cursor.execute("SELECT SNo ,PermitId FROM InNonInvoiceDtl WHERE PermitId = '{}' ORDER BY SNo".format(request.POST.get("PermitId")))
            for ind in range(1,len(self.cursor.fetchall())+1):
                self.cursor.execute("UPDATE InNonInvoiceDtl SET SNo = '{}' WHERE PermitId = '{}' ".format(ind,request.POST.get("PermitId")))
            self.conn.commit()

            self.cursor.execute("SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime FROM InNonInvoiceDtl WHERE PermitId = '{}' ORDER BY SNo".format(request.POST.get("PermitId")))
            self.invoice  = self.cursor.fetchall()
            return JsonResponse({
                "Result" : "INVOICE SAVED SUCCESSFULLY ...!",
                "invoice" : (pd.DataFrame(list(self.invoice), columns=['SNo' , 'InvoiceNo' , 'InvoiceDate' , 'TermType' , 'AdValoremIndicator' , 'PreDutyRateIndicator' , 'SupplierImporterRelationship' , 'SupplierCode' , 'ImportPartyCode' , 'TICurrency' , 'TIExRate' , 'TIAmount' , 'TISAmount' , 'OTCCharge' , 'OTCCurrency' , 'OTCExRate' , 'OTCAmount' , 'OTCSAmount' , 'FCCharge' , 'FCCurrency' , 'FCExRate' , 'FCAmount' , 'FCSAmount' , 'ICCharge' , 'ICCurrency' , 'ICExRate' , 'ICAmount' , 'ICSAmount' , 'CIFSUMAmount' , 'GSTPercentage' , 'GSTSUMAmount' , 'MessageType' , 'PermitId' , 'TouchUser' , 'TouchTime'])).to_dict('records'),
            })

class InNonItemLoad(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

        self.cursor.execute("SELECT InhouseCode,HSCode,Description,Brand,Model,DGIndicator FROM InNonhouseItemCode ")
        self.inhouseItemCode = self.cursor.fetchall()

        self.cursor.execute("SELECT HSCode,Description,UOM,Typeid,DUTYTYPID,Inpayment,InnonPayment,Out,Co,Transhipment,RPNEXPORT,DuitableUom,Excisedutyuom,Excisedutyrate,Customsdutyuom,Customsdutyrate,Kgmvisible FROM HSCode")#ImpControll,OutControll,TransControll <---This Field Add Only Kaizen Portal 
        self.hsCode = self.cursor.fetchall()

        self.cursor.execute("SELECT HSCode FROM ChkHsCode ")
        self.chkHsCode = self.cursor.fetchall()

    def get(self,request):
        return JsonResponse({
            "inhouseItemCode" : (pd.DataFrame(list(self.inhouseItemCode), columns=["InhouseCode", "HSCode", "Description","Brand","Model", "DGIndicator"])).to_dict('records'),
            "hsCode" : (pd.DataFrame(list(self.hsCode), columns=['HSCode','Description','UOM','Typeid','DUTYTYPID','Inpayment','InnonPayment','Out','Co','Transhipment','RPNEXPORT','DuitableUom','Excisedutyuom','Excisedutyrate','Customsdutyuom','Customsdutyrate','Kgmvisible'])).to_dict('records'),#,'ImpControll ,'OutControll','TransControll'<---This Field Add Only Kaizen Portal  '
            "chkHsCode" : (pd.DataFrame(list(self.chkHsCode), columns=["HSCode"])).to_dict('records'),
        })
    
    def post(self,request):

        CascValue = json.loads(request.POST.get('CascDatas'))

        self.cursor.execute("DELETE FROM INNONCASCDtl WHERE PermitId = '{}' AND ItemNo = '{}' " .format(request.POST.get('PermitId'),request.POST.get('ItemNo')))
        self.conn.commit()

        QryCasc = "INSERT INTO INNONCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for i in CascValue:
            ValCasc = (i['ItemNo'],i['ProductCode'],i['Quantity'],i['ProductUOM'],i['RowNo'],i['CascCode1'],i['CascCode2'],i['CascCode3'],i['PermitId'],i['MessageType'],i['TouchUser'],i['TouchTime'],i['CASCId'])
            self.cursor.execute(QryCasc,ValCasc)

        self.cursor.execute("SELECT PermitId,ItemNo FROM InNonItemDtl WHERE PermitId = '{}' AND ItemNo = '{}' " .format(request.POST.get('PermitId'),request.POST.get('ItemNo')))
        if self.cursor.fetchall():
            Result = "ITEM SUCCESSFULLY UPDATED...!"
            Qry = "UPDATE InNonItemDtl SET MessageType = %s,HSCode = %s,Description = %s,DGIndicator = %s,Contry = %s,Brand = %s,Model = %s,Vehicletype = %s,Enginecapacity = %s,Engineuom = %s,Orginregdate = %s,InHAWBOBL = %s,OutHAWBOBL = %s,DutiableQty = %s,DutiableUOM = %s,TotalDutiableQty = %s,TotalDutiableUOM = %s,InvoiceQuantity = %s,HSQty = %s,HSUOM = %s,AlcoholPer = %s,InvoiceNo = %s,ChkUnitPrice = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,InvoiceCharges = %s,CIFFOB = %s,OPQty = %s,OPUOM = %s,IPQty = %s,IPUOM = %s,InPqty = %s,InPUOM = %s,ImPQty = %s,ImPUOM = %s,PreferentialCode = %s,GSTRate = %s,GSTUOM = %s,GSTAmount = %s,ExciseDutyRate = %s,ExciseDutyUOM = %s,ExciseDutyAmount = %s,CustomsDutyRate = %s,CustomsDutyUOM = %s,CustomsDutyAmount = %s,OtherTaxRate = %s,OtherTaxUOM = %s,OtherTaxAmount = %s,CurrentLot = %s,PreviousLot = %s,LSPValue = %s,Making = %s,ShippingMarks1 = %s,ShippingMarks2 = %s,ShippingMarks3 = %s,ShippingMarks4 = %s,TouchUser = %s,TouchTime = %s,OptionalChrgeUOM = %s,Optioncahrge = %s,OptionalSumtotal = %s,OptionalSumExchage = %s WHERE PermitId = %s AND ItemNo = %s"
            Val = (request.POST.get('MessageType'),request.POST.get('HSCode'),request.POST.get('Description'),request.POST.get('DGIndicator'),request.POST.get('Contry'),request.POST.get('Brand'),request.POST.get('Model'),request.POST.get('Vehicletype'),request.POST.get('Enginecapacity'),request.POST.get('Engineuom'),request.POST.get('Orginregdate'),request.POST.get('InHAWBOBL'),request.POST.get('OutHAWBOBL'),request.POST.get('DutiableQty'),request.POST.get('DutiableUOM'),request.POST.get('TotalDutiableQty'),request.POST.get('TotalDutiableUOM'),request.POST.get('InvoiceQuantity'),request.POST.get('HSQty'),request.POST.get('HSUOM'),request.POST.get('AlcoholPer'),request.POST.get('InvoiceNo'),request.POST.get('ChkUnitPrice'),request.POST.get('UnitPrice'),request.POST.get('UnitPriceCurrency'),request.POST.get('ExchangeRate'),request.POST.get('SumExchangeRate'),request.POST.get('TotalLineAmount'),request.POST.get('InvoiceCharges'),request.POST.get('CIFFOB'),request.POST.get('OPQty'),request.POST.get('OPUOM'),request.POST.get('IPQty'),request.POST.get('IPUOM'),request.POST.get('InPqty'),request.POST.get('InPUOM'),request.POST.get('ImPQty'),request.POST.get('ImPUOM'),request.POST.get('PreferentialCode'),request.POST.get('GSTRate'),request.POST.get('GSTUOM'),request.POST.get('GSTAmount'),request.POST.get('ExciseDutyRate'),request.POST.get('ExciseDutyUOM'),request.POST.get('ExciseDutyAmount'),request.POST.get('CustomsDutyRate'),request.POST.get('CustomsDutyUOM'),request.POST.get('CustomsDutyAmount'),request.POST.get('OtherTaxRate'),request.POST.get('OtherTaxUOM'),request.POST.get('OtherTaxAmount'),request.POST.get('CurrentLot'),request.POST.get('PreviousLot'),request.POST.get('LSPValue'),request.POST.get('Making'),request.POST.get('ShippingMarks1'),request.POST.get('ShippingMarks2'),request.POST.get('ShippingMarks3'),request.POST.get('ShippingMarks4'),request.POST.get('TouchUser'),request.POST.get('TouchTime'),request.POST.get('OptionalChrgeUOM'),request.POST.get('Optioncahrge'),request.POST.get('OptionalSumtotal'),request.POST.get('OptionalSumExchage'),request.POST.get('PermitId'),request.POST.get('ItemNo'))
            self.cursor.execute(Qry,Val)
        else:
            Qry = "INSERT INTO InNonItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            Val = (request.POST.get('ItemNo'),request.POST.get('PermitId'),request.POST.get('MessageType'),request.POST.get('HSCode'),request.POST.get('Description').upper(),request.POST.get('DGIndicator'),request.POST.get('Contry'),request.POST.get('Brand'),request.POST.get('Model'),request.POST.get('Vehicletype'),request.POST.get('Enginecapacity'),request.POST.get('Engineuom'),request.POST.get('Orginregdate'),request.POST.get('InHAWBOBL'),request.POST.get('OutHAWBOBL'),request.POST.get('DutiableQty'),request.POST.get('DutiableUOM'),request.POST.get('TotalDutiableQty'),request.POST.get('TotalDutiableUOM'),request.POST.get('InvoiceQuantity'),request.POST.get('HSQty'),request.POST.get('HSUOM'),request.POST.get('AlcoholPer'),request.POST.get('InvoiceNo'),request.POST.get('ChkUnitPrice'),request.POST.get('UnitPrice'),request.POST.get('UnitPriceCurrency'),request.POST.get('ExchangeRate'),request.POST.get('SumExchangeRate'),request.POST.get('TotalLineAmount'),request.POST.get('InvoiceCharges'),request.POST.get('CIFFOB'),request.POST.get('OPQty'),request.POST.get('OPUOM'),request.POST.get('IPQty'),request.POST.get('IPUOM'),request.POST.get('InPqty'),request.POST.get('InPUOM'),request.POST.get('ImPQty'),request.POST.get('ImPUOM'),request.POST.get('PreferentialCode'),request.POST.get('GSTRate'),request.POST.get('GSTUOM'),request.POST.get('GSTAmount'),request.POST.get('ExciseDutyRate'),request.POST.get('ExciseDutyUOM'),request.POST.get('ExciseDutyAmount'),request.POST.get('CustomsDutyRate'),request.POST.get('CustomsDutyUOM'),request.POST.get('CustomsDutyAmount'),request.POST.get('OtherTaxRate'),request.POST.get('OtherTaxUOM'),request.POST.get('OtherTaxAmount'),request.POST.get('CurrentLot'),request.POST.get('PreviousLot'),request.POST.get('LSPValue'),request.POST.get('Making'),request.POST.get('ShippingMarks1'),request.POST.get('ShippingMarks2'),request.POST.get('ShippingMarks3'),request.POST.get('ShippingMarks4'),request.POST.get('TouchUser'),request.POST.get('TouchTime'),request.POST.get('OptionalChrgeUOM'),request.POST.get('Optioncahrge'),request.POST.get('OptionalSumtotal'),request.POST.get('OptionalSumExchage'))

            self.cursor.execute(Qry,Val)
            Result = "ITEM SUCCESSFULLY ADDED...!"
        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.POST.get('PermitId')))
        self.item = self.cursor.fetchall()

        self.cursor.execute("SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,CASCId FROM INNONCASCDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.POST.get('PermitId')))
        self.casc = self.cursor.fetchall()

        return JsonResponse({
            "Result":Result,
            "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records'),
            "casc" : (pd.DataFrame(list(self.casc), columns=['ItemNo','ProductCode','Quantity','ProductUOM','RowNo','CascCode1','CascCode2','CascCode3','CASCId'])).to_dict('records'),
        })

class ItemInNonExcelUpload(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def post(self,request):
        
        xlsx_file = request.FILES['file']
        PermitId = request.POST.get('PermitId')
        MsgType = request.POST.get('MsgType')
        userName = request.POST.get('UserName')
        TouchTime = request.POST.get('TouchTime')

        ItemInfo = pd.read_excel(xlsx_file, sheet_name="ItemInfo")
        CascInfo = pd.read_excel(xlsx_file, sheet_name="Casccodes")
        ContainerInfo = pd.read_excel(xlsx_file, sheet_name="ContainerInfo")

        ItemData = []
        CascData = []
        ContainerData = []

        ItemColumns = {
            'CountryofOrigin': '',
            'HSCode': '',
            'HSQty': '0.00',
            'TotalLineAmount': '0.00',
            'ItemCode': '',
            'Description': '',
            'DGIndicator': 'False',
            'Brand': '',
            'Model': '',
            'InHAWBOBL': '',
            'OutHAWBOBL': '',
            'HSUOM': '--Select--',
            'InvoiceNumber': '',
            'ItemCurrency': '--Select--',
            'UnitPrice': '0.00',
            'TotalDutiableQty': '0.00',
            'TotalDutiableUOM': '--Select--',
            'DutiableQty': '0.00',
            'DutiableUOM': '--Select--',
            'OuterPackQty': '0.00',
            'OuterPackUOM': '--Select--',
            'InPackQty': '0.00',
            'InPackUOM': '--Select--',
            'InnerPackQty': '0.00',
            'InnerPackUOM': '--Select--',
            'InmostPackQty': '0.00',
            'InmostPackUOM': '--Select--',
            'LastSellingPrice': '0.00',
            'TarrifPreferentialCode': '--Select--',
            'OtherTaxRate': '0.00',
            'OtherTaxUOM': '--Select--',
            'OtherTaxAmount': '0.00',
            'CurrentLot': '',
            'PreviousLot': '',
            'AlcoholPercentage': '0.00',
            'ShippingMarks1': '',
            'ShippingMarks2': '',
            'ShippingMarks3': '',
            'ShippingMarks4': '',
        }

        CascColumn = {
            'ItemNo': '',
            'ProductCode': '',
            'Quantity': '0.00',
            'ProductUOM': '--Select--',
            'RowNo': '',
            'CascCode1': '',
            'CascCode2': '',
            'CascCode3': '',
            'CASCId': '',
        }

        ContainerColumn = {
            'SNo': '',
            'ContainerNo': '',
            'SizeType': '',
            'Weight': '',
            'SealNo': '',
        }

        ItemInfo.fillna(ItemColumns, inplace=True)
        CascInfo.fillna(CascColumn, inplace=True)
        ContainerInfo.fillna(ContainerColumn, inplace=True)

        self.cursor.execute(f"SELECT PermitId FROM InNonItemDtl WHERE PermitId = '{PermitId}'")
        itemLen = len(self.cursor.fetchall())

        QryItem = "INSERT INTO InNonItemDtl (Contry,HSCode,HSQty,TotalLineAmount,Description,DGIndicator,Brand,Model,InHAWBOBL,OutHAWBOBL,HSUOM,InvoiceNo,UnitPriceCurrency,UnitPrice,TotalDutiableQty,TotalDutiableUOM,DutiableQty,DutiableUOM,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,LSPValue,PreferentialCode,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,AlcoholPer,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,ItemNo,PermitId,MessageType,TouchUser,TouchTime,InvoiceQuantity,ChkUnitPrice,ExchangeRate,SumExchangeRate,InvoiceCharges,CIFFOB,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,Making,VehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        for index, row in ItemInfo.iterrows():
            itemLen += 1
            Val = (row['CountryofOrigin'],row['HSCode'],row['HSQty'],row['TotalLineAmount'],row['Description'],row['DGIndicator'],row['Brand'],row['Model'],row['InHAWBOBL'],row['OutHAWBOBL'],row['HSUOM'],row['InvoiceNumber'],row['ItemCurrency'],row['UnitPrice'],row['TotalDutiableQty'],row['TotalDutiableUOM'],row['DutiableQty'],row['DutiableUOM'],row['OuterPackQty'],row['OuterPackUOM'],row['InPackQty'],row['InPackUOM'],row['InnerPackQty'],row['InnerPackUOM'],row['InmostPackQty'],row['InmostPackUOM'],row['LastSellingPrice'],row['TarrifPreferentialCode'],row['OtherTaxRate'],row['OtherTaxUOM'],row['OtherTaxAmount'],row['CurrentLot'],row['PreviousLot'],row['AlcoholPercentage'],row['ShippingMarks1'],row['ShippingMarks2'],row['ShippingMarks3'],row['ShippingMarks4'],itemLen,PermitId,MsgType,userName,TouchTime,"0.00",'0.00','0.00','0.00','0.00','0.00','0.00','PER','0.00','0.00','','0.00','0.00','','0.00','--Select--','--Select--',"--Select--",'--Select--','','--Select--','0.00','0.00','0.00')
            self.cursor.execute(QryItem,Val)
        #self.conn.commit()   

        QryCasc = "INSERT INTO INNONCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
       
        for index, row in CascInfo.iterrows():
            if row['ProductCode'] != "":
                ValCasc = (row['ItemNo'],row['ProductCode'],row['Quantity'],row['ProductUOM'],row['RowNo'],row['CascCode1'],row['CascCode2'],row['CascCode3'],PermitId,MsgType,userName,TouchTime,row['CASCId'])
                self.cursor.execute(QryCasc,ValCasc) 
        self.conn.commit()   

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.POST.get('PermitId')))
        self.item = self.cursor.fetchall()

        self.cursor.execute("SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,CASCId FROM INNONCASCDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.POST.get('PermitId')))
        self.casc = self.cursor.fetchall()

        return JsonResponse({
            "Result":"UPLOAD SUCCESSFULLY...!",
            "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records'),
            "casc" : (pd.DataFrame(list(self.casc), columns=['ItemNo','ProductCode','Quantity','ProductUOM','RowNo','CascCode1','CascCode2','CascCode3','CASCId'])).to_dict('records'),
        })
    
def InNonExcelDownload(request):
    response = HttpResponse(open('/Users/hightech/Desktop/Yosuva_KttProject/kttOut/KttProject/InNonPaymentExcel.xlsx', 'rb').read())
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = f'attachment; filename=InPaymentExcel.xlsx'
    return response

class AllItemUpdateInNon(View,SqlDb): 
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):

        ItemValue = json.loads(request.GET.get('ItemNo'))

        values_str = ', '.join(map(str, ItemValue))

        query1 = f"DELETE FROM InNonItemDtl WHERE ItemNo IN ({values_str}) AND PermitId = '{request.GET.get('PermitId')}' "
        self.cursor.execute(query1)

        query2 = f"DELETE FROM INNONCASCDtl WHERE ItemNo IN ({values_str}) AND PermitId = '{request.GET.get('PermitId')}' "
        self.cursor.execute(query2)

        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId FROM InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))

        Ic = 1 
        for itm in self.cursor.fetchall():
            self.cursor.execute("UPDATE InNonItemDtl SET ItemNo = '{}' WHERE PermitId = '{}' AND  ItemNo = '{}' ".format(Ic,request.GET.get('PermitId'),itm[0]))
            self.cursor.execute("UPDATE INNONCASCDtl SET ItemNo = '{}' WHERE PermitId = '{}' AND  ItemNo = '{}' ".format(Ic,request.GET.get('PermitId'),itm[0]))
            Ic += 1
 
        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))
        self.item = self.cursor.fetchall()

        self.cursor.execute("SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,CASCId FROM INNONCASCDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))
        self.casc = self.cursor.fetchall()

        return JsonResponse({
            "Result":"UPLOAD SUCCESSFULLY...!",
            "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records'),
            "casc" : (pd.DataFrame(list(self.casc), columns=['ItemNo','ProductCode','Quantity','ProductUOM','RowNo','CascCode1','CascCode2','CascCode3','CASCId'])).to_dict('records'),
        }) 

    def post(self,request):

        PermitId = request.POST.get('PermitId')

        Qry = "UPDATE InNonItemDtl SET MessageType = %s,HSCode = %s,Description = %s,DGIndicator = %s,Contry = %s,Brand = %s,Model = %s,Vehicletype = %s,Enginecapacity = %s,Engineuom = %s,Orginregdate = %s,InHAWBOBL = %s,OutHAWBOBL = %s,DutiableQty = %s,DutiableUOM = %s,TotalDutiableQty = %s,TotalDutiableUOM = %s,InvoiceQuantity = %s,HSQty = %s,HSUOM = %s,AlcoholPer = %s,InvoiceNo = %s,ChkUnitPrice = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,InvoiceCharges = %s,CIFFOB = %s,OPQty = %s,OPUOM = %s,IPQty = %s,IPUOM = %s,InPqty = %s,InPUOM = %s,ImPQty = %s,ImPUOM = %s,PreferentialCode = %s,GSTRate = %s,GSTUOM = %s,GSTAmount = %s,ExciseDutyRate = %s,ExciseDutyUOM = %s,ExciseDutyAmount = %s,CustomsDutyRate = %s,CustomsDutyUOM = %s,CustomsDutyAmount = %s,OtherTaxRate = %s,OtherTaxUOM = %s,OtherTaxAmount = %s,CurrentLot = %s,PreviousLot = %s,LSPValue = %s,Making = %s,ShippingMarks1 = %s,ShippingMarks2 = %s,ShippingMarks3 = %s,ShippingMarks4 = %s,TouchUser = %s,TouchTime = %s,OptionalChrgeUOM = %s,Optioncahrge = %s,OptionalSumtotal = %s,OptionalSumExchage = %s WHERE PermitId = %s AND ItemNo = %s"
        ItemValue = json.loads(request.POST.get('Item'))
        for Itm in ItemValue:
            itmNo = Itm.pop('ItemNo')
            Permit = Itm.pop('PermitId')
            Itm.update({'PermitId':Permit,"ItemNo":itmNo})

            try:self.cursor.execute(Qry,tuple(Itm.values()))
            except Exception as e:pass

        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitId))
        self.item = self.cursor.fetchall()

        self.cursor.execute(f"SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,CASCId FROM INNONCASCDtl WHERE PermitId = '{PermitId}' ORDER BY ItemNo")
        self.casc = self.cursor.fetchall()

        return JsonResponse({
            "Result":"UPLOAD SUCCESSFULLY...!",
            "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records'),
            "casc" : (pd.DataFrame(list(self.casc), columns=['ItemNo','ProductCode','Quantity','ProductUOM','RowNo','CascCode1','CascCode2','CascCode3','CASCId'])).to_dict('records'),
        })
    
class ConsolidateInNon(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def post(self,request):

        PermitId = request.POST.get('PermitId')
    
        self.cursor.execute("select Distinct HSCode,Contry,UnitPriceCurrency from InNonItemDtl where PermitId='" + PermitId + "' group by HSCode,Contry,UnitPriceCurrency")
        ItemDistinct = self.cursor.fetchall()

        DelItems = []
        for Dist in ItemDistinct:
            self.cursor.execute(f"SELECT Min(ItemNo),SUM(DutiableQty),SUM(TotalDutiableQty),SUM(InvoiceQuantity),SUM(HSQty),SUM(AlcoholPer),SUM(UnitPrice),SUM(SumExchangeRate),SUM(TotalLineAmount),SUM(InvoiceCharges),SUM(CIFFOB),SUM(OPQty),SUM(IPQty),SUM(InPqty),SUM(ImPQty),SUM(GSTAmount),SUM(ExciseDutyAmount),SUM(CustomsDutyAmount),SUM(OtherTaxAmount),SUM(OptionalSumtotal) FROM InNonItemDtl WHERE PermitId = '{PermitId}' AND  HSCode = '{Dist[0]} ' AND  Contry = '{Dist[1]}' AND UnitPriceCurrency = '{Dist[2]}'")
            SumData = (pd.DataFrame(list(self.cursor.fetchall()), columns=['ItemNo','DutiableQty','TotalDutiableQty','InvoiceQuantity','HSQty','AlcoholPer','UnitPrice','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','IPQty','InPqty','ImPQty','GSTAmount','ExciseDutyAmount','CustomsDutyAmount','OtherTaxAmount','OptionalSumtotal'])).to_dict('records')

            for SumItem in SumData:
                self.cursor.execute(f"UPDATE InNonItemDtl SET DutiableQty = '{SumItem['DutiableQty']}',TotalDutiableQty = '{SumItem['TotalDutiableQty']}' ,InvoiceQuantity = '{SumItem['InvoiceQuantity']}' ,HSQty = '{SumItem['HSQty']}' ,AlcoholPer = '{SumItem['AlcoholPer']}' ,UnitPrice = '{SumItem['UnitPrice']}' ,SumExchangeRate = '{SumItem['SumExchangeRate']}' ,TotalLineAmount = '{SumItem['TotalLineAmount']}' ,InvoiceCharges = '{SumItem['InvoiceCharges']}' ,CIFFOB = '{SumItem['CIFFOB']}' ,OPQty = '{SumItem['OPQty']}' ,IPQty = '{SumItem['IPQty']}' ,InPqty = '{SumItem['InPqty']}' ,ImPQty = '{SumItem['ImPQty']}' ,GSTAmount = '{SumItem['GSTAmount']}' ,ExciseDutyAmount = '{SumItem['ExciseDutyAmount']}' ,CustomsDutyAmount = '{SumItem['CustomsDutyAmount']}' ,OtherTaxAmount = '{SumItem['OtherTaxAmount']}' ,OptionalSumtotal = '{SumItem['OptionalSumtotal']}' WHERE PermitId = '{PermitId}' AND ItemNo = '{SumItem['ItemNo']}' ")
                self.conn.commit()
                DelItems.append(SumItem['ItemNo'])


        self.cursor.execute(f"SELECT ItemNo FROM InNonItemDtl WHERE PermitId = '{PermitId}' ")
        for It in self.cursor.fetchall():
            if It[0] not in DelItems:
                self.cursor.execute(f"DELETE FROM InNonItemDtl WHERE ItemNo = '{It[0]}' AND PermitId = '{PermitId}' ")
                self.cursor.execute(f"DELETE FROM INNONCASCDtl WHERE ItemNo = '{It[0]}' AND PermitId = '{PermitId}' ")
        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId FROM InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitId))
        Ic = 1 
        for itm in self.cursor.fetchall():
            self.cursor.execute("UPDATE InNonItemDtl SET ItemNo = '{}' WHERE PermitId = '{}' AND  ItemNo = '{}' ".format(Ic,PermitId,itm[0]))
            self.cursor.execute("UPDATE INNONCASCDtl SET ItemNo = '{}' WHERE PermitId = '{}' AND  ItemNo = '{}' ".format(Ic,PermitId,itm[0]))
            Ic += 1
        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitId))
        self.item = self.cursor.fetchall()

        self.cursor.execute("SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,CASCId FROM INNONCASCDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.POST.get('PermitId')))
        self.casc = self.cursor.fetchall()

        return JsonResponse({ 
            "Result":"UPLOAD SUCCESSFULLY...!",
            "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records'),
            "casc" : (pd.DataFrame(list(self.casc), columns=['ItemNo','ProductCode','Quantity','ProductUOM','RowNo','CascCode1','CascCode2','CascCode3','CASCId'])).to_dict('records')
        })
    
class ContainerLoad(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):
        self.cursor.execute(f"select Id,RowNo,ContainerNo,size,weight,SealNo from InnonContainerDtl where PermitId = '{request.GET.get('PermitId')}' Order By RowNo ")
        return JsonResponse({
            "ContainerValue": (pd.DataFrame(list(self.cursor.fetchall()), columns=['Id','RowNo','ContainerNo','size','weight','SealNo'])).to_dict('records'),
        })
    def post(self,request):
        result = "SOMTHING ERROR"
        if request.POST.get('Method') == "SAVE":
            self.cursor.execute(f"select RowNo , PermitId from InnonContainerDtl where RowNo = '{request.POST.get('RowNo')}' AND PermitId = '{request.POST.get('PermitId')}'")
            result = self.cursor.fetchall()
            if not(result):
                self.cursor.execute(f"INSERT INTO InnonContainerDtl (PermitId, RowNo,ContainerNo, size, weight,SealNo, MessageType,TouchUser,TouchTime) VALUES ('{request.POST.get('PermitId')}','{request.POST.get('RowNo')}','{request.POST.get('ContainerNo')}','{request.POST.get('size')}','{request.POST.get('weight')}','{request.POST.get('SealNo')}','{request.POST.get('MessageType')}','{request.POST.get('TouchUser')}','{request.POST.get('TouchTime')}')")
                result  = "SAVED SUCCESSFULLY...!"
            else:
                self.cursor.execute(f"Update InnonContainerDtl set ContainerNo = '{request.POST.get('ContainerNo')}',size = '{request.POST.get('size')}',weight =  '{request.POST.get('weight')}',SealNo = '{request.POST.get('SealNo')}',MessageType = '{request.POST.get('MessageType')}',TouchUser = '{request.POST.get('TouchUser')}',TouchTime = '{request.POST.get('TouchTime')}' where RowNo = '{request.POST.get('RowNo')}' AND PermitId = '{request.POST.get('PermitId')}'")
                result  = "UPDATED SUCCESSFULLY...!"

        elif request.POST.get('Method') == "DELETE":

            self.cursor.execute(f"DELETE FROM InnonContainerDtl where PermitId = '{request.POST.get('PermitId')}' AND RowNo = '{request.POST.get('SNo')}' ")
            self.conn.commit()

            self.cursor.execute(f"select * from InnonContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo ")
            c = 1
            for j in self.cursor.fetchall():
                self.cursor.execute(f"UPDATE InnonContainerDtl SET RowNo = {c} WHERE PermitId = '{j[1]}' AND RowNo = '{j[2]}'")
                c += 1

            result  = "DELETD SUCCESSFULLY...!"

        elif request.POST.get('Method') == "CHECKDELETE":

            ContainerId = json.loads(request.POST.get('IDS'))
            values_str = ', '.join(map(str, ContainerId))

            query1 = f"DELETE FROM InnonContainerDtl WHERE RowNo IN ({values_str}) AND PermitId = '{request.POST.get('PermitId')}' "
            self.cursor.execute(query1)

            self.conn.commit()

            self.cursor.execute(f"select * from InnonContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo ")
            c = 1
            for j in self.cursor.fetchall():
                self.cursor.execute(f"UPDATE InnonContainerDtl SET RowNo = {c} WHERE PermitId = '{j[1]}' AND RowNo = '{j[2]}'")
                c += 1
            result  = "DELETD SUCCESSFULLY...!"

        elif request.POST.get('Method') == "ALLDELETE":

            self.cursor.execute(f"DELETE FROM InnonContainerDtl WHERE  PermitId = '{request.POST.get('PermitId')}' ")

        self.conn.commit()
        self.cursor.execute(f"select Id,RowNo,ContainerNo,size,weight,SealNo from InnonContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo ")
        return JsonResponse({
            "ContainerValue": (pd.DataFrame(list(self.cursor.fetchall()), columns=['Id','RowNo','ContainerNo','size','weight','SealNo'])).to_dict('records'),
            'Result':result
        })
    
class AttachDocument(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):

        if request.GET.get('Method') == "DELETE":
            self.cursor.execute("DELETE FROM InNonFile WHERE Id = '{}' ".format(request.GET.get('Data')))
        elif request.GET.get('Method') == "ALLDELETE":
            self.cursor.execute("DELETE FROM InNonFile WHERE PermitId = '{}' AND Type = 'NEW' ".format(request.GET.get('PermitId')))
        
        self.conn.commit()

        self.cursor.execute(f"SELECT Id,Sno,Name,ContentType,DocumentType,Size,PermitId,Type FROM InNonFile where PermitId = '{request.GET.get('PermitId')}' AND Type = '{request.GET.get('Type')}' Order By Sno ")
        return JsonResponse({
            "attachFile": (pd.DataFrame(list(self.cursor.fetchall()), columns=['Id','Sno','Name','ContentType','DocumentType','Size','PermitId','Type'])).to_dict('records'),
        })
    
    def post(self,request):

        self.cursor.execute( "SELECT COUNT(PermitId) AS MaxItem FROM InNonFile  where   PermitId='" + request.POST.get('PermitId') + "' AND Type = '" +request.POST.get('Type')+"'")

        myfile = request.FILES.get('file')
        path1 = request.POST.get('FilePath')
        fileFormat = request.POST.get('ContentType').split('/')

        with open(path1+request.POST.get('Name')+'.'+fileFormat[1], 'wb+') as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)

        lenFile = int((self.cursor.fetchone())[0])+1
        Qry = "INSERT INTO InNonFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        Val = (lenFile,request.POST.get('Name')+'.'+fileFormat[1],request.POST.get('ContentType'),None,request.POST.get('DocumentType'),request.POST.get('InPaymentId'),request.POST.get('UserName'),
               request.POST.get('TouchTime'),request.POST.get('Size'),request.POST.get('PermitId'),request.POST.get('Type'))
        self.cursor.execute(Qry,Val)
        self.conn.commit()

        self.cursor.execute(f"SELECT Id,Sno,Name,ContentType,DocumentType,Size,PermitId,Type FROM InNonFile where PermitId = '{request.POST.get('PermitId')}' AND Type = '{request.POST.get('Type')}'  Order By Sno ")
        return JsonResponse({
            "attachFile": (pd.DataFrame(list(self.cursor.fetchall()), columns=['Id','Sno','Name','ContentType','DocumentType','Size','PermitId','Type'])).to_dict('records'),
            'Result':"SAVED SUCCESSFULLY...!"
        })

def AttachDownloadInNon(request,ID):
    s = SqlDb()
    s.cursor.execute("SELECT * FROM InNonFile WHERE Id = '{}' ".format(ID))
    data  = s.cursor.fetchone()
    FilePath = "/Users/Public/IMG/"
    FileName = data[2]
    FileType = data[3]
    response = HttpResponse(open(FilePath+FileName, 'rb').read())
    response['Content-Type'] = FileType
    response['Content-Disposition'] = f'attachment; filename={str(FileName)}'
    return response

class InNonSave(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def post(self,request):#txtcusRemrk

        self.cursor.execute("SELECT Refid,JobId,MSGId,PermitId FROM InNonHeaderTbl WHERE Refid = '{}' AND JobId = '{}' AND MSGId = '{}' AND PermitId = '{}'".format(request.POST.get('Refid'), request.POST.get('JobId'), request.POST.get('MSGId'), request.POST.get('PermitId')))

        Data = self.cursor.fetchone()

        self.cursor.execute("DELETE FROM InNonCPCDtl WHERE PermitId = '{}' ".format(request.POST.get('PermitId')))
        self.conn.commit()

        QryCpc = "INSERT INTO InNonCPCDtl (PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for cpc in json.loads(request.POST.get("CpcData")):
            
            ValCpc = (request.POST.get('PermitId'),request.POST.get('MessageType'),cpc[0],cpc[1],cpc[2],cpc[3],cpc[4],request.POST.get('TouchUser'), request.POST.get('TouchTime'))
            self.cursor.execute(QryCpc,ValCpc)

        if Data is None:
            QryIns = "INSERT INTO InNonHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            Val = (request.POST.get('Refid'), request.POST.get('JobId'), request.POST.get('MSGId'), request.POST.get('PermitId'), request.POST.get('TradeNetMailboxID'), request.POST.get('MessageType'), request.POST.get('DeclarationType'), request.POST.get('PreviousPermit'), request.POST.get('CargoPackType'), request.POST.get('InwardTransportMode'), request.POST.get('OutwardTransportMode'), request.POST.get('BGIndicator'), request.POST.get('SupplyIndicator'), request.POST.get('ReferenceDocuments'), request.POST.get('License'), request.POST.get('Recipient'), request.POST.get('DeclarantCompanyCode'), request.POST.get('ImporterCompanyCode'), request.POST.get('ExporterCompanyCode'), request.POST.get('InwardCarrierAgentCode'), request.POST.get('OutwardCarrierAgentCode'), request.POST.get('ConsigneeCode'), request.POST.get('FreightForwarderCode'), request.POST.get('ClaimantPartyCode'), request.POST.get('ArrivalDate'), request.POST.get('LoadingPortCode'), request.POST.get('VoyageNumber'), request.POST.get('VesselName'), request.POST.get('OceanBillofLadingNo'), request.POST.get('ConveyanceRefNo'), request.POST.get('TransportId'), request.POST.get('FlightNO'), request.POST.get('AircraftRegNo'), request.POST.get('MasterAirwayBill'), request.POST.get('ReleaseLocation'), request.POST.get('RecepitLocation'), request.POST.get('RecepilocaName'), request.POST.get('StorageLocation'), request.POST.get('ExhibitionSDate'), request.POST.get('ExhibitionEDate'), request.POST.get('BlanketStartDate'), request.POST.get('TradeRemarks'), request.POST.get('InternalRemarks'), request.POST.get('CustomerRemarks'), request.POST.get('DepartureDate'), request.POST.get('DischargePort'), request.POST.get('FinalDestinationCountry'), request.POST.get('OutVoyageNumber'), request.POST.get('OutVesselName'), request.POST.get('OutOceanBillofLadingNo'), request.POST.get('VesselType'), request.POST.get('VesselNetRegTon'), request.POST.get('VesselNationality'), request.POST.get('TowingVesselID'), request.POST.get('TowingVesselName'), request.POST.get('NextPort'), request.POST.get('LastPort'), request.POST.get('OutConveyanceRefNo'), request.POST.get('OutTransportId'), request.POST.get('OutFlightNO'), request.POST.get('OutAircraftRegNo'), request.POST.get('OutMasterAirwayBill'), request.POST.get('TotalOuterPack'), request.POST.get('TotalOuterPackUOM'), request.POST.get('TotalGrossWeight'), request.POST.get('TotalGrossWeightUOM'), request.POST.get('GrossReference'), request.POST.get('DeclareIndicator'), request.POST.get('NumberOfItems'), request.POST.get('TotalCIFFOBValue'), request.POST.get('TotalGSTTaxAmt'), request.POST.get('TotalExDutyAmt'), request.POST.get('TotalCusDutyAmt'), request.POST.get('TotalODutyAmt'), request.POST.get('TotalAmtPay'), request.POST.get('Status'), request.POST.get('TouchUser'), request.POST.get('TouchTime'), request.POST.get('PermitNumber'), request.POST.get('prmtStatus'), request.POST.get('ReleaseLocaName'), request.POST.get('Inhabl'), request.POST.get('outhbl'), request.POST.get('seastore'), request.POST.get('Cnb'), request.POST.get('DeclarningFor'), request.POST.get('MRDate'), request.POST.get('MRTime'))
            self.cursor.execute(QryIns,Val)

            self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(request.POST.get('TouchUser')))
            AccountId = self.cursor.fetchone()[0]

            self.cursor.execute("INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime)  VALUES ('" + request.POST.get('PermitId') + "','" + request.POST.get('MessageType') + "','" + AccountId + "','" + request.POST.get('MSGId') + "','" +request.POST.get('TouchUser') + "','" + request.POST.get('TouchTime') + "')")
        else:
            QryUpd = "UPDATE InNonHeaderTbl SET TradeNetMailboxID = %s,MessageType = %s,DeclarationType = %s,PreviousPermit = %s,CargoPackType = %s,InwardTransportMode = %s,OutwardTransportMode = %s,BGIndicator = %s,SupplyIndicator = %s,ReferenceDocuments = %s,License = %s,Recipient = %s,DeclarantCompanyCode = %s,ImporterCompanyCode = %s,ExporterCompanyCode = %s,InwardCarrierAgentCode = %s,OutwardCarrierAgentCode = %s,ConsigneeCode = %s,FreightForwarderCode = %s,ClaimantPartyCode = %s,ArrivalDate = %s,LoadingPortCode = %s,VoyageNumber = %s,VesselName = %s,OceanBillofLadingNo = %s,ConveyanceRefNo = %s,TransportId = %s,FlightNO = %s,AircraftRegNo = %s,MasterAirwayBill = %s,ReleaseLocation = %s,RecepitLocation = %s,RecepilocaName = %s,StorageLocation = %s,ExhibitionSDate = %s,ExhibitionEDate = %s,BlanketStartDate = %s,TradeRemarks = %s,InternalRemarks = %s,CustomerRemarks = %s,DepartureDate = %s,DischargePort = %s,FinalDestinationCountry = %s,OutVoyageNumber = %s,OutVesselName = %s,OutOceanBillofLadingNo = %s,VesselType = %s,VesselNetRegTon = %s,VesselNationality = %s,TowingVesselID = %s,TowingVesselName = %s,NextPort = %s,LastPort = %s,OutConveyanceRefNo = %s,OutTransportId = %s,OutFlightNO = %s,OutAircraftRegNo = %s,OutMasterAirwayBill = %s,TotalOuterPack = %s,TotalOuterPackUOM = %s,TotalGrossWeight = %s,TotalGrossWeightUOM = %s,GrossReference = %s,DeclareIndicator = %s,NumberOfItems = %s,TotalCIFFOBValue = %s,TotalGSTTaxAmt = %s,TotalExDutyAmt = %s,TotalCusDutyAmt = %s,TotalODutyAmt = %s,TotalAmtPay = %s,Status = %s,TouchUser = %s,TouchTime = %s,PermitNumber = %s,prmtStatus = %s,ReleaseLocaName = %s,Inhabl = %s,outhbl = %s,seastore = %s,Cnb = %s,DeclarningFor = %s,MRDate = %s,MRTime = %s  WHERE Refid = %s AND JobId = %s AND MSGId = %s AND PermitId = %s"
            Val = (request.POST.get('TradeNetMailboxID'),request.POST.get('MessageType'),request.POST.get('DeclarationType'),request.POST.get('PreviousPermit'),request.POST.get('CargoPackType'),request.POST.get('InwardTransportMode'),request.POST.get('OutwardTransportMode'),request.POST.get('BGIndicator'),request.POST.get('SupplyIndicator'),request.POST.get('ReferenceDocuments'),request.POST.get('License'),request.POST.get('Recipient'),request.POST.get('DeclarantCompanyCode'),request.POST.get('ImporterCompanyCode'),request.POST.get('ExporterCompanyCode'),request.POST.get('InwardCarrierAgentCode'),request.POST.get('OutwardCarrierAgentCode'),request.POST.get('ConsigneeCode'),request.POST.get('FreightForwarderCode'),request.POST.get('ClaimantPartyCode'),request.POST.get('ArrivalDate'),request.POST.get('LoadingPortCode'),request.POST.get('VoyageNumber'),request.POST.get('VesselName'),request.POST.get('OceanBillofLadingNo'),request.POST.get('ConveyanceRefNo'),request.POST.get('TransportId'),request.POST.get('FlightNO'),request.POST.get('AircraftRegNo'),request.POST.get('MasterAirwayBill'),request.POST.get('ReleaseLocation'),request.POST.get('RecepitLocation'),request.POST.get('RecepilocaName'),request.POST.get('StorageLocation'),request.POST.get('ExhibitionSDate'),request.POST.get('ExhibitionEDate'),request.POST.get('BlanketStartDate'),request.POST.get('TradeRemarks'),request.POST.get('InternalRemarks'),request.POST.get('CustomerRemarks'),request.POST.get('DepartureDate'),request.POST.get('DischargePort'),request.POST.get('FinalDestinationCountry'),request.POST.get('OutVoyageNumber'),request.POST.get('OutVesselName'),request.POST.get('OutOceanBillofLadingNo'),request.POST.get('VesselType'),request.POST.get('VesselNetRegTon'),request.POST.get('VesselNationality'),request.POST.get('TowingVesselID'),request.POST.get('TowingVesselName'),request.POST.get('NextPort'),request.POST.get('LastPort'),request.POST.get('OutConveyanceRefNo'),request.POST.get('OutTransportId'),request.POST.get('OutFlightNO'),request.POST.get('OutAircraftRegNo'),request.POST.get('OutMasterAirwayBill'),request.POST.get('TotalOuterPack'),request.POST.get('TotalOuterPackUOM'),request.POST.get('TotalGrossWeight'),request.POST.get('TotalGrossWeightUOM'),request.POST.get('GrossReference'),request.POST.get('DeclareIndicator'),request.POST.get('NumberOfItems'),request.POST.get('TotalCIFFOBValue'),request.POST.get('TotalGSTTaxAmt'),request.POST.get('TotalExDutyAmt'),request.POST.get('TotalCusDutyAmt'),request.POST.get('TotalODutyAmt'),request.POST.get('TotalAmtPay'),request.POST.get('Status'),request.POST.get('TouchUser'),request.POST.get('TouchTime'),request.POST.get('PermitNumber'),request.POST.get('prmtStatus'),request.POST.get('ReleaseLocaName'),request.POST.get('Inhabl'),request.POST.get('outhbl'),request.POST.get('seastore'),request.POST.get('Cnb'),request.POST.get('DeclarningFor'),request.POST.get('MRDate'),request.POST.get('MRTime'),request.POST.get('Refid'),request.POST.get('JobId'),request.POST.get('MSGId'),request.POST.get('PermitId'))
            self.cursor.execute(QryUpd,Val)


        if request.POST.get('StatusType') == "AME":
            self.cursor.execute("delete from InNonAmend where MSGId='" + request.POST.get('MSGId') + "' and Permitno='" + request.POST.get('Permitno') + "'")
            self.conn.commit()

            self.cursor.execute(f"insert into InNonAmend (Permitno,AmendmentCount,UpdateIndicator,ReplacementPermitno,DescriptionOfReason,PermitExtension,ExtendImportPeriod,DeclarationIndigator,TouchUser,TouchTme,MSGId,AmendType) VALUES ('{request.POST.get('Permitno')}','{request.POST.get('AmendmentCount')}','{request.POST.get('UpdateIndicator')}','{request.POST.get('ReplacementPermitno')}','{request.POST.get('DescriptionOfReason')}','{request.POST.get('PermitExtension')}','{request.POST.get('ExtendImportPeriod')}','{request.POST.get('DeclarationIndigator')}','{request.POST.get('TouchUser')}','{request.POST.get('TouchTime')}','{request.POST.get('MSGId')}','{request.POST.get('AmendType')}')")

        if request.POST.get('StatusType') == "CNL":
            self.cursor.execute("delete from InNonCancel where MSGId='" + request.POST.get('MSGId') + "' and Permitno='" + request.POST.get('CancelPermitno') + "'")
            self.conn.commit()
            self.cursor.execute(f"INSERT INTO InNonCancel (Permitno,UpdateIndicator,ReplacementPermitno,ResonForCancel,DescriptionOfReason,DeclarationIndigator,TouchUser,TouchTme,MSGId,CancelType) VALUES ('{request.POST.get('CancelPermitno')}','{request.POST.get('CancelUpdateIndicator')}','{request.POST.get('CancelReplacementPermitno')}','{request.POST.get('ResonForCancel')}','{request.POST.get('CancelDescriptionOfReason')}','{request.POST.get('CancelDeclarationIndigator')}','{request.POST.get('TouchUser')}','{request.POST.get('TouchTime')}','{request.POST.get('MSGId')}','{request.POST.get('CancelType')}')")
        
        self.conn.commit()

        return HttpResponse("/InonPaymentList/")

class InNonHeaderDelete(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):
        self.cursor.execute("UPDATE InNonHeaderTbl SET STATUS = 'DEL' WHERE Id = '{}' ".format(request.GET.get('InNonId')))
        self.conn.commit()
        return HttpResponse("/InonPaymentList/")
    
class CopyInNonPayment(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):
        

        Username = request.session['Username'] 

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")
        

        self.cursor.execute(f"SELECT PermitId FROM InNonHeaderTbl WHERE Id = '{request.GET.get('Id')}' ")

        CopyPermitId = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        ManageUserVal = self.cursor.fetchone()
        AccountId = ManageUserVal[0]

        self.cursor.execute("SELECT COUNT(*) + 1  FROM InNonHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'INPDEC' ".format(refDate))
        self.RefId = ("%03d" % self.cursor.fetchone()[0])

        self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute(f"INSERT INTO InNonHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime) SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{ManageUserVal[1]}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,'',CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{Username}','{NowDate}','','COPY',ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,'--Select--',MRDate,'' FROM InNonHeaderTbl WHERE Id = '{request.GET.get('Id')}'")

        self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','INPDEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')")

        self.cursor.execute(f"INSERT INTO InNonInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,'{self.PermitIdInNon}','{Username}','{NowDate}' FROM InNonInvoiceDtl WHERE PermitId = '{CopyPermitId}' ") 
        
        self.cursor.execute(f"INSERT INTO InNonItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,'{Username}','{NowDate}',OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM InNonItemDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO INNONCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId) SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,'{self.PermitIdInNon}',MessageType,'{Username}','{NowDate}',CASCId FROM INNONCASCDtl WHERE PermitId = '{CopyPermitId}'")
        
        self.cursor.execute(f"INSERT INTO InnonContainerDtl (PermitId, RowNo,ContainerNo, size, weight,SealNo, MessageType,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}', RowNo,ContainerNo, size, weight,SealNo, MessageType,'{Username}','{NowDate}' FROM InnonContainerDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO InNonCPCDtl (PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}',MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,'{Username}','{NowDate}' FROM InNonCPCDtl Where PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO InNonFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{Username}','{NowDate}',Size,'{self.PermitIdInNon}',Type FROM InNonFile WHERE PermitId = '{CopyPermitId}' ")
        
        self.conn.commit()

        self.cursor.execute(f"SELECT Id FROM InNonHeaderTbl WHERE PermitId = '{self.PermitIdInNon}' ")
        
        request.session['InNonId'] = self.cursor.fetchone()[0]
        
        return JsonResponse({"SUCCESS" : 'COPY ITEM'})
   

def CpcDeleteInNon(request,ID):
    s = SqlDb()
    s.cursor.execute(f"DELETE FROM InNonCPCDtl WHERE Id = '{ID}' ")
    s.conn.commit()
    return JsonResponse({"DELETE" : "DELETED"})
 
class InNonTransmitData(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):

        maiId = request.GET.get('mailId')

        self.cursor.execute("SELECT TOP 1 TouchUser FROM InNonHeaderTbl WHERE TradeNetMailboxID = '{}' ".format(maiId))

        try:
            Username = self.cursor.fetchone()[0]
        except Exception as e:
            Username = request.session['Username'] 

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        ManageUserVal = self.cursor.fetchone()
        AccountId = ManageUserVal[0]
        

        for Id in json.loads(request.GET.get("my_data")):
            self.cursor.execute(f"SELECT PermitId FROM InNonHeaderTbl WHERE Id = '{Id}' ")
            CopyPermitId = self.cursor.fetchone()[0]
            print("copypermit:",CopyPermitId)

            self.cursor.execute("SELECT COUNT(*) + 1  FROM InNonHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'INPDEC' ".format(refDate))
            self.RefId = ("%03d" % self.cursor.fetchone()[0])

            self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
            self.JobIdCount = self.cursor.fetchone()[0]

            self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
            self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
            self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"
            print("permit id:",self.PermitIdInNon)


            NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute(f"INSERT INTO InNonHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime) SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{maiId}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,'',CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{Username}','{NowDate}','','NEW',ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,'--Select--',MRDate,'' FROM InNonHeaderTbl WHERE Id = '{Id}'")

            self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','INPDEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')")

            self.cursor.execute(f"INSERT INTO InNonInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,'{self.PermitIdInNon}','{Username}','{NowDate}' FROM InNonInvoiceDtl WHERE PermitId = '{CopyPermitId}' ")
            
            self.cursor.execute(f"INSERT INTO InNonItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,'{Username}','{NowDate}',OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM InNonItemDtl WHERE PermitId = '{CopyPermitId}'")

            self.cursor.execute(f"INSERT INTO INNONCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId) SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,'{self.PermitIdInNon}',MessageType,'{Username}','{NowDate}',CASCId FROM INNONCASCDtl WHERE PermitId = '{CopyPermitId}'")
            
            self.cursor.execute(f"INSERT INTO InnonContainerDtl (PermitId, RowNo,ContainerNo, size, weight,SealNo, MessageType,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}', RowNo,ContainerNo, size, weight,SealNo, MessageType,'{Username}','{NowDate}' FROM InnonContainerDtl WHERE PermitId = '{CopyPermitId}'")

            self.cursor.execute(f"INSERT INTO InNonFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{Username}','{NowDate}',Size,'{self.PermitIdInNon}',Type FROM InNonFile WHERE PermitId = '{CopyPermitId}' ")
            
            self.conn.commit()

        return JsonResponse({"SUCCESS" : 'COPY ITEM'})
    
class InonPayementAmend(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
       
    def get(self,request,Id):

        Username = request.session['Username'] 

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute(f"SELECT PermitId,PermitNumber FROM InNonHeaderTbl WHERE Id = '{Id}' ")
        PermitIdValus = self.cursor.fetchone()
        CopyPermitId = PermitIdValus[0]

        self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        ManageUserVal = self.cursor.fetchone()
        AccountId = ManageUserVal[0]

        self.cursor.execute("SELECT COUNT(*) + 1  FROM InNonHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'INPDEC' ".format(refDate))
        self.RefId = ("%03d" % self.cursor.fetchone()[0])

        self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute(f"INSERT INTO InNonHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime) SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{ManageUserVal[1]}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,'',CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{Username}','{NowDate}',PermitNumber,'AME',ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,'--Select--',MRDate,'' FROM InNonHeaderTbl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','INPDEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')")

        self.cursor.execute(f"INSERT INTO InNonInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,'{self.PermitIdInNon}','{Username}','{NowDate}' FROM InNonInvoiceDtl WHERE PermitId = '{CopyPermitId}' ")
        
        self.cursor.execute(f"INSERT INTO InNonItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,'{Username}','{NowDate}',OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM InNonItemDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO INNONCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId) SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,'{self.PermitIdInNon}',MessageType,'{Username}','{NowDate}',CASCId FROM INNONCASCDtl WHERE PermitId = '{CopyPermitId}'")
        
        self.cursor.execute(f"INSERT INTO InnonContainerDtl (PermitId, RowNo,ContainerNo, size, weight,SealNo, MessageType,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}', RowNo,ContainerNo, size, weight,SealNo, MessageType,'{Username}','{NowDate}' FROM InnonContainerDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO InNonFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{Username}','{NowDate}',Size,'{self.PermitIdInNon}',Type FROM InNonFile WHERE PermitId = '{CopyPermitId}' ")
        
        self.conn.commit()

        self.cursor.execute(f"SELECT Id FROM InNonHeaderTbl WHERE PermitId = '{self.PermitIdInNon}'")
        InNonId = self.cursor.fetchone()[0]

        request.session['InNonId'] = InNonId

        return redirect("/InonPayementEdit/")

class InNonPaymentCcp(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,Data):
        pdfFiles = []
        for ID in Data.split(","):
            self.cursor.execute("SELECT Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime FROM InNonHeaderTbl WHERE Id = '{}' ".format(ID))

            InNonHeaderData = self.cursor.fetchall()

            PermitValues = (pd.DataFrame(list(InNonHeaderData), columns=['Refid','JobId','MSGId','PermitId','TradeNetMailboxID','MessageType','DeclarationType','PreviousPermit','CargoPackType','InwardTransportMode','OutwardTransportMode','BGIndicator','SupplyIndicator','ReferenceDocuments','License','Recipient','DeclarantCompanyCode','ImporterCompanyCode','ExporterCompanyCode','InwardCarrierAgentCode','OutwardCarrierAgentCode','ConsigneeCode','FreightForwarderCode','ClaimantPartyCode','ArrivalDate','LoadingPortCode','VoyageNumber','VesselName','OceanBillofLadingNo','ConveyanceRefNo','TransportId','FlightNO','AircraftRegNo','MasterAirwayBill','ReleaseLocation','RecepitLocation','RecepilocaName','StorageLocation','ExhibitionSDate','ExhibitionEDate','BlanketStartDate','TradeRemarks','InternalRemarks','CustomerRemarks','DepartureDate','DischargePort','FinalDestinationCountry','OutVoyageNumber','OutVesselName','OutOceanBillofLadingNo','VesselType','VesselNetRegTon','VesselNationality','TowingVesselID','TowingVesselName','NextPort','LastPort','OutConveyanceRefNo','OutTransportId','OutFlightNO','OutAircraftRegNo','OutMasterAirwayBill','TotalOuterPack','TotalOuterPackUOM','TotalGrossWeight','TotalGrossWeightUOM','GrossReference','DeclareIndicator','NumberOfItems','TotalCIFFOBValue','TotalGSTTaxAmt','TotalExDutyAmt','TotalCusDutyAmt','TotalODutyAmt','TotalAmtPay','Status','TouchUser','TouchTime','PermitNumber','prmtStatus','ReleaseLocaName','Inhabl','outhbl','seastore','Cnb','DeclarningFor','MRDate','MRTime']).to_dict('records'))[0]
        
            lftcol = 50
            rgtcol = 280
            self.countPage = 1

            if PermitValues['PermitNumber'] == "":
                PermitBar = "DRAFT"
                OldFilename = f"D:/Users/Public/PDFFilesKtt/{PermitBar}1.pdf"
                
            else:
                PermitBar = PermitValues['PermitNumber']
                OldFilename = f"D:/Users/Public/PDFFilesKtt/{PermitBar}1.pdf"
                barcode = code39.Standard39(PermitValues['PermitNumber'], barHeight=36.0, barWidth=1.1, baseline=9.0,size=12.0, N=3.0, X=1.0, StartsStopText=False, Extended=False)

            p = canvas.Canvas(OldFilename, pagesize=(595, 841))
            p.setTitle(PermitBar)
            inpstrtdate = ""
            inpEndate = ""

            p.setFont('Courier-Bold', 10)
            p.drawString(480, 750, PermitBar)

            if PermitValues['PermitNumber'] != "":
                barcode.drawOn(p, 330, 760)

            p.setFont('Courier', 10)
            p.drawString(400, 750, "PERMIT NO : ")

            p.drawString(rgtcol, 700, "CARGO CLEARANCE PERMIT")
            p.drawString(460, 700, ("PG : {} OF").format(self.countPage))
            self.countPage += 1

            if PermitValues['prmtStatus'] =="AMD":
                p.drawString(lftcol, 670, "MESSAGE TYPE      : IN-NON-PAYMENT UPDATED PERMIT")
            else: 
                p.drawString(lftcol, 670, "MESSAGE TYPE      : IN-NON-PAYMENT PERMIT")
                
            p.drawString(lftcol, 660, "DECLARATION TYPE  : " + (str(PermitValues["DeclarationType"])[6:]).upper())

            p.drawString(lftcol, 630, "IMPORTER:")

            self.cursor.execute(f"SELECT Name,Name1,Cruei FROM InNonImporter WHERE code = '{PermitValues['ImporterCompanyCode']}' ")
            ImportData = self.cursor.fetchone()
            ImportDataCruei = ImportData[2]
            ImportData = str(ImportData[0])+str(ImportData[1])

            if len(ImportData) >= 35:
                p.drawString(lftcol, 620, (ImportData[:35]).upper())
                p.drawString(lftcol, 610, (ImportData[35:]).upper())
            else:
                p.drawString(lftcol, 620, (ImportData).upper())
            p.drawString(lftcol, 600, str(ImportDataCruei).upper())

            p.drawString(lftcol, 590, "EXPORTER:")
            self.cursor.execute(f"SELECT Name,Name1,Cruei FROM InnonExporter WHERE code = '{PermitValues['ExporterCompanyCode']}' ")
            ExportData = self.cursor.fetchone()
            
            if ExportData is not None :
                ExportDataCruei = ExportData[2]
                ExportData = str(ExportData[0])+str(ExportData[1])

                if len(ImportData) >= 35:
                    p.drawString(lftcol, 580, (ExportData[:35]).upper())
                    p.drawString(lftcol, 570, (ExportData[35:]).upper())
                else:
                    p.drawString(lftcol, 580, (ExportData).upper())
                p.drawString(lftcol, 560, str(ExportDataCruei).upper())

            p.drawString(lftcol, 550, "HANDLING AGENT: ")
            p.drawString(lftcol, 540, " ")
            p.drawString(lftcol, 530, " ")
            p.drawString(lftcol, 520, " ")
            p.drawString(lftcol, 510, " ")
            p.drawString(lftcol, 500, "PORT OF LOADING/NEXT PORT OF CALL:")

            self.cursor.execute(f"SELECT PortCode,PortName FROM LoadingPort WHERE PortCode = '{PermitValues['NextPort']}'")
            NextPort = self.cursor.fetchone()
            if NextPort is not None:
                p.drawString(lftcol, 490, str(NextPort[1]).upper())

            p.drawString(lftcol, 480, "PORT OF DISCHARGE/FINAL PORT OF CALL ")

            self.cursor.execute(f"SELECT PortCode,PortName FROM LoadingPort WHERE PortCode = '{PermitValues['DischargePort']}'")
            DischargePort = self.cursor.fetchone()
            if DischargePort is not None:
                p.drawString(lftcol, 470, str(DischargePort[1]).upper())

            p.drawString(lftcol, 460, "COUNTRY OF FINAL DESTINATION:")
            if PermitValues['FinalDestinationCountry'] != "--Select--":
                p.drawString(lftcol, 450, str(PermitValues['FinalDestinationCountry']).split(":")[0])

            p.drawString(lftcol, 440, "INWARD CARRIER AGENT: ")

            InWard = "SELECT Name,Name1 FROM InnonInwardCarrierAgent where Code=%s"
            self.cursor.execute(InWard,(PermitValues['InwardCarrierAgentCode'],))
            InwardData = self.cursor.fetchone()
            if InwardData:
                InwardData = str(InwardData[0])+str(InwardData[1])

                if len(InwardData) >= 35:
                    p.drawString(lftcol, 430, (InwardData[:35]).upper().replace("\n"," "))
                    p.drawString(lftcol, 420, (InwardData[35:70]).upper().replace("\n"," "))
                    p.drawString(lftcol, 410, (InwardData[70:]).upper().replace("\n"," "))
                else:
                    p.drawString(lftcol, 430, (InwardData).upper().replace("\n"," "))

            p.drawString(lftcol, 400, "OUTWARD CARRIER AGENT: ")


            OutWard = "SELECT Name,Name1 FROM InnonOutwardCarrierAgent where Code=%s"
            self.cursor.execute(OutWard,(PermitValues['OutwardCarrierAgentCode'],))
            OutwardData = self.cursor.fetchone()
            if OutwardData is not None:
                OutwardData = str(OutwardData[0])+str(OutwardData[1])

                if len(OutwardData) >= 35:
                    p.drawString(lftcol, 390, (OutwardData[:35]).upper().replace("\n"," "))
                    p.drawString(lftcol, 380, (OutwardData[35:70]).upper().replace("\n"," "))
                    p.drawString(lftcol, 370, (OutwardData[70:]).upper().replace("\n"," "))
                else:
                    p.drawString(lftcol, 390, (OutwardData).upper().replace("\n"," "))

            p.drawString(lftcol, 360, "PLACE OF RELEASE: ")

            ReleaseY = 350
            ReleaseX = lftcol
            RelaseVal = str(PermitValues['ReleaseLocaName'] ).replace("\n" , '')

            for Re in range(len(RelaseVal)):
                p.drawString(ReleaseX, ReleaseY, str(RelaseVal[Re]))
                ReleaseX += 6

                if Re %32 == 0 and Re != 0:
                    ReleaseY -= 10
                    ReleaseX = lftcol

            ReleaseY =- 10 

            p.drawString(lftcol, ReleaseY, PermitValues['ReleaseLocation'])
            p.drawString(lftcol, 250, "LICENCE NO:")


            licence = (str(PermitValues['License']).upper()).split('-')
            p.drawString(lftcol, 240, licence[0])
            p.drawString(lftcol, 230, licence[1])
            p.drawString(lftcol, 220, licence[2])
            p.drawString(lftcol, 210, licence[3])
            p.drawString(lftcol, 200, licence[4])
            p.drawString(lftcol, 50,  "--------------------------------------------------------------------------------")
            
            Declarant = "SELECT Cruei FROM DeclarantCompany where tradenetmailboxId=%s"
            self.cursor.execute(Declarant,(PermitValues['TradeNetMailboxID'],))
            DeclarData = self.cursor.fetchone()
            
            p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format((DeclarData[0]).upper(), str(PermitValues['MSGId'][:8]).upper(), str(PermitValues['MSGId'][8:]).upper()))

            if PermitValues['prmtStatus'] =="AMD":
                self.cursor.execute(f"SELECT StartDate,EndDate FROM InnonAMDPMT where PermitNumber = '{PermitValues['PermitNumber']}' AND MsgId = '{PermitValues['MSGId']}' ")
                StartEnd = self.cursor.fetchone()
            else:
                self.cursor.execute(f"SELECT StartDate,EndDate FROM InnonPMT where PermitNumber = '{PermitValues['PermitNumber']}' ")
                StartEnd = self.cursor.fetchone()

            if StartEnd is not None:
                inpstrtdate = datetime.strptime(str(StartEnd[0]), '%Y-%m-%d').strftime('%d/%m/%Y')
                inpEndate = datetime.strptime(str(StartEnd[1]), '%Y-%m-%d').strftime('%d/%m/%Y')


            rgy = 630
            p.drawString(rgtcol, rgy, ("VALIDITY PERIOD      : {} - ").format(inpstrtdate))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("                       {}").format(inpEndate))
            rgy -= 20

            totalGross = "{:.3f}".format(float(PermitValues["TotalGrossWeight"]))

            p.drawString(rgtcol, rgy, ("TOTAL GROSS WT/UNIT  : {:>18}/{}").format(totalGross, PermitValues["TotalGrossWeightUOM"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOTAL OUTER PACK/UNIT: {:>18}/{}").format(PermitValues["TotalOuterPack"], PermitValues["TotalOuterPackUOM"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOT EXCISE DUT PAYABLE  : S${:>17}").format(PermitValues["TotalExDutyAmt"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOT CUSTOMS DUT PAYABLE : S${:>17}").format(PermitValues["TotalCusDutyAmt"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOT OTHER TAX PAYABLE   : S${:>17}").format(PermitValues["TotalODutyAmt"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOTAL GST AMT           : S${:>17}").format(PermitValues["TotalGSTTaxAmt"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOTAL AMOUNT PAYABLE    : S${:>17}").format(PermitValues["TotalAmtPay"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("CARGO PACKING TYPE: {} ").format(((PermitValues['CargoPackType'])[3:]).upper()))
            rgy -= 10
            p.drawString(rgtcol, rgy, "IN TRANSPORT IDENTIFIER: ")
            rgy -= 10

            
            if PermitValues['InwardTransportMode'] == "4 : Air":
                transidval = PermitValues['AircraftRegNo']
                CoveyanceNo = PermitValues['VesselName']
            elif PermitValues['InwardTransportMode'] == "1 : Sea":
                transidval = PermitValues['VesselName']
                CoveyanceNo = PermitValues['VesselName']
            else:
                transidval = PermitValues['TransportId']
                CoveyanceNo = PermitValues['TransportId']

            p.drawString(rgtcol, rgy, transidval.upper())
            rgy -= 10
            p.drawString(rgtcol, rgy, ("CONVEYANCE REFERENCE NO: {} ").format(CoveyanceNo.upper()))
            rgy -= 10
            p.drawString(rgtcol, rgy, "OBL/MAWB NO: ")
            rgy -= 10
            p.drawString(rgtcol, rgy, PermitValues['OceanBillofLadingNo'])
            rgy -= 10
            if str(PermitValues['ArrivalDate'].strftime('%d/%m/%Y')) != "01/01/1900":
                p.drawString(rgtcol, rgy, "ARRIVAL DATE         : {}".format((PermitValues['ArrivalDate']).strftime('%d/%m/%Y')))
            else:
                p.drawString(rgtcol, rgy, "ARRIVAL DATE         : {}".format((PermitValues['ArrivalDate']).strftime('%d/%m/%Y')))

            rgy -= 10
            p.drawString(rgtcol, rgy, "OU TRANSPORT IDENTIFIER: ")
            rgy -= 10

            if PermitValues['InwardTransportMode'] == "4 : Air":
                Outransport = PermitValues['OutAircraftRegNo']
                conveno = PermitValues["OutFlightNO"]
                mastebill = PermitValues["OutMasterAirwayBill"]
            
            elif PermitValues['InwardTransportMode'] == "1 : Sea":
                Outransport = PermitValues['OutVesselName']
                conveno = PermitValues["OutVoyageNumber"]
                mastebill = PermitValues["OutOceanBillofLadingNo"]
            else:
                Outransport = PermitValues['OutTransportId']
                conveno = PermitValues["OutConveyanceRefNo"]
                mastebill = ""

            p.drawString(rgtcol, rgy, str(Outransport).upper())
            rgy -= 10
            p.drawString(rgtcol, rgy, "CONVEYANCE REFERENCE NO:  "+str(conveno).upper())
            rgy -= 10
            p.drawString(rgtcol, rgy, "OBL/MAWB/UCR NO: ")
            rgy -= 10
            p.drawString(rgtcol, rgy, ""+str(mastebill).upper())
            rgy -= 10

            if str(PermitValues['DepartureDate'].strftime('%d/%m/%Y')) != "01/01/1900":
                p.drawString(rgtcol, rgy, "DEPARTURE DATE       : "+str(PermitValues['DepartureDate'].strftime('%d/%m/%Y')))
            else:
                p.drawString(rgtcol, rgy, "DEPARTURE DATE       : ")
            rgy -= 20

            p.drawString(rgtcol, rgy, "CERTIFICATE NO:  ")
            rgy -= 30

            p.drawString(rgtcol, rgy, "PLACE OF RECEIPT:")
            rgy -= 10

            ReleaseY = rgy
            ReleaseX = rgtcol
            ReciptVal = str(PermitValues['RecepilocaName'] ).replace("\n" , '')

            for Re in range(len(ReciptVal)):
                p.drawString(ReleaseX, ReleaseY, str(ReciptVal[Re]))
                ReleaseX += 6

                if Re %32 == 0 and Re != 0:
                    ReleaseY -= 10
                    ReleaseX = rgtcol

            ReleaseY -= 10

            p.drawString(rgtcol, ReleaseY, PermitValues['RecepitLocation'])
            p.drawString(rgtcol, 250, "CUSTOMS PROCEDURE CODE (CPC) : ")
            rely = 240

            self.cursor.execute(f"SELECT DISTINCT CPCType FROM InNonCPCDtl WHERE PermitId='{PermitValues['PermitId']}' ")
            CpcData = self.cursor.fetchall()

            for cpc in CpcData:
                p.drawString(rgtcol, rely, str(cpc[0]))
                rely -= 10

            if PermitValues['Cnb'] == "True" or PermitValues['Cnb'] == "true":
                p.drawString(rgtcol, rely, str("CNB"))

            #-------------------------------------------Heading Page Complete-----------------------------------------------#

            p.showPage()

            snox = 50
            hscodex = 100
            currentx = 180
            prviousx = 320
            makingx = 50
            cityx = 120
            brandx = 220
            itemy = 820

            def itemyF(itemy):
                if itemy <= 70:
                    itemy = 820
                    p.showPage()
                    p.setFont('Courier', 10)
                else:
                    itemy -= 10
                if itemy <= 820 and itemy >= 700:
                    p.setFont('Courier', 10)
                    p.drawString(rgtcol, itemy, "CARGO CLEARANCE PERMIT ")
                    p.drawString(460, itemy, ("PG : {} OF ").format(self.countPage))
                    self.countPage += 1
                    itemy -= 10
                    p.drawString(lftcol, itemy, "PERMIT NO : " +str(PermitBar))
                    p.drawString(rgtcol, itemy, "======================")
                    itemy -= 10
                    p.drawString(rgtcol, itemy, "(CONTINUATION PAGE)")
                    itemy -= 20
                    p.drawString(lftcol, itemy, "CONSIGNMENT DETAILS")
                    itemy -= 10
                    p.drawString(lftcol, itemy, "--------------------------------------------------------------------------------")
                    itemy -= 10

                    p.drawString(lftcol, itemy, "S/NO     HS CODE      CURRENT LOT NO         PREVIOUS LOT NO                ")
                    itemy -= 10

                    p.drawString(lftcol, itemy, "MARKING    CTY OF ORIGIN    BRAND NAME       MODEL                            ")
                    itemy -= 10

                    self.cursor.execute(f"SELECT count(InHAWBOBL) FROM InNonItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '' ")
                    ItemHeadData = self.cursor.fetchone()

                    if  ItemHeadData[0] is not None:
                        p.drawString(lftcol, itemy, "IN HAWB/HUCR/HBL                             OUT HAWB/HUCR/HBL                 ")
                        itemy -= 10
                    
                    p.drawString(lftcol, itemy, "PACKING/GOODS DESCRIPTION                    HS QUANTITY & UNIT               ")
                    itemy -= 10

                    p.drawString(lftcol, itemy, "                                             CIF/FOB VALUE (S$)               ")
                    itemy -= 10

                    self.cursor.execute(f"SELECT sum(LSPValue) FROM InNonItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '' ")
                    LspData = self.cursor.fetchone()

                    if str(LspData[0]) != str("0.00"):
                        p.drawString(lftcol, itemy, "                                             LSP VALUE (S$)                   ")
                        itemy -= 10

                    p.drawString(lftcol, itemy, "                                             GST AMOUNT (S$)                  ")
                    itemy -= 10

                    self.cursor.execute(f"SELECT count(DutiableUOM),sum(DutiableQty),sum(UnitPrice),sum(ExciseDutyRate),sum(CustomsDutyAmount) FROM InNonItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '--Select--' ")
                    DutyUom = self.cursor.fetchone()

                    if  DutyUom[0] is not None and Decimal(DutyUom[1]) != Decimal("0.0000"):
                        p.drawString(lftcol, itemy, "                                             DUT QTY/WT/VOL & UNIT            ")
                        itemy -= 10

                    if Decimal(DutyUom[2] != Decimal("0.00")):
                        p.drawString(lftcol, itemy, "                                             UNIT PRICE & CODE                 ")
                        itemy -= 10

                    if Decimal(DutyUom[3] != Decimal("0.00")):
                        p.drawString(lftcol, itemy, "                                             EXCISE DUTY PAYABLE (S$)          ")
                        itemy -= 10

                    if Decimal(DutyUom[4] != Decimal("0.00")):
                        p.drawString(lftcol, itemy, "                                             CUSTOMS DUTY PAYABLE(S$)          ")
                        itemy -= 10

                    p.drawString(snox, itemy, "MANUFACTURER'S NAME ")
                    itemy -= 10
                    p.drawString( snox, itemy, '-------------------------------------------------------------------------------')
                    itemy -= 10
                    p.drawString(lftcol, 50,  "--------------------------------------------------------------------------------")
                    p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format(str(DeclarData[0]).upper(), str(PermitValues['MSGId'][:8]).upper(), str(PermitValues['MSGId'][8:]).upper()))

                return itemy
            
            def Cascfunction(Item,CascId,Sno,itemy):
                self.cursor.execute(f"SELECT ProductCode,Quantity,ProductUOM FROM INNONCASCDtl WHERE ItemNo = '{Item['ItemNo']}' AND PermitId = '{Item['PermitId']}' AND CascId = '{CascId}' ")
                CascData = self.cursor.fetchone()
                if CascData is not None:
                    p.drawString(lftcol, itemy,  "--------------------------------------------------------------------------------")
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, 'S/NO')
                    p.drawString(lftcol+70, itemy, 'CA/SC PRODUCT CODE ')
                    p.drawString(lftcol+280, itemy, 'CA/SC PRODUCT QTY & UNIT')
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, '   {}'.format(Sno))
                    p.drawString(lftcol+70, itemy, str(CascData[0]).upper())
                    if str(CascData[1]) != "0.0000":
                        p.drawString(lftcol+280, itemy, ('{:10d}.{} {}').format(int(CascData[1]), str(CascData[1]).split(".")[1], CascData[2]))
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy,  "--------------------------------------------------------------------------------")

                return itemy

            itemy = itemyF(itemy)
            self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitValues['PermitId']))
            self.item = self.cursor.fetchall()
            ItemValues = (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records')
            
            for Item in ItemValues:
                p.drawString(lftcol, itemy, f"{'%02d' % Item['ItemNo']}     {Item['HSCode']}      {Item['CurrentLot']}         {Item['PreviousLot']}                ")
                itemy = itemyF(itemy)

                if Item['Making'] != "--Select--":
                    p.drawString(makingx, itemy, (str(Item['Making'])[:2]).upper())
                p.drawString(cityx-40, itemy, str(Item['Contry']).upper())
                p.drawString(brandx-105, itemy, str(Item['Brand']).upper())
                p.drawString(prviousx, itemy, str(Item['Model']).upper())
                itemy = itemyF(itemy)

                if Item["InHAWBOBL"] != '':
                    p.drawString(lftcol, itemy, str(Item['InHAWBOBL']).upper())
                    itemy = itemyF(itemy)

                DescriptionItem = Item['Description']

                DescX = lftcol
                Dcount = 1
                HSQtyName = True
                CiFob = True
                Lsp = True
                GstAmd = True
                TotDutiable = True
                ExciseAmd = True
                CustomDuty = True
                OtherDuty = True
                for D in range(len(DescriptionItem)):
                    if DescriptionItem[D] != "\n":
                        p.drawString(DescX, itemy, DescriptionItem[D])
                    DescX +=6
                    if "\n" == DescriptionItem[D]:
                        DescX = lftcol
                        itemy = itemyF(itemy)
                        Dcount += 1
                    if (D+1) % 50 == 0 : 
                        DescX = lftcol
                        itemy = itemyF(itemy)
                        Dcount += 1

                    if Dcount == 1 and HSQtyName:
                        p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(Item['HSQty']), str(Item['HSQty']).split(".")[1], Item['HSUOM']))
                        HSQtyName = False

                    if Dcount == 2 and CiFob:
                        p.drawString(prviousx+100, itemy, ('{:10d}.{}').format( int(Item['CIFFOB']), str(Item['CIFFOB']).split(".")[1]))
                        CiFob = False

                    if Dcount == 3 and Lsp:
                        Dcount += 1 
                        if Decimal(Item['LSPValue']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['LSPValue']), str(Item['LSPValue']).split(".")[1]))
                            Lsp = False
                    if Dcount == 4 and GstAmd:
                        p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['GSTAmount']), str(Item['GSTAmount']).split(".")[1]))
                        GstAmd = False

                    if Dcount == 5 and TotDutiable:
                        Dcount += 1 
                        if Decimal(Item['TotalDutiableQty']) != Decimal("0.0000"):
                            p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(Item['TotalDutiableQty']), str( Item['TotalDutiableQty']).split(".")[1], Item['TotalDutiableUOM']))
                            TotDutiable = False

                    if Dcount == 6 and ExciseAmd:
                        Dcount += 1 
                        if Decimal(Item['ExciseDutyAmount']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['ExciseDutyAmount']), str(Item['ExciseDutyAmount']).split(".")[1]))
                            ExciseAmd = False
                    
                    if Dcount == 7 and CustomDuty:
                        Dcount += 1
                        if Decimal(Item['CustomsDutyAmount']) != Decimal("0.00"): 
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['CustomsDutyAmount']), str(Item['CustomsDutyAmount']).split(".")[1]))

                    if Dcount == 8 and OtherDuty:
                        Dcount += 1
                        if Decimal(Item['OtherTaxAmount']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['OtherTaxAmount']), str(Item['OtherTaxAmount']).split(".")[1]))
                            OtherDuty = False
                else:
                    if Dcount <= 1:
                        p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(Item['HSQty']), str(Item['HSQty']).split(".")[1], Item['HSUOM']))
                        itemy = itemyF(itemy)
                    if Dcount <= 2:
                        p.drawString(prviousx+100, itemy, ('{:10d}.{}').format( int(Item['CIFFOB']), str(Item['CIFFOB']).split(".")[1]))
                        itemy = itemyF(itemy)

                    if Dcount <= 3:
                        if Decimal(Item['LSPValue']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['LSPValue']), str(Item['LSPValue']).split(".")[1]))
                            itemy = itemyF(itemy)

                    if Dcount <= 4:
                        p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['GSTAmount']), str(Item['GSTAmount']).split(".")[1]))
                        itemy = itemyF(itemy)

                    if Dcount <= 5:
                        if Decimal(Item['TotalDutiableQty']) != Decimal("0.0000"):
                            p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(Item['TotalDutiableQty']), str( Item['TotalDutiableQty']).split(".")[1], Item['TotalDutiableUOM']))
                            itemy = itemyF(itemy)

                    if Dcount <= 6:
                        if Decimal(Item['ExciseDutyAmount']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['ExciseDutyAmount']), str(Item['ExciseDutyAmount']).split(".")[1]))
                            itemy = itemyF(itemy)

                    if Dcount <= 7:
                        if Decimal(Item['CustomsDutyAmount']) != Decimal("0.00"): 
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['CustomsDutyAmount']), str(Item['CustomsDutyAmount']).split(".")[1]))
                            itemy = itemyF(itemy)

                    if Dcount <= 8:
                        if Decimal(Item['OtherTaxAmount']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['OtherTaxAmount']), str(Item['OtherTaxAmount']).split(".")[1]))
                            itemy = itemyF(itemy)

                self.cursor.execute(f"SELECT SupplierCode FROM InNonInvoiceDtl WHERE PermitId = '{Item['PermitId']}' AND InvoiceNo = '{Item['InvoiceNo']}' ")
                InvoiceData = self.cursor.fetchone()
                if InvoiceData != "":
                    self.cursor.execute(f"SELECT Name,Name1 FROM INNONSUPPLIERMANUFACTURERPARTY WHERE code = '{InvoiceData[0]}' ")
                    SupplyData = self.cursor.fetchone()
                    if SupplyData is not None:
                        SupplyData = (str(SupplyData[0]) + str(SupplyData[1])).upper()
                        p.drawString(lftcol, itemy, (SupplyData)[:50])
                        itemy = itemyF(itemy)
                        if len(SupplyData) >= 50:
                            p.drawString(lftcol, itemy, (SupplyData)[50:])
                            itemy = itemyF(itemy)

                self.cursor.execute(f"SELECT * FROM INNONCASCDtl WHERE ItemNo = '{Item['ItemNo']}' AND PermitId = '{Item['PermitId']}'")
                CascCheck = self.cursor.fetchall()

                if len(CascCheck) != 0:
                    itemy = Cascfunction(Item,'Casc1',"01",itemy)
                    itemy = Cascfunction(Item,'Casc2',"02",itemy)
                    itemy = Cascfunction(Item,'Casc3',"03",itemy)
                    itemy = Cascfunction(Item,'Casc4',"04",itemy)
                    itemy = Cascfunction(Item,'Casc5',"05",itemy)

                if str(Item['Enginecapacity']) != str("0.00") and str(Item['Enginecapacity']) != "":
                    p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, 'S/NO')
                    p.drawString(lftcol+70, itemy, 'ENGINE NO/CHASSIS NO ')
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, ("   {}").format("%02d" % Item['ItemNo']))
                    p.drawString(lftcol+70, itemy, str(Item['Enginecapacity']))
                    itemy = itemyF(itemy)
                    p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                
                p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                itemy = itemyF(itemy)-20
                p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                itemy = itemyF(itemy)

            def itemyF1(itemy):
                if itemy <= 60:
                    itemy = 820
                    p.showPage()
                    p.setFont('Courier', 10)
                else:
                    itemy -= 10
                if itemy <= 820 and itemy >= 780:
                    p.setFont('Courier', 10)
                    p.drawString(rgtcol, itemy, "CARGO CLEARANCE PERMIT ")
                    p.drawString(460, itemy, ("PG : {} OF").format(self.countPage))
                    self.countPage += 1
                    itemy -= 10
                    p.drawString(lftcol, itemy, "PERMIT NO : "+PermitBar)
                    p.drawString(rgtcol, itemy, "======================")
                    itemy -= 10
                    p.drawString(rgtcol, itemy, "(CONTINUATION PAGE)")
                    itemy -= 20
                    p.drawString(lftcol, itemy, "CONSIGNMENT DETAILS")
                    itemy -= 10
                    p.drawString(lftcol, itemy, "--------------------------------------------------------------------------------")
                    itemy -= 10
                    p.drawString(lftcol, 50,  "--------------------------------------------------------------------------------")
                    p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format((DeclarData[0]).upper(), str(PermitValues['MSGId'][:8]).upper(), str(PermitValues['MSGId'][8:]).upper()))
                return itemy
            
            TradeRemark = str(PermitValues['TradeRemarks']).upper()
            TradeX = lftcol
            for Tr in range(len(TradeRemark)):
                if TradeRemark[Tr] != "\n":
                    p.drawString(TradeX, itemy, TradeRemark[Tr])
                TradeX += 6
                if (Tr + 1) % 80 == 0 or TradeRemark[Tr] == "\n":
                    TradeX = lftcol
                    itemy = itemyF1(itemy)

            else:itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")

            self.cursor.execute(f"SELECT RowNo,ContainerNo,size,weight,SealNo FROM InnonContainerDtl WHERE PermitId = '{PermitValues['PermitId']}' ")
            ContainerData = self.cursor.fetchall()

            if len(ContainerData) != 0:
                itemy = itemyF1(itemy)
                p.drawString(lftcol, itemy, "CONTAINER IDENTIFIERS")
                itemy = itemyF1(itemy)
                for Cont in ContainerData:
                    p.drawString(lftcol, itemy, ("   {})").format("%02d" % Cont[0]))
                    p.drawString(lftcol+50, itemy, str(Cont[1]).upper())
                    p.drawString(lftcol+130, itemy, ("{}  {}").format(Cont[2][:3], Cont[2][3:5]))
                    p.drawString(lftcol+200, itemy, (str(Cont[3]))[:3])
                    p.drawString(lftcol+240, itemy, str(Cont[4]))
                    itemy = itemyF1(itemy)
            
            p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "NO UNAUTHORISED ADDITION/AMENDMENT TO THIS PERMIT MAY BE MADE AFTER APPROVAL")
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "NAME OF COMPANY:")
            Declarant = "SELECT name,DeclarantName,DeclarantCode,DeclarantTel FROM DeclarantCompany where tradenetmailboxId=%s"
            self.cursor.execute(Declarant,(PermitValues['TradeNetMailboxID'],))
            DeclarData = self.cursor.fetchone()
            p.drawString(lftcol+110, itemy, (DeclarData[0])[:67])
            itemy = itemyF1(itemy)
            p.drawString(lftcol+110, itemy, (DeclarData[0])[67:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "DECLARANT NAME :")
            p.drawString(lftcol+110, itemy, (DeclarData[1])[:67])
            itemy = itemyF1(itemy)
            p.drawString(lftcol+110, itemy, (DeclarData[1])[67:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "DECLARANT CODE :")
            p.drawString(lftcol+110, itemy, "XXXX"+(DeclarData[2])[-5:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "TEL NO         : ")
            p.drawString(lftcol+110, itemy, (DeclarData[3]))
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "CONTROLLING AGENCY/CUSTOMS CONDITIONS ")
            itemy = itemyF1(itemy)

            if PermitValues['prmtStatus'] == "AMD":
                self.cursor.execute(f"SELECT Conditioncode,ConditionDescription FROM InnonAMDPMT WHERE PermitNumber = '{PermitValues['PermitNumber']}' AND MsgId = '{PermitValues['MSGId']}' ORDER BY SNO")
            else:
                self.cursor.execute(f"SELECT Conditioncode,ConditionDescription FROM InnonPMT WHERE PermitNumber = '{PermitValues['PermitNumber']}' ORDER BY SNO")
            ControllingData = self.cursor.fetchall()

            for Control in ControllingData:
                p.setFont('Courier-Bold', 10)
                p.drawString(lftcol, itemy, Control[0])
                p.drawString(lftcol+30, itemy, "-")
                p.setFont('Courier', 10)

                p.drawString(lftcol+40, itemy, (Control[1])[:73])
                itemy = itemyF1(itemy)
                if len((Control[1])) > 73:
                    p.drawString(lftcol, itemy, (Control[1])[73:153])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 153:
                    p.drawString(lftcol, itemy, (Control[1])[153:233])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 233:
                    p.drawString(lftcol, itemy, (Control[1])[233:313])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 313:
                    p.drawString(lftcol, itemy, (Control[1])[313:393])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 393:
                    p.drawString(lftcol, itemy, (Control[1])[393:473])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 473:
                    p.drawString(lftcol, itemy, (Control[1])[473:])
                    itemy = itemyF1(itemy)
            p.save()
            existing_pdf = PdfFileReader(open(OldFilename, "rb"))
            output = PdfFileWriter()

            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(595, 841))
            can.setFont('Courier', 10)
            can.drawString(520, 700, str(len(existing_pdf.pages)))
            can.showPage()
            can.setFont('Courier', 10)
            can.drawString(520, 810, str(len(existing_pdf.pages)))
            can.showPage()
            can.setFont('Courier', 10)
            can.drawString(520, 820, str(len(existing_pdf.pages)))
            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            for i in range(len(existing_pdf.pages)):
                if i == 0:
                    page = existing_pdf.pages[i]
                    page.merge_page(new_pdf.pages[0])
                elif i == 1:
                    page = existing_pdf.pages[i]
                    page.merge_page(new_pdf.pages[1])
                else:
                    page = existing_pdf.pages[i]
                    page.merge_page(new_pdf.pages[2])
                output.add_page(page)
            
            NewFilename = f"D:/Users/Public/PDFFilesKtt/{PermitBar}.pdf"
            output_stream = open(NewFilename, "wb")
            output.write(output_stream)
            output_stream.close()

            if os.path.exists(OldFilename):
                os.remove(OldFilename)

            if len(Data.split(",")) ==1:
                with open(NewFilename, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                response = HttpResponse(pdf_data, content_type='application/pdf')
                response['Content-Disposition'] = f"attachment; filename={PermitValues['PermitNumber']}.pdf"
                return response
            else:
                pdfFiles.append(NewFilename)
        
        pdfWriter = PdfFileWriter()

        for file in pdfFiles:
            pdfFile = open(file, 'rb')
            pdfReader = PdfFileReader(pdfFile)

            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                pdfWriter.addPage(pageObj)

        MergeFiles = 'D:/Users/Public/PDFFilesKtt/MergedFiles.pdf'
        pdfOutputFile = open(MergeFiles, 'wb')
        pdfWriter.write(pdfOutputFile)

        pdfOutputFile.close()
        pdfFile.close()

        with open(MergeFiles, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="InpayMultiply.pdf"'
        return response
    
class PrintGstInNon(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,ID):
        self.cursor.execute("SELECT Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime FROM InNonHeaderTbl WHERE Id = '{}' ".format(ID))
        Inheader = (pd.DataFrame(list(self.cursor.fetchall()), columns=['Refid','JobId','MSGId','PermitId','TradeNetMailboxID','MessageType','DeclarationType','PreviousPermit','CargoPackType','InwardTransportMode','OutwardTransportMode','BGIndicator','SupplyIndicator','ReferenceDocuments','License','Recipient','DeclarantCompanyCode','ImporterCompanyCode','ExporterCompanyCode','InwardCarrierAgentCode','OutwardCarrierAgentCode','ConsigneeCode','FreightForwarderCode','ClaimantPartyCode','ArrivalDate','LoadingPortCode','VoyageNumber','VesselName','OceanBillofLadingNo','ConveyanceRefNo','TransportId','FlightNO','AircraftRegNo','MasterAirwayBill','ReleaseLocation','RecepitLocation','RecepilocaName','StorageLocation','ExhibitionSDate','ExhibitionEDate','BlanketStartDate','TradeRemarks','InternalRemarks','CustomerRemarks','DepartureDate','DischargePort','FinalDestinationCountry','OutVoyageNumber','OutVesselName','OutOceanBillofLadingNo','VesselType','VesselNetRegTon','VesselNationality','TowingVesselID','TowingVesselName','NextPort','LastPort','OutConveyanceRefNo','OutTransportId','OutFlightNO','OutAircraftRegNo','OutMasterAirwayBill','TotalOuterPack','TotalOuterPackUOM','TotalGrossWeight','TotalGrossWeightUOM','GrossReference','DeclareIndicator','NumberOfItems','TotalCIFFOBValue','TotalGSTTaxAmt','TotalExDutyAmt','TotalCusDutyAmt','TotalODutyAmt','TotalAmtPay','Status','TouchUser','TouchTime','PermitNumber','prmtStatus','ReleaseLocaName','Inhabl','outhbl','seastore','Cnb','DeclarningFor','MRDate','MRTime']).to_dict('records'))[0]
        
        self.cursor.execute("SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime FROM InNonInvoiceDtl WHERE PermitId = '{}' ORDER BY SNO ".format(Inheader['PermitId']))
        InvoiceData = (pd.DataFrame(list(self.cursor.fetchall()), columns=['SNo' , 'InvoiceNo' , 'InvoiceDate' , 'TermType' , 'AdValoremIndicator' , 'PreDutyRateIndicator' , 'SupplierImporterRelationship' , 'SupplierCode' , 'ImportPartyCode' , 'TICurrency' , 'TIExRate' , 'TIAmount' , 'TISAmount' , 'OTCCharge' , 'OTCCurrency' , 'OTCExRate' , 'OTCAmount' , 'OTCSAmount' , 'FCCharge' , 'FCCurrency' , 'FCExRate' , 'FCAmount' , 'FCSAmount' , 'ICCharge' , 'ICCurrency' , 'ICExRate' , 'ICAmount' , 'ICSAmount' , 'CIFSUMAmount' , 'GSTPercentage' , 'GSTSUMAmount' , 'MessageType' , 'PermitId' , 'TouchUser' , 'TouchTime'])).to_dict('records')
        
        self.cursor.execute(f"SELECT Name,Cruei FROM InNonImporter  WHERE code = '{InvoiceData[0]['ImportPartyCode']}' ")
        Import = self.cursor.fetchone()

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(595, 841))

        can.setFont('Times-Bold', 9)
        x = 10
        y = 820
        can.drawString(200, y, "GOODS AND SERVICE TAX (GST) - CALCULATION SHEET")
        y -= 20
        can.drawString(x, y, "COMPANY NAME:")
        can.drawString(x+440, y, "JOB NUMBER:")
        y -= 15
        can.drawString(x, y, "COMPANY UEN:")
        can.drawString(x+440, y, "JOB CREATED:")
        y -= 15
        can.drawString(x, y, "PERMIT NUMBER:")
        can.drawString(x+440, y, "MESSAGE ID:")

        can.setFont('Times-Roman', 9)
        x = 100
        y = 820
        y -= 20
        can.drawString(x, y, Import[0])
        can.drawString(x+420, y, Inheader['JobId'])
        y -= 15
        can.drawString(x, y, Import[1])
        can.drawString(
            x+410, y, (Inheader['TouchTime']).strftime("%d/%m/%Y  %H:%M:%S"))
        y -= 15
        can.drawString(x, y, Inheader['PermitNumber'])
        can.drawString(x+420, y, Inheader['MSGId'])
        x = 10
        for invoiceD in InvoiceData:
            can.setFont('Times-Bold', 9)
            y -= 25
            can.drawString(x, y, "-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            y -= 15
            can.drawString(x, y, "INVOICE NUMBER:")
            y -= 15
            can.drawString(x, y, "INVOICE TERM:")
            can.setFont('Times-Roman', 9)
            y -= 15
            can.drawString(x+100, y+30, invoiceD['InvoiceNo'])
            y -= 15
            can.drawString(x+80, y+30, invoiceD['TermType'])

            rejectStatus = [['SNO', 'ITEM', "CURRENCY","EXCHG. RATE", "PERC.", "AMOUNT", "AMOUNT (SGD)"]]
            rejectStatus.append(["1", 'TOTAL INVOICE', ((invoiceD['TICurrency']) if '--Select--' != (invoiceD['TICurrency']) else ""), invoiceD['TIExRate'], "", invoiceD['TIAmount'], invoiceD['TISAmount']])

            rejectStatus.append(["2", 'FREIGHT CHARGES', ((invoiceD['FCCurrency']) if '--Select--' != (invoiceD['FCCurrency'])else ""), invoiceD['FCExRate'], invoiceD['FCCharge'], invoiceD['FCAmount'], invoiceD['FCSAmount']])

            rejectStatus.append(["3", 'INSURANCE', ((invoiceD['ICCurrency']) if '--Select--' != (invoiceD['ICCurrency'])else ""), invoiceD['ICExRate'], invoiceD['ICCharge'], invoiceD['ICAmount'], invoiceD['ICSAmount']])

            rejectStatus.append(["4", 'OTHER CHARGES', ((invoiceD['OTCCurrency']) if '--Select--' != (invoiceD['OTCCurrency'])else ""), invoiceD['OTCExRate'], invoiceD['OTCCharge'], invoiceD['OTCAmount'], invoiceD['OTCSAmount']])

            rejectStatus.append(["5", 'CUSTOMS VALUE', "", "","", "", invoiceD['CIFSUMAmount']])

            rejectStatus.append(["6", 'GST', "", "", invoiceD['GSTPercentage'], "", invoiceD['GSTSUMAmount']])

            col_widths = [80, 90, 80, 80, 80, 80]
            table = Table(rejectStatus, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('COLWIDTHS', (2, -1), (-1, -1), 102),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('SPLITLONGWORDS', (0, 0), (-1, -1), 1),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            table.wrapOn(can, 0, 0)
            table.drawOn(can, 10, y-120)
            y -= 120

        can.save()
        packet.seek(0)
        response = HttpResponse(packet, content_type='application/pdf')
        Per = Inheader['PermitNumber']
        response['Content-Disposition'] = f'attachment; filename="{Per}_GST.pdf"'
        return response
    
class InNonDelHblHawb(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,PermitId):

        self.cursor.execute("update InNonItemDtl  set InHAWBOBL='',OutHAWBOBL=''  where  MessageType='INPDEC' AND PermitId='" + PermitId + "' ")
        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitId))
        self.item = self.cursor.fetchall()

        return JsonResponse({
            "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records'),
        }) 

class XmlGen(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self) 

    def get(self,request):
        for Id in json.loads(request.GET.get("my_data")):

            self.cursor.execute("Select prmtStatus,TradeNetMailboxID,PermitId,MSGId from InNonHeaderTbl where Id='" + Id + "' and Status!='DEL'")

            Data = self.cursor.fetchone()
            PermitId = Data[2]
            self.prmtStatus = Data[0]
            if self.prmtStatus == "CNL":
                self.CnlExml(PermitId)
            else:
                self.NewXml(PermitId)

        return JsonResponse({"Data":"Genarated"})
    

    def indent(self,elem, level=0):
        i = "\n" + level*"  "
        j = "\n" + (level-1)*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem
    
    def NewXml(self,PermitId):
        self.cursor.execute("SELECT Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime FROM InNonHeaderTbl WHERE PermitId = '{}' ".format(PermitId))
        InNonHeaderData = self.cursor.fetchall()

        PermitValues = (pd.DataFrame(list(InNonHeaderData), columns=['Refid','JobId','MSGId','PermitId','TradeNetMailboxID','MessageType','DeclarationType','PreviousPermit','CargoPackType','InwardTransportMode','OutwardTransportMode','BGIndicator','SupplyIndicator','ReferenceDocuments','License','Recipient','DeclarantCompanyCode','ImporterCompanyCode','ExporterCompanyCode','InwardCarrierAgentCode','OutwardCarrierAgentCode','ConsigneeCode','FreightForwarderCode','ClaimantPartyCode','ArrivalDate','LoadingPortCode','VoyageNumber','VesselName','OceanBillofLadingNo','ConveyanceRefNo','TransportId','FlightNO','AircraftRegNo','MasterAirwayBill','ReleaseLocation','RecepitLocation','RecepilocaName','StorageLocation','ExhibitionSDate','ExhibitionEDate','BlanketStartDate','TradeRemarks','InternalRemarks','CustomerRemarks','DepartureDate','DischargePort','FinalDestinationCountry','OutVoyageNumber','OutVesselName','OutOceanBillofLadingNo','VesselType','VesselNetRegTon','VesselNationality','TowingVesselID','TowingVesselName','NextPort','LastPort','OutConveyanceRefNo','OutTransportId','OutFlightNO','OutAircraftRegNo','OutMasterAirwayBill','TotalOuterPack','TotalOuterPackUOM','TotalGrossWeight','TotalGrossWeightUOM','GrossReference','DeclareIndicator','NumberOfItems','TotalCIFFOBValue','TotalGSTTaxAmt','TotalExDutyAmt','TotalCusDutyAmt','TotalODutyAmt','TotalAmtPay','Status','TouchUser','TouchTime','PermitNumber','prmtStatus','ReleaseLocaName','Inhabl','outhbl','seastore','Cnb','DeclarningFor','MRDate','MRTime']).to_dict('records'))[0]
        
        Root = ET.Element("TradenetDeclaration",{
            'xmlns:cbc' : "urn:crimsonlogic:tn:schema:xsd:CommonBasicComponents-2",
            'xmlns:cac' : "urn:crimsonlogic:tn:schema:xsd:CommonAggregateComponents-2",
            'xmlns:inp' : "urn:crimsonlogic:tn:schema:xsd:InNonPayment",
            'xmlns:ipt' : "urn:crimsonlogic:tn:schema:xsd:InPayment",
            'xmlns:out' : "urn:crimsonlogic:tn:schema:xsd:OutwardDeclaration",
            'xmlns:tnp' : "urn:crimsonlogic:tn:schema:xsd:TranshipmentMovement",
            'xmlns:coo' : "urn:crimsonlogic:tn:schema:xsd:CertificateOfOrigin",
            'xmlns' : "urn:crimsonlogic:tn:schema:xsd:TradenetDeclaration",
            'dateTime' : datetime.now().strftime("%Y%m%d%H%M"),
            'instanceIdentifier' : PermitValues['JobId']
            })
        
        ET.SubElement(Root,'cbc:MessageVersion').text = "041"

        ET.SubElement(Root,'cbc:SenderID').text =  PermitValues['TradeNetMailboxID'].upper()

        if (PermitValues['TradeNetMailboxID'].split("."))[1] != "QXMF004" :
            ET.SubElement(Root,'cbc:RecipientID').text =  "DCS4.DCS4001"
        else:
            ET.SubElement(Root,'cbc:RecipientID').text =  "DCST.DCST401"

        ET.SubElement(Root,'cbc:TotalNumberOfDeclaration').text =  "1"

        InboundMsg = ET.SubElement(Root,"InboundMessage")

        if self.prmtStatus == "AME":

            self.cursor.execute(f"select Count(PermitNumber) from InNonHeaderTbl where PermitId='" + PermitValues['PermitId'] + "' and (Status='APR' or Status='AME') and prmtStatus='AMD'")
            AMendData = self.cursor.fetchone()

            self.cursor.execute("select UpdateIndicator,Permitno,PermitExtension,DescriptionOfReason from InNonAmend where Permitno='" + PermitValues["PermitNumber"] + "' and MSGId='" + PermitValues["MSGId"] + "'")
            AmdData = self.cursor.fetchone()

            InNonPayment = ET.SubElement(InboundMsg,"inp:InNonPaymentUpdate")
            AmdUpd = ET.SubElement(InNonPayment,"cac:Update")
            ET.SubElement(AmdUpd,'cbc:UpdateIndicatorCode').text =  str(AmdData[0]).upper()
            ET.SubElement(AmdUpd,'cbc:UpdateRequestNumber').text =  str(int(AMendData[0])+1).upper()
            ET.SubElement(AmdUpd,'cbc:UpdatePermitNumber').text =  str(AmdData[1]).upper()

            Amendment = ET.SubElement(AmdUpd,'cac:Amendment')
            ET.SubElement(Amendment,'cbc:PermitValidityExtensionIndicator').text =  str(AmdData[2]).upper()
            ET.SubElement(Amendment,'cbc:AmendmentReason').text =  str(AmdData[3]).upper()

        else:
            InNonPayment = ET.SubElement(InboundMsg,"inp:InNonPayment")

        Header = ET.SubElement(InNonPayment,"inp:Header")

        ET.SubElement(Header,'cbc:MessageReference').text =  PermitValues['MSGId'].upper()
        Uniq = ET.SubElement(Header,'cac:UniqueReferenceNumber')

        self.cursor.execute(f"SELECT cruei,DeclarantCode,DeclarantName,DeclarantTel,Name,Name1 FROM DeclarantCompany WHERE tradenetmailboxId = '{PermitValues['TradeNetMailboxID']}' ")
        DeclarData = self.cursor.fetchone()
        ET.SubElement(Uniq,'cbc:ID').text =  DeclarData[0]
        ET.SubElement(Uniq,'cbc:Date').text =  PermitValues['MSGId'][:8]
        ET.SubElement(Uniq,'cbc:SequenceNumeric').text =  PermitValues['MSGId'][-4:]

        ET.SubElement(Header,'cbc:DeclarantID').text =  PermitValues['TradeNetMailboxID'].upper()
        ET.SubElement(Header,'cbc:CommonAccessReference').text =  PermitValues['MessageType'].upper()
        ET.SubElement(Header,'cbc:DeclarationType').text =  PermitValues['DeclarationType'][:3].upper()
        ET.SubElement(Header,'cbc:DeclarationIndicator').text =  PermitValues['DeclareIndicator'].upper()

        if PermitValues['PreviousPermit'] != "":
            ET.SubElement(Header,'cbc:PreviousPermitNumber').text =  PermitValues['DeclareIndicator'].upper()

        if len(PermitValues['TradeRemarks']) > 512:
            Trade = ET.SubElement(Header,'cac:Remarks')
            ET.SubElement(Trade,'cbc:FreeText').text =  (PermitValues['TradeRemarks'].upper())[:512]
            ET.SubElement(Trade,'cbc:FreeText').text =  (PermitValues['TradeRemarks'].upper())[512:]
        elif len(PermitValues['TradeRemarks']) <= 512:
            Trade = ET.SubElement(Header,'cac:Remarks')
            ET.SubElement(Trade,'cbc:FreeText').text =  PermitValues['TradeRemarks'].upper()
        
        if PermitValues['BGIndicator'].upper() != "--Select--":
            ET.SubElement(Header,'cbc:BankerGuaranteeCode').text =  PermitValues['BGIndicator'][:1].upper()

        
        Cargo = ET.SubElement(InNonPayment,"inp:Cargo")
        ET.SubElement(Cargo,'cbc:CargoPackingType').text =  PermitValues['CargoPackType'][:1].upper()

        Rlease = ET.SubElement(Cargo,"cac:ReleaseLocation")
        ET.SubElement(Rlease,'cbc:LocationCode').text =  PermitValues['ReleaseLocation'].upper()
        ET.SubElement(Rlease,'cbc:LocationName').text =  PermitValues['ReleaseLocaName'].upper()

        Recipt = ET.SubElement(Cargo,"cac:ReceiptLocation")
        ET.SubElement(Recipt,'cbc:LocationCode').text =  PermitValues['RecepitLocation'].upper()
        ET.SubElement(Recipt,'cbc:LocationName').text =  PermitValues['RecepilocaName'].upper()

        if PermitValues['StorageLocation'] != "":
            Recipt = ET.SubElement(Cargo,"cac:StorageLocation")
            ET.SubElement(Recipt,'cbc:LocationCode').text =  PermitValues['StorageLocation'].upper()
            self.cursor.execute(f"SELECT description FROM StorageLocation WHERE StorageCode = '{PermitValues['StorageLocation']}' ")
            ET.SubElement(Recipt,'cbc:LocationName').text =  self.cursor.fetchone()[0].upper()

        if PermitValues['CargoPackType'][:1] == "9":
            self.cursor.execute("select RowNo,ContainerNo,Size,Weight,SealNo from InnonContainerDtl where PermitID='" + PermitId + "' ORDER BY RowNo")
            Container = self.cursor.fetchall()

            for Cn in Container:
                Contain = ET.SubElement(Cargo,"cac:TransportEquipment")
                ET.SubElement(Contain,'cbc:SequenceNumeric').text =  str(Cn[0])
                ET.SubElement(Contain,'cbc:EquipmentID').text =  str(Cn[1]).upper()
                ET.SubElement(Contain,'cbc:SizeTypeCode').text =  str(Cn[2])[:5]
                ET.SubElement(Contain,'cbc:EquipmentWeightMeasureNumeric').text =  str(Cn[3]).upper()
                Trans = ET.SubElement(Contain,"cac:TransportEquipmentSeal")
                ET.SubElement(Trans,'cbc:SealID').text =  str(Cn[4]).upper()
        
        if PermitValues['SupplyIndicator'] == "True" or PermitValues['SupplyIndicator'] == "true":
            ET.SubElement(Cargo,'cbc:SealID').text =  str(Cn[4])

        if str(PermitValues['BlanketStartDate']) != "1900-01-01 00:00:00" and PermitValues['BlanketStartDate'] != "":
            ET.SubElement(Cargo,'cbc:BlanketStartDate').text =  str(PermitValues['BlanketStartDate'].strftime('%Y%m%d'))

        #---------------------------------------Ipt-----------------------------#
        TransPort = ET.SubElement(InNonPayment,"inp:Transport")
        if PermitValues['InwardTransportMode'] != "--Select--" and PermitValues['InwardTransportMode'][0] != "N":
            
            InWardTransPort = ET.SubElement(TransPort,"cac:InwardTransport")
            InWardTransPortMeans = ET.SubElement(InWardTransPort,"cac:TransportMeans")
            InWardTransPortMeansMode = ET.SubElement(InWardTransPortMeans,"cac:TransportMode")
            ET.SubElement(InWardTransPortMeansMode,'cbc:ModeCode').text =  PermitValues['InwardTransportMode'][:1].upper()

            if PermitValues['InwardTransportMode'][:1] == "1":
                ET.SubElement(InWardTransPortMeansMode,'cbc:ConveyanceReferenceNumber').text =  PermitValues['VoyageNumber'].upper()
                ET.SubElement(InWardTransPortMeansMode,'cbc:TransportIdentifier').text =  PermitValues['VesselName'].upper()
                if PermitValues['OceanBillofLadingNo'] != "":
                    ET.SubElement(InWardTransPortMeansMode,'cbc:MAWBOUCROBLNumber').text =  PermitValues['OceanBillofLadingNo'].upper()
            elif PermitValues['InwardTransportMode'][:1] == "4":
                ET.SubElement(InWardTransPortMeansMode,'cbc:ConveyanceReferenceNumber').text =  PermitValues['FlightNO'].upper()
                if PermitValues['InwardTransportMode'] != "":
                    ET.SubElement(InWardTransPortMeans,'cbc:MAWBOUCROBLNumber').text =  PermitValues['MasterAirwayBill'].upper()
            else:
                ET.SubElement(InWardTransPortMeansMode,'cbc:ConveyanceReferenceNumber').text =  PermitValues['ConveyanceRefNo'].upper()
                if PermitValues['TransportId'] != "":
                    ET.SubElement(InWardTransPortMeansMode,'cbc:TransportIdentifier').text =  PermitValues['TransportId'].upper()

            if PermitValues['ArrivalDate'] != "" and str(PermitValues['ArrivalDate'].strftime("%Y-%m-%d") )!= "1900-01-01":
                ET.SubElement(InWardTransPort,'cbc:ArrivalDate').text =  str(PermitValues['ArrivalDate'].strftime('%Y%m%d')).upper()
            
            if PermitValues['LoadingPortCode'] != "":
                ET.SubElement(InWardTransPort,'cbc:LoadingPort').text =  str(PermitValues['LoadingPortCode']).upper()
                
        if PermitValues['OutwardTransportMode'] != "--Select--" and PermitValues['OutwardTransportMode'][0] != "N":
            OutWardTransPort = ET.SubElement(TransPort,"cac:OutwardTransport")
            OutWardTransPortMeans = ET.SubElement(OutWardTransPort,"cac:TransportMeans")
            OutWardTransPortMeansMode = ET.SubElement(OutWardTransPortMeans,"cac:TransportMode")
            ET.SubElement(OutWardTransPortMeansMode,'cbc:ModeCode').text =  PermitValues['OutwardTransportMode'][:1].upper()
            
            if PermitValues['OutwardTransportMode'][:1] == "1":
                ET.SubElement(OutWardTransPortMeansMode,'cbc:ConveyanceReferenceNumber').text =  PermitValues['OutVoyageNumber'].upper()
                ET.SubElement(OutWardTransPortMeansMode,'cbc:TransportIdentifier').text =  PermitValues['OutVesselName'].upper()
                if PermitValues['OutOceanBillofLadingNo'] != "":
                    ET.SubElement(OutWardTransPortMeans,'cbc:MAWBOUCROBLNumber').text =  PermitValues['OutOceanBillofLadingNo'].upper()
                
                if PermitValues['VesselType'] != "--Select--":
                    AddtionalVessel = ET.SubElement(OutWardTransPortMeans,"cac:AdditionalVesselInformation")
                    ET.SubElement(AddtionalVessel,'cbc:VesselType').text =  ((PermitValues['VesselType'].upper()).split(":")[0]).strip()
                
                    if PermitValues['VesselNetRegTon'] != "":
                        ET.SubElement(AddtionalVessel,'cbc:NetRegisterTonnage').text =  PermitValues['VesselNetRegTon'].upper()

                    if PermitValues['VesselNationality'] != "" and PermitValues['VesselNationality'] != "--Select--":
                        ET.SubElement(AddtionalVessel,'cbc:VesselNationality').text =  (PermitValues['VesselNationality'].split(':'))[0].upper()
                    
                    if PermitValues['TowingVesselID'] != "":
                    
                        TowlingOut = ET.SubElement(AddtionalVessel,"cac:TowingVessel")
                        ET.SubElement(TowlingOut,'cbc:VesselID').text =  (PermitValues['TowingVesselID']).upper()
                        ET.SubElement(TowlingOut,'cbc:VesselName').text =  (PermitValues['TowingVesselName']).upper()

                    if PermitValues['NextPort'] != "":
                        ET.SubElement(AddtionalVessel,'cbc:LoadingNextPort').text =  PermitValues['NextPort'].upper()

                    if PermitValues['LastPort'] != "":
                        ET.SubElement(AddtionalVessel,'cbc:LoadingFinalPort').text =  PermitValues['LastPort'].upper()
                

            elif PermitValues['OutwardTransportMode'][:1] == "4":
                ET.SubElement(OutWardTransPortMeansMode,'cbc:ConveyanceReferenceNumber').text =  PermitValues['OutFlightNO'].upper()
                if PermitValues['OutwardTransportMode'] != "":
                    ET.SubElement(OutWardTransPortMeans,'cbc:MAWBOUCROBLNumber').text =  PermitValues['OutMasterAirwayBill'].upper()
            else:
                if PermitValues['OutConveyanceRefNo'] !="":
                    ET.SubElement(OutWardTransPortMeansMode,'cbc:ConveyanceReferenceNumber').text =  PermitValues['OutConveyanceRefNo'].upper()

                if PermitValues['TransportId'] !="":
                    ET.SubElement(OutWardTransPortMeansMode,'cbc:TransportIdentifier').text =  PermitValues['TransportId'].upper()

            if PermitValues['DepartureDate'] != "" and PermitValues['DepartureDate'].strftime("%Y-%m-%d")!= "1900-01-01":
                ET.SubElement(OutWardTransPort,'cbc:DepartureDate').text =  str(PermitValues['DepartureDate'].strftime('%Y%m%d')).upper()
            
            if PermitValues['DischargePort'] != "":
                ET.SubElement(OutWardTransPort,'cbc:DischargePort').text =  str(PermitValues['DischargePort']).upper()

            if PermitValues['FinalDestinationCountry'] != "--Select--":
                ET.SubElement(OutWardTransPort,'cbc:FinalDestinationCountry').text =  (str(PermitValues['FinalDestinationCountry']).upper()).split(":")[0]

        Party = ET.SubElement(InNonPayment,"inp:Party")

        DecParty = ET.SubElement(Party,"cac:DeclarantParty") 
        DecPersonal = ET.SubElement(DecParty,"cac:PersonInformation")
        ET.SubElement(DecPersonal,'cbc:CodeValue').text =  str(DeclarData[1]).upper()
        ET.SubElement(DecPersonal,'cbc:Name').text =  str(DeclarData[2]).upper()
        ET.SubElement(DecParty,'cbc:Telephone').text =  str(DeclarData[3]).upper()

        DecAgentParty = ET.SubElement(Party,"cac:DeclaringAgentParty")
        DecPartyIden = ET.SubElement(DecAgentParty,"cac:PartyIdentification")
        ET.SubElement(DecPartyIden,'cbc:ID').text =  str(DeclarData[0]).upper()

        DecPartyName = ET.SubElement(DecAgentParty,"cac:PartyName")
        ET.SubElement(DecPartyName,'cbc:Name').text =  str(DeclarData[4]).upper()
        if DeclarData[5] != "":
            ET.SubElement(DecPartyName,'cbc:Name').text =  str(DeclarData[5]).upper()

        if PermitValues['FreightForwarderCode'] != "":
            self.cursor.execute(f"SELECT Cruei,Name,Name1 FROM FreightForwarder WHERE code = '{PermitValues['FreightForwarderCode']}' ")
            FrightData = self.cursor.fetchone()

            FrieghtParty = ET.SubElement(Party,"cac:FreightForwarderParty")
            FrightNotiFy = ET.SubElement(FrieghtParty,"cac:PartyIdentification")
            ET.SubElement(FrightNotiFy,'cbc:ID').text =  str(FrightData[0]).upper()

            FrightParty = ET.SubElement(FrieghtParty,"cac:PartyName")
            ET.SubElement(FrightParty,'cbc:Name').text =  str(FrightData[1]).upper()

            if FrightData[2] != "":
                ET.SubElement(FrightParty,'cbc:Name').text =  str(FrightData[2]).upper()

        if PermitValues['InwardCarrierAgentCode'] != "":
            self.cursor.execute(f"SELECT Cruei,Name,Name1 FROM InnonInwardCarrierAgent WHERE code = '{PermitValues['InwardCarrierAgentCode']}' ")
            InwardData = self.cursor.fetchone()

            InwardParty = ET.SubElement(Party,"cac:InwardCarrierAgentParty")
            InwardNotify = ET.SubElement(InwardParty,"cac:PartyIdentification")
            ET.SubElement(InwardNotify,'cbc:ID').text =  str(InwardData[0]).upper()

            InwardPartName = ET.SubElement(InwardParty,"cac:PartyName")
            ET.SubElement(InwardPartName,'cbc:Name').text =  str(InwardData[1]).upper()
            if InwardData[2] != "":
                ET.SubElement(InwardPartName,'cbc:Name').text =  str(InwardData[2]).upper()

        if PermitValues['ImporterCompanyCode'] != "":
            self.cursor.execute(f"SELECT Cruei,Name,Name1 FROM InNonImporter WHERE code = '{PermitValues['ImporterCompanyCode']}' ")
            ImportData = self.cursor.fetchone()

            ImpParty = ET.SubElement(Party,"cac:ImporterParty")
            ImpNotify = ET.SubElement(ImpParty,"cac:PartyIdentification")
            ET.SubElement(ImpNotify,'cbc:ID').text =  str(ImportData[0]).upper()

            ImpPartName = ET.SubElement(ImpParty,"cac:PartyName")
            ET.SubElement(ImpPartName,'cbc:ID').text =  str(ImportData[1]).upper()
            if ImportData[2] != "":
                ET.SubElement(ImpPartName,'cbc:Name').text =  str(ImportData[2]).upper()

        if PermitValues['OutwardCarrierAgentCode'] != "":
            self.cursor.execute(f"SELECT Cruei,Name,Name1 FROM InnonOutwardCarrierAgent WHERE code = '{PermitValues['OutwardCarrierAgentCode']}' ")
            OutWardData = self.cursor.fetchone()

            OutWardParty = ET.SubElement(Party,"cac:OutwardCarrierAgentParty")
            OutNotiFy = ET.SubElement(OutWardParty,"cac:PartyIdentification")
            ET.SubElement(OutNotiFy,'cbc:ID').text =  str(OutWardData[0]).upper()

            OutWardPartName = ET.SubElement(OutWardParty,"cac:PartyName")
            ET.SubElement(OutWardPartName,'cbc:Name').text =  str(OutWardData[1]).upper()
            if OutWardData[1] !="":
                ET.SubElement(OutWardPartName,'cbc:Name').text =  str(OutWardData[2]).upper()

        if PermitValues['ExporterCompanyCode'] != "":
            self.cursor.execute(f"SELECT Cruei,Name,Name1 FROM InnonExporter WHERE code = '{PermitValues['ExporterCompanyCode']}' ")
            ExportData = self.cursor.fetchone()

            ExportParty = ET.SubElement(Party,"cac:ExporterParty")
            ExportPartyDetail = ET.SubElement(ExportParty,"cac:PartyDetail")
            ExportParty = ET.SubElement(ExportPartyDetail,"cac:PartyIdentification")
            ET.SubElement(ExportParty,'cbc:ID').text =  str(ExportData[0]).upper()

            OutWardPartName = ET.SubElement(ExportParty,"cac:PartyName")
            ET.SubElement(OutWardPartName,'cbc:Name').text =  str(ExportData[1]).upper()
            if ExportData[2] != "":
                ET.SubElement(OutWardPartName,'cbc:Name').text =  str(ExportData[2]).upper()

        if PermitValues['ConsigneeCode'] != "":
            self.cursor.execute(f"SELECT ConsigneeName,ConsigneeName1,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSubDivi,ConsigneeSub,ConsigneePostal,ConsigneeCountry FROM InnonConsignee WHERE ConsigneeCode = '{PermitValues['ConsigneeCode']}' ")
            ConsignData = self.cursor.fetchone()

            ConsignParty = ET.SubElement(Party,"cac:ConsigneeParty")
            ConsignPartyName = ET.SubElement(ConsignParty,"cac:PartyName")
            ET.SubElement(ConsignPartyName,'cbc:Name').text =  str(ConsignData[0]).upper()
            if ConsignData[1] != "":
                ET.SubElement(ConsignPartyName,'cbc:Name').text =  str(ConsignData[1]).upper()

            ConsignPartyAddre = ET.SubElement(ConsignParty,"cac:Address")
            ConsignPartyAddLine = ET.SubElement(ConsignPartyAddre,"cac:AddressLine")

            if ConsignData[2] != "":
                ET.SubElement(ConsignPartyAddLine,'cbc:Line').text =  str(ConsignData[2]).upper()
            if ConsignData[3] != "":
                ET.SubElement(ConsignPartyAddLine,'cbc:Line').text =  str(ConsignData[3]).upper()
            if ConsignData[4] != "":
                ET.SubElement(ConsignPartyAddLine,'cbc:CityName').text =  str(ConsignData[4]).upper()
            if ConsignData[5] != "":
                ET.SubElement(ConsignPartyAddLine,'cbc:CountrySubentityCode').text =  str(ConsignData[5]).upper()
            if ConsignData[6] != "":
                ET.SubElement(ConsignPartyAddLine,'cbc:CountrySubentity').text =  str(ConsignData[6]).upper()
            if ConsignData[7] != "":
                ET.SubElement(ConsignPartyAddLine,'cbc:PostalZone').text =  str(ConsignData[7]).upper()
            if ConsignData[8] != "":
                ET.SubElement(ConsignPartyAddLine,'cbc:CountryCode').text =  str(ConsignData[8]).upper()
        
        if PermitValues["ClaimantPartyCode"] != "" :
            self.cursor.execute("select CRUEI,Name,ClaimantName1,Name1,Name2,ClaimantName FROM InnonClaimantParty WHERE Name='" + PermitValues["ClaimantPartyCode"] + "'")
            ClaimantData = self.cursor.fetchone()
            
            ClaimantParty = ET.SubElement(Party,"cac:ClaimantParty")
            PartyDetail = ET.SubElement(ClaimantParty,"cac:PartyDetail")
            ClainmentPartyIdentification = ET.SubElement(PartyDetail,"cac:PartyIdentification") 

            ET.SubElement(ClainmentPartyIdentification,'cbc:ID').text =  str(ClaimantData[0]).upper()

            ClainmentInfoPartyName = ET.SubElement(PartyDetail,"cac:PartyName")
            ET.SubElement(ClainmentInfoPartyName,'cbc:Name').text =  str(ClaimantData[3]).upper()
            ET.SubElement(ClainmentInfoPartyName,'cbc:Name').text =  str(ClaimantData[4]).upper()
            if ClaimantData[5]:
                ClaimantInformation = ET.SubElement(ClaimantParty,"cac:ClaimantInformation")
                ET.SubElement(ClaimantInformation,'cbc:CodeValue').text =  str(ClaimantData[5]).upper()
            if ClaimantData[4] != "":
                ET.SubElement(ClaimantInformation,'cbc:Name').text =  str(ClaimantData[4]).upper()

        if PermitValues["License"] != "":
            Licence = ET.SubElement(Party,"cac:Licence")
            for Li in PermitValues["License"].split("-"):
                if (Li != ""):
                    ET.SubElement(Licence,'cbc:ReferenceID').text =  str(Li).upper()
       
        self.cursor.execute("select DocumentType,Name from InNonFile where InPaymentId='" + PermitValues["MSGId"] + "' and PermitId='" + PermitValues["PermitId"] + "'")
        InFileDocument = self.cursor.fetchall()
        if InFileDocument != "":
            for File in InFileDocument:
                SupportDocument = ET.SubElement(Party,"cac:SupportingDocumentReference")
                ET.SubElement(SupportDocument,'cbc:DocumentID').text =  str(File[0].split(":")[0]).upper()
                ET.SubElement(SupportDocument,'cbc:Filename').text =  str(File[1]).upper()

        self.cursor.execute("SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime FROM InNonInvoiceDtl WHERE PermitId = '{}' ORDER BY SNO ".format(PermitValues["PermitId"]))
        self.invoice  = self.cursor.fetchall()

        InvoiceData = (pd.DataFrame(list(self.invoice), columns=['SNo' , 'InvoiceNo' , 'InvoiceDate' , 'TermType' , 'AdValoremIndicator' , 'PreDutyRateIndicator' , 'SupplierImporterRelationship' , 'SupplierCode' , 'ImportPartyCode' , 'TICurrency' , 'TIExRate' , 'TIAmount' , 'TISAmount' , 'OTCCharge' , 'OTCCurrency' , 'OTCExRate' , 'OTCAmount' , 'OTCSAmount' , 'FCCharge' , 'FCCurrency' , 'FCExRate' , 'FCAmount' , 'FCSAmount' , 'ICCharge' , 'ICCurrency' , 'ICExRate' , 'ICAmount' , 'ICSAmount' , 'CIFSUMAmount' , 'GSTPercentage' , 'GSTSUMAmount' , 'MessageType' , 'PermitId' , 'TouchUser' , 'TouchTime'])).to_dict('records')

        for InData in InvoiceData:
            InvoiceName =  ET.SubElement(InNonPayment,"cac:Invoice")
            if str(InData['InvoiceNo']) != "":
                ET.SubElement(InvoiceName,'cbc:InvoiceNumber').text =  str(InData['InvoiceNo']).upper()
            if str(InData['InvoiceDate']) != "":
                ET.SubElement(InvoiceName,'cbc:InvoiceDate').text =  str(InData['InvoiceDate'].strftime('%Y%m%d')).upper()

            if InData["SupplierCode"] != "":
                self.cursor.execute("select CRUEI,Name,Name1 FROM INNONSUPPLIERMANUFACTURERPARTY WHERE Code='" + InData["SupplierCode"] + "'")
                SupplierData = self.cursor.fetchone()

                SuppLyManufact = ET.SubElement(InvoiceName,"cac:SupplierManufacturerParty")
                ET.SubElement(SuppLyManufact,'cbc:CodeValue').text =  str(SupplierData[0]).upper()
                ET.SubElement(SuppLyManufact,'cbc:Name').text =  str(SupplierData[1]).upper()
                if SupplierData[2] != "":
                    ET.SubElement(SuppLyManufact,'cbc:Name').text =  str(SupplierData[2]).upper()

            if InData['TermType'] != "":
                ET.SubElement(InvoiceName,'cbc:UnitPriceTermType').text =  str(InData['TermType'][:3]).upper()
            
            if InData['TICurrency'] != "--Select--" and InData['TICurrency'] != "":
                TotalInvoiceValue = ET.SubElement(InvoiceName,"cac:TotalInvoiceValue")
                ET.SubElement(TotalInvoiceValue,'cbc:Amount' ,{"currencyID" :str(InData['TICurrency'])}).text =  str(InData['TIAmount']).upper()
                ET.SubElement(TotalInvoiceValue,'cbc:ExchangeRate').text =  str(InData['TIExRate']).upper()

            if InData['FCCurrency'] != "--Select--" and InData['FCCurrency'] != "":
                FreightCharge = ET.SubElement(InvoiceName,"cac:FreightCharge")
                ET.SubElement(FreightCharge,'cbc:Amount' ,{"currencyID" :str(InData['FCCurrency'])}).text =  str(InData['FCAmount']).upper()
                ET.SubElement(FreightCharge,'cbc:ExchangeRate').text =  str(InData['FCExRate']).upper()
                ET.SubElement(FreightCharge,'cbc:ChargePercent').text =  str(InData['FCCharge']).upper()

            if InData['ICCurrency'] != "--Select--" and InData['ICCurrency'] != "":
                InsuranceCharge = ET.SubElement(InvoiceName,"cac:InsuranceCharge")
                ET.SubElement(InsuranceCharge,'cbc:Amount' ,{"currencyID" :str(InData['ICCurrency'])}).text =  str(InData['ICAmount']).upper()
                ET.SubElement(InsuranceCharge,'cbc:ExchangeRate').text =  str(InData['ICExRate']).upper()
                ET.SubElement(InsuranceCharge,'cbc:ChargePercent').text =  str(InData['ICCharge']).upper()

            if InData['OTCCurrency'] != "--Select--" and InData['OTCCurrency'] != "":
                OtherTaxableCharge = ET.SubElement(InvoiceName,"cac:OtherTaxableCharge")
                ET.SubElement(OtherTaxableCharge,'cbc:Amount' ,{"currencyID" :str(InData['OTCCurrency'])}).text =  str(InData['OTCAmount']).upper()
                ET.SubElement(OtherTaxableCharge,'cbc:ExchangeRate').text =  str(InData['OTCExRate']).upper()
                ET.SubElement(OtherTaxableCharge,'cbc:ChargePercent').text =  str(InData['OTCCharge']).upper()

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitValues["PermitId"]))
        self.item  = self.cursor.fetchall()

        ItemData = (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records')

        for ItData in ItemData:
            ItemName =  ET.SubElement(InNonPayment,"inp:Item")

            ET.SubElement(ItemName,'cbc:ItemSequenceNumeric').text =  str(ItData['ItemNo']).upper()
            ET.SubElement(ItemName,'cbc:ItemHarmonizedSystemCode').text =  str(ItData['HSCode']).upper()
            ET.SubElement(ItemName,'cbc:GoodsDescription').text =  str(ItData['Description'].replace("&",' ')).upper()

            ItemQuantity =  ET.SubElement(ItemName,"cac:ItemQuantity")

            if int(ItData['HSQty']) > 0 and str(ItData['HSQty']) != "": ET.SubElement(ItemQuantity,'cbc:HarmonizedSystemQuantity',{"unitCode":ItData['HSUOM']}).text =  str(ItData['HSQty']).upper()

            if int(ItData['TotalDutiableQty']) > 0 and str(ItData['TotalDutiableQty']) != "": ET.SubElement(ItemQuantity,'cbc:TotalDutiableQuantity',{"unitCode":ItData['TotalDutiableUOM']}).text =  str(ItData['TotalDutiableQty']).upper()

            if int(ItData['DutiableQty']) > 0 and str(ItData['DutiableQty']) != "":  ET.SubElement(ItemQuantity,'cbc:DutiableQuantity',{"unitCode":ItData['DutiableUOM']}).text =  str(ItData['DutiableQty']).upper()

            if int(ItData['AlcoholPer']) > 0 and str(ItData['AlcoholPer']) != "": ET.SubElement(ItemQuantity,'cbc:AlcoholPercent').text =  str(ItData['AlcoholPer']).upper()

            if ItData['Contry'] != "" :
                ET.SubElement(ItemName,'cbc:OriginCountry').text =  str(ItData['Contry'][:2]).upper()

            if ItData['UnitPriceCurrency'] != "--Select--" :
                TransactionValue =  ET.SubElement(ItemName,"cac:TransactionValue")
                if int(ItData['UnitPrice']) > 0  :
                    UnitPriceValue = ET.SubElement(TransactionValue,"cac:UnitPriceValue")
                    ET.SubElement(UnitPriceValue,'cbc:Amount',{"currencyID":ItData['UnitPriceCurrency']}).text =  str(ItData['UnitPrice']).upper()
                    ET.SubElement(UnitPriceValue,'cbc:ExchangeRate').text =  str(ItData['ExchangeRate']).upper()
                if int(ItData['Optioncahrge']) > 0  :
                    OptionalItemCharge = ET.SubElement(TransactionValue,"cac:OptionalItemCharge")
                    if ItData['OptionalSumtotal'] >0:
                        ET.SubElement(OptionalItemCharge,'cbc:Amount',{"currencyID":ItData['OptionalChrgeUOM']}).text =  str(ItData['OptionalSumtotal']).upper()
                    if int(ItData['Optioncahrge']) > 0:
                        ET.SubElement(OptionalItemCharge,'cbc:ExchangeRate').text =  str(ItData['Optioncahrge']).upper()

            self.cursor.execute("SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,CASCId FROM INNONCASCDtl WHERE PermitId = '{}' AND ItemNo = '{}'  ORDER BY ItemNo".format(ItData['PermitId'],ItData['ItemNo']))
            self.casc = self.cursor.fetchall()

            CascData = (pd.DataFrame(list(self.casc), columns=['ItemNo','ProductCode','Quantity','ProductUOM','RowNo','CascCode1','CascCode2','CascCode3','CASCId'])).to_dict('records')

            for Casc in CascData:
                CASCProduct =  ET.SubElement(ItemName,"cac:CASCProduct")
                ET.SubElement(CASCProduct,'cbc:CASCProductCode').text =  str(Casc['ProductCode']).upper()
                ET.SubElement(CASCProduct,'cbc:CASCProductQuantity').text =  str(Casc['Quantity']).upper()
                if str(Casc['CascCode1']) != "" or str(Casc['CascCode2']) != "" or str(Casc['CascCode3']) != "":
                    AddiCasc = ET.SubElement(CASCProduct,"cac:AdditionalCASCIdentification")
                    if str(Casc['CascCode1']) != "":
                        ET.SubElement(AddiCasc,'cbc:CASCCodeOne').text =  str(Casc['CascCode1']).upper()
                    if str(Casc['CascCode2']) != "":
                        ET.SubElement(AddiCasc,'cbc:CASCCodeTwo').text =  str(Casc['CascCode2']).upper()
                    if str(Casc['CascCode3']) != "":
                        ET.SubElement(AddiCasc,'cbc:CASCCodeThree').text =  str(Casc['CascCode3']).upper()

            if str(ItData['Brand']) != "" : ET.SubElement(ItemName,'cbc:BrandName').text =  str(ItData['Brand']).upper()
            if str(ItData['Model']) != "" :  ET.SubElement(ItemName,'cbc:ModelDescription').text =  str(ItData['Model']).upper()
            if str(ItData['DGIndicator']) != "": ET.SubElement(ItemName,'cbc:DangerousGoodsIndicator').text =  str(ItData['DGIndicator']).upper()

            if ItData['OPUOM'] != "--Select--" or ItData['IPUOM'] != "--Select--" or  ItData['InPUOM'] != "--Select--" or ItData['ImPUOM'] != "--Select--" :
                PackingDescription = ET.SubElement(ItemName,"cac:PackingDescription")

                if str(ItData['OPUOM']) != "--Select--" : ET.SubElement(PackingDescription,'cbc:OuterPackQuantity',{"unitCode":str(ItData['OPUOM'])}).text =  str(ItData['OPQty']).upper()

                if str(ItData['IPUOM']) != "--Select--" : ET.SubElement(PackingDescription,'cbc:InPackQuantity',{"unitCode":str(ItData['IPUOM'])}).text =  str(ItData['IPQty']).upper()

                if str(ItData['InPUOM']) != "--Select--" : ET.SubElement(PackingDescription,'cbc:InnerPackQuantity',{"unitCode":str(ItData['InPUOM'])}).text =  str(ItData['InPqty']).upper()

                if str(ItData['ImPUOM']) != "--Select--" : ET.SubElement(PackingDescription,'cbc:InmostPackQuantity',{"unitCode":str(ItData['ImPUOM'])}).text =  str(ItData['ImPQty']).upper()

            if ItData['ShippingMarks1'] != "":
                Shipping = ET.SubElement(ItemName,"cac:ShippingMarksInformation")
                ET.SubElement(Shipping,'cbc:ShippingMarks').text =  str(ItData['ShippingMarks1']).upper()

            if ItData['CurrentLot'] != "":
                LotIdentification = ET.SubElement(ItemName,"cac:LotIdentification")
                ET.SubElement(LotIdentification,'cbc:CurrentLotNumber').text =  str(ItData['CurrentLot']).upper()
                if str(ItData['PreviousLot']) != "" : ET.SubElement(LotIdentification,'cbc:PreviousLotNumber').text =  str(ItData['PreviousLot']).upper()

                if str(ItData['Making']) != "--Select--" : ET.SubElement(LotIdentification,'cbc:Marking').text =  str(ItData['Marking']).upper()[:2]

            if str(ItData['InHAWBOBL']) != "" : ET.SubElement(ItemName,'cbc:InHAWBHUCRHBLNumber').text =  str(ItData['InHAWBOBL']).upper()

            if str(ItData['OutHAWBOBL']) != "" : ET.SubElement(ItemName,'cbc:OutHAWBHUCRHBLNumber').text =  str(ItData['OutHAWBOBL']).upper()

            if str(ItData['InvoiceNo']) != "--Select--" : ET.SubElement(ItemName,'cbc:ItemInvoiceNumber').text =  str(ItData['InvoiceNo']).upper()

            if str(ItData['Enginecapacity']) != "0.00" and str(ItData['Enginecapacity']) != "":
                MotorVehicle = ET.SubElement(ItemName,"cac:MotorVehicle")
                if str(ItData['Enginecapacity']) != "0.00" and str(ItData['Enginecapacity']) != "" :
                    ET.SubElement(MotorVehicle,'cbc:Enginecapacity' , {"unitCode" : ItData['Engineuom'].split(":")[0]}).text =  str(ItData['Enginecapacity']).upper()
                
                if str(ItData['Orginregdate']) != "" and ItData['Orginregdate'].strftime("%Y-%m-%d")!= "1900-01-01":
                    ET.SubElement(MotorVehicle,'cbc:OriginalRegistrationDate').text =  str(ItData['Orginregdate'].strftime("%Y%m%d")).upper()

            Tariff = ET.SubElement(ItemName,"cac:Tariff")

            if ItData['PreferentialCode'] != "--Select--":
                ET.SubElement(Tariff,'cbc:PreferentialCode').text =  str(ItData['PreferentialCode']).upper().split(":")[0]
            if int(ItData['GSTRate']) > 0 or int(ItData['GSTAmount'] > 0):
                GoodsAndServicesTax = ET.SubElement(Tariff,"cac:GoodsAndServicesTax")

                if int(ItData['GSTRate']) > 0 :
                    ET.SubElement(GoodsAndServicesTax,'cbc:GoodsAndServicesTaxPercent').text =  str(ItData['GSTRate'])
                
                if int(ItData['GSTAmount']) > 0 :
                    ET.SubElement(GoodsAndServicesTax,'cbc:GoodsAndServicesTaxAmount').text =  str(ItData['GSTAmount'])
            
            if ItData['ExciseDutyUOM'] != "--Select--" and int(ItData['ExciseDutyRate']) > 0 :
                ExciseDuty = ET.SubElement(Tariff,"cac:ExciseDuty")
                ET.SubElement(ExciseDuty,'cbc:DutyRate').text =  str(ItData['ExciseDutyRate'])
                ET.SubElement(ExciseDuty,'cbc:DutyRateUnit').text =  str(ItData['ExciseDutyUOM'])
                ET.SubElement(ExciseDuty,'cbc:DutyAmount').text =  str(ItData['ExciseDutyAmount'])

            if ItData['CustomsDutyUOM'] != "--Select--" and int(ItData['CustomsDutyRate']) > 0 :
                CustomsDuty = ET.SubElement(Tariff,"cac:CustomsDuty")
                ET.SubElement(CustomsDuty,'cbc:DutyRate').text =  str(ItData['CustomsDutyRate'])
                ET.SubElement(CustomsDuty,'cbc:DutyRateUnit').text =  str(ItData['CustomsDutyUOM'])
                ET.SubElement(CustomsDuty,'cbc:DutyAmount').text =  str(ItData['CustomsDutyAmount'])

            if ItData['OtherTaxUOM'] != "--Select--":
                OtherTax = ET.SubElement(Tariff,"cac:OtherTax")
                ET.SubElement(OtherTax,'cbc:DutyRate').text =  str(ItData['OtherTaxRate'])
                ET.SubElement(OtherTax,'cbc:DutyRateUnit').text =  str(ItData['OtherTaxUOM'])
                ET.SubElement(OtherTax,'cbc:DutyAmount').text =  str(ItData['OtherTaxAmount'])

            if ItData['OtherTaxUOM'] != "--Select--":
                OtherTax = ET.SubElement(Tariff,"cac:OtherTax")
                ET.SubElement(OtherTax,'cbc:DutyRate').text =  str(ItData['OtherTaxRate'])
                ET.SubElement(OtherTax,'cbc:DutyRateUnit').text =  str(ItData['OtherTaxUOM'])
                ET.SubElement(OtherTax,'cbc:DutyAmount').text =  str(ItData['OtherTaxAmount'])


        Summary = ET.SubElement(InNonPayment,"inp:Summary")

        if int(PermitValues["NumberOfItems"]) > 0:
            ET.SubElement(Summary,"cbc:NumberOfItems").text = str(int(PermitValues["NumberOfItems"]))

        if int(PermitValues["TotalCIFFOBValue"]) > 0:
            ET.SubElement(Summary,"cbc:TotalCIFFOBValue").text = str(int(PermitValues["TotalCIFFOBValue"]))

        if str(PermitValues["TotalOuterPackUOM"]) !=  "--Select--" :
            ET.SubElement(Summary,"cbc:TotalOuterPack",{"unitCode" : str(PermitValues["TotalOuterPackUOM"])} ).text = str(PermitValues["TotalOuterPack"])

        if str(PermitValues["TotalGrossWeightUOM"]) !=  "--Select--" and str(PermitValues["TotalGrossWeightUOM"]) != "":
            ET.SubElement(Summary,"cbc:TotalGrossWeight",{"unitCode" : str(PermitValues["TotalGrossWeightUOM"])} ).text = str(PermitValues["TotalGrossWeight"])

        if int(PermitValues["TotalGSTTaxAmt"]) > 0 :
            TotalTariff = ET.SubElement(Summary,"cac:TotalTariff")
            ET.SubElement(TotalTariff,"cbc:TotalGoodsAndServicesTaxAmount").text = str(PermitValues["TotalGSTTaxAmt"])

            if int(PermitValues["TotalExDutyAmt"]) > 0 :
                ET.SubElement(TotalTariff,"cbc:TotalExciseDutyAmount").text = str(int(PermitValues["TotalExDutyAmt"]))

            if int(PermitValues["TotalCusDutyAmt"]) > 0 :
                ET.SubElement(TotalTariff,"cbc:TotalCustomsDutyAmount").text = str(PermitValues["TotalCusDutyAmt"])

            if int(PermitValues["TotalODutyAmt"]) > 0 :
                ET.SubElement(TotalTariff,"cbc:TotalOtherTaxAmount").text = str(PermitValues["TotalODutyAmt"])

        tree = ET.ElementTree(self.indent(Root))
        tree.write(f'/Users/Public/QXMF004/KaizenXML/{PermitValues["MSGId"]}.xml')
        
    def CnlExml(self,PermitId):
        pass

def InNonSubmit(request):
    permitNumber1 = json.loads(request.GET.get("PermitNumber"))
    s = SqlDb('SecondDb')
    s1 = SqlDb('default')
    for ID in permitNumber1:
        s1.cursor.execute(f"SELECT * FROM InNonHeaderTbl WHERE Id='{ID}' ")
        permitNumber = s1.cursor.fetchone()[4]
        TouchUser = str(request.session['Username']).upper() 
        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        s.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(TouchUser))
        ManageUserVal = s.cursor.fetchone()
        AccountId = ManageUserVal[0]
        MailId = ManageUserVal[1]

        s.cursor.execute("SELECT COUNT(*) + 1  FROM InNonHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'INPDEC' ".format(refDate))
        RefId = ("%03d" % s.cursor.fetchone()[0])

        s.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        JobIdCount = s.cursor.fetchone()[0]

        JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % JobIdCount}" 
        MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % JobIdCount}"
        NewPermitId = f"{TouchUser}{refDate}{RefId}"

        TouchTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        try:
            s1.cursor.execute(f"SELECT * FROM InNonHeaderTbl WHERE PermitId='{permitNumber}' ")
            Heading = [i[0] for i in s1.cursor.description]
            HeadData = [dict(zip(Heading,row)) for row in s1.cursor.fetchall()]
            HeadQry = ("INSERT INTO InNonHeaderTbl(Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
            for head in HeadData:
                headVal = (RefId,JobId,MsgId,NewPermitId,MailId,head['MessageType'],head['DeclarationType'],head['PreviousPermit'],head['CargoPackType'],head['InwardTransportMode'],head['OutwardTransportMode'],head['BGIndicator'],head['SupplyIndicator'],head['ReferenceDocuments'],head['License'],head['Recipient'],head['DeclarantCompanyCode'],head['ImporterCompanyCode'],head['ExporterCompanyCode'],head['InwardCarrierAgentCode'],head['OutwardCarrierAgentCode'],head['ConsigneeCode'],head['FreightForwarderCode'],head['ClaimantPartyCode'],head['ArrivalDate'],head['LoadingPortCode'],head['VoyageNumber'],head['VesselName'],head['OceanBillofLadingNo'],head['ConveyanceRefNo'],head['TransportId'],head['FlightNO'],head['AircraftRegNo'],head['MasterAirwayBill'],head['ReleaseLocation'],head['RecepitLocation'],head['RecepilocaName'],head['StorageLocation'],head['ExhibitionSDate'],head['ExhibitionEDate'],head['BlanketStartDate'],head['TradeRemarks'],head['InternalRemarks'],head['CustomerRemarks'],head['DepartureDate'],head['DischargePort'],head['FinalDestinationCountry'],head['OutVoyageNumber'],head['OutVesselName'],head['OutOceanBillofLadingNo'],head['VesselType'],head['VesselNetRegTon'],head['VesselNationality'],head['TowingVesselID'],head['TowingVesselName'],head['NextPort'],head['LastPort'],head['OutConveyanceRefNo'],head['OutTransportId'],head['OutFlightNO'],head['OutAircraftRegNo'],head['OutMasterAirwayBill'],head['TotalOuterPack'],head['TotalOuterPackUOM'],head['TotalGrossWeight'],head['TotalGrossWeightUOM'],head['GrossReference'],head['DeclareIndicator'],head['NumberOfItems'],head['TotalCIFFOBValue'],head['TotalGSTTaxAmt'],head['TotalExDutyAmt'],head['TotalCusDutyAmt'],head['TotalODutyAmt'],head['TotalAmtPay'],head['Status'],TouchUser,TouchTime,head['PermitNumber'],head['prmtStatus'],head['ReleaseLocaName'],head['Inhabl'],head['outhbl'],head['seastore'],head['Cnb'],head['DeclarningFor'],head['MRDate'],head['MRTime'])
                s.cursor.execute(HeadQry,headVal)

            s.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{NewPermitId}','INPDEC','{AccountId}','{MsgId}','{TouchUser}','{TouchTime}') ")

            InvoiceQry = "INSERT INTO InNonInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM InNonInvoiceDtl WHERE PermitId='{permitNumber}' ")
            InvoiceHead = [i[0] for i in s1.cursor.description]
            InvoiceData = [dict(zip(InvoiceHead,row)) for row in s1.cursor.fetchall()] 
            for head in InvoiceData:
                InvoiceVal= (head['SNo'],head['InvoiceNo'],head['InvoiceDate'],head['TermType'],head['AdValoremIndicator'],head['PreDutyRateIndicator'],head['SupplierImporterRelationship'],head['SupplierCode'],head['ImportPartyCode'],head['TICurrency'],head['TIExRate'],head['TIAmount'],head['TISAmount'],head['OTCCharge'],head['OTCCurrency'],head['OTCExRate'],head['OTCAmount'],head['OTCSAmount'],head['FCCharge'],head['FCCurrency'],head['FCExRate'],head['FCAmount'],head['FCSAmount'],head['ICCharge'],head['ICCurrency'],head['ICExRate'],head['ICAmount'],head['ICSAmount'],head['CIFSUMAmount'],head['GSTPercentage'],head['GSTSUMAmount'],head['MessageType'],NewPermitId,TouchUser,TouchTime)
                s.cursor.execute(InvoiceQry,InvoiceVal)

            ItemQry = "INSERT INTO InNonItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM InNonItemDtl WHERE PermitId='{permitNumber}' ")
            ItemHead = [i[0] for i in s1.cursor.description]
            ItemData = [dict(zip(ItemHead,row)) for row in s1.cursor.fetchall()]
            for head in ItemData:
                ItemVal= (head['ItemNo'],NewPermitId,head['MessageType'],head['HSCode'],head['Description'],head['DGIndicator'],head['Contry'],head['Brand'],head['Model'],head['Vehicletype'],head['Enginecapacity'],head['Engineuom'],head['Orginregdate'],head['InHAWBOBL'],head['OutHAWBOBL'],head['DutiableQty'],head['DutiableUOM'],head['TotalDutiableQty'],head['TotalDutiableUOM'],head['InvoiceQuantity'],head['HSQty'],head['HSUOM'],head['AlcoholPer'],head['InvoiceNo'],head['ChkUnitPrice'],head['UnitPrice'],head['UnitPriceCurrency'],head['ExchangeRate'],head['SumExchangeRate'],head['TotalLineAmount'],head['InvoiceCharges'],head['CIFFOB'],head['OPQty'],head['OPUOM'],head['IPQty'],head['IPUOM'],head['InPqty'],head['InPUOM'],head['ImPQty'],head['ImPUOM'],head['PreferentialCode'],head['GSTRate'],head['GSTUOM'],head['GSTAmount'],head['ExciseDutyRate'],head['ExciseDutyUOM'],head['ExciseDutyAmount'],head['CustomsDutyRate'],head['CustomsDutyUOM'],head['CustomsDutyAmount'],head['OtherTaxRate'],head['OtherTaxUOM'],head['OtherTaxAmount'],head['CurrentLot'],head['PreviousLot'],head['LSPValue'],head['Making'],head['ShippingMarks1'],head['ShippingMarks2'],head['ShippingMarks3'],head['ShippingMarks4'],TouchUser,TouchTime,head['OptionalChrgeUOM'],head['Optioncahrge'],head['OptionalSumtotal'],head['OptionalSumExchage'])
                s.cursor.execute(ItemQry,ItemVal)

            ItemCascQry = "INSERT INTO INNONCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM INNONCASCDtl WHERE PermitId='{permitNumber}' ")
            ItemCascHead = [i[0] for i in s1.cursor.description]
            ItemCascData = [dict(zip(ItemCascHead,row)) for row in s1.cursor.fetchall()]
            for head in ItemCascData:
                ItemCascVal= (head['ItemNo'],head['ProductCode'],head['Quantity'],head['ProductUOM'],head['RowNo'],head['CascCode1'],head['CascCode2'],head['CascCode3'],NewPermitId,head['MessageType'],TouchUser,TouchTime,head['CASCId'])
                s.cursor.execute(ItemCascQry,ItemCascVal)

            ContainerQry = "INSERT INTO InnonContainerDtl (PermitId,RowNo,ContainerNo,Size,Weight,SealNo,MessageType,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM InnonContainerDtl WHERE PermitId='{permitNumber}' ")
            ContainerHead = [i[0] for i in s1.cursor.description]
            ContainerData = [dict(zip(ContainerHead,row)) for row in s1.cursor.fetchall()]
            for head in ContainerData:
                ContainerVal= (NewPermitId,head['RowNo'],head['ContainerNo'],head['Size'],head['Weight'],head['SealNo'],head['MessageType'],TouchUser,TouchTime)
                s.cursor.execute(ContainerQry,ContainerVal)

            CpcQry = "INSERT INTO InNonCPCDtl (PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM InNonCPCDtl WHERE PermitId='{permitNumber}' ")
            CpcHead = [i[0] for i in s1.cursor.description]
            CpcData = [dict(zip(CpcHead,row)) for row in s1.cursor.fetchall()]
            for head in CpcData:
                CpcVal= (NewPermitId,head['MessageType'],head['RowNo'],head['CPCType'],head['ProcessingCode1'],head['ProcessingCode2'],head['ProcessingCode3'],TouchUser,TouchTime)
                s.cursor.execute(CpcQry,CpcVal) 

            InfileQry = "INSERT INTO InNonFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM InNonFile WHERE PermitId='{permitNumber}' ")
            InFileHead = [i[0] for i in s1.cursor.description]
            InFileData = [dict(zip(InFileHead,row)) for row in s1.cursor.fetchall()]
            for head in InFileData:
                InfileVal= (head['Sno'],head['Name'],head['ContentType'],head['Data'],head['DocumentType'],head['InPaymentId'],TouchUser,TouchTime,head['Size'],NewPermitId,head['Type'])
                s.cursor.execute(InfileQry,InfileVal)

            s.conn.commit()
            print("saved SuccessFully")
        except Exception as e:
            pass
        finally:
            return JsonResponse({"Success":"Genrate"})

    return JsonResponse({"Success":"Genrate"})
 
class InonPayementCancel(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
       
    def get(self,request,Id):

        Username = request.session['Username'] 

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute(f"SELECT PermitId,PermitNumber FROM InNonHeaderTbl WHERE Id = '{Id}' ")
        PermitIdValus = self.cursor.fetchone()
        CopyPermitId = PermitIdValus[0]

        self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        ManageUserVal = self.cursor.fetchone()
        AccountId = ManageUserVal[0]

        self.cursor.execute("SELECT COUNT(*) + 1  FROM InNonHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'INPDEC' ".format(refDate))
        self.RefId = ("%03d" % self.cursor.fetchone()[0])

        self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute(f"INSERT INTO InNonHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime) SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{ManageUserVal[1]}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{Username}','{NowDate}',PermitNumber,'CNL',ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,'--Select--',MRDate,MRTime FROM InNonHeaderTbl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','INPDEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')")

        self.cursor.execute(f"INSERT INTO InNonInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ImportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,'{self.PermitIdInNon}','{Username}','{NowDate}' FROM InNonInvoiceDtl WHERE PermitId = '{CopyPermitId}' ")
        
        self.cursor.execute(f"INSERT INTO InNonItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,'{Username}','{NowDate}',OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM InNonItemDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO INNONCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId) SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,'{self.PermitIdInNon}',MessageType,'{Username}','{NowDate}',CASCId FROM INNONCASCDtl WHERE PermitId = '{CopyPermitId}'")
        
        self.cursor.execute(f"INSERT INTO InnonContainerDtl (PermitId, RowNo,ContainerNo, size, weight,SealNo, MessageType,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}', RowNo,ContainerNo, size, weight,SealNo, MessageType,'{Username}','{NowDate}' FROM InnonContainerDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO InNonFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{Username}','{NowDate}',Size,'{self.PermitIdInNon}',Type FROM InNonFile WHERE PermitId = '{CopyPermitId}' ")
        
        self.conn.commit()

        self.cursor.execute(f"SELECT Id FROM InNonHeaderTbl WHERE PermitId = '{self.PermitIdInNon}'")
        InNonId = self.cursor.fetchone()[0]

        request.session['InNonId'] = InNonId

        return redirect("/InonPayementEdit/")
    
class PrintSatusInNon(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
    
    def get(self,request,ID):
        FileName = f"/Users/Public/PDF-Files/CancelStatus{(datetime.now()).strftime('%d-%m-%Y %H-%M-%s')}.pdf"
        can = canvas.Canvas(FileName, pagesize=(595, 841))

        can.setFont('Times-Roman', 9)
        can.drawString(480, 820, "PG : 1 OF 1")
        
        self.cursor.execute("SELECT Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime FROM InNonHeaderTbl WHERE Id = '{}' ".format(ID))
        Inheader = (pd.DataFrame(list(self.cursor.fetchall()), columns=['Refid','JobId','MSGId','PermitId','TradeNetMailboxID','MessageType','DeclarationType','PreviousPermit','CargoPackType','InwardTransportMode','OutwardTransportMode','BGIndicator','SupplyIndicator','ReferenceDocuments','License','Recipient','DeclarantCompanyCode','ImporterCompanyCode','ExporterCompanyCode','InwardCarrierAgentCode','OutwardCarrierAgentCode','ConsigneeCode','FreightForwarderCode','ClaimantPartyCode','ArrivalDate','LoadingPortCode','VoyageNumber','VesselName','OceanBillofLadingNo','ConveyanceRefNo','TransportId','FlightNO','AircraftRegNo','MasterAirwayBill','ReleaseLocation','RecepitLocation','RecepilocaName','StorageLocation','ExhibitionSDate','ExhibitionEDate','BlanketStartDate','TradeRemarks','InternalRemarks','CustomerRemarks','DepartureDate','DischargePort','FinalDestinationCountry','OutVoyageNumber','OutVesselName','OutOceanBillofLadingNo','VesselType','VesselNetRegTon','VesselNationality','TowingVesselID','TowingVesselName','NextPort','LastPort','OutConveyanceRefNo','OutTransportId','OutFlightNO','OutAircraftRegNo','OutMasterAirwayBill','TotalOuterPack','TotalOuterPackUOM','TotalGrossWeight','TotalGrossWeightUOM','GrossReference','DeclareIndicator','NumberOfItems','TotalCIFFOBValue','TotalGSTTaxAmt','TotalExDutyAmt','TotalCusDutyAmt','TotalODutyAmt','TotalAmtPay','Status','TouchUser','TouchTime','PermitNumber','prmtStatus','ReleaseLocaName','Inhabl','outhbl','seastore','Cnb','DeclarningFor','MRDate','MRTime']).to_dict('records'))[0]
        
        self.cursor.execute(f"SELECT Cruei,Name,Name1 FROM InNonImporter WHERE code = '{Inheader['ImporterCompanyCode']}' ")
        Import = self.cursor.fetchone()

        self.cursor.execute(f"SELECT portname FROM LoadingPort where PortCode = '{Inheader['LoadingPortCode']}'")
        Loading = self.cursor.fetchone()

        style = getSampleStyleSheet()['Normal']
        style.fontName = 'Times-Roman'  # Set the font family
        style.fontSize = 9
        style.spaceBefore = 0 
        

        rejectStatus = [['SERIAL NO ','CODE','MESSAGE']]
        TitleStatus = ''
        if Inheader['Status'] == "REJ":
            y_ax = 430
            filename = "RejectStatus"
            TitleStatus = 'REJECTION MESSAGE'
            self.cursor.execute("select Sno,ErrorId,ErrorDescription from InnonRejectStatus  where MsgId = '"+Inheader['MSGId']+"' AND PermitNumber='" + Inheader["PermitNumber"] + "' and MAILBOXID='" + Inheader["TradeNetMailboxID"] + "' order by Sno")
            for Re in self.cursor.fetchall():
                rejectStatus.append([Paragraph(str(Re[0]),style),Paragraph(str(Re[1]),style),Paragraph(Re[2],style)])
        elif Inheader['Status'] == "QRY":
            y_ax = 430
            filename = "QUERY_STATUS"
            TitleStatus = 'QUERY MESSAGE'
            self.cursor.execute("select Sno,ErrorId,ErrorDescription from InnonRejectStatus  where MsgId = '"+Inheader['MSGId']+"' AND PermitNumber='" + Inheader["PermitNumber"] + "' and MAILBOXID='" + Inheader["TradeNetMailboxID"] + "' order by Sno")
            for Re in self.cursor.fetchall():
                rejectStatus.append([Paragraph(str(Re[0]),style),Paragraph(str(Re[1]),style),Paragraph(Re[2],style)])

        elif Inheader['Status'] == "CNL":
            filename = f"Cancellation_{Inheader['PermitNumber']}"
            TitleStatus = 'CANCELLATION MESSAGE'
            can.rect(50, 460, 500, 50)
            self.cursor.execute(f"SELECT ResonForCancel,DescriptionOfReason FROM InNonCancel WHERE PermitNo = '{Inheader['PermitNumber']}' ")
            InpayCancel = self.cursor.fetchone()
            if InpayCancel:
                can.drawString(60, 490, f"CANCELLATION REASON : {((InpayCancel[0]).upper())[:4]}")
                can.drawString(60, 475, f"DESCRIPTION OF REASON : {(InpayCancel[1]).upper()}")
            y_ax = 370

            self.cursor.execute("select Sno,ConditionCde,ConditionDes from InnonCancelPermit  where MsgId = '"+Inheader['MSGId']+"' AND PermitNumber='" + Inheader["PermitNumber"] + "' and MAILBOXID='" + Inheader["TradeNetMailboxID"] + "' order by Sno")
            for Re in self.cursor.fetchall():
                rejectStatus.append([Paragraph(str(Re[0]),style),Paragraph(str(Re[1]),style),Paragraph(Re[2],style)])
        can.setFont('Times-Bold', 10)
        can.drawString(250, 790, TitleStatus)
        can.setFont('Times-Roman', 9)
        coveyance = ''
        Obl_hawb = ''
        InTransportId = ''
        if ((Inheader['InwardTransportMode'])[4:]).upper() == "SEA":
            Obl_hawb = Inheader['OceanBillofLadingNo']
            coveyance = Inheader['VoyageNumber']
            InTransportId = Inheader['VesselName']
        elif ((Inheader['InwardTransportMode'])[4:]).upper() == "AIR":
            Obl_hawb = Inheader['MasterAirwayBill']
            coveyance = Inheader['FlightNO']
            InTransportId = Inheader['VesselName']


        can.rect(50, 530, 500, 250)

        can.drawString(60, 760, "MESSAGE TYPE :  IN-NON-PAYMENT DECLARATION  ")
        can.drawString(60, 745, f"DECLARATION TYPE : {Inheader['DeclarationType']}")
        can.drawString(60, 730, f"COMPANY UEN : {Import[0]}")
        can.drawString(60, 715, f"COMPANY NAME : {Import[1]}")
        can.drawString(60, 700, f"PORT OF LOADING : {Loading[0]}")
        can.drawString(60, 685, "PORT OF DISCHARGE : ")
        can.drawString(60, 670, "DESTINATION COUNTRY : ")

        can.drawString(60, 655, f"IN TRANSPORT ID : {InTransportId}")
        can.drawString(60, 640, f"ARRIVAL DATE : {(str(Inheader['ArrivalDate']))}")
        can.drawString(60, 625, f"CONVEYANCE NO : {coveyance}")
        can.drawString(60, 610, f"MAWB / OBL : {Obl_hawb}")
        can.drawString(60, 595, "OUT TRANSPORT ID :")
        can.drawString(60, 580, "DEPARTURE DATE :")
        can.drawString(60, 565, "CONVEYANCE NO :")
        can.drawString(60, 550, "MAWB / OBL :")
        createDate = (Inheader['TouchTime']).strftime("%d-%m-%Y")
        can.drawString(310, 760, f"CREATE DATE : {createDate}")
        can.drawString(310, 745, f"MESSAGE ID : {Inheader['MSGId']}")
        can.drawString(310, 730, f"PERMIT NUMBER : {Inheader['PermitNumber']}")
        can.drawString(310, 715, f"PREVIOUS PERMIT : {Inheader['PreviousPermit']}")
        can.drawString(310, 700, f"PLACE OF RELEASE : {Inheader['ReleaseLocaName']}")
        can.drawString(310, 685, f"PLACE OF RECEIPT : {Inheader['RecepilocaName']}")
        can.drawString(310, 670, f"TOTAL OUTER PACKAGE : {Inheader['TotalOuterPack']}/{Inheader['TotalOuterPackUOM']}")
        can.drawString(310, 655, f"TOTAL GROSS WEIGHT : {Inheader['TotalGrossWeight']}/{Inheader['TotalGrossWeightUOM']}")
        can.drawString(310, 640, f"NUMBER OF ITEMS : {int(Inheader['NumberOfItems'])}")

        col_widths = [90, 70, 340]
        table = Table(rejectStatus,colWidths=col_widths)
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('COLWIDTHS', (2, -1), (-1, -1), 102),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('SPLITLONGWORDS', (0, 0), (-1, -1), 1), 
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        table.wrapOn(can, 0, 0)
        table.drawOn(can, 50, y_ax)
        can.showPage()
        can.save()

        with open(FileName, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        FileName1 = f"CancelStatus{(datetime.now()).strftime('%d-%m-%Y %H-%M-%s')}.pdf"
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{FileName1}"'

        return response

class DownloadCcpInNon(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,Data):
        pdfFiles = []
        for ID in Data.split(","):
            self.cursor.execute("SELECT Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,ExporterCompanyCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,ConsigneeCode,FreightForwarderCode,ClaimantPartyCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,RecepilocaName,StorageLocation,ExhibitionSDate,ExhibitionEDate,BlanketStartDate,TradeRemarks,InternalRemarks,CustomerRemarks,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocaName,Inhabl,outhbl,seastore,Cnb,DeclarningFor,MRDate,MRTime FROM InNonHeaderTbl WHERE Id = '{}' ".format(ID))

            InNonHeaderData = self.cursor.fetchall()

            PermitValues = (pd.DataFrame(list(InNonHeaderData), columns=['Refid','JobId','MSGId','PermitId','TradeNetMailboxID','MessageType','DeclarationType','PreviousPermit','CargoPackType','InwardTransportMode','OutwardTransportMode','BGIndicator','SupplyIndicator','ReferenceDocuments','License','Recipient','DeclarantCompanyCode','ImporterCompanyCode','ExporterCompanyCode','InwardCarrierAgentCode','OutwardCarrierAgentCode','ConsigneeCode','FreightForwarderCode','ClaimantPartyCode','ArrivalDate','LoadingPortCode','VoyageNumber','VesselName','OceanBillofLadingNo','ConveyanceRefNo','TransportId','FlightNO','AircraftRegNo','MasterAirwayBill','ReleaseLocation','RecepitLocation','RecepilocaName','StorageLocation','ExhibitionSDate','ExhibitionEDate','BlanketStartDate','TradeRemarks','InternalRemarks','CustomerRemarks','DepartureDate','DischargePort','FinalDestinationCountry','OutVoyageNumber','OutVesselName','OutOceanBillofLadingNo','VesselType','VesselNetRegTon','VesselNationality','TowingVesselID','TowingVesselName','NextPort','LastPort','OutConveyanceRefNo','OutTransportId','OutFlightNO','OutAircraftRegNo','OutMasterAirwayBill','TotalOuterPack','TotalOuterPackUOM','TotalGrossWeight','TotalGrossWeightUOM','GrossReference','DeclareIndicator','NumberOfItems','TotalCIFFOBValue','TotalGSTTaxAmt','TotalExDutyAmt','TotalCusDutyAmt','TotalODutyAmt','TotalAmtPay','Status','TouchUser','TouchTime','PermitNumber','prmtStatus','ReleaseLocaName','Inhabl','outhbl','seastore','Cnb','DeclarningFor','MRDate','MRTime']).to_dict('records'))[0]
        
            lftcol = 50
            rgtcol = 280
            self.countPage = 1

            if PermitValues['PermitNumber'] == "":
                PermitBar = "DRAFT"
                OldFilename = f"D:/Users/Public/PDFFilesKtt/{PermitBar}1.pdf"
                
            else:
                PermitBar = PermitValues['PermitNumber']
                OldFilename = f"D:/Users/Public/PDFFilesKtt/{PermitBar}1.pdf"
                barcode = code39.Standard39(PermitValues['PermitNumber'], barHeight=36.0, barWidth=1.1, baseline=9.0,size=12.0, N=3.0, X=1.0, StartsStopText=False, Extended=False)

            p = canvas.Canvas(OldFilename, pagesize=(595, 841))
            p.setTitle(PermitBar)
            inpstrtdate = ""
            inpEndate = ""

            p.setFont('Courier-Bold', 10)
            p.drawString(480, 750, PermitBar)

            if PermitValues['PermitNumber'] != "":
                barcode.drawOn(p, 330, 760)

            p.setFont('Courier', 10)
            p.drawString(400, 750, "PERMIT NO : ")

            p.drawString(rgtcol, 700, "CARGO CLEARANCE PERMIT")
            p.drawString(460, 700, ("PG : {} OF").format(self.countPage))
            self.countPage += 1

            if PermitValues['prmtStatus'] =="AMD":
                p.drawString(lftcol, 670, "MESSAGE TYPE      : IN-NON-PAYMENT UPDATED PERMIT")
            else: 
                p.drawString(lftcol, 670, "MESSAGE TYPE      : IN-NON-PAYMENT PERMIT")
                
            p.drawString(lftcol, 660, "DECLARATION TYPE  : " + (str(PermitValues["DeclarationType"])[6:]).upper())

            p.drawString(lftcol, 630, "IMPORTER:")

            self.cursor.execute(f"SELECT Name,Name1,Cruei FROM InNonImporter WHERE code = '{PermitValues['ImporterCompanyCode']}' ")
            ImportData = self.cursor.fetchone()
            ImportDataCruei = ImportData[2]
            ImportData = str(ImportData[0])+str(ImportData[1])

            if len(ImportData) >= 35:
                p.drawString(lftcol, 620, (ImportData[:35]).upper())
                p.drawString(lftcol, 610, (ImportData[35:]).upper())
            else:
                p.drawString(lftcol, 620, (ImportData).upper())
            p.drawString(lftcol, 600, str(ImportDataCruei).upper())

            p.drawString(lftcol, 590, "EXPORTER:")
            self.cursor.execute(f"SELECT Name,Name1,Cruei FROM InnonExporter WHERE code = '{PermitValues['ExporterCompanyCode']}' ")
            ExportData = self.cursor.fetchone()
            
            if ExportData is not None :
                ExportDataCruei = ExportData[2]
                ExportData = str(ExportData[0])+str(ExportData[1])

                if len(ImportData) >= 35:
                    p.drawString(lftcol, 580, (ExportData[:35]).upper())
                    p.drawString(lftcol, 570, (ExportData[35:]).upper())
                else:
                    p.drawString(lftcol, 580, (ExportData).upper())
                p.drawString(lftcol, 560, str(ExportDataCruei).upper())

            p.drawString(lftcol, 550, "HANDLING AGENT: ")
            p.drawString(lftcol, 540, " ")
            p.drawString(lftcol, 530, " ")
            p.drawString(lftcol, 520, " ")
            p.drawString(lftcol, 510, " ")
            p.drawString(lftcol, 500, "PORT OF LOADING/NEXT PORT OF CALL:")

            self.cursor.execute(f"SELECT PortCode,PortName FROM LoadingPort WHERE PortCode = '{PermitValues['NextPort']}'")
            NextPort = self.cursor.fetchone()
            if NextPort is not None:
                p.drawString(lftcol, 490, str(NextPort[1]).upper())

            p.drawString(lftcol, 480, "PORT OF DISCHARGE/FINAL PORT OF CALL ")

            self.cursor.execute(f"SELECT PortCode,PortName FROM LoadingPort WHERE PortCode = '{PermitValues['DischargePort']}'")
            DischargePort = self.cursor.fetchone()
            if DischargePort is not None:
                p.drawString(lftcol, 470, str(DischargePort[1]).upper())

            p.drawString(lftcol, 460, "COUNTRY OF FINAL DESTINATION:")
            if PermitValues['FinalDestinationCountry'] != "--Select--":
                p.drawString(lftcol, 450, str(PermitValues['FinalDestinationCountry']).split(":")[0])

            p.drawString(lftcol, 440, "INWARD CARRIER AGENT: ")

            InWard = "SELECT Name,Name1 FROM InnonInwardCarrierAgent where Code=%s"
            self.cursor.execute(InWard,(PermitValues['InwardCarrierAgentCode'],))
            InwardData = self.cursor.fetchone()
            if InwardData:
                InwardData = str(InwardData[0])+str(InwardData[1])

                if len(InwardData) >= 35:
                    p.drawString(lftcol, 430, (InwardData[:35]).upper().replace("\n"," "))
                    p.drawString(lftcol, 420, (InwardData[35:70]).upper().replace("\n"," "))
                    p.drawString(lftcol, 410, (InwardData[70:]).upper().replace("\n"," "))
                else:
                    p.drawString(lftcol, 430, (InwardData).upper().replace("\n"," "))

            p.drawString(lftcol, 400, "OUTWARD CARRIER AGENT: ")


            OutWard = "SELECT Name,Name1 FROM InnonOutwardCarrierAgent where Code=%s"
            self.cursor.execute(OutWard,(PermitValues['OutwardCarrierAgentCode'],))
            OutwardData = self.cursor.fetchone()
            if OutwardData is not None:
                OutwardData = str(OutwardData[0])+str(OutwardData[1])

                if len(OutwardData) >= 35:
                    p.drawString(lftcol, 390, (OutwardData[:35]).upper().replace("\n"," "))
                    p.drawString(lftcol, 380, (OutwardData[35:70]).upper().replace("\n"," "))
                    p.drawString(lftcol, 370, (OutwardData[70:]).upper().replace("\n"," "))
                else:
                    p.drawString(lftcol, 390, (OutwardData).upper().replace("\n"," "))

            p.drawString(lftcol, 360, "PLACE OF RELEASE: ")

            ReleaseY = 350
            ReleaseX = lftcol
            RelaseVal = str(PermitValues['ReleaseLocaName'] ).replace("\n" , '')

            for Re in range(len(RelaseVal)):
                p.drawString(ReleaseX, ReleaseY, str(RelaseVal[Re]))
                ReleaseX += 6

                if Re %32 == 0 and Re != 0:
                    ReleaseY -= 10
                    ReleaseX = lftcol

            ReleaseY =- 10 

            p.drawString(lftcol, ReleaseY, PermitValues['ReleaseLocation'])
            p.drawString(lftcol, 250, "LICENCE NO:")


            licence = (str(PermitValues['License']).upper()).split('-')
            p.drawString(lftcol, 240, licence[0])
            p.drawString(lftcol, 230, licence[1])
            p.drawString(lftcol, 220, licence[2])
            p.drawString(lftcol, 210, licence[3])
            p.drawString(lftcol, 200, licence[4])
            p.drawString(lftcol, 50,  "--------------------------------------------------------------------------------")
            
            Declarant = "SELECT Cruei FROM DeclarantCompany where tradenetmailboxId=%s"
            self.cursor.execute(Declarant,(PermitValues['TradeNetMailboxID'],))
            DeclarData = self.cursor.fetchone()
            
            p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format((DeclarData[0]).upper(), str(PermitValues['MSGId'][:8]).upper(), str(PermitValues['MSGId'][8:]).upper()))

            if PermitValues['prmtStatus'] =="AMD":
                self.cursor.execute(f"SELECT StartDate,EndDate FROM InnonAMDPMT where PermitNumber = '{PermitValues['PermitNumber']}' AND MsgId = '{PermitValues['MSGId']}' ")
                StartEnd = self.cursor.fetchone()
            else:
                self.cursor.execute(f"SELECT StartDate,EndDate FROM InnonPMT where PermitNumber = '{PermitValues['PermitNumber']}' ")
                StartEnd = self.cursor.fetchone()

            if StartEnd is not None:
                inpstrtdate = datetime.strptime(str(StartEnd[0]), '%Y-%m-%d').strftime('%d/%m/%Y')
                inpEndate = datetime.strptime(str(StartEnd[1]), '%Y-%m-%d').strftime('%d/%m/%Y')


            rgy = 630
            p.drawString(rgtcol, rgy, ("VALIDITY PERIOD      : {} - ").format(inpstrtdate))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("                       {}").format(inpEndate))
            rgy -= 20

            totalGross = "{:.3f}".format(float(PermitValues["TotalGrossWeight"]))

            p.drawString(rgtcol, rgy, ("TOTAL GROSS WT/UNIT  : {:>18}/{}").format(totalGross, PermitValues["TotalGrossWeightUOM"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOTAL OUTER PACK/UNIT: {:>18}/{}").format(PermitValues["TotalOuterPack"], PermitValues["TotalOuterPackUOM"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOT EXCISE DUT PAYABLE  : S${:>17}").format(PermitValues["TotalExDutyAmt"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOT CUSTOMS DUT PAYABLE : S${:>17}").format(PermitValues["TotalCusDutyAmt"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOT OTHER TAX PAYABLE   : S${:>17}").format(PermitValues["TotalODutyAmt"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOTAL GST AMT           : S${:>17}").format(PermitValues["TotalGSTTaxAmt"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("TOTAL AMOUNT PAYABLE    : S${:>17}").format(PermitValues["TotalAmtPay"]))
            rgy -= 10
            p.drawString(rgtcol, rgy, ("CARGO PACKING TYPE: {} ").format(((PermitValues['CargoPackType'])[3:]).upper()))
            rgy -= 10
            p.drawString(rgtcol, rgy, "IN TRANSPORT IDENTIFIER: ")
            rgy -= 10

            
            if PermitValues['InwardTransportMode'] == "4 : Air":
                transidval = PermitValues['AircraftRegNo']
                CoveyanceNo = PermitValues['VesselName']
            elif PermitValues['InwardTransportMode'] == "1 : Sea":
                transidval = PermitValues['VesselName']
                CoveyanceNo = PermitValues['VesselName']
            else:
                transidval = PermitValues['TransportId']
                CoveyanceNo = PermitValues['TransportId']

            p.drawString(rgtcol, rgy, transidval.upper())
            rgy -= 10
            p.drawString(rgtcol, rgy, ("CONVEYANCE REFERENCE NO: {} ").format(CoveyanceNo.upper()))
            rgy -= 10
            p.drawString(rgtcol, rgy, "OBL/MAWB NO: ")
            rgy -= 10
            p.drawString(rgtcol, rgy, PermitValues['OceanBillofLadingNo'])
            rgy -= 10
            if str(PermitValues['ArrivalDate'].strftime('%d/%m/%Y')) != "01/01/1900":
                p.drawString(rgtcol, rgy, "ARRIVAL DATE         : {}".format((PermitValues['ArrivalDate']).strftime('%d/%m/%Y')))
            else:
                p.drawString(rgtcol, rgy, "ARRIVAL DATE         : {}".format((PermitValues['ArrivalDate']).strftime('%d/%m/%Y')))

            rgy -= 10
            p.drawString(rgtcol, rgy, "OU TRANSPORT IDENTIFIER: ")
            rgy -= 10

            if PermitValues['InwardTransportMode'] == "4 : Air":
                Outransport = PermitValues['OutAircraftRegNo']
                conveno = PermitValues["OutFlightNO"]
                mastebill = PermitValues["OutMasterAirwayBill"]
            
            elif PermitValues['InwardTransportMode'] == "1 : Sea":
                Outransport = PermitValues['OutVesselName']
                conveno = PermitValues["OutVoyageNumber"]
                mastebill = PermitValues["OutOceanBillofLadingNo"]
            else:
                Outransport = PermitValues['OutTransportId']
                conveno = PermitValues["OutConveyanceRefNo"]
                mastebill = ""

            p.drawString(rgtcol, rgy, str(Outransport).upper())
            rgy -= 10
            p.drawString(rgtcol, rgy, "CONVEYANCE REFERENCE NO:  "+str(conveno).upper())
            rgy -= 10
            p.drawString(rgtcol, rgy, "OBL/MAWB/UCR NO: ")
            rgy -= 10
            p.drawString(rgtcol, rgy, ""+str(mastebill).upper())
            rgy -= 10

            if str(PermitValues['DepartureDate'].strftime('%d/%m/%Y')) != "01/01/1900":
                p.drawString(rgtcol, rgy, "DEPARTURE DATE       : "+str(PermitValues['DepartureDate'].strftime('%d/%m/%Y')))
            else:
                p.drawString(rgtcol, rgy, "DEPARTURE DATE       : ")
            rgy -= 20

            p.drawString(rgtcol, rgy, "CERTIFICATE NO:  ")
            rgy -= 30

            p.drawString(rgtcol, rgy, "PLACE OF RECEIPT:")
            rgy -= 10

            ReleaseY = rgy
            ReleaseX = rgtcol
            ReciptVal = str(PermitValues['RecepilocaName'] ).replace("\n" , '')

            for Re in range(len(ReciptVal)):
                p.drawString(ReleaseX, ReleaseY, str(ReciptVal[Re]))
                ReleaseX += 6

                if Re %32 == 0 and Re != 0:
                    ReleaseY -= 10
                    ReleaseX = rgtcol

            ReleaseY -= 10

            p.drawString(rgtcol, ReleaseY, PermitValues['RecepitLocation'])
            p.drawString(rgtcol, 250, "CUSTOMS PROCEDURE CODE (CPC) : ")
            rely = 240

            self.cursor.execute(f"SELECT DISTINCT CPCType FROM InNonCPCDtl WHERE PermitId='{PermitValues['PermitId']}' ")
            CpcData = self.cursor.fetchall()

            for cpc in CpcData:
                p.drawString(rgtcol, rely, str(cpc[0]))
                rely -= 10

            if PermitValues['Cnb'] == "True" or PermitValues['Cnb'] == "true":
                p.drawString(rgtcol, rely, str("CNB"))

            #-------------------------------------------Heading Page Complete-----------------------------------------------#

            p.showPage()

            snox = 50
            hscodex = 100
            currentx = 180
            prviousx = 320
            makingx = 50
            cityx = 120
            brandx = 220
            itemy = 820

            def itemyF(itemy):
                if itemy <= 70:
                    itemy = 820
                    p.showPage()
                    p.setFont('Courier', 10)
                else:
                    itemy -= 10
                if itemy <= 820 and itemy >= 700:
                    p.setFont('Courier', 10)
                    p.drawString(rgtcol, itemy, "CARGO CLEARANCE PERMIT ")
                    p.drawString(460, itemy, ("PG : {} OF ").format(self.countPage))
                    self.countPage += 1
                    itemy -= 10
                    p.drawString(lftcol, itemy, "PERMIT NO : " +str(PermitBar))
                    p.drawString(rgtcol, itemy, "======================")
                    itemy -= 10
                    p.drawString(rgtcol, itemy, "(CONTINUATION PAGE)")
                    itemy -= 20
                    p.drawString(lftcol, itemy, "CONSIGNMENT DETAILS")
                    itemy -= 10
                    p.drawString(lftcol, itemy, "--------------------------------------------------------------------------------")
                    itemy -= 10

                    p.drawString(lftcol, itemy, "S/NO     HS CODE      CURRENT LOT NO         PREVIOUS LOT NO                ")
                    itemy -= 10

                    p.drawString(lftcol, itemy, "MARKING    CTY OF ORIGIN    BRAND NAME       MODEL                            ")
                    itemy -= 10

                    self.cursor.execute(f"SELECT count(InHAWBOBL) FROM InNonItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '' ")
                    ItemHeadData = self.cursor.fetchone()

                    if  ItemHeadData[0] is not None:
                        p.drawString(lftcol, itemy, "IN HAWB/HUCR/HBL                             OUT HAWB/HUCR/HBL                 ")
                        itemy -= 10
                    
                    p.drawString(lftcol, itemy, "PACKING/GOODS DESCRIPTION                    HS QUANTITY & UNIT               ")
                    itemy -= 10

                    p.drawString(lftcol, itemy, "                                             CIF/FOB VALUE (S$)               ")
                    itemy -= 10

                    self.cursor.execute(f"SELECT sum(LSPValue) FROM InNonItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '' ")
                    LspData = self.cursor.fetchone()

                    if str(LspData[0]) != str("0.00"):
                        p.drawString(lftcol, itemy, "                                             LSP VALUE (S$)                   ")
                        itemy -= 10

                    p.drawString(lftcol, itemy, "                                             GST AMOUNT (S$)                  ")
                    itemy -= 10

                    self.cursor.execute(f"SELECT count(DutiableUOM),sum(DutiableQty),sum(UnitPrice),sum(ExciseDutyRate),sum(CustomsDutyAmount) FROM InNonItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '--Select--' ")
                    DutyUom = self.cursor.fetchone()

                    if  DutyUom[0] is not None and Decimal(DutyUom[1]) != Decimal("0.0000"):
                        p.drawString(lftcol, itemy, "                                             DUT QTY/WT/VOL & UNIT            ")
                        itemy -= 10

                    if Decimal(DutyUom[2] != Decimal("0.00")):
                        p.drawString(lftcol, itemy, "                                             UNIT PRICE & CODE                 ")
                        itemy -= 10

                    if Decimal(DutyUom[3] != Decimal("0.00")):
                        p.drawString(lftcol, itemy, "                                             EXCISE DUTY PAYABLE (S$)          ")
                        itemy -= 10

                    if Decimal(DutyUom[4] != Decimal("0.00")):
                        p.drawString(lftcol, itemy, "                                             CUSTOMS DUTY PAYABLE(S$)          ")
                        itemy -= 10

                    p.drawString(snox, itemy, "MANUFACTURER'S NAME ")
                    itemy -= 10
                    p.drawString( snox, itemy, '-------------------------------------------------------------------------------')
                    itemy -= 10
                    p.drawString(lftcol, 50,  "--------------------------------------------------------------------------------")
                    p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format((DeclarData[0]).upper(), str(PermitValues['MSGId'][:8]).upper(), str(PermitValues['MSGId'][8:]).upper()))

                return itemy
            
            def Cascfunction(Item,CascId,Sno,itemy):
                self.cursor.execute(f"SELECT ProductCode,Quantity,ProductUOM FROM INNONCASCDtl WHERE ItemNo = '{Item['ItemNo']}' AND PermitId = '{Item['PermitId']}' AND CascId = '{CascId}' ")
                CascData = self.cursor.fetchone()
                if CascData is not None:
                    p.drawString(lftcol, itemy,  "--------------------------------------------------------------------------------")
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, 'S/NO')
                    p.drawString(lftcol+70, itemy, 'CA/SC PRODUCT CODE ')
                    p.drawString(lftcol+280, itemy, 'CA/SC PRODUCT QTY & UNIT')
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, '   {}'.format(Sno))
                    p.drawString(lftcol+70, itemy, str(CascData[0]).upper())
                    if str(CascData[1]) != "0.0000":
                        p.drawString(lftcol+280, itemy, ('{:10d}.{} {}').format(int(CascData[1]), str(CascData[1]).split(".")[1], CascData[2]))
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy,  "--------------------------------------------------------------------------------")

                return itemy

            itemy = itemyF(itemy)
            self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM  InNonItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitValues['PermitId']))
            self.item = self.cursor.fetchall()
            ItemValues = (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records')
            
            for Item in ItemValues:
                p.drawString(lftcol, itemy, f"{'%02d' % Item['ItemNo']}     {Item['HSCode']}      {Item['CurrentLot']}         {Item['PreviousLot']}                ")
                itemy = itemyF(itemy)

                if Item['Making'] != "--Select--":
                    p.drawString(makingx, itemy, (str(Item['Making'])[:2]).upper())
                p.drawString(cityx-40, itemy, str(Item['Contry']).upper())
                p.drawString(brandx-105, itemy, str(Item['Brand']).upper())
                p.drawString(prviousx, itemy, str(Item['Model']).upper())
                itemy = itemyF(itemy)

                if Item["InHAWBOBL"] != '':
                    p.drawString(lftcol, itemy, str(Item['InHAWBOBL']).upper())
                    itemy = itemyF(itemy)

                DescriptionItem = Item['Description']

                DescX = lftcol
                Dcount = 1
                HSQtyName = True
                CiFob = True
                Lsp = True
                GstAmd = True
                TotDutiable = True
                ExciseAmd = True
                CustomDuty = True
                OtherDuty = True
                for D in range(len(DescriptionItem)):
                    if DescriptionItem[D] != "\n":
                        p.drawString(DescX, itemy, DescriptionItem[D])
                    DescX +=6
                    if "\n" == DescriptionItem[D]:
                        DescX = lftcol
                        itemy = itemyF(itemy)
                        Dcount += 1
                    if (D+1) % 50 == 0 :
                        DescX = lftcol
                        itemy = itemyF(itemy)
                        Dcount += 1

                    if Dcount == 1 and HSQtyName:
                        p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(Item['HSQty']), str(Item['HSQty']).split(".")[1], Item['HSUOM']))
                        HSQtyName = False

                    if Dcount == 2 and CiFob:
                        p.drawString(prviousx+100, itemy, ('{:10d}.{}').format( int(Item['CIFFOB']), str(Item['CIFFOB']).split(".")[1]))
                        CiFob = False

                    if Dcount == 3 and Lsp:
                        Dcount += 1 
                        if Decimal(Item['LSPValue']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['LSPValue']), str(Item['LSPValue']).split(".")[1]))
                            Lsp = False
                    if Dcount == 4 and GstAmd:
                        p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['GSTAmount']), str(Item['GSTAmount']).split(".")[1]))
                        GstAmd = False

                    if Dcount == 5 and TotDutiable:
                        Dcount += 1 
                        if Decimal(Item['TotalDutiableQty']) != Decimal("0.0000"):
                            p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(Item['TotalDutiableQty']), str( Item['TotalDutiableQty']).split(".")[1], Item['TotalDutiableUOM']))
                            TotDutiable = False

                    if Dcount == 6 and ExciseAmd:
                        Dcount += 1 
                        if Decimal(Item['ExciseDutyAmount']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['ExciseDutyAmount']), str(Item['ExciseDutyAmount']).split(".")[1]))
                            ExciseAmd = False
                    
                    if Dcount == 7 and CustomDuty:
                        Dcount += 1
                        if Decimal(Item['CustomsDutyAmount']) != Decimal("0.00"): 
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['CustomsDutyAmount']), str(Item['CustomsDutyAmount']).split(".")[1]))

                    if Dcount == 8 and OtherDuty:
                        Dcount += 1
                        if Decimal(Item['OtherTaxAmount']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['OtherTaxAmount']), str(Item['OtherTaxAmount']).split(".")[1]))
                            OtherDuty = False
                else:
                    if Dcount <= 1:
                        p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(Item['HSQty']), str(Item['HSQty']).split(".")[1], Item['HSUOM']))
                        itemy = itemyF(itemy)
                    if Dcount <= 2:
                        p.drawString(prviousx+100, itemy, ('{:10d}.{}').format( int(Item['CIFFOB']), str(Item['CIFFOB']).split(".")[1]))
                        itemy = itemyF(itemy)

                    if Dcount <= 3:
                        if Decimal(Item['LSPValue']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['LSPValue']), str(Item['LSPValue']).split(".")[1]))
                            itemy = itemyF(itemy)

                    if Dcount <= 4:
                        p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['GSTAmount']), str(Item['GSTAmount']).split(".")[1]))
                        itemy = itemyF(itemy)

                    if Dcount <= 5:
                        if Decimal(Item['TotalDutiableQty']) != Decimal("0.0000"):
                            p.drawString(prviousx+100, itemy, ('{:8d}.{} {}').format(int(Item['TotalDutiableQty']), str( Item['TotalDutiableQty']).split(".")[1], Item['TotalDutiableUOM']))
                            itemy = itemyF(itemy)

                    if Dcount <= 6:
                        if Decimal(Item['ExciseDutyAmount']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['ExciseDutyAmount']), str(Item['ExciseDutyAmount']).split(".")[1]))
                            itemy = itemyF(itemy)

                    if Dcount <= 7:
                        if Decimal(Item['CustomsDutyAmount']) != Decimal("0.00"): 
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['CustomsDutyAmount']), str(Item['CustomsDutyAmount']).split(".")[1]))
                            itemy = itemyF(itemy)

                    if Dcount <= 8:
                        if Decimal(Item['OtherTaxAmount']) != Decimal("0.00"):
                            p.drawString(prviousx+100, itemy, ('{:10d}.{}').format(int(Item['OtherTaxAmount']), str(Item['OtherTaxAmount']).split(".")[1]))
                            itemy = itemyF(itemy)

                self.cursor.execute(f"SELECT SupplierCode FROM InNonInvoiceDtl WHERE PermitId = '{Item['PermitId']}' AND InvoiceNo = '{Item['InvoiceNo']}' ")
                InvoiceData = self.cursor.fetchone()
                if InvoiceData != "":
                    self.cursor.execute(f"SELECT Name,Name1 FROM INNONSUPPLIERMANUFACTURERPARTY WHERE code = '{InvoiceData[0]}' ")
                    SupplyData = self.cursor.fetchone()
                    if SupplyData is not None:
                        SupplyData = (str(SupplyData[0]) + str(SupplyData[1])).upper()
                        p.drawString(lftcol, itemy, (SupplyData)[:50])
                        itemy = itemyF(itemy)
                        if len(SupplyData) >= 50:
                            p.drawString(lftcol, itemy, (SupplyData)[50:])
                            itemy = itemyF(itemy)

                self.cursor.execute(f"SELECT * FROM INNONCASCDtl WHERE ItemNo = '{Item['ItemNo']}' AND PermitId = '{Item['PermitId']}'")
                CascCheck = self.cursor.fetchall()

                if len(CascCheck) != 0:
                    itemy = Cascfunction(Item,'Casc1',"01",itemy)
                    itemy = Cascfunction(Item,'Casc2',"02",itemy)
                    itemy = Cascfunction(Item,'Casc3',"03",itemy)
                    itemy = Cascfunction(Item,'Casc4',"04",itemy)
                    itemy = Cascfunction(Item,'Casc5',"05",itemy)

                if str(Item['Enginecapacity']) != str("0.00") and str(Item['Enginecapacity']) != "":
                    p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, 'S/NO')
                    p.drawString(lftcol+70, itemy, 'ENGINE NO/CHASSIS NO ')
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, ("   {}").format("%02d" % Item['ItemNo']))
                    p.drawString(lftcol+70, itemy, str(Item['Enginecapacity']))
                    itemy = itemyF(itemy)
                    p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                
                p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                itemy = itemyF(itemy)-20
                p.drawString(snox, itemy, '-------------------------------------------------------------------------------')
                itemy = itemyF(itemy)

            def itemyF1(itemy):
                if itemy <= 60:
                    itemy = 820
                    p.showPage()
                    p.setFont('Courier', 10)
                else:
                    itemy -= 10
                if itemy <= 820 and itemy >= 780:
                    p.setFont('Courier', 10)
                    p.drawString(rgtcol, itemy, "CARGO CLEARANCE PERMIT ")
                    p.drawString(460, itemy, ("PG : {} OF").format(self.countPage))
                    self.countPage += 1
                    itemy -= 10
                    p.drawString(lftcol, itemy, "PERMIT NO : "+PermitBar)
                    p.drawString(rgtcol, itemy, "======================")
                    itemy -= 10
                    p.drawString(rgtcol, itemy, "(CONTINUATION PAGE)")
                    itemy -= 20
                    p.drawString(lftcol, itemy, "CONSIGNMENT DETAILS")
                    itemy -= 10
                    p.drawString(lftcol, itemy, "--------------------------------------------------------------------------------")
                    itemy -= 10
                    p.drawString(lftcol, 50,  "--------------------------------------------------------------------------------")
                    p.drawString(lftcol, 40,  ("UNIQUE REF : {} {} {}").format((DeclarData[0]).upper(), str(PermitValues['MSGId'][:8]).upper(), str(PermitValues['MSGId'][8:]).upper()))
                return itemy
            
            TradeRemark = str(PermitValues['TradeRemarks']).upper()
            TradeX = lftcol
            for Tr in range(len(TradeRemark)):
                if TradeRemark[Tr] != "\n":
                    p.drawString(TradeX, itemy, TradeRemark[Tr])
                TradeX += 6
                if (Tr + 1) % 80 == 0 or TradeRemark[Tr] == "\n":
                    TradeX = lftcol
                    itemy = itemyF1(itemy)

            else:itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")

            self.cursor.execute(f"SELECT RowNo,ContainerNo,size,weight,SealNo FROM InnonContainerDtl WHERE PermitId = '{PermitValues['PermitId']}' ")
            ContainerData = self.cursor.fetchall()

            if len(ContainerData) != 0:
                itemy = itemyF1(itemy)
                p.drawString(lftcol, itemy, "CONTAINER IDENTIFIERS")
                itemy = itemyF1(itemy)
                for Cont in ContainerData:
                    p.drawString(lftcol, itemy, ("   {})").format("%02d" % Cont[0]))
                    p.drawString(lftcol+50, itemy, str(Cont[1]).upper())
                    p.drawString(lftcol+130, itemy, ("{}  {}").format(Cont[2][:3], Cont[2][3:5]))
                    p.drawString(lftcol+200, itemy, (str(Cont[3]))[:3])
                    p.drawString(lftcol+240, itemy, str(Cont[4]))
                    itemy = itemyF1(itemy)
            
            p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "NO UNAUTHORISED ADDITION/AMENDMENT TO THIS PERMIT MAY BE MADE AFTER APPROVAL")
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "NAME OF COMPANY:")
            Declarant = "SELECT name,DeclarantName,DeclarantCode,DeclarantTel FROM DeclarantCompany where tradenetmailboxId=%s"
            self.cursor.execute(Declarant,(PermitValues['TradeNetMailboxID'],))
            DeclarData = self.cursor.fetchone()
            p.drawString(lftcol+110, itemy, (DeclarData[0])[:67])
            itemy = itemyF1(itemy)
            p.drawString(lftcol+110, itemy, (DeclarData[0])[67:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "DECLARANT NAME :")
            p.drawString(lftcol+110, itemy, (DeclarData[1])[:67])
            itemy = itemyF1(itemy)
            p.drawString(lftcol+110, itemy, (DeclarData[1])[67:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "DECLARANT CODE :")
            p.drawString(lftcol+110, itemy, "XXXX"+(DeclarData[2])[-5:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "TEL NO         : ")
            p.drawString(lftcol+110, itemy, (DeclarData[3]))
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "-------------------------------------------------------------------------------")
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "CONTROLLING AGENCY/CUSTOMS CONDITIONS ")
            itemy = itemyF1(itemy)

            if PermitValues['prmtStatus'] == "AMD":
                self.cursor.execute(f"SELECT Conditioncode,ConditionDescription FROM InnonAMDPMT WHERE PermitNumber = '{PermitValues['PermitNumber']}' AND MsgId = '{PermitValues['MSGId']}' ORDER BY SNO")
            else:
                self.cursor.execute(f"SELECT Conditioncode,ConditionDescription FROM InnonPMT WHERE PermitNumber = '{PermitValues['PermitNumber']}' ORDER BY SNO")
            ControllingData = self.cursor.fetchall()

            for Control in ControllingData:
                p.setFont('Courier-Bold', 10)
                p.drawString(lftcol, itemy, Control[0])
                p.drawString(lftcol+30, itemy, "-")
                p.setFont('Courier', 10)

                p.drawString(lftcol+40, itemy, (Control[1])[:73])
                itemy = itemyF1(itemy)
                if len((Control[1])) > 73:
                    p.drawString(lftcol, itemy, (Control[1])[73:153])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 153:
                    p.drawString(lftcol, itemy, (Control[1])[153:233])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 233:
                    p.drawString(lftcol, itemy, (Control[1])[233:313])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 313:
                    p.drawString(lftcol, itemy, (Control[1])[313:393])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 393:
                    p.drawString(lftcol, itemy, (Control[1])[393:473])
                    itemy = itemyF1(itemy)
                if len((Control[1])) > 473:
                    p.drawString(lftcol, itemy, (Control[1])[473:])
                    itemy = itemyF1(itemy)
            p.save()
            existing_pdf = PdfFileReader(open(OldFilename, "rb"))
            output = PdfFileWriter()

            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(595, 841))
            can.setFont('Courier', 10)
            can.drawString(520, 700, str(len(existing_pdf.pages)))
            can.showPage()
            can.setFont('Courier', 10)
            can.drawString(520, 810, str(len(existing_pdf.pages)))
            can.showPage()
            can.setFont('Courier', 10)
            can.drawString(520, 820, str(len(existing_pdf.pages)))
            can.save()
            packet.seek(0)
            new_pdf = PdfFileReader(packet)
            for i in range(len(existing_pdf.pages)):
                if i == 0:
                    page = existing_pdf.pages[i]
                    page.merge_page(new_pdf.pages[0])
                elif i == 1:
                    page = existing_pdf.pages[i]
                    page.merge_page(new_pdf.pages[1])
                else:
                    page = existing_pdf.pages[i]
                    page.merge_page(new_pdf.pages[2])
                output.add_page(page)
            
            NewFilename = f"D:/Users/Public/PDFFilesKtt/{PermitBar}.pdf"
            output_stream = open(NewFilename, "wb")
            output.write(output_stream)
            output_stream.close()

            if os.path.exists(OldFilename):
                os.remove(OldFilename)

            pdfFiles.append(NewFilename)

        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="Zip_{(datetime.now()).strftime("%Y-%B-%d-%H%M")}.zip"'

        with zipfile.ZipFile(response, mode='w') as zip_file:
            for file_path in pdfFiles:
                if os.path.isfile(file_path):
                    folder_name = "Files"
                    arcname = os.path.join(folder_name, os.path.basename(file_path))
                    zip_file.write(file_path, arcname=arcname)

        return response

class DeleteAllInNon(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
    def get(self,request,Id):
        Ids = Id.split(',')
        self.cursor.execute(f"UPDATE InNonHeaderTbl SET Status = 'DEL' WHERE Id IN {tuple(Ids)} ")
        self.conn.commit()
        return redirect('/InonPaymentList')

class AutoCOmpl(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):
        self.cursor.execute(f"SELECT Top 10 Code,Name FROM InNonImporter WHERE status = 'Active' AND Code LIKE '{request.GET.get('term','')}%'  ORDER BY Name ")
        result = [(val[0]+":" +val[1]) for val in self.cursor.fetchall()]
        return JsonResponse(result,safe=False)
    
class DownloadDataInNon(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
    def get(self,request,Id):
        Headerrow_num = 0
        Containerrow_num = 0
        InvoiceWorkrow_num = 0
        ItemWorkRow_num = 0
        CascRow_num = 0
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        headerWork = wb.add_sheet('Header')

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        bg_color = xlwt.Pattern()
        bg_color.pattern = xlwt.Pattern.SOLID_PATTERN
        bg_color.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
        font_style.pattern = bg_color

        columns = ['Id','Refid','JobId','MSGId','PermitId','TradeNetMailboxID','MessageType','DeclarationType','PreviousPermit','CargoPackType','InwardTransportMode','OutwardTransportMode','BGIndicator','SupplyIndicator','ReferenceDocuments','License','Recipient','DeclarantCompanyCode','ImporterCompanyCode','ExporterCompanyCode','InwardCarrierAgentCode','OutwardCarrierAgentCode','ConsigneeCode','FreightForwarderCode','ClaimantPartyCode','ArrivalDate','LoadingPortCode','VoyageNumber','VesselName','OceanBillofLadingNo','ConveyanceRefNo','TransportId','FlightNO','AircraftRegNo','MasterAirwayBill','ReleaseLocation','RecepitLocation','RecepilocaName','StorageLocation','ExhibitionSDate','ExhibitionEDate','BlanketStartDate','TradeRemarks','InternalRemarks','CustomerRemarks','DepartureDate','DischargePort','FinalDestinationCountry','OutVoyageNumber','OutVesselName','OutOceanBillofLadingNo','VesselType','VesselNetRegTon','VesselNationality','TowingVesselID','TowingVesselName','NextPort','LastPort','OutConveyanceRefNo','OutTransportId','OutFlightNO','OutAircraftRegNo','OutMasterAirwayBill','TotalOuterPack','TotalOuterPackUOM','TotalGrossWeight','TotalGrossWeightUOM','GrossReference','DeclareIndicator','NumberOfItems','TotalCIFFOBValue','TotalGSTTaxAmt','TotalExDutyAmt','TotalCusDutyAmt','TotalODutyAmt','TotalAmtPay','Status','TouchUser','TouchTime','PermitNumber','prmtStatus','ReleaseLocaName','Inhabl','outhbl','seastore','Cnb','DeclarningFor','MRDate','MRTime']
        for col_num in range(len(columns)):
            headerWork.write(Headerrow_num, col_num, columns[col_num], font_style)

        ContainerWork = wb.add_sheet('Container')
        columns = ['Id', 'PermitId', 'RowNo', 'ContainerNo', 'size','weight', 'SealNo', 'MessageType', 'TouchUser', 'TouchTime']
        for col_num in range(len(columns)):
            ContainerWork.write(Containerrow_num, col_num,columns[col_num], font_style)

        InvoiceWork = wb.add_sheet('Invoice')
        columns = ['Id','SNo' , 'InvoiceNo' , 'InvoiceDate' , 'TermType' , 'AdValoremIndicator' , 'PreDutyRateIndicator' , 'SupplierImporterRelationship' , 'SupplierCode' , 'ImportPartyCode' , 'TICurrency' , 'TIExRate' , 'TIAmount' , 'TISAmount' , 'OTCCharge' , 'OTCCurrency' , 'OTCExRate' , 'OTCAmount' , 'OTCSAmount' , 'FCCharge' , 'FCCurrency' , 'FCExRate' , 'FCAmount' , 'FCSAmount' , 'ICCharge' , 'ICCurrency' , 'ICExRate' , 'ICAmount' , 'ICSAmount' , 'CIFSUMAmount' , 'GSTPercentage' , 'GSTSUMAmount' , 'MessageType' , 'PermitId' , 'TouchUser' , 'TouchTime']
        for col_num in range(len(columns)):
            InvoiceWork.write(InvoiceWorkrow_num, col_num,columns[col_num], font_style)


        ItemWork = wb.add_sheet('Item')
        columns = ['Id','ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','Vehicletype','Enginecapacity','Engineuom','Orginregdate','InHAWBOBL','OutHAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','InvoiceNo','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','LSPValue','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage']

        for col_num in range(len(columns)):
            ItemWork.write(ItemWorkRow_num, col_num, columns[col_num], font_style)
        CascWork = wb.add_sheet('Casc')

        columns = ["Id","ItemNo","ProductCode", "Quantity","ProductUOM", "RowNo","CascCode1","CascCode2","CascCode3","PermitId", "MessageType","TouchUser","TouchTime","CascId"]
        for col_num in range(len(columns)):
            CascWork.write(CascRow_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()
        font_style.font.bold = False
        odd_row_style = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue;')
        even_row_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;')

        for Id in Id.split(","):
            self.cursor.execute(f"SELECT * FROM InNonHeaderTbl WHERE Id = '{Id}' ")
            PermitVal = self.cursor.fetchall()
            for row in PermitVal:
                Headerrow_num += 1
                style = odd_row_style if Headerrow_num % 2 == 0 else even_row_style
                for col_num in range(len(row)):
                    headerWork.write(Headerrow_num, col_num,row[col_num], style)

            for permitIDS in PermitVal:
                self.cursor.execute(f"SELECT * FROM InnonContainerDtl WHERE permitId = '{permitIDS[4]}' order by Id,PermitId")
                for row in self.cursor.fetchall():
                    Containerrow_num += 1
                    style = odd_row_style if Containerrow_num % 2 == 0 else even_row_style
                    for col_num in range(len(row)):
                        ContainerWork.write(Containerrow_num, col_num,row[col_num], style)

                self.cursor.execute(f"SELECT * FROM InNonInvoiceDtl WHERE permitId = '{permitIDS[4]}' order by Sno,PermitId")
                Inv = self.cursor.fetchall()
                for row in Inv:
                    InvoiceWorkrow_num += 1
                    style = odd_row_style if InvoiceWorkrow_num % 2 == 0 else even_row_style
                    for col_num in range(len(row)):
                        InvoiceWork.write(InvoiceWorkrow_num, col_num,row[col_num], style)

                self.cursor.execute(f"SELECT * FROM InNonItemDtl WHERE permitId = '{permitIDS[4]}' order by Id,PermitId")
                Ite = self.cursor.fetchall()
                for row in Ite:
                    ItemWorkRow_num += 1
                    style = odd_row_style if ItemWorkRow_num % 2 == 0 else even_row_style
                    for col_num in range(len(row)):
                        ItemWork.write(ItemWorkRow_num, col_num,row[col_num], style)

                self.cursor.execute(f"SELECT * FROM INNONCASCDtl WHERE permitId = '{permitIDS[4]}' order by Id,PermitId")
                Cascd = self.cursor.fetchall()
                for row in Cascd:
                    CascRow_num += 1
                    style = odd_row_style if CascRow_num % 2 == 0 else even_row_style
                    for col_num in range(len(row)):
                        CascWork.write(CascRow_num, col_num,row[col_num], style)



        wb.save(response)

        return response

