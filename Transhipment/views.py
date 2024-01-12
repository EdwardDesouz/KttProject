from django.shortcuts import render 
from KttApp.views import SqlDb
from django.views import View
from KttApp.models import *
import pandas as pd
from django.http import JsonResponse

class TransHome(View):
    def get(self,request):
        context = {
            'CustomiseReport': CustomiseReport.objects.filter(ReportName="IPT", UserName=request.session['Username']).exclude(FiledName='id'),
            'ManageUserMail': ManageUser.objects.filter(Status='Active').order_by('MailBoxId').values_list('MailBoxId', flat=True).distinct(),
            'UserName':request.session['Username']
        }
        return render(request,'Transhipment/Listpage.html',context) 

class TranshList(View,SqlDb):
    def __init__(self): 
        SqlDb.__init__(self)
       
    def get(self,request):
        Username = request.session['Username'] 

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        AccountId = self.cursor.fetchone()[0]

        nowdata = datetime.now()-timedelta(days=60)
        self.cursor.execute("SELECT t1.Id as 'ID', t1.JobId as 'JOB ID', t1.MSGId as 'MSG ID', CONVERT(varchar, t1.TouchTime, 105) AS 'DEC DATE',SUBSTRING(t1.DeclarationType, 1, CHARINDEX(':', t1.DeclarationType) - 1) AS 'DEC TYPE', t1.TouchUser AS 'CREATE', t2.TradeNetMailboxID AS 'DEC ID', CONVERT(varchar, t1.ArrivalDate, 105) AS ETA, t1.PermitNumber AS 'PERMIT NO', t3.Name+' '+t3.Name1 AS 'IMPORTER',STUFF((SELECT distinct(', ' +  US.InHAWBOBL)  FROM TranshipmentItemDtl  US  WHERE US.PermitId = t1.PermitId FOR XML PATH('')), 1, 1, '') 'HAWB',CASE   WHEN  t1.InwardTransportMode = '4 : Air' THEN t1.MasterAirwayBill WHEN t1.InwardTransportMode = '1 : Sea'  THEN t1.OceanBillofLadingNo  ELSE ''  END AS 'MAWB/OBL',t1.LoadingPortCode as POL,t1.MessageType as 'MSG TYPE', t1.InwardTransportMode as TPT,t1.PreviousPermit as 'PRE PMT',t1.GrossReference as 'X REF', t1.InternalRemarks as 'INT REM',t1.Status as 'STATUS' FROM  TranshipmentHeader AS t1 INNER JOIN DeclarantCompany AS t2 ON t1.DeclarantCompanyCode = t2.Code INNER JOIN transImporter AS t3 ON t1.ImporterCompanyCode = t3.Code INNER JOIN ManageUser AS t6 ON t6.UserId=t1.TouchUser  where  t1.Status != 'DEL' and t6.AccountId='" + AccountId + "'  GROUP BY t1.Id, t1.JobId, t1.MSGId, t1.TouchTime, t1.TouchUser,t1.DeclarationType, t1.ArrivalDate, t1.PermitId,t1.PermitNumber, t1.InwardTransportMode, t1.MasterAirwayBill,t1.OceanBillofLadingNo, t1.LoadingPortCode, t1.MessageType, t1.InwardTransportMode,  t1.PreviousPermit,t1.InternalRemarks, t1.Status, t2.TradeNetMailboxID, t3.Name,t3.Name1,t6.AccountId,t1.License ,t1.GrossReference , t1.ReleaseLocation, t1.DischargePort ,t1.RecepitLocation ,t1.OutwardTransportMode ,t1.DeclarningFor ,t2.DeclarantName order by t1.Id Desc")

        # heading = self.cursor.description
        headers = [i[0] for i in self.cursor.description]
        return JsonResponse((pd.DataFrame(list(self.cursor.fetchall()), columns=headers)).to_dict('records'),safe=False)
    
class TranshListnew(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request):
        Username = request.session["Username"]

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))

        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) + 1  FROM TranshipmentHeader WHERE MSGId LIKE '%{}%' AND MessageType = 'TNPDEC' ".format(refDate))
        self.RefId = "%03d" % self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate, AccountId))
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}"

        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"

        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"+ Username+ "'")
        InNonHeadData = self.cursor.fetchone()
        context = {
            "UserName": Username,
            "PermitId": self.PermitIdInNon,
            "JobId": self.JobId,
            "RefId": self.RefId,
            "MsgId": self.MsgId,
            "AccountId": AccountId,
            "LoginStatus": InNonHeadData[0],
            "PermitNumber": "",
            "prmtStatus": "",
            "DateLastUpdated": InNonHeadData[1],
            "MailBoxId": InNonHeadData[2],
            "SeqPool": InNonHeadData[3],
            "StartSequence": InNonHeadData[4],
            "TradeNetMailboxID": InNonHeadData[5],
            "DeclarantName": InNonHeadData[6],
            "DeclarantCode": InNonHeadData[7],
            "DeclarantTel": InNonHeadData[8],
            "CRUEI": InNonHeadData[9],
            "Code": InNonHeadData[10],
            "name": InNonHeadData[11],
            "name1": InNonHeadData[12],
            "DeclarationType": CommonMaster.objects.filter(TypeId=18, StatusId=1).order_by("Name"),
            "CargoType": CommonMaster.objects.filter(TypeId=2, StatusId=1),
            "OutWardTransportMode": CommonMaster.objects.filter(TypeId=3, StatusId=1).order_by("Name"),
            "DeclaringFor": CommonMaster.objects.filter(TypeId=81, StatusId=1).order_by("Name"),
            "BgIndicator": CommonMaster.objects.filter(TypeId=4, StatusId=1).order_by("Name"),
            "DocumentAttachmentType": CommonMaster.objects.filter(TypeId=5, StatusId=1).order_by("Name"),
            "CoType": CommonMaster.objects.filter(TypeId=16, StatusId=1).order_by("Name"),
            "CertificateType": CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by("Name"),
            "Currency": Currency.objects.filter().order_by("Currency"),
            "Container": CommonMaster.objects.filter(TypeId=6, StatusId=1).order_by("Name"),
            "TotalOuterPack": CommonMaster.objects.filter(TypeId=10, StatusId=1).order_by("Name"),
            "InvoiceTermType": CommonMaster.objects.filter(TypeId=7, StatusId=1).order_by("Name"),
            "Making": CommonMaster.objects.filter(TypeId=12, StatusId=1).order_by("Name"),
            "VesselType": CommonMaster.objects.filter(TypeId=14, StatusId=1).order_by("Name"),
        }
        return render(request, "Transhipment/Newpage.html", context)


class TranshItem(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
    def get(self,request,Permitid):
        return JsonResponse({'message':'Item Page load item'})
    
    def post(self,request):
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TranshipmentItemDtl'"
        self.cursor.execute(query)
            
        result = self.cursor.fetchall()
        for i in result:
            print(i[0])
        return JsonResponse({'message':'Item Saved'}) 