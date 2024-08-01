from django.shortcuts import render,redirect
from django.views import View
from KttApp.models import *
from KttApp.views import SqlDb
from datetime import *
import pandas as pd
from django.http import JsonResponse
from django.http import HttpResponse
import os
import json
from datetime import datetime
import xlwt

def coolist(request):
    # context={}
    # Username=request.session["Username"]
    # context.update({"Username":Username})
    return render (request,'coo/coolist.html',{
        'CustomiseReport': CustomiseReport.objects.filter(ReportName="CODEC", UserName=request.session['Username']).exclude(FiledName='id'),
        'ManageUserMail': ManageUser.objects.filter(Status='Active').order_by('MailBoxId').values_list('MailBoxId', flat=True).distinct(),
        'UserName':request.session['Username']
        })



class coolistTable(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):
        Username=request.session["Username"]

        self.cursor.execute(
             "SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username)
        )
        AccountId=self.cursor.fetchone()[0]
        # print('list AccountId:',AccountId)

        nowdata = datetime.now() - timedelta(days=60)
        self.cursor.execute(
        
                "SELECT t1.Id as 'ID', t1.JobId as 'JOB ID', t1.MSGId as 'MSG ID',CONVERT(varchar, t1.TouchTime, 105) AS 'DEC DATE', t1.ApplicationType AS 'DEC TYPE', t1.TouchUser AS 'CREATE', t2.TradeNetMailboxID AS 'DEC ID', CONVERT(varchar, t1.DepartureDate, 105) AS ETD, t1.PermitNumber AS 'PERMIT NO',  t3.Name+' '+t3.Name1 AS 'EXPORTER', t1.DischargePort as POD,CASE   WHEN  t1.COType = '--Select--' THEN '-'    WHEN t1.COType != ''  THEN SUBSTRING(t1.COType,0,3)    ELSE ''  END  as 'CO TYPE' ,CASE   WHEN  t1.CerDtlType1 = '--Select--' THEN '-'    WHEN t1.CerDtlType1 != ''  THEN SUBSTRING(t1.CerDtlType1,0,3)    ELSE ''  END  as 'CERT TYPE',t1.CertificateNumber as 'CERT NO', t1.MessageType as 'MSG TYPE',t1.OutwardTransportMode as TPT, t1.PreviousPermitNo as 'PRE PMT',t1.GrossReference as 'X REF', t1.InternalRemarks as 'INT REM', t1.Status as 'STATUS'  FROM  COHeaderTbl AS t1 left JOIN   DeclarantCompany AS t2   ON t1.DeclarantCompanyCode = t2.Code   left JOIN COExporter AS t3   ON t1.ExporterCompanyCode = t3.Code  left JOIN ManageUser AS t6 ON t6.UserId=t1.TouchUser  where  t6.AccountId='"
                + AccountId
                + "'and convert(varchar,t1.TouchTime,111)>='"
                + nowdata.strftime("%Y/%m/%d")
                + "' GROUP BY t1.Id, t1.JobId, t1.MSGId, t1.TouchTime, t1.TouchUser, t1.ApplicationType, t1.DepartureDate, t1.PermitId,t1.PermitNumber,t1.PreviousPermitNo, t1.OutwardTransportMode, t1.DischargePort, t1.MessageType, t1.OutwardTransportMode, t1.PreviousPermitNo, t1.InternalRemarks, t1.Status, t2.TradeNetMailboxID,t2.DeclarantName , t3.Code,t6.AccountId,t3.Name,t3.Name1,t1.CerDtlType1,t1.COType,t1.CurrencyCode,t1.GrossReference  ,t1.OutwardTransportMode ,t1.DeclarningFor,t1.CertificateNumber order by t1.Id Desc"
                ) # where t1.Status !=DEL

        self.HeaderInNon = self.cursor.fetchall()

        result = (
            pd.DataFrame(
                list(self.HeaderInNon),
                columns=[
                    "ID",
                    "JOBID",
                    "MSGID",
                    "DECDATE",
                    "DECTYPE",
                    "CREATE",
                    "DECID",
                    "ETD",
                    "PERMITNO",
                    "EXPORTER",
                    "POD",
                    "COTYPE",
                    "CERTTYPE",
                    "CERTNO",
                    "MSGTYPE",
                    "TPT",
                    "PREPMT",
                    "XREF",
                    "INTREM",
                    "STATUS",
                ],
                
            )
            
        ).to_dict("records")
       

        # print('below result is:',result)
        # print("CoType:",result.COTYPE)
        # for row in result:
        #     print("CoType:", row["COTYPE"])

        # print("CoType:", result[0]["COTYPE"])
       

        return JsonResponse(result, safe=False)
        




class coolistnew(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

        
    def get(self,request):
        Username = request.session["Username"]
        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")
        currentDate = datetime.now().strftime("%d/%m/%Y")
    

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))

        AccountId = self.cursor.fetchone()[0]
        

        self.cursor.execute( "SELECT COUNT(*) + 1  FROM COHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'COODEC' ".format(refDate))
        self.RefId = "%03d" % self.cursor.fetchone()[0]
   

        self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate, AccountId))
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}"

        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"

        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        print("PermitId:", self.PermitIdInNon)
        print("JobId:", self.JobId)
        print("RefId:",self.RefId)
        print('accountid:',AccountId)
    

        self.cursor.execute(
        "select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"
        + Username
        + "'"
         )
        InNonHeadData = self.cursor.fetchone()
        context={
        "UserName": Username,
        "PermitId":self.PermitIdInNon,
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
        "OutwardTransportMode":CommonMaster.objects.filter(TypeId=3, StatusId=1).order_by('Name'),
        "DeclaringFor":CommonMaster.objects.filter(TypeId=80, StatusId=1).order_by('Name'),
        "DocumentAttachmentType": CommonMaster.objects.filter(TypeId=5, StatusId=1).order_by("Name"),
        "cotypeMode":CommonMaster.objects.filter(TypeId=16, StatusId=1).order_by('Name'),
        "CertificateMode1":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),
        "CertificateMode2":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),
        "Currency": Currency.objects.filter().order_by("Currency"),
        "FinalDestinationCountry":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),  
        "HsQuantity":CommonMaster.objects.filter(TypeId=10, StatusId=1).order_by('Name'),   
        "CurrUnitPrice":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'), 
        "Country": COUNTRY.objects.all().order_by("CountryCode"),
        "CurrentDate": currentDate 
    }  
        print('New:',AccountId)
        return render (request,'coo/coonew.html',context)


class CooHscode(View, SqlDb):
    def get(self, request):
        SqlDb.__init__(self)
        self.cursor.execute("select * from HSCode")
        headers = [i[0] for i in self.cursor.description]
        return JsonResponse(
            {
                "hscode": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )


class ExporterUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT * FROM CoExporter WHERE Status = 'Active' "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "exporter": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)
    
    
class TransportDeclarantUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT * FROM CoExporter WHERE Status = 'Active' "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "declarant": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)


class TransportOCAgentUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT * FROM COOutwardCarrierAgent WHERE Status = 'Active' "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "outwardcarrier": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)


class TransportFforwarderUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT * FROM COFreightForwarder WHERE Status = 'Active' "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "freforwarder": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)


class TransportConsigneUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT * FROM COConsignee WHERE Status = 'Active' "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "consignee": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )

        # print("Party Context:", self.Partycontext)
    def get(self, request):
        return JsonResponse(self.Partycontext)


class TransportMFacturarUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT * FROM COManufacturer WHERE Status = 'Active' "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "Mfactutrer": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )
        # print("Party Context:", self.Partycontext)
    def get(self, request):
        return JsonResponse(self.Partycontext)

# Cargo page DISCHARGE PORT

class CargoDiscargeportUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            # "SELECT * FROM HSCode WHERE Status = 'Active' "
            "SELECT * FROM LoadingPort "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "Dcportcode": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)
    
# Item page HSCODE  

class ItemHSCODEUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            # "SELECT * FROM HSCode WHERE Status = 'Active' "
            "SELECT * FROM HSCode "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "ItemHscode": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)
    

    # Item page COOCODE  
    

class ItemCOOUrl(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
         
            "SELECT * FROM Country "
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "CooCode": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=headers
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)
    

class CooLoad(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

        self.cursor.execute("SELECT  Currency,CurrencyRate FROM Currency ORDER BY Currency")
        self.currency = self.cursor.fetchall()

    def get(self,request):
            return JsonResponse({

                "currency" : (pd.DataFrame(list(self.currency), columns=["Currency", "CurrencyRate"])).to_dict('records'), 
            })   
    
# class ItemSave(View,SqlDb):
#     def __init__(self):
#         SqlDb.__init__(self)

#     def get(self,request,Permit):
#         # self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(request.session['Username'] ))
#         # AccountId = self.cursor.fetchone()[0]
#         # print('accountiditemsave:',AccountId)

        
#         query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'COHeaderTbl'"
#         self.cursor.execute(query) 
#         result = self.cursor.fetchall()
#         context = {}
#         self.cursor.execute(
#             f"select * from COItemDtl WHERE PermitId = '{Permit}' ORDER BY ItemNo"
#         )
#         print('permit id is:',Permit)
      
#         headers = [i[0] for i in self.cursor.description]
#         context.update(
#             {
#                 "item": (
#                     pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
#                 ).to_dict("records")
#             }
#         )
#         return JsonResponse(context)

#     def post(self,request):
#         ItemNo = request.POST.get('ItemNo')
#         PermitId = request.POST.get('PermitId')
#         MessageType = request.POST.get('MessageType')
#         HSCode = request.POST.get('HSCode')
#         Description = request.POST.get('Description')
#         Contry = request.POST.get('Contry')
#         UnitPrice = request.POST.get('UnitPrice')
#         UnitPriceCurrency = request.POST.get('UnitPriceCurrency')
#         ExchangeRate = "0.00"
#         SumExchangeRate = "0.00"
#         TotalLineAmount = request.POST.get('TotalLineAmount')
#         CIFFOB = request.POST.get('CIFFOB')
#         InvoiceQty = request.POST.get('InvoiceQty')
#         HSQTY = request.POST.get('HSQTY')
#         HSUOM = request.POST.get('HSUOM')
#         ShippingMark = request.POST.get('ShippingMark')
#         CerItemQty = request.POST.get('CerItemQty')
#         CerItemUOM = request.POST.get('CerItemUOM')
#         ManfCostDate = request.POST.get('ManfCostDate')
#         TextileCat = request.POST.get('TextileCat')
#         TextileQuotaQty = "0.00"
#         TextileQuotaQtyUOM = request.POST.get('TextileQuotaQtyUOM')
#         ItemValue = request.POST.get('ItemValue')
#         InvoiceNumber = request.POST.get('InvoiceNumber')
#         InvoiceDate = request.POST.get('InvoiceDate')
#         HSOnCer = request.POST.get('HSOnCer')
#         OriginCriterion = request.POST.get('OriginCriterion')
#         PerOrgainCRI = request.POST.get('PerOrgainCRI')
#         CertificateDes = request.POST.get('CertificateDes')
#         Touch_user = request.session["Username"]
#         TouchTime = datetime.now() 
#         Val = (ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime)
#         message = ''
#         try:
#             self.cursor.execute(f"select * from COItemDtl WHERE PermitId = '{PermitId}' and ItemNo='{ItemNo}' ")
#             result=self.cursor.fetchall()
#             print('result is:',result)
#             print('length of result:',len(result))
#             # print('perimitid:',PermitId)

#             if len(result) == 0:
#                 Qry = "INSERT INTO COItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#                 self.cursor.execute(Qry,Val)
               
#             else:     # Update Query in the Coo Item page when we click the edit icon the updated data will added
#                 print("its a update")
#                 Qry = f"Update COItemDtl set ItemNo = %s,PermitId = %s,MessageType = %s,HSCode = %s,Description = %s,Contry = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,CIFFOB = %s,InvoiceQty = %s,HSQTY = %s,HSUOM = %s,ShippingMark = %s,CerItemQty = %s,CerItemUOM = %s,ManfCostDate = %s,TextileCat = %s,TextileQuotaQty = %s,TextileQuotaQtyUOM = %s,ItemValue = %s,InvoiceNumber = %s,InvoiceDate = %s,HSOnCer = %s,OriginCriterion = %s,PerOrgainCRI = %s,CertificateDes = %s,Touch_user = %s,TouchTime = %s"
#                 self.cursor.execute(Qry,Val)
#             self.conn.commit()
#             message = "Saved Item"         
#         except Exception as e:
#             print("Error : ",e)
#             message = "Did Not saved "
#         context = {}
#         self.cursor.execute(
#             f"select * from COItemDtl WHERE PermitId = '{PermitId}' ORDER BY ItemNo"
#         )
#         headers = [i[0] for i in self.cursor.description]
#         context.update(
#             {
#                 "item": (
#                     pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
#                 ).to_dict("records")
#             }
#         )
#         context['message'] = message
#         return JsonResponse(context)
    
class ItemSave(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request, Permit):
        context = {}
        self.cursor.execute(
            f"select * from COItemDtl WHERE PermitId = '{Permit}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "item": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        return JsonResponse(context)

    def post(self, request):
        context = {}
        message = ""

        self.cursor.execute(
            f"SELECT ItemNo,PermitId FROM COItemDtl WHERE ItemNo = '{request.POST.get('ItemNo')}' AND PermitId = '{request.POST.get('PermitId')}' "
        )
        if self.cursor.fetchone() is None:
            try:
                Qry = "INSERT INTO COItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (
                    request.POST.get("ItemNo"),
                    request.POST.get("PermitId"),
                    request.POST.get("MessageType"),          
                    request.POST.get("HSCode"),
                    request.POST.get("Description"),
                    request.POST.get("Contry"),
                    request.POST.get("UnitPrice"),
                    request.POST.get("UnitPriceCurrency"),
                    request.POST.get("ExchangeRate"),
                    request.POST.get("SumExchangeRate"),
                    request.POST.get("TotalLineAmount"),
                    request.POST.get("CIFFOB"),
                    request.POST.get("InvoiceQty"),
                    request.POST.get("HSQTY"),
                    request.POST.get("HSUOM"),
                    request.POST.get("ShippingMark"),
                    request.POST.get("CerItemQty"),
                    request.POST.get("CerItemUOM"),
                    request.POST.get("ManfCostDate"),
                    request.POST.get("TextileCat"),
                    request.POST.get("TextileQuotaQty"),
                    request.POST.get("TextileQuotaQtyUOM"),
                    request.POST.get("ItemValue"),
                    request.POST.get("InvoiceNumber"),
                    request.POST.get("InvoiceDate"),
                    request.POST.get("HSOnCer"),
                    request.POST.get("OriginCriterion"),
                    request.POST.get("PerOrgainCRI"),
                    request.POST.get("CertificateDes"),
                    str(request.session["Username"]).upper(),
                    datetime.now(),
                )
                self.cursor.execute(Qry, val)
                message = "Inserted Successfully...!"
            except Exception as e:
                message = "Did not saved...!"
        else:
            try:
                Val = (
                    request.POST.get("ItemNo"),
                    request.POST.get("PermitId"),
                    request.POST.get("MessageType"),          
                    request.POST.get("HSCode"),
                    request.POST.get("Description"),
                    request.POST.get("Contry"),
                    request.POST.get("UnitPrice"),
                    request.POST.get("UnitPriceCurrency"),
                    request.POST.get("ExchangeRate"),
                    request.POST.get("SumExchangeRate"),
                    request.POST.get("TotalLineAmount"),
                    request.POST.get("CIFFOB"),
                    request.POST.get("InvoiceQty"),
                    request.POST.get("HSQTY"),
                    request.POST.get("HSUOM"),
                    request.POST.get("ShippingMark"),
                    request.POST.get("CerItemQty"),
                    request.POST.get("CerItemUOM"),
                    request.POST.get("ManfCostDate"),
                    request.POST.get("TextileCat"),
                    request.POST.get("TextileQuotaQty"),
                    request.POST.get("TextileQuotaQtyUOM"),
                    request.POST.get("ItemValue"),
                    request.POST.get("InvoiceNumber"),
                    request.POST.get("InvoiceDate"),
                    request.POST.get("HSOnCer"),
                    request.POST.get("OriginCriterion"),
                    request.POST.get("PerOrgainCRI"),
                    request.POST.get("CertificateDes"),
                    str(request.session["Username"]).upper(),
                    datetime.now(),
                )
                PermitId = request.POST.get("PermitId")
                ItemNo = request.POST.get("ItemNo")
                Qry = f"UPDATE COItemDtl SET ItemNo = %s,PermitId = %s,MessageType = %s,HSCode = %s,Description = %s,Contry = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,CIFFOB = %s,InvoiceQty = %s,HSQTY = %s,HSUOM = %s,ShippingMark = %s,CerItemQty = %s,CerItemUOM = %s,ManfCostDate = %s,TextileCat = %s,TextileQuotaQty = %s,TextileQuotaQtyUOM = %s,ItemValue = %s,InvoiceNumber = %s,InvoiceDate = %s,HSOnCer = %s,OriginCriterion = %s,PerOrgainCRI = %s,CertificateDes = %s,Touch_user = %s,TouchTime = %s  WHERE PermitId = '{PermitId}' AND ItemNo = '{ItemNo}'  "
                self.cursor.execute(Qry, Val)
                message = "Updated Successfully...!"
            except Exception as e:
                message = "Did not Updated"
                
        self.conn.commit()

        context.update({"message": message})

        self.cursor.execute(
            f"select * from COItemDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "item": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        for item in context["item"]:
            print("Row of the values:")
            for key, value in item.items():
                print(f"{key}: {(value)}")
        return JsonResponse(context)
    

    

class CooItemDelete(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):
        data=json.loads(request.GET.get("ItemNo"))
        permitid=request.GET.get('PermitId')

        # for i in data:
        #     print(i)

        values_str = ", ".join(map(str, data))

        query1 = f"DELETE FROM COItemDtl WHERE ItemNo IN ({values_str}) AND PermitId = '{permitid}' "
        self.cursor.execute(query1)

        context = {}
        message = ''

        self.cursor.execute(
            f"select * from COItemDtl WHERE PermitId = '{permitid}' ORDER BY ItemNo"
        )
     


        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "item": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        context['message'] = message
        return JsonResponse(context)
    

class SavePermit(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

        

    def post(self,request):
      
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'COItemDtl'"
        self.cursor.execute(query)

        result = self.cursor.fetchall()
        # for i in result:
           
        # #    print('results are:',i)
      
        Refid = request.POST.get('Refid')
        JobId = request.POST.get('JobId')
        MSGId = request.POST.get('MSGId')
        PermitId = request.POST.get('PermitId')
        TradeNetMailboxID = request.POST.get('TradeNetMailboxID')
        MessageType = request.POST.get('MessageType')
        ApplicationType = request.POST.get('ApplicationType')
        PreviousPermitNo = request.POST.get('PreviousPermitNo')
        OutwardTransportMode = request.POST.get('OutwardTransportMode')
        ReferenceDocuments = request.POST.get('ReferenceDocuments')
        COType = request.POST.get('COType')
        CerDtlType1 = request.POST.get('CerDtlType1')
        CerDtlCopy1 = request.POST.get('CerDtlCopy1')
        CerDtlType2 = request.POST.get('CerDtlType2')
        CerDtlCopy2 = request.POST.get('CerDtlCopy2')
        CurrencyCode = request.POST.get('CurrencyCode')
        AdditionalCer = request.POST.get('AdditionalCer')
        TransportDtl = request.POST.get('TransportDtl')
        PerferenceContent = request.POST.get('PerferenceContent')
        DeclarantCompanyCode = request.POST.get('DeclarantCompanyCode')
        ExporterCompanyCode = request.POST.get('ExporterCompanyCode')
        OutwardCarrierAgentCode = request.POST.get('OutwardCarrierAgentCode')
        FreightForwarderCode = request.POST.get('FreightForwarderCode')
        CONSIGNEECode = request.POST.get('CONSIGNEECode')
        Manufacturer = request.POST.get('Manufacturer')
        DepartureDate = request.POST.get('DepartureDate')
        DischargePort = request.POST.get('DischargePort')
        FinalDestinationCountry = request.POST.get('FinalDestinationCountry')
        OutVoyageNumber = request.POST.get('OutVoyageNumber')
        OutVesselName = request.POST.get('OutVesselName')
        OutConveyanceRefNo = request.POST.get('OutConveyanceRefNo')
        OutTransportId = request.POST.get('OutTransportId')
        OutFlightNO = request.POST.get('OutFlightNO')
        OutAircraftRegNo = request.POST.get('OutAircraftRegNo')
        TotalOuterPack = request.POST.get('TotalOuterPack')
        TotalOuterPackUOM = request.POST.get('TotalOuterPackUOM')
        TotalGrossWeight = request.POST.get('TotalGrossWeight')
        TotalGrossWeightUOM = request.POST.get('TotalGrossWeightUOM')
        DeclareIndicator = request.POST.get('DeclareIndicator')
        NumberOfItems = request.POST.get('NumberOfItems')
        InternalRemarks = request.POST.get('InternalRemarks')
        TradeRemarks = request.POST.get('TradeRemarks')
        Status = request.POST.get('Status')
        TouchUser = request.POST.get('TouchUser')
        TouchTime = request.POST.get('TouchTime')
        prmtStatus = request.POST.get('prmtStatus')
        PermitNumber = request.POST.get('PermitNumber')
        EntryYear = request.POST.get('EntryYear')
        Percomwealth = request.POST.get('Percomwealth')
        Gpsdonorcountry = request.POST.get('Gpsdonorcountry')
        Additionalrecieptant = request.POST.get('Additionalrecieptant')
        GrossReference = request.POST.get('GrossReference')
        DeclarningFor = request.POST.get('DeclarningFor')
        CertificateNumber = request.POST.get('CertificateNumber')
        MRDate = request.POST.get('MRDate')
        MRTime = request.POST.get('MRTime')
        

        # print("This is a new permit datas")

        Val = (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,ApplicationType,PreviousPermitNo,OutwardTransportMode,ReferenceDocuments,COType,CerDtlType1,CerDtlCopy1,CerDtlType2,CerDtlCopy2,CurrencyCode,AdditionalCer,TransportDtl,PerferenceContent,DeclarantCompanyCode,ExporterCompanyCode,OutwardCarrierAgentCode,FreightForwarderCode,CONSIGNEECode,Manufacturer,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,DeclareIndicator,NumberOfItems,InternalRemarks,TradeRemarks,Status,TouchUser,TouchTime,prmtStatus,PermitNumber,EntryYear,Percomwealth,Gpsdonorcountry,Additionalrecieptant,GrossReference,DeclarningFor,CertificateNumber,MRDate,MRTime)
        # for i in Val:
        #     print(['type:',type(i)],i)
        #below code is working   
        message=''
        try:
            self.cursor.execute(f"select * from COHeaderTbl WHERE PermitId = '{PermitId}'  ")
            print('perimitid:',PermitId)
            result=self.cursor.fetchall()
            print("The Result Is : ",result)
            # print('result:',len(result))

            if len(result)==0:
                print('yes length is 0')
                Qry="INSERT INTO COHeaderTbl(Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,ApplicationType,PreviousPermitNo,OutwardTransportMode,ReferenceDocuments,COType,CerDtlType1,CerDtlCopy1,CerDtlType2,CerDtlCopy2,CurrencyCode,AdditionalCer,TransportDtl,PerferenceContent,DeclarantCompanyCode,ExporterCompanyCode,OutwardCarrierAgentCode,FreightForwarderCode,CONSIGNEECode,Manufacturer,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,DeclareIndicator,NumberOfItems,InternalRemarks,TradeRemarks,Status,TouchUser,TouchTime,prmtStatus,PermitNumber,EntryYear,Percomwealth,Gpsdonorcountry,Additionalrecieptant,GrossReference,DeclarningFor,CertificateNumber,MRDate,MRTime)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(Qry,Val)
                self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(request.POST.get('TouchUser')))
                AccountId = self.cursor.fetchone()[0]
                

                # self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{request.POST.get("PermitId")}','{request.POST.get("AccountId")}','{request.POST.get("MSGId")}','{str(request.session['Username']).upper()}','{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')")
                self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{PermitId}','{MessageType}','{AccountId}','{MSGId}','{TouchUser}','{TouchTime}')")
               
                print('Inserted values:', Val) 
                

            else:
                print('its a update')
                Qry=f"Update COHeaderTbl set Refid=%s,JobId=%s,MSGId=%s,PermitId=%s,TradeNetMailboxID=%s,MessageType=%s,ApplicationType=%s,PreviousPermitNo=%s,OutwardTransportMode=%s,ReferenceDocuments=%s,COType=%s,CerDtlType1=%s,CerDtlCopy1=%s,CerDtlType2=%s,CerDtlCopy2=%s,CurrencyCode=%s,AdditionalCer=%s,TransportDtl=%s,PerferenceContent=%s,DeclarantCompanyCode=%s,ExporterCompanyCode=%s,OutwardCarrierAgentCode=%s,FreightForwarderCode=%s,CONSIGNEECode=%s,Manufacturer=%s,DepartureDate=%s,DischargePort=%s,FinalDestinationCountry=%s,OutVoyageNumber=%s,OutVesselName=%s,OutConveyanceRefNo=%s,OutTransportId=%s,OutFlightNO=%s,OutAircraftRegNo=%s,TotalOuterPack=%s,TotalOuterPackUOM=%s,TotalGrossWeight=%s,TotalGrossWeightUOM=%s,DeclareIndicator=%s,NumberOfItems=%s,InternalRemarks=%s,TradeRemarks=%s,Status=%s,TouchUser=%s,TouchTime=%s,prmtStatus=%s,PermitNumber=%s,EntryYear=%s,Percomwealth=%s,Gpsdonorcountry=%s,Additionalrecieptant=%s,GrossReference=%s,DeclarningFor=%s,CertificateNumber=%s,MRDate=%s,MRTime=%s WHERE PermitId = '{PermitId}'"
                self.cursor.execute(Qry,Val)
            print('Updated values:', Val) 
            self.conn.commit()
            message = "Saved Item"
           

        except Exception as e:
            print("Error : ",e)
            message = "Did Not saved "
        context={}

        self.cursor.execute(
            f"select * from COHeaderTbl WHERE PermitId = '{PermitId}' "
        )
        headers=[i[0] for i in self.cursor.description]
        context.update(
            {
                "Item": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        context['message'] = message
        return JsonResponse(context)
      
         


class CooEdit(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request,id):
        Username = request.session["Username"]
        # print("Username:",Username)

        self.cursor.execute(f"SELECT * FROM COHeaderTbl WHERE id = {id}")
        headers = [i[0] for i in self.cursor.description]
        outAll = list(self.cursor.fetchall())
        # print("outAll:",outAll)


        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))

        AccountId = self.cursor.fetchone()[0]
        # print("AccountId:",AccountId)

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"+ Username+ "'")
        InNonHeadData = self.cursor.fetchone()
        # print("InNonHeadData:",InNonHeadData)
        context = {
            "UserName": Username,
            "PermitId": outAll[0][4],
            "JobId": outAll[0][2],
            "RefId": outAll[0][1],
            "MsgId": outAll[0][3],
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
            "OutwardTransportMode":CommonMaster.objects.filter(TypeId=3, StatusId=1).order_by('Name'),
            "DeclaringFor":CommonMaster.objects.filter(TypeId=80, StatusId=1).order_by('Name'),
            "cotypeMode":CommonMaster.objects.filter(TypeId=16, StatusId=1).order_by('Name'),
            "CertificateMode1":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),
            "CertificateMode2":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),
            "Currency": Currency.objects.filter().order_by("Currency"),
            "FinalDestinationCountry":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),  
            "HsQuantity":CommonMaster.objects.filter(TypeId=10, StatusId=1).order_by('Name'),   
            "CurrUnitPrice":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'), 
            "Country": COUNTRY.objects.all().order_by("CountryCode"),
            
        }
        
        context.update({
            "CooData" : (pd.DataFrame(outAll, columns=headers)).to_dict("records"),
 
        }) 
        for item in context["CooData"]:
            print("Row:")
            for key, value in item.items():
                print(f"  {key}: {value}")
 
        # print("cotypeMode:", outAll[0]["cotypeMode"])
        # print("CoType:", list(context["cotypeMode"].values_list("Name", flat=True)))
        return render(request,"coo/coonew.html", context)
    
class CooListDelete(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,id):
        # print("The Id is  : ",id)
        self.cursor.execute("UPDATE COHeaderTbl SET STATUS = 'DEL' WHERE Id = '{}' ".format(id))
        self.conn.commit()
        return JsonResponse({'  ' : 'Deleted : '+str(id)})
    

# This below code is for mac:

def CooItemExcelDownload(request):
    downloads_dir = os.path.expanduser("~/Downloads")
    file_path = os.path.join(downloads_dir, "CoExcelTemplate.xlsx")

    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            response = HttpResponse(file.read())
            response["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            response["Content-Disposition"] = "attachment; filename=CoExcelTemplate.xlsx"
            return response
    else:
        return HttpResponse("The file does not exist.")
    
# Party page + button functions for loading and add the values
class PartyLoad(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM CoExporter WHERE status = 'Active' ORDER BY Name ")
        self.importer = self.cursor.fetchall()

        self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM COOutwardCarrierAgent WHERE status = 'Active' ORDER BY Name")
        self.exporter = self.cursor.fetchall()

        self.cursor.execute("SELECT Code,Name,Name1,CRUEI FROM COFreightForwarder WHERE status = 'Active' ORDER BY Name")
        self.inward = self.cursor.fetchall()

        self.cursor.execute("SELECT ConsigneeCode,ConsigneeName,ConsigneeName1,ConsigneeCRUEI,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSub,ConsigneeSubDivi,ConsigneePostal,ConsigneeCountry FROM COConsignee ORDER BY ConsigneeName")
        self.consign = self.cursor.fetchall() 

        self.cursor.execute("SELECT ManufacturerCode,ManufacturerName,ManufacturerName1,ManufacturerCRUEI,ManufacturerAddress,ManufacturerAddress1,ManufacturerCity,ManufacturerSubDivi,ManufacturerSub,ManufacturerPostal,ManufacturerCountry FROM COManufacturer where Status = 'Active' ")
        self.Manufact = self.cursor.fetchall() 

    def post(self, request):
        DbName = request.POST.get("ModelName")
        if DbName == "ExporterModel":
            Qry = "select code from COExporter where code = %s"
            val = (request.POST.get("code"),)
            self.cursor.execute(Qry, val)

            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO COExporter(code,cruei,name,name1,status,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val = (
                    request.POST.get("code"),
                    request.POST.get("cruei"),
                    request.POST.get("name"),
                    request.POST.get("name1"),
                    "Active",
                    request.POST.get("TouchUser"),
                    request.POST.get("TouchTime"),
                )
                self.cursor.execute(Qry, val)
                self.conn.commit()
                self.cursor.execute(
                    "SELECT Code,Name,Name1,CRUEI FROM COExporter WHERE status = 'Active' "
                )
                importer = self.cursor.fetchall()

                return JsonResponse(
                    {
                        "Result": "Exporter Saved ...!",
                        "Exporter": (
                            pd.DataFrame(
                                list(importer),
                                columns=["Code", "Name", "Name1", "CRUEI"],
                            )
                        ).to_dict("records"),
                    }
                )
            else:
                return JsonResponse({"Result": " Yes Exporter Code Already Exists ...!"})

        elif DbName == "OutwardModel":
            Qry = "select code from COOutwardCarrierAgent where code = %s"
            val = (request.POST.get("code"),)
            self.cursor.execute(Qry, val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO COOutwardCarrierAgent(code,cruei,name,name1,status,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s) "
                Val = (
                    request.POST.get("code"),
                    request.POST.get("cruei"),
                    request.POST.get("name"),
                    request.POST.get("name1"),
                    "Active",
                    request.POST.get("TouchUser"),
                    request.POST.get("TouchTime"),
                )
                self.cursor.execute(Qry, Val)
                self.conn.commit()

                self.cursor.execute(
                    "SELECT Code,Name,Name1,CRUEI FROM COOutwardCarrierAgent WHERE status = 'Active' "
                )
                return JsonResponse(
                    {
                        "Result": "OutwardCarrierAgent Saved ...!",
                        "Outward": (
                            pd.DataFrame(
                                list(self.cursor.fetchall()),
                                columns=["Code", "Name", "Name1", "CRUEI"],
                            )
                        ).to_dict("records"),
                    }
                )
            else:
                return JsonResponse(
                    {"Result": " Yes OutwardCarrierAgent Code Already Exists ...!"}
                )

        elif DbName == "FreightModel":
            Qry = "select code from COFreightForwarder where code = %s"
            Val = (request.POST.get("code"),)
            self.cursor.execute(Qry, Val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO COFreightForwarder(code,cruei,name,name1,status,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s) "
                Val = (
                    request.POST.get("code"),
                    request.POST.get("cruei"),
                    request.POST.get("name"),
                    request.POST.get("name1"),
                    "Active",
                    request.POST.get("TouchUser"),
                    request.POST.get("TouchTime"),
                )
                self.cursor.execute(Qry, Val)
                self.conn.commit()
                self.cursor.execute(
                    "SELECT Code,Name,Name1,CRUEI FROM COFreightForwarder WHERE status = 'Active' "
                )
                fright = self.cursor.fetchall()
                
                return JsonResponse(
                    {
                        "Result": "FreightForwarder Saved ...!",
                        "FreightForwarder": (
                            pd.DataFrame(
                                list(fright), columns=["Code", "Name", "Name1", "CRUEI"]
                            )
                        ).to_dict("records"),
                    }
                )
            else:
                return JsonResponse(
                    {"Result": " Yes FreightForwarder Code Already Exists ...!"}
                )

       

        elif DbName == "CONSIGNE":
                ConQry = "SELECT ConsigneeCode FROM COConsignee where ConsigneeCode=%s"
                self.cursor.execute(ConQry,(request.POST.get("ConsigneeCode"),))
                val = self.cursor.fetchone()
                if val:
                    return JsonResponse({"Result" : " Yes THIS CODE IS ALREADY EXISTS ...!",  "consign" : (pd.DataFrame(list(self.consign), columns=["ConsigneeCode", "ConsigneeName", "ConsigneeName1","ConsigneeCRUEI","ConsigneeAddress", "ConsigneeAddress1", "ConsigneeCity","ConsigneeSub","ConsigneeSubDivi","ConsigneePostal","ConsigneeCountry"])).to_dict('records'),})
                else:
                    Qry = ("INSERT INTO COConsignee (ConsigneeCode,ConsigneeName,ConsigneeName1,ConsigneeCRUEI,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSub,ConsigneeSubDivi,ConsigneePostal,ConsigneeCountry,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    val = (request.POST.get("ConsigneeCode"),request.POST.get("ConsigneeName"),request.POST.get("ConsigneeName1"),request.POST.get("ConsigneeCRUEI"),request.POST.get("ConsigneeAddress"),request.POST.get("ConsigneeAddress1"),request.POST.get("ConsigneeCity"),
                            request.POST.get("ConsigneeSub"),request.POST.get("ConsigneeSubDivi"),request.POST.get("ConsigneePostal"),request.POST.get("ConsigneeCountry"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),"Active")
                    self.cursor.execute(Qry,val)
                    self.conn.commit()
                    self.cursor.execute("SELECT ConsigneeCode,ConsigneeName,ConsigneeName1,ConsigneeCRUEI,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSub,ConsigneeSubDivi,ConsigneePostal,ConsigneeCountry FROM COConsignee ORDER BY ConsigneeName")
                    self.consign = self.cursor.fetchall()
                    print("Value inserted successfully:", val)
                    return JsonResponse({
                        "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                        "consign" : (pd.DataFrame(list(self.consign), columns=["ConsigneeCode", "ConsigneeName", "ConsigneeName1","ConsigneeCRUEI","ConsigneeAddress", "ConsigneeAddress1", "ConsigneeCity","ConsigneeSub","ConsigneeSubDivi","ConsigneePostal","ConsigneeCountry"])).to_dict('records'),
                    })
       

        elif DbName == "MANFACTUTRER":
                ConQry = "SELECT ManufacturerCode FROM COManufacturer where ManufacturerCode=%s"
                self.cursor.execute(ConQry,(request.POST.get("ManufacturerCode"),))
                val = self.cursor.fetchone()
                if val:
                    return JsonResponse({"Result" : " YES THIS CODE IS ALREADY EXISTS ...!",  "Manufact" : (pd.DataFrame(list(self.Manufact), columns=["ManufacturerCode", "ManufacturerName", "ManufacturerName1","ManufacturerCRUEI","ManufacturerAddress", "ManufacturerAddress1", "ManufacturerCity","ManufacturerSub","ManufacturerSubDivi","ManufacturerPostal","ManufacturerCountry"])).to_dict('records'),})
                else:
                    Qry = ("INSERT INTO COManufacturer (ManufacturerCode,ManufacturerName,ManufacturerName1,ManufacturerCRUEI,ManufacturerAddress,ManufacturerAddress1,ManufacturerCity,ManufacturerSub,ManufacturerSubDivi,ManufacturerPostal,ManufacturerCountry,TouchUser,TouchTime,Status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    val = (request.POST.get("ManufacturerCode"),request.POST.get("ManufacturerName"),request.POST.get("ManufacturerName1"),request.POST.get("ManufacturerCRUEI"),request.POST.get("ManufacturerAddress"),request.POST.get("ManufacturerAddress1"),request.POST.get("ManufacturerCity"),
                            request.POST.get("ManufacturerSub"),request.POST.get("ManufacturerSubDivi"),request.POST.get("ManufacturerPostal"),request.POST.get("ManufacturerCountry"),request.POST.get("TouchUser"),request.POST.get("TouchTime"),"Active")
                    self.cursor.execute(Qry,val)
                    self.conn.commit()
                    self.cursor.execute("SELECT ManufacturerCode,ManufacturerName,ManufacturerName1,ManufacturerCRUEI,ManufacturerAddress,ManufacturerAddress1,ManufacturerCity,ManufacturerSub,ManufacturerSubDivi,ManufacturerPostal,ManufacturerCountry FROM COManufacturer ORDER BY ManufacturerName")
                    self.Manufact = self.cursor.fetchall()
                    print("Value inserted successfully:", val)
                    return JsonResponse({
                        "Result" : "THIS CODE SAVED SUCCESSFULLY ...!",
                        "Manufact" : (pd.DataFrame(list(self.Manufact), columns=["ManufacturerCode", "ManufacturerName", "ManufacturerName1","ManufacturerCRUEI","ManufacturerAddress", "ManufacturerAddress1", "ManufacturerCity","ManufacturerSub","ManufacturerSubDivi","ManufacturerPostal","ManufacturerCountry"])).to_dict('records'),
                    })

class ItemCodeSave(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def post(self,request):
        DbName = request.POST.get("ModelName")
        if DbName == "COOInhouseItemModel":
            Qry = "select InhouseCode from COOInhouseItem where InhouseCode = %s"
            print("QryItemCode:",Qry)
            Val = (request.POST.get("InhouseCode"),)
            self.cursor.execute(Qry, Val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO COOInhouseItem(InhouseCode,HsCode,Description,cooCode,CooName,manufactdate,OrginCert,CertificateHscode,PerCentOrgCert,CertficateDescrp,ShippingMarks,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                Val = (
                    request.POST.get("InhouseCode"),
                    request.POST.get("HsCode"),
                    request.POST.get("Description"),
                    request.POST.get("cooCode"),
                    request.POST.get("CooName"),
                    request.POST.get("manufactdate"),
                    request.POST.get("OrginCert"),
                    request.POST.get("CertificateHscode"),
                    request.POST.get("PerCentOrgCert"),
                    request.POST.get("CertficateDescrp"),
                    request.POST.get("ShippingMarks"),
                    request.POST.get("TouchUser"),
                    request.POST.get("TouchTime")

                )
                self.cursor.execute(Qry, Val)
                self.conn.commit()
                return JsonResponse({"Result": "COOInhouseItem Saved ...!"})
            else:
                return JsonResponse(
                    {"Result": "COOInhouseItem Code Already Exists ...!"}
                )                
     


                
# class AllItemUpdateCoo(View,SqlDb):
#     def __init__(self):
#         SqlDb.__init__(self)
    
#     def get(self,request):

#         ItemValue=json.loads(request.GET.get('ItemNo'))

#         values_str = ', '.join(map(str, ItemValue))

#         query = f"DELETE FROM COItemDtl WHERE ItemNo IN ({values_str}) AND PermitId = '{request.GET.get('PermitId')}' "
#         self.cursor.execute(query)

#         self.conn.commit()

#         self.cursor.execute("SELECT ItemNo,PermitId FROM COItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))
    
#         Ic = 1 
#         for itm in self.cursor.fetchall():
#             self.cursor.execute("UPDATE COItemDtl SET ItemNo = '{}' WHERE PermitId = '{}' AND  ItemNo = '{}' ".format(Ic,request.GET.get('PermitId'),itm[0]))
#             Ic += 1
 
#         self.conn.commit()

#         self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime,Hawblno FROM  COItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))
#         self.item = self.cursor.fetchall()

#         return JsonResponse({
#             "Result":"UPLOAD SUCCESSFULLY...!",
#             "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','Contry','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','CIFFOB','InvoiceQty','HSQTY','HSUOM','ShippingMark','CerItemQty','CerItemUOM','ManfCostDate','TextileCat','TextileQuotaQty','TextileQuotaQtyUOM','ItemValue','InvoiceNumber','InvoiceDate','HSOnCer','OriginCriterion','PerOrgainCRI','CertificateDes','Touch_user','TouchTime','Hawblno'])).to_dict('records'),

#         }) 
#     def post(self,request):

#         PermitId = request.POST.get('PermitId')

#         Qry = "UPDATE COItemDtl SET  MessageType = %s,HSCode = %s,Description = %s,Contry = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,CIFFOB = %s,InvoiceQty = %s,HSQTY = %s,HSUOM = %s,ShippingMark = %s,CerItemQty = %s,CerItemUOM = %s,ManfCostDate = %s,TextileCat = %s,TextileQuotaQty = %s,TextileQuotaQtyUOM = %s,ItemValue = %s,InvoiceNumber = %s,InvoiceDate = %s,HSOnCer = %s,OriginCriterion = %s,PerOrgainCRI = %s,CertificateDes = %s,Touch_user = %s,TouchTime = %s,Hawblno = %s WHERE PermitId = %s AND ItemNo = %s"
#         ItemValue = json.loads(request.POST.get('Item'))
#         for Itm in ItemValue:
#             itmNo = Itm.pop('ItemNo')
#             Permit = Itm.pop('PermitId')
#             Itm.update({'PermitId':Permit,"ItemNo":itmNo})

#             try:self.cursor.execute(Qry,tuple(Itm.values()))
#             except Exception as e:pass

#         self.conn.commit()

#         self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime,Hawblno FROM  COItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitId))
#         self.item = self.cursor.fetchall()

#         return JsonResponse({
#             "Result":"UPLOAD SUCCESSFULLY...!",

#              "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','Contry','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','CIFFOB','InvoiceQty','HSQTY','HSUOM','ShippingMark','CerItemQty','CerItemUOM','ManfCostDate','TextileCat','TextileQuotaQty','TextileQuotaQtyUOM','ItemValue','InvoiceNumber','InvoiceDate','HSOnCer','OriginCriterion','PerOrgainCRI','CertificateDes','Touch_user','TouchTime','Hawblno'])).to_dict('records'),
            
            
#         })


# class AllItemUpdateCoo(View, SqlDb):
#     def __init__(self):
#         SqlDb.__init__(self)
    
#     def get(self, request):

#         ItemValue = json.loads(request.GET.get('ItemAllDataInNon'))
#         values_str = ', '.join(map(str, ItemValue))

#         print("ItemValue:", ItemValue)  

#         query = f"DELETE FROM COItemDtl WHERE ItemNo IN ({values_str}) AND PermitId = '{request.GET.get('PermitId')}' "
#         print("DELETE Query:", query)  

#         self.cursor.execute(query)
#         self.conn.commit()

#         self.cursor.execute("SELECT ItemNo,PermitId FROM COItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))
    
#         Ic = 1 
#         for itm in self.cursor.fetchall():
#             print("Item being updated:", itm)  
#             self.cursor.execute("UPDATE COItemDtl SET ItemNo = '{}' WHERE PermitId = '{}' AND  ItemNo = '{}' ".format(Ic, request.GET.get('PermitId'), itm[0]))
#             Ic += 1
 
#         self.conn.commit()

#         self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime FROM  COItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.GET.get('PermitId')))
#         self.item = self.cursor.fetchall()

#         print("Fetched items:", self.item)  

#         return JsonResponse({
#             "Result": "UPLOAD SUCCESSFULLY...!",
#             "item": (pd.DataFrame(list(self.item), columns=['ItemNo', 'PermitId', 'MessageType', 'HSCode', 'Description', 'Contry', 'UnitPrice', 'UnitPriceCurrency', 'ExchangeRate', 'SumExchangeRate', 'TotalLineAmount', 'CIFFOB', 'InvoiceQty', 'HSQTY', 'HSUOM', 'ShippingMark', 'CerItemQty', 'CerItemUOM', 'ManfCostDate', 'TextileCat', 'TextileQuotaQty', 'TextileQuotaQtyUOM', 'ItemValue', 'InvoiceNumber', 'InvoiceDate', 'HSOnCer', 'OriginCriterion', 'PerOrgainCRI', 'CertificateDes', 'Touch_user', 'TouchTime'])).to_dict('records'),

#         }) 

#     def post(self, request):

#         PermitId = request.POST.get('PermitId')

#         Qry = "UPDATE COItemDtl SET  MessageType = %s,HSCode = %s,Description = %s,Contry = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,CIFFOB = %s,InvoiceQty = %s,HSQTY = %s,HSUOM = %s,ShippingMark = %s,CerItemQty = %s,CerItemUOM = %s,ManfCostDate = %s,TextileCat = %s,TextileQuotaQty = %s,TextileQuotaQtyUOM = %s,ItemValue = %s,InvoiceNumber = %s,InvoiceDate = %s,HSOnCer = %s,OriginCriterion = %s,PerOrgainCRI = %s,CertificateDes = %s,Touch_user = %s,TouchTime = %s WHERE PermitId = %s AND ItemNo = %s"
#         ItemValue = json.loads(request.POST.get('Item'))
#         for Itm in ItemValue:
#             itmNo = Itm.pop('ItemNo')
#             Permit = Itm.pop('PermitId')
#             Itm.update({'PermitId': Permit, "ItemNo": itmNo})

   
#             print("Values for SQL Query:", tuple(Itm.values()))

#         try:
#             self.cursor.execute(Qry, tuple(Itm.values()))
#         except Exception as e:
#             print("Error executing SQL query:", str(e))


#         self.conn.commit()

#         self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime FROM  COItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitId))
#         self.item = self.cursor.fetchall()

#         return JsonResponse({
#             "Result": "UPLOAD SUCCESSFULLY...!",
#             "item": (pd.DataFrame(list(self.item), columns=['ItemNo', 'PermitId', 'MessageType', 'HSCode', 'Description', 'Contry', 'UnitPrice', 'UnitPriceCurrency', 'ExchangeRate', 'SumExchangeRate', 'TotalLineAmount', 'CIFFOB', 'InvoiceQty', 'HSQTY', 'HSUOM', 'ShippingMark', 'CerItemQty', 'CerItemUOM', 'ManfCostDate', 'TextileCat', 'TextileQuotaQty', 'TextileQuotaQtyUOM', 'ItemValue', 'InvoiceNumber', 'InvoiceDate', 'HSOnCer', 'OriginCriterion', 'PerOrgainCRI', 'CertificateDes', 'Touch_user', 'TouchTime'])).to_dict('records'),
#         })
                


# def AllItemUpdateCoo(request):
#     db = SqlDb()
    

#     print("hello ")
#     ItemValue = json.loads(request.POST.get('ItemAllDataInNon'))

#     PermitId = request.POST.get('PermitId')

   

#     qry = "UPDATE COItemDtl SET MessageType = %s,HSCode = %s,Description = %s,Contry = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,CIFFOB = %s,InvoiceQty = %s,HSQTY = %s,HSUOM = %s,ShippingMark = %s,CerItemQty = %s,CerItemUOM = %s,ManfCostDate = %s,TextileCat = %s,TextileQuotaQty = %s,TextileQuotaQtyUOM = %s,ItemValue = %s,InvoiceNumber = %s,InvoiceDate = %s,HSOnCer = %s,OriginCriterion = %s,PerOrgainCRI = %s,CertificateDes = %s,Touch_user = %s,TouchTime = %s WHERE ItemNo = %s AND PermitId = %s"
    
    
#     for i in ItemValue:
#         val = (i['MessageType'],i['HSCode'],i['Description'],i['Contry'],i['UnitPrice'],i['UnitPriceCurrency'],i['ExchangeRate'],i['SumExchangeRate'],i['TotalLineAmount'],i['CIFFOB'],i['InvoiceQty'],i['HSQTY'],i['HSUOM'],i['ShippingMark'],i['CerItemQty'],i['CerItemUOM'],i['ManfCostDate'],i['TextileCat'],i['TextileQuotaQty'],i['TextileQuotaQtyUOM'],i['ItemValue'],i['InvoiceNumber'],i['InvoiceDate'],i['HSOnCer'],i['OriginCriterion'],i['PerOrgainCRI'],i['CertificateDes'],i['Touch_user'],i['TouchTime'],i['ItemNo'],PermitId)
#         db.cursor.execute(qry,val)
#         db.conn.commit()

#     context = {}
#     db.cursor.execute(
#         f"select * from COItemDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
#     )
#     headers = [i[0] for i in db.cursor.description]
#     context.update(
#         {
#             "Result": "UPLOAD SUCCESSFULLY...!",
#             "item": (
#                 pd.DataFrame(list(db.cursor.fetchall()), columns=headers)
#             ).to_dict("records")
#         }
#     )
    
#     return JsonResponse(context)
                


def AllItemUpdateCoo(request):
    try:
        db = SqlDb()
        ItemValue = json.loads(request.POST.get('ItemAllDataInNon'))
        PermitId = request.POST.get('PermitId')

        qry = "UPDATE COItemDtl SET MessageType = %s,HSCode = %s,Description = %s,Contry = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,CIFFOB = %s,InvoiceQty = %s,HSQTY = %s,HSUOM = %s,ShippingMark = %s,CerItemQty = %s,CerItemUOM = %s,ManfCostDate = %s,TextileCat = %s,TextileQuotaQty = %s,TextileQuotaQtyUOM = %s,ItemValue = %s,InvoiceNumber = %s,InvoiceDate = %s,HSOnCer = %s,OriginCriterion = %s,PerOrgainCRI = %s,CertificateDes = %s,Touch_user = %s,TouchTime = %s WHERE ItemNo = %s AND PermitId = %s"
       

        for i in ItemValue:
            val = (i['MessageType'], i['HSCode'], i['Description'], i['Contry'], i['UnitPrice'], i['UnitPriceCurrency'], i['ExchangeRate'], i['SumExchangeRate'], i['TotalLineAmount'], i['CIFFOB'], i['InvoiceQty'], i['HSQTY'], i['HSUOM'], i['ShippingMark'], i['CerItemQty'], i['CerItemUOM'], i['ManfCostDate'], i['TextileCat'], i['TextileQuotaQty'], i['TextileQuotaQtyUOM'], i['ItemValue'], i['InvoiceNumber'], i['InvoiceDate'], i['HSOnCer'], i['OriginCriterion'], i['PerOrgainCRI'], i['CertificateDes'], i['Touch_user'], i['TouchTime'], i['ItemNo'], PermitId)
            db.cursor.execute(qry, val)
            db.conn.commit()

        context = {}
        db.cursor.execute(
            f"SELECT * FROM COItemDtl WHERE PermitId = '{PermitId}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in db.cursor.description]
        context.update(
            {
                "Result": "UPLOAD SUCCESSFULLY...!",
                "item": (
                    pd.DataFrame(list(db.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )

        return JsonResponse(context)

    except Exception as e:
        print('error:',e)
        error_message = str(e)
        print('error_message:',error_message)
        return JsonResponse({"error": error_message}, status=500)
    

#CooList Transmit
    

def CooTransmit(request):
    permitNumber1 = json.loads(request.GET.get("PermitNumber"))
    s = SqlDb('SecondDb')
    s1 = SqlDb('default')


    for ID in permitNumber1:
        s1.cursor.execute(f"SELECT * FROM COHeaderTbl WHERE Id='{ID}' ")
        permitNumber = s1.cursor.fetchone()[4]
        TouchUser = str(request.session['Username']).upper() 
        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")
        print("permitNumber:",permitNumber)

        s.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(TouchUser))
        ManageUserVal = s.cursor.fetchone()
        AccountId = ManageUserVal[0]
        MailId = ManageUserVal[1] 

        s.cursor.execute("SELECT COUNT(*) + 1  FROM COHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'COODEC' ".format(refDate))
        RefId = ("%03d" % s.cursor.fetchone()[0])

        s.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        JobIdCount = s.cursor.fetchone()[0]


        JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % JobIdCount}" 
        MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % JobIdCount}"
        NewPermitId = f"{TouchUser}{refDate}{RefId}"

        TouchTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            s1.cursor.execute(f"SELECT * FROM COHeaderTbl WHERE PermitId='{permitNumber}' ")
            Heading = [i[0] for i in s1.cursor.description]
            HeadData = [dict(zip(Heading,row)) for row in s1.cursor.fetchall()]
            HeadQry = ("INSERT INTO COHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,ApplicationType,PreviousPermitNo,OutwardTransportMode,ReferenceDocuments,COType,CerDtlType1,CerDtlCopy1,CerDtlType2,CerDtlCopy2,CurrencyCode,AdditionalCer,TransportDtl,PerferenceContent,DeclarantCompanyCode,ExporterCompanyCode,OutwardCarrierAgentCode,FreightForwarderCode,CONSIGNEECode,Manufacturer,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,DeclareIndicator,NumberOfItems,InternalRemarks,TradeRemarks,Status,TouchUser,TouchTime,prmtStatus,PermitNumber,EntryYear,Percomwealth,Gpsdonorcountry,Additionalrecieptant,GrossReference,DeclarningFor,CertificateNumber,MRDate,MRTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
            for head in HeadData:
                headVal = (RefId,JobId,MsgId,NewPermitId,MailId,head['MessageType'],head['ApplicationType'],head['PreviousPermitNo'],head['OutwardTransportMode'],head['ReferenceDocuments'],head['COType'],head['CerDtlType1'],head['CerDtlCopy1'],head['CerDtlType2'],head['CerDtlCopy2'],head['CurrencyCode'],head['AdditionalCer'],head['TransportDtl'],head['PerferenceContent'],head['DeclarantCompanyCode'],head['ExporterCompanyCode'],head['OutwardCarrierAgentCode'],head['FreightForwarderCode'],head['CONSIGNEECode'],head['Manufacturer'],head['DepartureDate'],head['DischargePort'],head['FinalDestinationCountry'],head['OutVoyageNumber'],head['OutVesselName'],head['OutConveyanceRefNo'],head['OutTransportId'],head['OutFlightNO'],head['OutAircraftRegNo'],head['TotalOuterPack'],head['TotalOuterPackUOM'],head['TotalGrossWeight'],head['TotalGrossWeightUOM'],head['DeclareIndicator'],head['NumberOfItems'],head['InternalRemarks'],head['TradeRemarks'],head['Status'],TouchUser,TouchTime,head['prmtStatus'],head['PermitNumber'],head['EntryYear'],head['Percomwealth'],head['Gpsdonorcountry'],head['Additionalrecieptant'],head['GrossReference'],head['DeclarningFor'],head['CertificateNumber'],head['MRDate'],head['MRTime'])
                s.cursor.execute(HeadQry,headVal)

            s.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{NewPermitId}','COODEC','{AccountId}','{MsgId}','{TouchUser}','{TouchTime}') ")

            ItemQry = "INSERT INTO COItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            s1.cursor.execute(f"SELECT * FROM COItemDtl WHERE PermitId='{permitNumber}' ")
            ItemHead = [i[0] for i in s1.cursor.description]
            ItemData = [dict(zip(ItemHead,row)) for row in s1.cursor.fetchall()]
            for head in ItemData:
                ItemVal= (head['ItemNo'],NewPermitId,head['MessageType'],head['HSCode'],head['Description'],head['Contry'],head['UnitPrice'],head['UnitPriceCurrency'],head['ExchangeRate'],head['SumExchangeRate'],head['TotalLineAmount'],head['CIFFOB'],head['InvoiceQty'],head['HSQTY'],head['HSUOM'],head['ShippingMark'],head['CerItemQty'],head['CerItemUOM'],head['ManfCostDate'],head['TextileCat'],head['TextileQuotaQty'],head['TextileQuotaQtyUOM'],head['ItemValue'],head['InvoiceNumber'],head['InvoiceDate'],head['HSOnCer'],head['OriginCriterion'],head['PerOrgainCRI'],head['CertificateDes'],TouchUser,TouchTime)
                s.cursor.execute(ItemQry,ItemVal)

            InfileQry = "INSERT INTO COFileUpload (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,filepath,Size,PermitId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM COFileUpload WHERE PermitId='{permitNumber}' ")
            InFileHead = [i[0] for i in s1.cursor.description]
            InFileData = [dict(zip(InFileHead,row)) for row in s1.cursor.fetchall()]
            for head in InFileData:
                InfileVal= (head['Sno'],head['Name'],head['ContentType'],head['Data'],head['DocumentType'],head['InPaymentId'],TouchUser,TouchTime,head['filepath'],head['Size'],NewPermitId)
                s.cursor.execute(InfileQry,InfileVal)

            s.conn.commit()
            print("saved SuccessFully")
            # print("HeadData:", HeadData)
            # print("ItemData:", ItemData)
            # print("InFileData:", InFileData)
       
        except Exception as e:
                print('error:',e)
                error_message = str(e)
                print('error_message:',error_message)
        finally:
            return JsonResponse({"Success":"Genrate"})

    return JsonResponse({"Success":"Genrate"})


class CooItemCode(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

        self.cursor.execute("SELECT InhouseCode,HsCode,Description,cooCode,CooName,manufactdate,OrginCert,CertificateHscode,PerCentOrgCert,CertficateDescrp,ShippingMarks FROM COOInhouseItem  ")
        self.inhouseItemCode = self.cursor.fetchall()

        self.cursor.execute("SELECT HSCode,Description,UOM,Typeid,DUTYTYPID,Inpayment,InnonPayment,Out,Co,Transhipment,RPNEXPORT,DuitableUom,Excisedutyuom,Excisedutyrate,Customsdutyuom,Customsdutyrate,Kgmvisible FROM HSCode")#ImpControll,OutControll,TransControll <---This Field Add Only Kaizen Portal 
        self.hsCode = self.cursor.fetchall()

        self.cursor.execute("SELECT HSCode FROM ChkHsCode ")
        self.chkHsCode = self.cursor.fetchall()

    def get(self,request):
        return JsonResponse({
            "inhouseItemCode" : (pd.DataFrame(list(self.inhouseItemCode), columns=["InhouseCode", "HsCode", "Description","cooCode","CooName", "manufactdate", "OrginCert","CertificateHscode","PerCentOrgCert","CertficateDescrp","ShippingMarks"])).to_dict('records'),
            "hsCode" : (pd.DataFrame(list(self.hsCode), columns=['HSCode','Description','UOM','Typeid','DUTYTYPID','Inpayment','InnonPayment','Out','Co','Transhipment','RPNEXPORT','DuitableUom','Excisedutyuom','Excisedutyrate','Customsdutyuom','Customsdutyrate','Kgmvisible'])).to_dict('records'),#,'ImpControll ,'OutControll','TransControll'<---This Field Add Only Kaizen Portal  '
            "chkHsCode" : (pd.DataFrame(list(self.chkHsCode), columns=["HSCode"])).to_dict('records'),
        })
        

        
    def post(self,request):

        

        self.cursor.execute("SELECT PermitId,ItemNo FROM COItemDtl WHERE PermitId = '{}' AND ItemNo = '{}' " .format(request.POST.get('PermitId'),request.POST.get('ItemNo')))
        if self.cursor.fetchall():
            Result = "ITEM SUCCESSFULLY UPDATED...!"
            Qry = " UPDATE COItemDtl SET MessageType = %s,HSCode = %s,Description = %s,Contry = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,CIFFOB = %s,InvoiceQty = %s,HSQTY = %s,HSUOM = %s,ShippingMark = %s,CerItemQty = %s,CerItemUOM = %s,ManfCostDate = %s,TextileCat = %s,TextileQuotaQty = %s,TextileQuotaQtyUOM = %s,ItemValue = %s,InvoiceNumber = %s,InvoiceDate = %s,HSOnCer = %s,OriginCriterion = %s,PerOrgainCRI = %s,CertificateDes = %s,Touch_user = %s,TouchTime = %s  WHERE PermitId = %s AND ItemNo = %s "
            Val = (request.POST.get('MessageType'),request.POST.get('HSCode'),request.POST.get('Description'),request.POST.get('Contry'),request.POST.get('UnitPrice'),request.POST.get('UnitPriceCurrency'),request.POST.get('ExchangeRate'),request.POST.get('SumExchangeRate'),request.POST.get('TotalLineAmount'),request.POST.get('CIFFOB'),request.POST.get('InvoiceQty'),request.POST.get('HSUOM'),request.POST.get('HSUOM'),request.POST.get('ShippingMark'),request.POST.get('CerItemQty'),request.POST.get('CerItemUOM'),request.POST.get('ManfCostDate'),request.POST.get('TextileCat'),request.POST.get('TextileQuotaQty'),request.POST.get('TextileQuotaQtyUOM'),request.POST.get('ItemValue'),request.POST.get('InvoiceNumber'),request.POST.get('InvoiceDate'),request.POST.get('HSOnCer'),request.POST.get('OriginCriterion'),request.POST.get('PerOrgainCRI'),request.POST.get('CertificateDes'),request.POST.get('Touch_user'),request.POST.get('TouchTime'),request.POST.get('PermitId'),request.POST.get('ItemNo'))
            self.cursor.execute(Qry,Val)
        else:
            
            Qry = "INSERT INTO COItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            Val = (request.POST.get('ItemNo'),request.POST.get('PermitId'),request.POST.get('MessageType'),request.POST.get('HSCode'),request.POST.get('Description'),request.POST.get('Contry'),request.POST.get('UnitPrice'),request.POST.get('UnitPriceCurrency'),request.POST.get('ExchangeRate'),request.POST.get('SumExchangeRate'),request.POST.get('TotalLineAmount'),request.POST.get('CIFFOB'),request.POST.get('InvoiceQty'),request.POST.get('HSUOM'),request.POST.get('HSUOM'),request.POST.get('ShippingMark'),request.POST.get('CerItemQty'),request.POST.get('CerItemUOM'),request.POST.get('ManfCostDate'),request.POST.get('TextileCat'),request.POST.get('TextileQuotaQty'),request.POST.get('TextileQuotaQtyUOM'),request.POST.get('ItemValue'),request.POST.get('InvoiceNumber'),request.POST.get('InvoiceDate'),request.POST.get('HSOnCer'),request.POST.get('OriginCriterion'),request.POST.get('PerOrgainCRI'),request.POST.get('CertificateDes'),request.POST.get('Touch_user'),request.POST.get('TouchTime'))

            self.cursor.execute(Qry,Val)
            Result = "ITEM SUCCESSFULLY ADDED...!"
        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime FROM  COItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(request.POST.get('PermitId')))
        self.item = self.cursor.fetchall()

        

        return JsonResponse({
            "Result":Result,
            "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','Contry','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','CIFFOB','InvoiceQty','HSQTY','HSUOM','ShippingMark','CerItemQty','CerItemUOM','ManfCostDate','TextileCat','TextileQuotaQty','TextileQuotaQtyUOM','ItemValue','InvoiceNumber','InvoiceDate','HSOnCer','OriginCriterion','PerOrgainCRI','CertificateDes','Touch_user','TouchTime'])).to_dict('records'),
            
        })
     


#List page Copy
    

class CopyCoo(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):
        try:

            Username = request.session['Username'] 

            refDate = datetime.now().strftime("%Y%m%d")
            jobDate = datetime.now().strftime("%Y-%m-%d")

            self.cursor.execute(f"SELECT PermitId FROM COHeaderTbl WHERE Id = '{request.GET.get('Id')}' ")

            CopyPermitId = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(Username))
            ManageUserVal = self.cursor.fetchone()
            AccountId = ManageUserVal[0]

            self.cursor.execute("SELECT COUNT(*) + 1  FROM COHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'COODEC' ".format(refDate))
            self.RefId = ("%03d" % self.cursor.fetchone()[0])

            self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
            self.JobIdCount = self.cursor.fetchone()[0]

            self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
            self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
            self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

            NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute(f"""
        INSERT INTO COHeaderTbl (
            Refid, JobId, MSGId, PermitId, TradeNetMailboxID, MessageType, ApplicationType, PreviousPermitNo,
            OutwardTransportMode, ReferenceDocuments, COType, CerDtlType1, CerDtlCopy1, CerDtlType2, CerDtlCopy2,
            CurrencyCode, AdditionalCer, TransportDtl, PerferenceContent, DeclarantCompanyCode, ExporterCompanyCode,
            OutwardCarrierAgentCode, FreightForwarderCode, CONSIGNEECode, Manufacturer, DepartureDate, DischargePort,
            FinalDestinationCountry, OutVoyageNumber, OutVesselName, OutConveyanceRefNo, OutTransportId, OutFlightNO,
            OutAircraftRegNo, TotalOuterPack, TotalOuterPackUOM, TotalGrossWeight, TotalGrossWeightUOM, DeclareIndicator,
            NumberOfItems, InternalRemarks, TradeRemarks, Status, TouchUser, TouchTime, prmtStatus, PermitNumber,
            EntryYear, Percomwealth, Gpsdonorcountry, Additionalrecieptant, GrossReference, DeclarningFor,
            CertificateNumber, MRDate, MRTime
        )
        SELECT 
            '{self.RefId}', '{self.JobId}', '{self.MsgId}', '{self.PermitIdInNon}','{ManageUserVal[1]}',
            MessageType, ApplicationType, PreviousPermitNo, OutwardTransportMode, ReferenceDocuments, COType, CerDtlType1,
            CerDtlCopy1, CerDtlType2, CerDtlCopy2, CurrencyCode, AdditionalCer, TransportDtl, PerferenceContent,
            DeclarantCompanyCode, ExporterCompanyCode, OutwardCarrierAgentCode, FreightForwarderCode, CONSIGNEECode,
            Manufacturer, DepartureDate, DischargePort, FinalDestinationCountry, OutVoyageNumber, OutVesselName,
            OutConveyanceRefNo, OutTransportId, OutFlightNO, OutAircraftRegNo, TotalOuterPack, TotalOuterPackUOM,
            TotalGrossWeight, TotalGrossWeightUOM, DeclareIndicator, NumberOfItems, InternalRemarks, TradeRemarks,
            'DRF', '{Username}', '{NowDate}', 'COPY', PermitNumber, EntryYear, Percomwealth, Gpsdonorcountry,
            Additionalrecieptant, GrossReference, '--Select--', CertificateNumber, MRDate, ''
            FROM COHeaderTbl WHERE Id = '{request.GET.get('Id')}'""")



            # self.cursor.execute(f"INSERT INTO COHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,ApplicationType,PreviousPermitNo,OutwardTransportMode,ReferenceDocuments,COType,CerDtlType1,CerDtlCopy1,CerDtlType2,CerDtlCopy2,CurrencyCode,AdditionalCer,TransportDtl,PerferenceContent,DeclarantCompanyCode,ExporterCompanyCode,OutwardCarrierAgentCode,FreightForwarderCode,CONSIGNEECode,Manufacturer,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,DeclareIndicator,NumberOfItems,InternalRemarks,TradeRemarks,InternalRemarks,Status,TouchUser,TouchTime,prmtStatus,PermitNumber,EntryYear,Percomwealth,Gpsdonorcountry,Additionalrecieptant,GrossReference,DeclarningFor,CertificateNumber,MRDate,MRTime,TransmitId) SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{ManageUserVal[1]}','',MessageType,ApplicationType,PreviousPermitNo,OutwardTransportMode,ReferenceDocuments,COType,CerDtlType1,CerDtlCopy1,CerDtlType2,CerDtlCopy2,CurrencyCode,AdditionalCer,TransportDtl,PerferenceContent,DeclarantCompanyCode,ExporterCompanyCode,OutwardCarrierAgentCode,FreightForwarderCode,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,DeclareIndicator,NumberOfItems,InternalRemarks,TradeRemarks,'DRF','{Username}','{NowDate}','','COPY',Percomwealth,Gpsdonorcountry,Additionalrecieptant,GrossReference,'--Select--',MRDate,'' FROM COHeaderTbl WHERE Id = '{request.GET.get('Id')}'")
        
            self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','COODEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')")
            
            self.cursor.execute(f"INSERT INTO COItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime,Hawblno) SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,'{Username}','{NowDate}',Hawblno FROM COItemDtl WHERE PermitId = '{CopyPermitId}'")

            self.cursor.execute(f"INSERT INTO COFileUpload (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,filepath,Size,PermitId) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{Username}','{NowDate}',filepath,Size,'{self.PermitIdInNon}' FROM COFileUpload WHERE PermitId = '{CopyPermitId}' ")
            
            self.conn.commit()

            self.cursor.execute(f"SELECT Id FROM COHeaderTbl WHERE PermitId = '{self.PermitIdInNon}' ")
            
            request.session['id'] = self.cursor.fetchone()[0]
        
            
            return JsonResponse({"SUCCESS" : 'COPY ITEM'})
        
        except Exception as e:
            
            print(f"An error occurred: {str(e)}")
    

def EditCoo(request):
    request.session["PermitId"] = request.POST.get("PermitId")
    # return JsonResponse({"testing ":"testing"})   
    return render (request,'coo/coonew.html')


class CooTransmitData(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):

        maiId = request.GET.get('mailId')
        print('maiId:',maiId)

        self.cursor.execute("SELECT TOP 1 TouchUser FROM COHeaderTbl WHERE TradeNetMailboxID = '{}' ".format(maiId))

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
            self.cursor.execute(f"SELECT PermitId FROM COHeaderTbl WHERE Id = '{Id}' ")
            CopyPermitId = self.cursor.fetchone()[0]
            print("copypermit:",CopyPermitId)

            self.cursor.execute("SELECT COUNT(*) + 1  FROM COHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'COODEC' ".format(refDate))
            self.RefId = ("%03d" % self.cursor.fetchone()[0])

            self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
            self.JobIdCount = self.cursor.fetchone()[0]

            self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
            self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
            self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"
            print("permit id:",self.PermitIdInNon)


            NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # self.cursor.execute(f"INSERT INTO COHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,ApplicationType,PreviousPermitNo,OutwardTransportMode,ReferenceDocuments,COType,CerDtlType1,CerDtlCopy1,CerDtlType2,CerDtlCopy2,CurrencyCode,AdditionalCer,TransportDtl,PerferenceContent,DeclarantCompanyCode,ExporterCompanyCode,OutwardCarrierAgentCode,FreightForwarderCode,CONSIGNEECode,Manufacturer,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,DeclareIndicator,NumberOfItems,InternalRemarks,TradeRemarks,Status,TouchUser,TouchTime,prmtStatus,PermitNumber,EntryYear,Percomwealth,Gpsdonorcountry,Additionalrecieptant,GrossReference,DeclarningFor,CertificateNumber,MRDate,MRTime)
            #                      SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{maiId}',MessageType,ApplicationType,PreviousPermitNo,OutwardTransportMode,ReferenceDocuments,COType,CerDtlType1,CerDtlCopy1,CerDtlType2,CerDtlCopy2,CurrencyCode,AdditionalCer,TransportDtl,PerferenceContent,DeclarantCompanyCode,ExporterCompanyCode,OutwardCarrierAgentCode,FreightForwarderCode,CONSIGNEECode,Manufacturer,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,DeclareIndicator,NumberOfItems,'',TradeRemarks,'DRF','{Username}','{NowDate}','NEW','',EntryYear,Percomwealth,Gpsdonorcountry,Additionalrecieptant,GrossReference,'--Select--',CertificateNumber,MRDate,'' FROM COHeaderTbl WHERE Id = '{Id}'")
            
            self.cursor.execute(f"""
             INSERT INTO COHeaderTbl (
                Refid, JobId, MSGId, PermitId, TradeNetMailboxID, MessageType, ApplicationType, PreviousPermitNo, OutwardTransportMode, ReferenceDocuments,
                COType, CerDtlType1, CerDtlCopy1, CerDtlType2, CerDtlCopy2, CurrencyCode, AdditionalCer, TransportDtl, PerferenceContent, DeclarantCompanyCode,
                ExporterCompanyCode, OutwardCarrierAgentCode, FreightForwarderCode, CONSIGNEECode, Manufacturer, DepartureDate, DischargePort, FinalDestinationCountry,
                OutVoyageNumber, OutVesselName, OutConveyanceRefNo, OutTransportId, OutFlightNO, OutAircraftRegNo, TotalOuterPack, TotalOuterPackUOM, TotalGrossWeight,
                TotalGrossWeightUOM, DeclareIndicator, NumberOfItems, InternalRemarks, TradeRemarks, Status, TouchUser, TouchTime, prmtStatus, PermitNumber, EntryYear,
                Percomwealth, Gpsdonorcountry, Additionalrecieptant, GrossReference, DeclarningFor, CertificateNumber, MRDate, MRTime)
                 SELECT 
                '{self.RefId}', '{self.JobId}', '{self.MsgId}', '{self.PermitIdInNon}', '{maiId}', MessageType, ApplicationType, PreviousPermitNo, OutwardTransportMode,
                ReferenceDocuments, COType, CerDtlType1, CerDtlCopy1, CerDtlType2, CerDtlCopy2, CurrencyCode, AdditionalCer, TransportDtl, PerferenceContent,
                DeclarantCompanyCode, ExporterCompanyCode, OutwardCarrierAgentCode, FreightForwarderCode, CONSIGNEECode, Manufacturer, DepartureDate, DischargePort,
                FinalDestinationCountry, OutVoyageNumber, OutVesselName, OutConveyanceRefNo, OutTransportId, OutFlightNO, OutAircraftRegNo, TotalOuterPack,
                TotalOuterPackUOM, TotalGrossWeight, TotalGrossWeightUOM, DeclareIndicator, NumberOfItems, '', TradeRemarks, 'DRF', '{Username}', '{NowDate}', 'NEW', '',
                EntryYear, Percomwealth, Gpsdonorcountry, Additionalrecieptant, GrossReference, '--Select--', CertificateNumber, MRDate, ''
                FROM COHeaderTbl  WHERE  Id = '{Id}' """)

            self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','CODEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')")
            
            # self.cursor.execute(f"INSERT INTO COItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime,Hawblno) 
            #                     SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,'{Username}','{NowDate}',Hawblno FROM COItemDtl WHERE PermitId = '{CopyPermitId}'")
            
            self.cursor.execute(f"INSERT INTO COItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,Touch_user,TouchTime,Hawblno) "
                     f"SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,Contry,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,CIFFOB,InvoiceQty,HSQTY,HSUOM,ShippingMark,CerItemQty,CerItemUOM,ManfCostDate,TextileCat,TextileQuotaQty,TextileQuotaQtyUOM,ItemValue,InvoiceNumber,InvoiceDate,HSOnCer,OriginCriterion,PerOrgainCRI,CertificateDes,'{Username}','{NowDate}',Hawblno FROM COItemDtl WHERE PermitId = '{CopyPermitId}'")
            
            self.cursor.execute(f"INSERT INTO COFileUpload (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,filepath,Size,PermitId) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{Username}','{NowDate}',filepath,Size,'{self.PermitIdInNon}' FROM COFileUpload WHERE PermitId = '{CopyPermitId}' ")
            
            self.conn.commit()

        return JsonResponse({"SUCCESS" : 'COPY ITEM'})
    


class CooDownloadData(View,SqlDb):
    
    def __init__(self):
        SqlDb.__init__(self)
    def get(self,request,Id):
        Headerrow_num = 0
        ItemWorkRow_num = 0
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

        columns = ['Refid', 'JobId', 'MSGId', 'PermitId', 'TradeNetMailboxID', 'MessageType', 'ApplicationType', 'PreviousPermitNo', 'OutwardTransportMode', 'ReferenceDocuments',
                'COType', 'CerDtlType1', 'CerDtlCopy1', 'CerDtlType2', 'CerDtlCopy2', 'CurrencyCode', 'AdditionalCer', 'TransportDtl', 'PerferenceContent', 'DeclarantCompanyCode',
                'ExporterCompanyCode', 'OutwardCarrierAgentCode', 'FreightForwarderCode', 'CONSIGNEECode', 'Manufacturer', 'DepartureDate', 'DischargePort', 'FinalDestinationCountry',
                'OutVoyageNumber', 'OutVesselName', 'OutConveyanceRefNo', 'OutTransportId', 'OutFlightNO', 'OutAircraftRegNo', 'TotalOuterPack', 'TotalOuterPackUOM', 'TotalGrossWeight',
                'TotalGrossWeightUOM', 'DeclareIndicator', 'NumberOfItems', 'InternalRemarks', 'TradeRemarks', 'Status', 'TouchUser', 'TouchTime', 'prmtStatus', 'PermitNumber', 'EntryYear',
                'Percomwealth', 'Gpsdonorcountry', 'Additionalrecieptant', 'GrossReference', 'DeclarningFor', 'CertificateNumber', 'MRDate', 'MRTime']
        for col_num in range(len(columns)):
            headerWork.write(Headerrow_num, col_num, columns[col_num], font_style)


        ItemWork = wb.add_sheet('Item')
        columns = ['Id','ItemNo','PermitId','MessageType','HSCode','Description','Contry','UnitPrice','UnitPriceCurrency','ExchangeRate',
                'SumExchangeRate','TotalLineAmount','CIFFOB','InvoiceQty','HSQTY','HSUOM','ShippingMark','CerItemQty','CerItemUOM','ManfCostDate','TextileCat','TextileQuotaQty',
                'TextileQuotaQtyUOM','ItemValue','InvoiceNumber','InvoiceDate','HSOnCer','OriginCriterion','PerOrgainCRI','CertificateDes','Touch_user','TouchTime','Hawblno']
        for col_num in range(len(columns)):
            ItemWork.write(ItemWorkRow_num, col_num, columns[col_num], font_style)


        font_style = xlwt.XFStyle()
        font_style.font.bold = False
        odd_row_style = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue;')
        even_row_style = xlwt.easyxf('pattern: pattern solid, fore_colour white;')

        for Id in Id.split(","):
            self.cursor.execute(f"SELECT * FROM COHeaderTbl WHERE Id = '{Id}' ")
            PermitVal = self.cursor.fetchall()
            for row in PermitVal:
                Headerrow_num += 1
                style = odd_row_style if Headerrow_num % 2 == 0 else even_row_style
                for col_num in range(len(row)):
                    headerWork.write(Headerrow_num, col_num,row[col_num], style)
        for permitIDS in PermitVal:
            self.cursor.execute(f"SELECT * FROM COItemDtl WHERE permitId = '{permitIDS[4]}' order by Id,PermitId")
            Ite = self.cursor.fetchall()
            for row in Ite:
                ItemWorkRow_num += 1
                style = odd_row_style if ItemWorkRow_num % 2 == 0 else even_row_style
                for col_num in range(len(row)):
                    ItemWork.write(ItemWorkRow_num, col_num,row[col_num], style)

        wb.save(response)

        return response
    


class ItemCooExcelUpload(View,SqlDb):
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
       

        ItemColumns ={
            'CountryofOrigin' : '' ,
            'HSCode' : '' ,
            'HSQty' : '0.00' ,
            'TotalLineAmount' : '0.00' ,
            'ItemCode' : '' ,
            'Description' : '' ,
            'HAWBOBL' : '' ,
            'HSUOM' : '--Select--' ,
            'ItemCurrency' : '--Select--' ,
            'UnitPrice' : '0.00' ,
            'ShippingMarks1' : '' ,
            'ShippingMarks2' : '' ,
            'ShippingMarks3' : '' ,
            'ShippingMarks4' : '' ,
            'CerItemQty' : '0.00' ,
            'CerItemUOM' : '--Select--' ,
            'CIFValOfCer' : '0.00' ,
            'ManufactureCostDate' : '' ,
            'TexCat' : '' ,
            'TexQuotaQty' : '0.00' ,
            'TexQuotaUOM' : '--Select--' ,
            'CerInvNo' : '' ,
            'CerInvDate' : '' ,
            'OriginOfCer' : '' ,
            'HSCodeCer' : '' ,
            'PerContent' : '' ,
            'CertificateDescription' : '' ,
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
            'EndUserDes' : '',
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

        self.cursor.execute(f"SELECT PermitId FROM COItemDtl WHERE PermitId = '{PermitId}'")
        itemLen_query = self.cursor.fetchone()

        itemLen = 0
        if itemLen_query is not None:
            itemLen = itemLen_query[0]

        for index, row in ItemInfo.iterrows():
            itemLen += 1
            data = {
                'ItemNo' : itemLen,
                'PermitId' : PermitId,
                'MessageType' : MsgType,
                'HSCode' : row['HSCode'],
                'Description' : row['Description'],
                'Contry' : row['CountryofOrigin'],
                'UnitPrice' : row['UnitPrice'],
                'UnitPriceCurrency' : row['ItemCurrency'],
                'ExchangeRate' : '0.00',
                'SumExchangeRate' : '0.00',
                'TotalLineAmount' : row['TotalLineAmount'],
                'CIFFOB' : '0.00',
                'InvoiceQty' : '0.00',
                'HSQTY' : row['HSQty'],
                'HSUOM' : row['HSUOM'],
                'ShippingMark' : row['ShippingMarks1'],
                'CerItemQty' : row['CerItemQty'],
                'CerItemUOM' : row['CerItemUOM'],
                'ManfCostDate' : row['ManufactureCostDate'],
                'TextileCat' : row['TexCat'],
                'TextileQuotaQty' : row['TexQuotaQty'],
                'TextileQuotaQtyUOM' : row['TexQuotaUOM'],
                'ItemValue' : '0.00',
                'InvoiceNumber' : '0.00',
                'InvoiceDate' :row['CerInvDate'],
                'HSOnCer' : '0.00',
                'OriginCriterion' : '0.00',
                'PerOrgainCRI' : '0.00',
                'CertificateDes' : row['CertificateDescription'],
                'Touch_user' : userName,
                'TouchTime' : TouchTime,
                'Hawblno' : row['HAWBOBL'],           
            }             
            try:
                columns = ', '.join([f'[{key}]' for key in data.keys()])
                values = ', '.join(['%s' for _ in range(len(data))])
                insert_statement = f'INSERT INTO COItemDtl ({columns}) VALUES ({values})'
                self.cursor.execute(insert_statement, tuple(data.values()))
                self.conn.commit()
            except Exception as e:
                print(e)

        context = {}
        self.cursor.execute(
            f"select * from COItemDtl WHERE PermitId = '{PermitId}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "item": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )

        return JsonResponse(context)
        



    


    #CooShow



# class CooShow(View,SqlDb):
#     def __init__(self):
#         SqlDb.__init__(self)

#     def get(self, request,id):
#         Username = request.session["Username"]
#         # print("Username:",Username)

#         self.cursor.execute(f"SELECT * FROM COHeaderTbl WHERE id = {id}")
#         headers = [i[0] for i in self.cursor.description]
#         outAll = list(self.cursor.fetchall())
#         print("outAll:",outAll)

#         self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))

#         AccountId = self.cursor.fetchone()[0]
#         # print("AccountId:",AccountId)

#         self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"+ Username+ "'")
#         InNonHeadData = self.cursor.fetchone()
#         # print("InNonHeadData:",InNonHeadData)

#         self.cursor.execute(f"SELECT * FROM CoPMT WHERE id = {id}")

#         context = {
#             "UserName": Username,
#             "PermitId": outAll[0][4],
#             "JobId": outAll[0][2],
#             "RefId": outAll[0][1],
#             "MsgId": outAll[0][3],
#             "AccountId": AccountId,
#             "LoginStatus": InNonHeadData[0],
#             "PermitNumber": "",
#             "prmtStatus": "",
#             "DateLastUpdated": InNonHeadData[1],
#             "MailBoxId": InNonHeadData[2],
#             "SeqPool": InNonHeadData[3],
#             "StartSequence": InNonHeadData[4],
#             "TradeNetMailboxID": InNonHeadData[5],
#             "DeclarantName": InNonHeadData[6],
#             "DeclarantCode": InNonHeadData[7],
#             "DeclarantTel": InNonHeadData[8],
#             "CRUEI": InNonHeadData[9],
#             "Code": InNonHeadData[10],
#             "name": InNonHeadData[11],
#             "name1": InNonHeadData[12],
#             "OutwardTransportMode":CommonMaster.objects.filter(TypeId=3, StatusId=1).order_by('Name'),
#             "DeclaringFor":CommonMaster.objects.filter(TypeId=80, StatusId=1).order_by('Name'),
#             "cotypeMode":CommonMaster.objects.filter(TypeId=16, StatusId=1).order_by('Name'),
#             "CertificateMode1":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),
#             "CertificateMode2":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),
#             "Currency": Currency.objects.filter().order_by("Currency"),
#             "FinalDestinationCountry":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),  
#             "HsQuantity":CommonMaster.objects.filter(TypeId=10, StatusId=1).order_by('Name'),   
#             "CurrUnitPrice":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'), 
#             "Country": COUNTRY.objects.all().order_by("CountryCode"),
            
#         }
        
#         context.update({
#             "Show" : (pd.DataFrame(outAll, columns=headers)).to_dict("records"),
 
#         }) 
#         for item in context["Show"]:
#             print("Row:")
#             for key, value in item.items():
#                 print(f"  {key}: {value}")
#         return render(request,"coo/coonew.html", context)
    

class CooShow(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request,id):
        # print("ID:", id)
       
        Username = request.session["Username"]
       

        self.cursor.execute(f"SELECT * FROM COHeaderTbl WHERE id = {id}")
        headers = [i[0] for i in self.cursor.description]
        outAll = list(self.cursor.fetchall())
        self.cursor.execute(f"SELECT * FROM COHeaderTbl WHERE id = {id}")
        result = self.cursor.fetchone()
        
        if result:
            fetched_id = result[0] 
            print("Fetched permit's ID:", fetched_id)
        else:
            print("No records found for the given ID.") 
       

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        AccountId = self.cursor.fetchone()[0]
        

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"+ Username+ "'")
        InNonHeadData = self.cursor.fetchone()
        

        # self.cursor.execute(f"SELECT * FROM CoPMT WHERE id = {id}")
        # result = self.cursor.fetchone()
        # if result:
        #     fetched_id = result[0] 
        #     print("Fetched ID:", fetched_id)
        # else:
        #     print("No records found for the given ID.")    
        # print('result:',result)  

        self.cursor.execute(f"SELECT * FROM CoPMT WHERE id = {id}")
        result = self.cursor.fetchone()
        print("Result:", result)

        if result:
            fetched_id = result[0] 
            print("Fetched ID:", fetched_id)
            
        else:
            print("No records found for the given ID.")
  
        

        context = {
            "UserName": Username,
            "PermitId": outAll[0][4],
            "JobId": outAll[0][2],
            "RefId": outAll[0][1],
            "MsgId": outAll[0][3],
            "AccountId": AccountId,
            "LoginStatus": InNonHeadData[0],
            "PermitNumber": "",
            "prmtStatus": "",
            # "ConditionCode": Status,
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
            "OutwardTransportMode":CommonMaster.objects.filter(TypeId=3, StatusId=1).order_by('Name'),
            "DeclaringFor":CommonMaster.objects.filter(TypeId=80, StatusId=1).order_by('Name'),
            "cotypeMode":CommonMaster.objects.filter(TypeId=16, StatusId=1).order_by('Name'),
            "CertificateMode1":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),
            "CertificateMode2":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),
            "Currency": Currency.objects.filter().order_by("Currency"),
            "FinalDestinationCountry":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'),  
            "HsQuantity":CommonMaster.objects.filter(TypeId=10, StatusId=1).order_by('Name'),   
            "CurrUnitPrice":CommonMaster.objects.filter(TypeId=17, StatusId=1).order_by('Name'), 
            "Country": COUNTRY.objects.all().order_by("CountryCode"),
            
        }
        
        
        context.update({
            "Show" : (pd.DataFrame(outAll, columns=headers)).to_dict("records"),
 
        }) 
        for item in context["Show"]:
            print("Row:")
            for key, value in item.items():
                print(f"  {key}: {value}")
        return render(request,"coo/coonew.html", context)
    




   
   


            


            







                




    

    



    





