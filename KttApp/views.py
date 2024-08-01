from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
from openpyxl import load_workbook

# import pymssql
import pandas as pd
import json
from django.db.models import Sum, Min
from django.views import View
from rest_framework import viewsets, filters
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend 
from django.db import connections
from reportlab.pdfgen import canvas
import io
from reportlab.graphics.barcode import code39
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
from decimal import *


class SqlDb:
    def __init__(self, database_name="default"):
        self.conn = connections[database_name]
        self.cursor = self.conn.cursor()


class LoginMain(View):
    def get(self, request):
        return render(request, "Login.html")


def Login(request):
    context = {}
    Username = request.POST.get("Username")
    if request.method == "POST":
        Username = request.POST.get("Username")
        pswd = request.POST.get("Password")
        check = request.POST.get("ChkLogin")
        if ManageUser.objects.filter(UserName=Username, Password=pswd).exists():
            if ManageUser.objects.filter(
                UserName=Username, LoginStatus="True"
            ).exists():
                if check:
                    request.session["Username"] = Username
                    request.session["Permit_Id"] = "NEW"
                    context.update({"Success": "Success"})
                else:
                    context.update(
                        {"Error": "User Already Login with another System...!!!"}
                    )
            else:
                upd = ManageUser.objects.get(UserName=Username)
                upd.LoginStatus = "True"
                upd.save()
                request.session["Username"] = Username
                request.session["Permit_Id"] = "NEW"
                context.update({"Success": "Success"})
        elif Username == "" and pswd == "":
            context.update({})
        else:
            context.update({"Error": "Enter Correct Password and Username"})
    else:
        try:
            upd = ManageUser.objects.get(UserName=Username)
            upd.LoginStatus = "False"
            upd.save()
        except:
            pass
    return render(request, "LoginPage/Login.html", context)


def Home(request):
    return render(
        request,
        "Home.html",
    )


def Inpayment(request):
    context = {}
    Username = request.session["Username"]
    context.update(
        {
            "UserName": Username,
            "CustomiseReport": CustomiseReport.objects.filter(
                ReportName="IPT", UserName=Username
            ).exclude(FiledName="id"),
            "ManageUserMail": ManageUser.objects.filter(Status="Active")
            .order_by("MailBoxId")
            .values_list("MailBoxId", flat=True)
            .distinct(),
            "InondeclarationTypeValue": CommonMaster.objects.filter(
                TypeId=13, StatusId=1
            ),
        }
    )
    return render(request, "Inpayment/InpaymentList.html", context)


def InpaymentNew(request, arg):
    nowRefId = datetime.now().strftime("%Y%m%d")
    nowJobId = datetime.now().strftime("%Y-%m-%d")
    Username = request.session["Username"]
    Permit_Id = request.session["Permit_Id"]
    currentDate = datetime.now().strftime("%d/%m/%Y")
    s = SqlDb()
    context = {}
    if arg == "REFUND":
        context.update(
            {
                "REFUND": "NEW",
                "TypeofRefund": CommonMaster.objects.filter(
                    TypeId=77, StatusId=1
                ).order_by("Name"),
                "ReasonForRefund": CommonMaster.objects.filter(
                    TypeId=76, StatusId=1
                ).order_by("Name"),
            }
        )

    if arg == "AMEND":
        context.update({"AMEND": "AMEND"})

    if arg == "CANCEL":
        context.update(
            {
                "CANCEL": "CANCEL",
                "CancelType": CommonMaster.objects.filter(
                    TypeId=75, StatusId=1
                ).order_by("Name"),
            }
        )

    if (
        arg == "EDIT"
        or arg == "COPY"
        or arg == "REFUND"
        or arg == "AMEND"
        or arg == "CANCEL"
        or arg == "SHOW"
    ):
        for i in InheaderTbl.objects.filter(PermitId=Permit_Id):
            s.cursor.execute(
                "select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1,DeclarantCompany.code from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId="
                " +'{UserName}'".format(UserName=i.TouchUser)
            )
            headData = s.cursor.fetchall()
            inHeaderPermitId = str(i.PermitId).upper()
            inHeaderMsgId = i.MSGId
            inHeaderJobId = i.JobId
            inHeaderReId = i.Refid
            context.update(
                {
                    "EDIT": "EDIT",
                    "Header": InheaderTbl.objects.filter(PermitId=Permit_Id),
                }
            )
            print("Header:")
            for key, value in context["Header"].values()[0].items():
                print(f"{key}: {value}")
            
            
        if arg == "SHOW":
            context.update({"SHOW": True})

        if InpaymentRefund.objects.filter(MsgId=i.MSGId).exists():
            context.update(
                {
                    "REFUND": "EDIT",
                    "TypeofRefund": CommonMaster.objects.filter(
                        TypeId=77, StatusId=1
                    ).order_by("Name"),
                    "ReasonForRefund": CommonMaster.objects.filter(
                        TypeId=76, StatusId=1
                    ).order_by("Name"),
                }
            )
        if InpaymentCancel.objects.filter(MsgId=i.MSGId).exists():
            context.update(
                {
                    "CANCEL": "EDIT",
                    "CancelType": CommonMaster.objects.filter(
                        TypeId=75, StatusId=1
                    ).order_by("Name"),
                }
            )
        if InpaymentAmend.objects.filter(MsgId=i.MSGId).exists():
            context.update({"AMEND": "AMEND"})

    elif arg == "NEW":
        s.cursor.execute(
            "select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1,DeclarantCompany.code from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId="
            " +'{UserName}'".format(UserName=request.session["Username"])
        )
        headData = s.cursor.fetchall()
        for i in ManageUser.objects.filter(UserName=Username):
            mailBoxId = i.MailBoxId
            AccountId = i.AccountId
        inHeaderReId = (
            len(
                InheaderTbl.objects.filter(
                    MSGId__icontains=nowRefId, MessageType="IPTDEC"
                )
            )
            + 1
        )
        inHeaderReId = "%03d" % inHeaderReId
        inHeaderJobId1 = (
            len(
                PermitCount.objects.filter(
                    TouchTime__icontains=nowJobId, AccountId=AccountId
                )
            )
            + 1
        )
        inHeaderJobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % inHeaderJobId1}"
        inHeaderMsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % inHeaderJobId1}"
        inHeaderPermitId = f"{Username}{nowRefId}{inHeaderReId}"
        request.session["Permit_Id"] = inHeaderPermitId

    context.update(
        {
            "UserName": Username,
            "PermitId": str(inHeaderPermitId).upper(),
            "MsgId": inHeaderMsgId,
            "JobId": inHeaderJobId,
            "RefId": inHeaderReId,
            "headmailId": headData[0][2],
            "headdeclarantName": headData[0][6],
            "headdeclarantCode": headData[0][7],
            "headdeclarantTelephone": headData[0][8],
            "headCrueiNo": headData[0][9],
            "headname": headData[0][11],
            "headname1": headData[0][12],
            "headdataCode": headData[0][13],
            "CurrentDate": currentDate ,
            "DeclarationType": CommonMaster.objects.filter(TypeId=1, StatusId=1),
            "InondeclarationTypeValue": CommonMaster.objects.filter(
                TypeId=13, StatusId=1
            ),
            "CargoType": CommonMaster.objects.filter(TypeId=2, StatusId=1),
            "InwardTransportMode": CommonMaster.objects.filter(
                TypeId=3, StatusId=1
            ).order_by("Name"),
            "DeclaringFor": CommonMaster.objects.filter(TypeId=80, StatusId=1).order_by(
                "Name"
            ),
            "BgIndicator": CommonMaster.objects.filter(TypeId=4, StatusId=1).order_by(
                "Name"
            ),
            "DocumentAttachmentType": CommonMaster.objects.filter(
                TypeId=5, StatusId=1
            ).order_by("Name"),
            "totalOuterPack": CommonMaster.objects.filter(
                TypeId=10, StatusId=1
            ).order_by("Name"),
            "Currency": Currency.objects.all().order_by("Currency"),
            "invoiceTermType": CommonMaster.objects.filter(
                TypeId=7, StatusId=1
            ).order_by("Name"),
            "Container": CommonMaster.objects.filter(TypeId=6, StatusId=1).order_by(
                "Name"
            ),
            "MakingLot": CommonMaster.objects.filter(TypeId=12, StatusId=1).order_by(
                "Name"
            ),
            "VehicalType": CommonMaster.objects.filter(TypeId=20, StatusId=1).order_by(
                "Name"
            ),
            "EngineCapacity": CommonMaster.objects.filter(
                TypeId=21, StatusId=1
            ).order_by("Name"),
            "Preferntial": CommonMaster.objects.filter(TypeId=11, StatusId=1).order_by(
                "Name"
            ),
            "ReleaseLocation": ReleaseLocation.objects.all().order_by("locationCode"),
            "ReceiptLocation": ReceiptLocation.objects.all().order_by("locationCode"),
            "LoadingPort": LoadingPort.objects.all().order_by("portcode"),
            "Country": COUNTRY.objects.all().order_by("CountryCode"),
        }
    )

    return render(request, "Inpayment/InpaymentNew.html", context)



def InpaymentHeader(request):
    Username = request.session["Username"]
    s = SqlDb()
    for i in ManageUser.objects.filter(UserName=Username):
        mailBoxId = i.MailBoxId
        AccountId = i.AccountId
    nowdata = datetime.now() - timedelta(days=60)
    s.cursor.execute(
        "SELECT t1.Id as 'ID', t1.JobId as 'JOB ID', t1.MSGId as 'MSG ID', CONVERT(varchar, t1.TouchTime, 105) AS 'DEC DATE', SUBSTRING(t1.DeclarationType, 1, case when  CHARINDEX(' ', t1.DeclarationType ) = 0 then LEN(t1.DeclarationType) else CHARINDEX(' ', t1.DeclarationType) - 1 end) AS 'DEC TYPE', t1.TouchUser AS 'CREATE', t2.TradeNetMailboxID AS 'DEC ID', CONVERT(varchar, t1.ArrivalDate, 105) AS ETA, t1.PermitNumber AS 'PERMIT NO',t3.Name+' '+t3.Name1 AS 'IMPORTER',STUFF((SELECT distinct(', ' +  US.InHAWBOBL)  FROM ItemDtl US WHERE US.PermitId = t1.PermitId FOR XML PATH('')), 1, 1, '') 'HAWB',CASE  WHEN  t1.InwardTransportMode = '4 : Air' THEN t1.MasterAirwayBill  WHEN t1.InwardTransportMode = '1 : Sea'  THEN t1.OceanBillofLadingNo  ELSE ''  END AS 'MAWB/OBL',t1.LoadingPortCode as POL, t1.MessageType as 'MSG TYPE',t1.InwardTransportMode as TPT, t1.PreviousPermit as 'PRE PMT',t1.GrossReference as 'X REF', t1.InternalRemarks as 'INT REM',SUM(t1.TotalGSTTaxAmt) AS 'GST AMT', t1.Status as 'STATUS', 'Default' as  'COLOR',t1.PermitId  FROM  InHeaderTbl AS t1 left JOIN DeclarantCompany AS t2 ON t1.DeclarantCompanyCode = t2.Code left JOIN Importer AS t3 ON t1.ImporterCompanyCode = t3.Code   left JOIN ManageUser AS t6 ON t6.UserId=t1.TouchUser   where t6.AccountId='"
        + AccountId
        + "' and convert(varchar,t1.TouchTime,111)>='"
        + nowdata.strftime("%Y/%m/%d")
        + " 'GROUP BY t1.Id, t1.JobId, t1.MSGId, t1.TouchTime, t1.TouchUser, t1.DeclarationType, t1.ArrivalDate, t1.PermitId, t1.InwardTransportMode, t1.MasterAirwayBill, t1.OceanBillofLadingNo, t1.LoadingPortCode, t1.MessageType, t1.InwardTransportMode, t1.PreviousPermit,t1.InternalRemarks, t1.Status, t2.TradeNetMailboxID,t2.DeclarantName,t1.GrossReference ,t1.License,t1.ReleaseLocation,t1.RecepitLocation,t1.DeclarningFor,t3.Name,t3.Name1,t6.AccountId,t1.PermitNumber"
    )

    # result = (pd.DataFrame(list(s.cursor.fetchall()), columns=["id","JobId","MSGId","DECDATE","DECTYPE","CREATE","DECID","ETA","PERMITNO","IMPORTER","HAWB","MAWBOBL","POL","MSGTYPE","TPT","PREPMT","XREF","INTREM","GSTAMT","STATUS","default","PermitId"])).to_dict('records')
    headLen = list(s.cursor.fetchall())
    headLen.sort(reverse=True)
    result = []
    result = list(
        map(
            lambda row: {
                "id": row[0],
                "JobId": row[1],
                "MSGId": row[2],
                "DECDATE": row[3],
                "DECTYPE": row[4],
                "CREATE": row[5],
                "DECID": row[6],
                "ETA": row[7],
                "PERMITNO": row[8],
                "IMPORTER": row[9],
                "HAWB": row[10],
                "MAWBOBL": row[11],
                "POL": row[12],
                "MSGTYPE": row[13],
                "TPT": row[14],
                "PREPMT": row[15],
                "XREF": row[16],
                "INTREM": row[17],
                "GSTAMT": str(row[18]),
                "STATUS": row[19],
                "default": row[20],
                "PermitId": row[21],
            },
            headLen,
        )
    )
    return JsonResponse(result, safe=False)


def ItemExcelDownload(request):
    response = HttpResponse(
        open(
            "D:\\New folder\\NNR REPORT FILE\\OUT & COO Type Changes\\RET\\RET\\ExcelTemplate\\InPaymentExcel.xlsx",
            "rb",
        ).read()
    )
    response["Content-Type"] = "text/csv"
    response["Content-Disposition"] = f"attachment; filename=InPaymentExcel.xlsx"
    return response


def ItemExcelUpload(request):
    xlsx_file = request.FILES["file"]

    PermitId = request.POST.get("PermitId")
    MsgType = request.POST.get("MsgType")
    userName = request.POST.get("UserName")
    TouchTime = request.POST.get("TouchTime")
    

    ItemInfo = pd.read_excel(xlsx_file, sheet_name="ItemInfo")
    print('ItemInfo:', ItemInfo)
    print('ItemInfo data types:', ItemInfo.dtypes)

    casc = False
    contain = False
    if "Casccodes" in pd.ExcelFile(xlsx_file).sheet_names:
        CascInfo = pd.read_excel(xlsx_file, sheet_name="Casccodes")
        casc = True
        print('CascInfo:', CascInfo)
        print('CascInfo data types:', CascInfo.dtypes)

    if "ContainerInfo" in pd.ExcelFile(xlsx_file).sheet_names:
        contain = True
        ContainerInfo = pd.read_excel(xlsx_file, sheet_name="ContainerInfo")
        print('ContainerInfo:', ContainerInfo)
        print('ContainerInfo data types:', ContainerInfo.dtypes)
    
    ItemData = []
    CascData = []
    ContainerData = []

    ItemColumns = {
        "CountryofOrigin": "",
        "HSCode": "",
        "HSQty": "0.00",
        "TotalLineAmount": "0.00",
        "ItemCode": "",
        "Description": "",
        "DGIndicator": "False",
        "Brand": "",
        "Model": "",
        "InHAWBOBL": "",
        "OutHAWBOBL": "",
        "HSUOM": "--Select--",
        "InvoiceNumber": "",
        "ItemCurrency": "--Select--",
        "UnitPrice": "0.00",
        "TotalDutiableQty": "0.00",
        "TotalDutiableUOM": "--Select--",
        "DutiableQty": "0.00",
        "DutiableUOM": "--Select--",
        "OuterPackQty": "0.00",
        "OuterPackUOM": "--Select--",
        "InPackQty": "0.00",
        "InPackUOM": "--Select--",
        "InnerPackQty": "0.00",
        "InnerPackUOM": "--Select--",
        "InmostPackQty": "0.00",
        "InmostPackUOM": "--Select--",
        "LastSellingPrice": "0.00",
        "TarrifPreferentialCode": "--Select--",
        "OtherTaxRate": "0.00",
        "OtherTaxUOM": "--Select--",
        "OtherTaxAmount": "0.00",
        "CurrentLot": "",
        "PreviousLot": "",
        "AlcoholPercentage": "0.00",
        "ShippingMarks1": "",
        "ShippingMarks2": "",
        "ShippingMarks3": "",
        "ShippingMarks4": "",
    }

    CascColumn = {
        "ItemNo": "",
        "ProductCode": "",
        "Quantity": "0.00",
        "ProductUOM": "--Select--",
        "RowNo": "",
        "CascCode1": "",
        "CascCode2": "",
        "CascCode3": "",
        "CASCId": "",
    }

    ContainerColumn = {
        "SNo": "",
        "ContainerNo": "",
        "SizeType": "",
        "Weight": "",
        "SealNo": "",
    }

    ItemInfo.fillna(ItemColumns, inplace=True)
    
    
    if casc and contain:
        for index, row in ItemInfo.iterrows():
            ItemLen = len(ItemDtl.objects.filter(PermitId=PermitId)) + (index + 1)
            try:
                ItemData.append(
                    ItemDtl(
                        Contry=row["CountryofOrigin"],
                        HSCode=row["HSCode"],
                        HSQty=row["HSQty"],
                        TotalLineAmount=row["TotalLineAmount"],
                        Description=row["Description"],
                        DGIndicator=row["DGIndicator"],
                        Brand=row["Brand"],
                        Model=row["Model"],
                        InHAWBOBL=row["InHAWBOBL"],
                        HSUOM=row["HSUOM"],
                        InvoiceNo=row["InvoiceNumber"],
                        UnitPriceCurrency=row["ItemCurrency"],
                        UnitPrice=row["UnitPrice"],
                        TotalDutiableQty=row["TotalDutiableQty"],
                        TotalDutiableUOM=row["TotalDutiableUOM"],
                        DutiableQty=row["DutiableQty"],
                        DutiableUOM=row["DutiableUOM"],
                        OPQty=row["OuterPackQty"],
                        OPUOM=row["OuterPackUOM"],
                        IPQty=row["InPackQty"],
                        IPUOM=row["InPackUOM"],
                        InPqty=row["InnerPackQty"],
                        InPUOM=row["InnerPackUOM"],
                        ImPQty=row["InmostPackQty"],
                        ImPUOM=row["InmostPackUOM"],
                        LSPValue=row["LastSellingPrice"],
                        PreferentialCode=row["TarrifPreferentialCode"],
                        OtherTaxRate=row["OtherTaxRate"],
                        OtherTaxUOM=row["OtherTaxUOM"],
                        OtherTaxAmount=row["OtherTaxAmount"],
                        CurrentLot=row["CurrentLot"],
                        PreviousLot=row["PreviousLot"],
                        AlcoholPer=row["AlcoholPercentage"],
                        ShippingMarks1=row["ShippingMarks1"],
                        ShippingMarks2=row["ShippingMarks2"],
                        ShippingMarks3=row["ShippingMarks3"],
                        ShippingMarks4=row["ShippingMarks4"],
                        ItemNo=ItemLen,
                        PermitId=PermitId,
                        MessageType=MsgType,
                        TouchUser=userName,
                        TouchTime=TouchTime,
                        InvoiceQuantity="0.00",
                        ChkUnitPrice="0.00",
                        ExchangeRate="0.00",
                        SumExchangeRate="0.00",
                        InvoiceCharges="0.00",
                        CIFFOB="0.00",
                        GSTRate="0.00",
                        GSTUOM="PER",
                        GSTAmount="0.00",
                        ExciseDutyRate="0.00",
                        ExciseDutyUOM="--Select--",
                        ExciseDutyAmount="0.00",
                        CustomsDutyRate="0.00",
                        CustomsDutyUOM="",
                        CustomsDutyAmount="0.00",
                        Making="--Select--",
                        VehicleType="--Select--",
                        EngineCapcity="--Select--",
                        EngineCapUOM="--Select--",
                        orignaldatereg=TouchTime,
                        OptionalChrgeUOM="--Select--",
                        Optioncahrge="0.00",
                        OptionalSumtotal="0.00",
                        OptionalSumExchage="0.00",
                    )
                )
            except Exception as e:
                pass
        
        ItemDtl.objects.bulk_create(ItemData)  
    else:
        ItemColumns = {
            "Description" : "",
            "HSCode" : "",
            "HSUOM" : "--Select--",
            "INV QTY" : "0.00",
            "HSQty" : "0.00",
            "ProductCode" : "",
            "Quantity" : "0.00",
            "ProductUOM" : "--Select--",
            "CountryofOrigin" : "",
            "RowNo" : "",
            "CascCode1" : "",
            "CascCode2" : "",
            "CascCode3" : "",
            "CASCId" : "",
            "Brand" : "",
            "InvoiceNumber" : "",
            "Currency" : "0.00",
            "Exchangerate" : "0.00",
            "Total Line Amount " : "0.00",
            "Invoice Amount " : "0.00",
            "Other Amount " : "0.00",
            "Freight Amount" : "0.00",
            "insurance Amount" : "0.00",
            "invoice charge " : "0.00",
            "CIF value " : "0.00",
            "GST Amount " : "0.00",  
        }                       
        ItemInfo.fillna(ItemColumns, inplace=True)
        
        for index, row in ItemInfo.iterrows():
            ItemLen = len(ItemDtl.objects.filter(PermitId=PermitId))+1
            if row["HSCode"] != "":
                try: 
                    ItemDtl.objects.create(
                            Contry=row["CountryofOrigin"],
                            HSCode=str(int(row["HSCode"])),
                            HSQty=row["HSQty"],
                            TotalLineAmount=row["Total Line Amount"],
                            Description=row["Description"],
                            DGIndicator="False",
                            Brand=row["Brand"],
                            Model="",
                            InHAWBOBL="",
                            HSUOM=row["HSUOM"],
                            InvoiceNo=row["InvoiceNumber"],
                            UnitPriceCurrency="--Select--",
                            UnitPrice="0.00",
                            TotalDutiableQty="0.00",
                            TotalDutiableUOM="--Select--",
                            DutiableQty="0.00",
                            DutiableUOM="--Select--",
                            OPQty="0.00",
                            OPUOM="--Select--",
                            IPQty="0.00",
                            IPUOM="--Select--",
                            InPqty="0.00",
                            InPUOM="--Select--",
                            ImPQty="0.00",
                            ImPUOM="--Select--",
                            LSPValue="0.00",
                            PreferentialCode="--Select--",
                            OtherTaxRate="0.00",
                            OtherTaxUOM="--Select--",
                            OtherTaxAmount="0.00",
                            CurrentLot="",
                            PreviousLot="",
                            AlcoholPer="0.00",
                            ShippingMarks1="",
                            ShippingMarks2="",
                            ShippingMarks3="",
                            ShippingMarks4="",
                            ItemNo=ItemLen,
                            PermitId=PermitId,
                            MessageType=MsgType,
                            TouchUser=userName,
                            TouchTime=TouchTime,
                            InvoiceQuantity="0.00",
                            ChkUnitPrice="0.00",
                            ExchangeRate="0.00",
                            SumExchangeRate="0.00",
                            InvoiceCharges="0.00",
                            CIFFOB="0.00",
                            GSTRate="0.00",
                            GSTUOM="PER",
                            GSTAmount="0.00",
                            ExciseDutyRate="0.00",
                            ExciseDutyUOM="--Select--",
                            ExciseDutyAmount="0.00",
                            CustomsDutyRate="0.00",
                            CustomsDutyUOM="",
                            CustomsDutyAmount="0.00",
                            Making="--Select--",
                            VehicleType="--Select--",
                            EngineCapcity="--Select--",
                            EngineCapUOM="--Select--",
                            orignaldatereg="",
                            OptionalChrgeUOM="--Select--",
                            Optioncahrge="0.00",
                            OptionalSumtotal="0.00",
                            OptionalSumExchage="0.00",
                        )
                    if row["ProductCode"] != "":
                        Cascdtl.objects.create(
                            ItemNo=ItemLen,
                            ProductCode=row["ProductCode"],
                            Quantity=row["Quantity"],
                            ProductUOM=row["ProductUOM"],
                            RowNo=str(int(row["RowNo"])),
                            CascCode1=row["CascCode1"],
                            CascCode2=row["CascCode2"],
                            CascCode3=row["CascCode3"],
                            PermitId=PermitId,
                            MessageType=MsgType,
                            TouchUser=userName,
                            TouchTime=TouchTime,
                            CascId=row["CASCId"],
                        )

                except Exception as e:
                    print("Error while creating object:", e)
            else:
                print("Loop is Breaked")
                break
    

    if casc:
        CascInfo.fillna(CascColumn, inplace=True)
        for index, row in CascInfo.iterrows():
            if row["ProductCode"] != "":
                CascData.append(
                    Cascdtl(
                        ItemNo=row["ItemNo"],
                        ProductCode=row["ProductCode"],
                        Quantity=row["Quantity"],
                        ProductUOM=row["ProductUOM"],
                        RowNo=row["RowNo"],
                        CascCode1=row["CascCode1"],
                        CascCode2=row["CascCode2"],
                        CascCode3=row["CascCode3"],
                        PermitId=PermitId,
                        MessageType=MsgType,
                        TouchUser=userName,
                        TouchTime=TouchTime,
                        CascId=row["CASCId"],
                    )
                )
        Cascdtl.objects.bulk_create(CascData)
    
    if contain:
        ContainerInfo.fillna(ContainerColumn, inplace=True)
        for index, row in ContainerInfo.iterrows():
            if row["SNo"] != "":
                ContainerData.append(
                    PermitId=PermitId,
                    RowNo=row["SNo"],
                    ContainerNo=row["ContainerNo"],
                    size=row["SizeType"],
                    weight=row["Weight"],
                    SealNo=row["SealNo"],
                    MessageType=MsgType,
                    TouchUser=userName,
                    TouchTime=TouchTime,
                )
        ContainerDtl.objects.bulk_create(ContainerData)
    

    Item = list(ItemDtl.objects.filter(PermitId=PermitId).order_by("ItemNo").values())
    ItemCasc = list(Cascdtl.objects.filter(PermitId=PermitId).order_by("ItemNo").values())

    print("Item Data:")
    for item in Item:
        for key, value in item.items():
            print(f"{key}: {type(value)}")

    print("\nItem Casc Data:")
    for item_casc in ItemCasc:
        for key, value in item_casc.items():
            print(f"{key}: {type(value)}")

    return JsonResponse({"Item": Item, "ItemCasc": ItemCasc,"message": "All Item Inserted Successfully", "Result": "Deleted"})



# def ItemExcelUpload(request):

#     xlsx_file = request.FILES["file"]

#     PermitId = request.POST.get("PermitId")
#     MsgType = request.POST.get("MsgType")
#     userName = request.POST.get("UserName")
#     TouchTime = request.POST.get("TouchTime")
    
#     # Read the Excel file, explicitly specifying the data type of the "HSCode" column as string
#     ItemInfo = pd.read_excel(xlsx_file, sheet_name="ItemInfo", dtype={"HSCode": str})
#     print('ItemInfo:',ItemInfo)
#     print('ItemInfo data types:', ItemInfo.dtypes)
    
#     casc = False
#     contain = False
#     if "Casccodes" in pd.ExcelFile(xlsx_file).sheet_names:
#         CascInfo = pd.read_excel(xlsx_file, sheet_name="Casccodes")
#         casc = True
#         print('CascInfo:', CascInfo)
#         print('CascInfo data types:', CascInfo.dtypes)

#     if "ContainerInfo" in pd.ExcelFile(xlsx_file).sheet_names:
#         contain = True
#         ContainerInfo = pd.read_excel(xlsx_file, sheet_name="ContainerInfo")
#         print('ContainerInfo:', ContainerInfo)
#         print('ContainerInfo data types:', ContainerInfo.dtypes)
#     ItemData = []
#     CascData = []
#     ContainerData = []

#     ItemColumns = {
#         "CountryofOrigin": "",
#         "HSCode": "",
#         "HSQty": "0.00",
#         "TotalLineAmount": "0.00",
#         "ItemCode": "",
#         "Description": "",
#         "DGIndicator": "False",
#         "Brand": "",
#         "Model": "",
#         "InHAWBOBL": "",
#         "OutHAWBOBL": "",
#         "HSUOM": "--Select--",
#         "InvoiceNumber": "",
#         "ItemCurrency": "--Select--",
#         "UnitPrice": "0.00",
#         "TotalDutiableQty": "0.00",
#         "TotalDutiableUOM": "--Select--",
#         "DutiableQty": "0.00",
#         "DutiableUOM": "--Select--",
#         "OuterPackQty": "0.00",
#         "OuterPackUOM": "--Select--",
#         "InPackQty": "0.00",
#         "InPackUOM": "--Select--",
#         "InnerPackQty": "0.00",
#         "InnerPackUOM": "--Select--",
#         "InmostPackQty": "0.00",
#         "InmostPackUOM": "--Select--",
#         "LastSellingPrice": "0.00",
#         "TarrifPreferentialCode": "--Select--",
#         "OtherTaxRate": "0.00",
#         "OtherTaxUOM": "--Select--",
#         "OtherTaxAmount": "0.00",
#         "CurrentLot": "",
#         "PreviousLot": "",
#         "AlcoholPercentage": "0.00",
#         "ShippingMarks1": "",
#         "ShippingMarks2": "",
#         "ShippingMarks3": "",
#         "ShippingMarks4": "",
#     }

#     CascColumn = {
#         "ItemNo": "",
#         "ProductCode": "",
#         "Quantity": "0.00",
#         "ProductUOM": "--Select--",
#         "RowNo": "",
#         "CascCode1": "",
#         "CascCode2": "",
#         "CascCode3": "",
#         "CASCId": "",
#     }

#     ContainerColumn = {
#         "SNo": "",
#         "ContainerNo": "",
#         "SizeType": "",
#         "Weight": "",
#         "SealNo": "",
#     }

#     ItemInfo.fillna(ItemColumns, inplace=True)
    
    
#     if casc and contain:
#         for index, row in ItemInfo.iterrows():
#             ItemLen = len(ItemDtl.objects.filter(PermitId=PermitId)) + (index + 1)
#             try:
#                 ItemData.append(
#                     ItemDtl(
#                         Contry=row["CountryofOrigin"],
#                         HSCode=row["HSCode"],
#                         HSQty=row["HSQty"],
#                         TotalLineAmount=row["TotalLineAmount"],
#                         Description=row["Description"],
#                         DGIndicator=row["DGIndicator"],
#                         Brand=row["Brand"],
#                         Model=row["Model"],
#                         InHAWBOBL=row["InHAWBOBL"],
#                         HSUOM=row["HSUOM"],
#                         InvoiceNo=row["InvoiceNumber"],
#                         UnitPriceCurrency=row["ItemCurrency"],
#                         UnitPrice=row["UnitPrice"],
#                         TotalDutiableQty=row["TotalDutiableQty"],
#                         TotalDutiableUOM=row["TotalDutiableUOM"],
#                         DutiableQty=row["DutiableQty"],
#                         DutiableUOM=row["DutiableUOM"],
#                         OPQty=row["OuterPackQty"],
#                         OPUOM=row["OuterPackUOM"],
#                         IPQty=row["InPackQty"],
#                         IPUOM=row["InPackUOM"],
#                         InPqty=row["InnerPackQty"],
#                         InPUOM=row["InnerPackUOM"],
#                         ImPQty=row["InmostPackQty"],
#                         ImPUOM=row["InmostPackUOM"],
#                         LSPValue=row["LastSellingPrice"],
#                         PreferentialCode=row["TarrifPreferentialCode"],
#                         OtherTaxRate=row["OtherTaxRate"],
#                         OtherTaxUOM=row["OtherTaxUOM"],
#                         OtherTaxAmount=row["OtherTaxAmount"],
#                         CurrentLot=row["CurrentLot"],
#                         PreviousLot=row["PreviousLot"],
#                         AlcoholPer=row["AlcoholPercentage"],
#                         ShippingMarks1=row["ShippingMarks1"],
#                         ShippingMarks2=row["ShippingMarks2"],
#                         ShippingMarks3=row["ShippingMarks3"],
#                         ShippingMarks4=row["ShippingMarks4"],
#                         ItemNo=ItemLen,
#                         PermitId=PermitId,
#                         MessageType=MsgType,
#                         TouchUser=userName,
#                         TouchTime=TouchTime,
#                         InvoiceQuantity="0.00",
#                         ChkUnitPrice="0.00",
#                         ExchangeRate="0.00",
#                         SumExchangeRate="0.00",
#                         InvoiceCharges="0.00",
#                         CIFFOB="0.00",
#                         GSTRate="0.00",
#                         GSTUOM="PER",
#                         GSTAmount="0.00",
#                         ExciseDutyRate="0.00",
#                         ExciseDutyUOM="--Select--",
#                         ExciseDutyAmount="0.00",
#                         CustomsDutyRate="0.00",
#                         CustomsDutyUOM="",
#                         CustomsDutyAmount="0.00",
#                         Making="--Select--",
#                         VehicleType="--Select--",
#                         EngineCapcity="--Select--",
#                         EngineCapUOM="--Select--",
#                         orignaldatereg=TouchTime,
#                         OptionalChrgeUOM="--Select--",
#                         Optioncahrge="0.00",
#                         OptionalSumtotal="0.00",
#                         OptionalSumExchage="0.00",
#                     )
#                 )
#             except Exception as e:
#                 pass
        
#         ItemDtl.objects.bulk_create(ItemData)  
#     else:
#         ItemColumns = {
#             "Description" : "",
#             "HSCode" : "",
#             "HSUOM" : "--Select--",
#             "INV QTY" : "0.00",
#             "HSQty" : "0.00",
#             "ProductCode" : "",
#             "Quantity" : "0.00",
#             "ProductUOM" : "--Select--",
#             "CountryofOrigin" : "",
#             "RowNo" : "",
#             "CascCode1" : "",
#             "CascCode2" : "",
#             "CascCode3" : "",
#             "CASCId" : "",
#             "Brand" : "",
#             "InvoiceNumber" : "",
#             "Currency" : "0.00",
#             "Exchangerate" : "0.00",
#             "Total Line Amount " : "0.00",
#             "Invoice Amount " : "0.00",
#             "Other Amount " : "0.00",
#             "Freight Amount" : "0.00",
#             "insurance Amount" : "0.00",
#             "invoice charge " : "0.00",
#             "CIF value " : "0.00",
#             "GST Amount " : "0.00",  
#         }                       
#         ItemInfo.fillna(ItemColumns, inplace=True)
        
#         for index, row in ItemInfo.iterrows():
#             ItemLen = len(ItemDtl.objects.filter(PermitId=PermitId))+1
#             if row["HSCode"] != "":
#                 try: 
#                     ItemDtl.objects.create(
#                             Contry=row["CountryofOrigin"],
#                             HSCode=str(row["HSCode"]),
#                             HSQty=row["HSQty"],
#                             TotalLineAmount=row["Total Line Amount"],
#                             Description=row["Description"],
#                             DGIndicator="False",
#                             Brand=row["Brand"],
#                             Model="",
#                             InHAWBOBL="",
#                             HSUOM=row["HSUOM"],
#                             InvoiceNo=row["InvoiceNumber"],
#                             UnitPriceCurrency="--Select--",
#                             UnitPrice="0.00",
#                             TotalDutiableQty="0.00",
#                             TotalDutiableUOM="--Select--",
#                             DutiableQty="0.00",
#                             DutiableUOM="--Select--",
#                             OPQty="0.00",
#                             OPUOM="--Select--",
#                             IPQty="0.00",
#                             IPUOM="--Select--",
#                             InPqty="0.00",
#                             InPUOM="--Select--",
#                             ImPQty="0.00",
#                             ImPUOM="--Select--",
#                             LSPValue="0.00",
#                             PreferentialCode="--Select--",
#                             OtherTaxRate="0.00",
#                             OtherTaxUOM="--Select--",
#                             OtherTaxAmount="0.00",
#                             CurrentLot="",
#                             PreviousLot="",
#                             AlcoholPer="0.00",
#                             ShippingMarks1="",
#                             ShippingMarks2="",
#                             ShippingMarks3="",
#                             ShippingMarks4="",
#                             ItemNo=ItemLen,
#                             PermitId=PermitId,
#                             MessageType=MsgType,
#                             TouchUser=userName,
#                             TouchTime=TouchTime,
#                             InvoiceQuantity="0.00",
#                             ChkUnitPrice="0.00",
#                             ExchangeRate="0.00",
#                             SumExchangeRate="0.00",
#                             InvoiceCharges="0.00",
#                             CIFFOB="0.00",
#                             GSTRate="0.00",
#                             GSTUOM="PER",
#                             GSTAmount="0.00",
#                             ExciseDutyRate="0.00",
#                             ExciseDutyUOM="--Select--",
#                             ExciseDutyAmount="0.00",
#                             CustomsDutyRate="0.00",
#                             CustomsDutyUOM="",
#                             CustomsDutyAmount="0.00",
#                             Making="--Select--",
#                             VehicleType="--Select--",
#                             EngineCapcity="--Select--",
#                             EngineCapUOM="--Select--",
#                             orignaldatereg="",
#                             OptionalChrgeUOM="--Select--",
#                             Optioncahrge="0.00",
#                             OptionalSumtotal="0.00",
#                             OptionalSumExchage="0.00",
#                         )
#                     if row["ProductCode"] != "":
#                         Cascdtl.objects.create(
#                             ItemNo=ItemLen,
#                             ProductCode=row["ProductCode"],
#                             Quantity=row["Quantity"],
#                             ProductUOM=row["ProductUOM"],
#                             RowNo=str(row["RowNo"]),
#                             CascCode1=row["CascCode1"],
#                             CascCode2=row["CascCode2"],
#                             CascCode3=row["CascCode3"],
#                             PermitId=PermitId,
#                             MessageType=MsgType,
#                             TouchUser=userName,
#                             TouchTime=TouchTime,
#                             CascId=row["CASCId"],
#                         )

#                 except Exception as e:
#                     print("Error while creating object:", e)
#             else:
#                 print("Loop is Breaked")
#                 break
    

#     if casc:
#         CascInfo.fillna(CascColumn, inplace=True)
#         for index, row in CascInfo.iterrows():
#             if row["ProductCode"] != "":
#                 CascData.append(
#                     Cascdtl(
#                         ItemNo=row["ItemNo"],
#                         ProductCode=row["ProductCode"],
#                         Quantity=row["Quantity"],
#                         ProductUOM=row["ProductUOM"],
#                         RowNo=row["RowNo"],
#                         CascCode1=row["CascCode1"],
#                         CascCode2=row["CascCode2"],
#                         CascCode3=row["CascCode3"],
#                         PermitId=PermitId,
#                         MessageType=MsgType,
#                         TouchUser=userName,
#                         TouchTime=TouchTime,
#                         CascId=row["CASCId"],
#                     )
#                 )
#         Cascdtl.objects.bulk_create(CascData)
    
#     if contain:
#         ContainerInfo.fillna(ContainerColumn, inplace=True)
#         for index, row in ContainerInfo.iterrows():
#             if row["SNo"] != "":
#                 ContainerData.append(
#                     PermitId=PermitId,
#                     RowNo=row["SNo"],
#                     ContainerNo=row["ContainerNo"],
#                     size=row["SizeType"],
#                     weight=row["Weight"],
#                     SealNo=row["SealNo"],
#                     MessageType=MsgType,
#                     TouchUser=userName,
#                     TouchTime=TouchTime,
#                 )
#         ContainerDtl.objects.bulk_create(ContainerData)
    

#     Item = list(ItemDtl.objects.filter(PermitId=PermitId).order_by("ItemNo").values())
#     ItemCasc = list(Cascdtl.objects.filter(PermitId=PermitId).order_by("ItemNo").values())
#     print("Item Data:")
#     for item in Item:
#         for key, value in item.items():
#             print(f"{key}: {type(value)}")

#     print("\nItem Casc Data:")
#     for item_casc in ItemCasc:
#         for key, value in item_casc.items():
#             print(f"{key}: {type(value)}")
#     return JsonResponse({"Item": Item, "ItemCasc": ItemCasc,"message": "All Item Inserted Successfully", "Result": "Deleted"})


def AllItemUpdate(request):
    try:
        Item = json.loads(request.POST.get("Item"))
        PermitId = request.POST.get("PermitId")
        df = pd.DataFrame(Item)
        s = SqlDb()
        for _, rows in df.iterrows():
            Qry = f"UPDATE ItemDtl SET MessageType  = %s  , HSCode  = %s  , Description  = %s  , DGIndicator  = %s  , Contry  = %s  , Brand  = %s  , Model  = %s  , InHAWBOBL  = %s  , DutiableQty  = %s  , DutiableUOM  = %s  , TotalDutiableQty  = %s  , TotalDutiableUOM  = %s  , InvoiceQuantity  = %s  , HSQty  = %s  , HSUOM  = %s  , AlcoholPer  = %s  , InvoiceNo  = %s  , ChkUnitPrice  = %s  , UnitPrice  = %s  , UnitPriceCurrency  = %s  , ExchangeRate  = %s  , SumExchangeRate  = %s  , TotalLineAmount  = %s  , InvoiceCharges  = %s  , CIFFOB  = %s  , OPQty  = %s  , OPUOM  = %s  , IPQty  = %s  , IPUOM  = %s  , InPqty  = %s  , InPUOM  = %s  , ImPQty  = %s  , ImPUOM  = %s  , PreferentialCode  = %s  , GSTRate  = %s  , GSTUOM  = %s  , GSTAmount  = %s  , ExciseDutyRate  = %s  , ExciseDutyUOM  = %s  , ExciseDutyAmount  = %s  , CustomsDutyRate  = %s  , CustomsDutyUOM  = %s  , CustomsDutyAmount  = %s  , OtherTaxRate  = %s  , OtherTaxUOM  = %s  , OtherTaxAmount  = %s  , CurrentLot  = %s  , PreviousLot  = %s  , LSPValue  = %s  , Making  = %s  , ShippingMarks1  = %s  , ShippingMarks2  = %s  , ShippingMarks3  = %s  , ShippingMarks4  = %s  , TouchUser  = %s  , TouchTime  = %s  , VehicleType  = %s  , EngineCapcity  = %s  , EngineCapUOM  = %s  , orignaldatereg  = %s  , OptionalChrgeUOM  = %s  , Optioncahrge  = %s  , OptionalSumtotal  = %s  , OptionalSumExchage  = %s  WHERE ItemNo  = %s AND PermitId  = %s"
            Val = (
                rows["MessageType"],
                rows["HSCode"],
                rows["Description"],
                rows["DGIndicator"],
                rows["Contry"],
                rows["Brand"],
                rows["Model"],
                rows["InHAWBOBL"],
                rows["DutiableQty"],
                rows["DutiableUOM"],
                rows["TotalDutiableQty"],
                rows["TotalDutiableUOM"],
                rows["InvoiceQuantity"],
                rows["HSQty"],
                rows["HSUOM"],
                rows["AlcoholPer"],
                rows["InvoiceNo"],
                rows["ChkUnitPrice"],
                rows["UnitPrice"],
                rows["UnitPriceCurrency"],
                rows["ExchangeRate"],
                rows["SumExchangeRate"],
                rows["TotalLineAmount"],
                rows["InvoiceCharges"],
                rows["CIFFOB"],
                rows["OPQty"],
                rows["OPUOM"],
                rows["IPQty"],
                rows["IPUOM"],
                rows["InPqty"],
                rows["InPUOM"],
                rows["ImPQty"],
                rows["ImPUOM"],
                rows["PreferentialCode"],
                rows["GSTRate"],
                rows["GSTUOM"],
                rows["GSTAmount"],
                rows["ExciseDutyRate"],
                rows["ExciseDutyUOM"],
                rows["ExciseDutyAmount"],
                rows["CustomsDutyRate"],
                rows["CustomsDutyUOM"],
                rows["CustomsDutyAmount"],
                rows["OtherTaxRate"],
                rows["OtherTaxUOM"],
                rows["OtherTaxAmount"],
                rows["CurrentLot"],
                rows["PreviousLot"],
                rows["LSPValue"],
                rows["Making"],
                rows["ShippingMarks1"],
                rows["ShippingMarks2"],
                rows["ShippingMarks3"],
                rows["ShippingMarks4"],
                rows["TouchUser"],
                rows["TouchTime"],
                rows["VehicleType"],
                rows["EngineCapcity"],
                rows["EngineCapUOM"],
                rows["orignaldatereg"],
                rows["OptionalChrgeUOM"],
                rows["Optioncahrge"],
                rows["OptionalSumtotal"],
                rows["OptionalSumExchage"],
                rows["ItemNo"],
                rows["PermitId"],
            )
            s.cursor.execute(Qry, Val)
        s.conn.commit()
        Item = list(ItemDtl.objects.filter(PermitId=PermitId).order_by("ItemNo").values())
        ItemCasc = list(Cascdtl.objects.filter(PermitId=PermitId).order_by("ItemNo").values())
        return JsonResponse(
            {
                "Item": Item,
                "ItemCasc": ItemCasc,
                "message": "All Item Updated Successfully!!!",
            }
        )
    except Exception as e:
        print(e)
        Item = list(ItemDtl.objects.filter(PermitId=PermitId).order_by("ItemNo").values())
        ItemCasc = list(Cascdtl.objects.filter(PermitId=PermitId).order_by("ItemNo").values())
        return JsonResponse(
            {
                "Item": Item,
                "ItemCasc": ItemCasc,
                "message": "Did Not Saved Somthing Error Please check the Records",
            }
        )


def ItemConsolidate(request):
    permitId = request.POST.get("PermitId")

    results = (
        ItemDtl.objects.filter(PermitId=permitId)
        .values("HSCode", "Description", "Contry", "UnitPriceCurrency")
        .annotate(
            ItemNo=Min("ItemNo"),
            DutiableQty=Sum("DutiableQty"),
            TotalDutiableQty=Sum("TotalDutiableQty"),
            InvoiceQuantity=Sum("InvoiceQuantity"),
            HSQty=Sum("HSQty"),
            AlcoholPer=Sum("AlcoholPer"),
            UnitPrice=Sum("UnitPrice"),
            SumExchangeRate=Sum("SumExchangeRate"),
            TotalLineAmount=Sum("TotalLineAmount"),
            InvoiceCharges=Sum("InvoiceCharges"),
            CIFFOB=Sum("CIFFOB"),
            OPQty=Sum("OPQty"),
            IPQty=Sum("IPQty"),
            InPqty=Sum("InPqty"),
            ImPQty=Sum("ImPQty"),
            GSTAmount=Sum("GSTAmount"),
            ExciseDutyAmount=Sum("ExciseDutyAmount"),
            CustomsDutyAmount=Sum("CustomsDutyAmount"),
            OtherTaxAmount=Sum("OtherTaxAmount"),
            OptionalSumtotal=Sum("OptionalSumtotal"),
        )
        .order_by("ItemNo")
    )
    itemNum = []
    for p in results:
        itemNum.append(p["ItemNo"])
        ItemDtl.objects.filter(PermitId=permitId, ItemNo=p["ItemNo"]).update(
            DutiableQty=p["DutiableQty"],
            TotalDutiableQty=p["TotalDutiableQty"],
            InvoiceQuantity=p["InvoiceQuantity"],
            HSQty=p["HSQty"],
            AlcoholPer=p["AlcoholPer"],
            UnitPrice=p["UnitPrice"],
            SumExchangeRate=p["SumExchangeRate"],
            TotalLineAmount=p["TotalLineAmount"],
            InvoiceCharges=p["InvoiceCharges"],
            CIFFOB=p["CIFFOB"],
            OPQty=p["OPQty"],
            IPQty=p["IPQty"],
            InPqty=p["InPqty"],
            ImPQty=p["ImPQty"],
            GSTAmount=p["GSTAmount"],
            ExciseDutyAmount=p["ExciseDutyAmount"],
            CustomsDutyAmount=p["CustomsDutyAmount"],
            OtherTaxAmount=p["OtherTaxAmount"],
            OptionalSumtotal=p["OptionalSumtotal"],
        )

    for j in ItemDtl.objects.filter(PermitId=permitId):
        if j.ItemNo not in itemNum:
            ItemDtl.objects.filter(PermitId=permitId, ItemNo=j.ItemNo).delete()
            Cascdtl.objects.filter(PermitId=permitId, ItemNo=j.ItemNo).delete()
    c = 1
    for p in itemNum:
        ItemDtl.objects.filter(PermitId=permitId, ItemNo=p).update(ItemNo=c)
        Cascdtl.objects.filter(PermitId=permitId, ItemNo=p).update(ItemNo=c)
        c = c + 1

    Item = list(ItemDtl.objects.filter(PermitId=permitId).order_by("ItemNo").values()) 
    ItemCasc = list(
        Cascdtl.objects.filter(PermitId=permitId).order_by("ItemNo").values()
    )
    return JsonResponse({"Item": Item, "ItemCasc": ItemCasc, "Result": "updated"})


def EditInpayment(request):
    request.session["Permit_Id"] = request.POST.get("Permitid")
    return JsonResponse({"Checking Values  ": "true"})


def RefundLoad(request):
    return JsonResponse(
        {
            "Refund": list(
                InpaymentRefund.objects.filter(MsgId=request.POST.get("MsgId")).values()
            ),
            "RefundValSummary": list(
                RefundValSummary.objects.filter(
                    MsgId=request.POST.get("MsgId")
                ).values()
            ),
            "ReundItemSumm": list(
                ReundItemSumm.objects.filter(MsgId=request.POST.get("MsgId")).values()
            ),
        }
    )


def CanceLoad(request):
    return JsonResponse(
        {
            "Cancel": list(
                InpaymentCancel.objects.filter(MsgId=request.POST.get("MsgId")).values()
            )
        }
    )


def AmendLoad(request):
    return JsonResponse(
        {
            "Amend": list(
                InpaymentAmend.objects.filter(MsgId=request.POST.get("MsgId")).values()
            )
        }
    )


def DeleteAllFunction(request):
    data = json.loads(request.POST.get("my_data"))
    for d in data:
        obj = InheaderTbl.objects.get(PermitId=d)
        obj.Status = "DEL"
        obj.save()
    return JsonResponse({"Deleted": "Deleted"})


def LoadingPartyModels(request):
    return JsonResponse(
        {
            "Importer": list(
                Importer.objects.filter(status="Active").order_by("name").values()
            )
        }
    )


# def InpaymentItemDelHblHawb(request):
#     for item in ItemDtl.objects.filter(PermitId=request.session["Permit_Id"]):
#         obj = ItemDtl.objects.get(id=item.id)
#         obj.InHAWBOBL = ""
#         obj.save()
#     return JsonResponse(
#         {
#             "Item": list(
#                 ItemDtl.objects.filter(PermitId=request.session["Permit_Id"])
#                 .order_by("ItemNo")
#                 .values()
#             )
#         }
#    )

def InpaymentItemDelHblHawb(request):
    items = ItemDtl.objects.filter(PermitId=request.session["Permit_Id"])

    for item in items:
        obj = ItemDtl.objects.get(id=item.id)
        obj.InHAWBOBL = ""
        obj.save()

    item_values = list(
        items.order_by("ItemNo").values()
    )

    # Print key-value pairs to the terminal
    print('hello')
    for item in item_values:
        for key, value in item.items():
            print(f"{key}: {value}")

    return JsonResponse(
        {
            "Item": item_values
        }
    )

   


class CargoPageSave(View, SqlDb):
    def dispatch(self, request):
        SqlDb.__init__(self)
        DbName = request.POST.get("ModelName")
        if DbName == "ImporterModel":
            Qry = "select code from Importer where code = %s"
            val = (request.POST.get("code"),)
            self.cursor.execute(Qry, val)

            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO Importer(code,cruei,name,name1,status,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
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
                    "SELECT Code,Name,Name1,CRUEI FROM Importer WHERE status = 'Active' "
                )
                importer = self.cursor.fetchall()

                return JsonResponse(
                    {
                        "Result": "Importer Saved ...!",
                        "Importer": (
                            pd.DataFrame(
                                list(importer),
                                columns=["Code", "Name", "Name1", "CRUEI"],
                            )
                        ).to_dict("records"),
                    }
                )
            else:
                return JsonResponse({"Result": "Importer Code Already Exists ...!"})

        elif DbName == "InawrdModel":
            Qry = "select code from InwardCarrierAgent where code = %s"
            val = (request.POST.get("code"),)
            self.cursor.execute(Qry, val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO InwardCarrierAgent(code,cruei,name,name1,status,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s) "
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
                    "SELECT Code,Name,Name1,CRUEI FROM InwardCarrierAgent WHERE status = 'Active' "
                )
                return JsonResponse(
                    {
                        "Result": "InwardCarrierAgent Saved ...!",
                        "Inward": (
                            pd.DataFrame(
                                list(self.cursor.fetchall()),
                                columns=["Code", "Name", "Name1", "CRUEI"],
                            )
                        ).to_dict("records"),
                    }
                )
            else:
                return JsonResponse(
                    {"Result": "InwardCarrierAgent Code Already Exists ...!"}
                )

        elif DbName == "FreightModel":
            Qry = "select code from FreightForwarder where code = %s"
            Val = (request.POST.get("code"),)
            self.cursor.execute(Qry, Val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO FreightForwarder(code,cruei,name,name1,status,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s) "
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
                    "SELECT Code,Name,Name1,CRUEI FROM FreightForwarder WHERE status = 'Active' "
                )
                fright = self.cursor.fetchall()
                return JsonResponse(
                    {
                        "Result": "FreightForwarder Saved ...!",
                        "Frieght": (
                            pd.DataFrame(
                                list(fright), columns=["Code", "Name", "Name1", "CRUEI"]
                            )
                        ).to_dict("records"),
                    }
                )
            else:
                return JsonResponse(
                    {"Result": "FreightForwarder Code Already Exists ...!"}
                )

        elif DbName == "ClaimantModel":
            Qry = "select ClaimantCode from ClaimantParty  where ClaimantCode = %s"
            Val = (request.POST.get("ClaimantCode"),)
            self.cursor.execute(Qry, Val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO ClaimantParty (ClaimantCode,cruei,name,name1,ClaimantName,ClaimantName1,status,TouchUser,TouchTime) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                Val = (
                    request.POST.get("ClaimantCode"),
                    request.POST.get("cruei"),
                    request.POST.get("name"),
                    request.POST.get("name1"),
                    request.POST.get("ClaimantName"),
                    request.POST.get("ClaimantName1"),
                    "Active",
                    request.POST.get("TouchUser"),
                    request.POST.get("TouchTime"),
                )
                self.cursor.execute(Qry, Val)
                self.conn.commit()
                return JsonResponse({"Result": "ClaimantParty  Saved ...!"})
            else:
                return JsonResponse(
                    {"Result": "ClaimantParty  Code Already Exists ...!"}
                )

        elif DbName == "SupplierModel":
            Qry = "select code from SUPPLIERMANUFACTURERPARTY  where code = %s"
            Val = (request.POST.get("code"),)
            self.cursor.execute(Qry, Val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO SUPPLIERMANUFACTURERPARTY (code,cruei,name,name1,status,TouchUser,TouchTime) VALUES  (%s,%s,%s,%s,%s,%s,%s)"
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
                    "SELECT Code,Name,Name1,CRUEI FROM SUPPLIERMANUFACTURERPARTY WHERE status = 'Active' "
                )
                supply = self.cursor.fetchall()
                return JsonResponse(
                    {
                        "Result": "SUPPLIERMANUFACTURERPARTY  Saved ...!",
                        "Supply": (
                            pd.DataFrame(
                                list(supply), columns=["Code", "Name", "Name1", "CRUEI"]
                            )
                        ).to_dict("records"),
                    }
                )
            else:
                return JsonResponse(
                    {"Result": "SUPPLIERMANUFACTURERPARTY  Code Already Exists ...!"}
                )

        elif DbName == "InhouseItemCodeModel":
            Qry = "select InhouseCode from InhouseItemCode where InhouseCode = %s"
            Val = (request.POST.get("InhouseCode"),)
            self.cursor.execute(Qry, Val)
            if not (self.cursor.fetchall()):
                Qry = "INSERT INTO InhouseItemCode(InhouseCode,Hscode,Description,Brand,Model,DgIndicator,DeclType,ProductCode,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                Val = (
                    request.POST.get("InhouseCode"),
                    request.POST.get("Hscode"),
                    request.POST.get("Description"),
                    request.POST.get("Brand"),
                    request.POST.get("Model"),
                    request.POST.get("DgIndicator"),
                    request.POST.get("DeclType"),
                    request.POST.get("ProductCode"),
                    request.POST.get("TouchUser"),
                    request.POST.get("TouchTime"),
                )
                self.cursor.execute(Qry, Val)
                self.conn.commit()
                return JsonResponse({"Result": "InhouseItemCode Saved ...!"})
            else:
                return JsonResponse(
                    {"Result": "InhouseItemCode Code Already Exists ...!"}
                )

        elif DbName == "GET":
            self.cursor.execute("SELECT * FROM Importer WHERE status = 'Active' ")
            return JsonResponse({"Importer": self.cursor.fetchall()})
        else:
            return JsonResponse({"error": "Invalid function name"}, status=404)

    def get(self):
        self.cursor.execute("SELECT * FROM Importer WHERE status = 'Active' ")
        return JsonResponse({"Importer": self.cursor.fetchall()})


class ContainerSave(View, SqlDb):
    def post(self, request):
        SqlDb.__init__(self)
        if request.POST.get("Method") == "SAVE":
            self.cursor.execute(
                f"select RowNo , PermitId from ContainerDtl where RowNo = '{request.POST.get('RowNo')}' AND PermitId = '{request.POST.get('PermitId')}'"
            )
            result = self.cursor.fetchall()
            if not (result):
                self.cursor.execute(
                    f"INSERT INTO ContainerDtl (PermitId, RowNo,ContainerNo, size, weight,SealNo, MessageType,TouchUser,TouchTime) VALUES ('{request.POST.get('PermitId')}','{request.POST.get('RowNo')}','{request.POST.get('ContainerNo')}','{request.POST.get('size')}','{request.POST.get('weight')}','{request.POST.get('SealNo')}','{request.POST.get('MessageType')}','{request.POST.get('TouchUser')}','{request.POST.get('TouchTime')}')"
                )
                self.conn.commit()
                self.cursor.execute(
                    f"select * from ContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
                )
                return JsonResponse(
                    {
                        "ContainerValue": list(self.cursor.fetchall()),
                        "Result": "Container Data Saved SuccessFully ...!",
                    }
                )
            else:
                self.cursor.execute(
                    f"Update ContainerDtl set ContainerNo = '{request.POST.get('ContainerNo')}',size = '{request.POST.get('size')}',weight =  '{request.POST.get('weight')}',SealNo = '{request.POST.get('SealNo')}',MessageType = '{request.POST.get('MessageType')}',TouchUser = '{request.POST.get('TouchUser')}',TouchTime = '{request.POST.get('TouchTime')}' where RowNo = '{request.POST.get('RowNo')}' AND PermitId = '{request.POST.get('PermitId')}'"
                )
                self.conn.commit()

                self.cursor.execute(
                    f"select * from ContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo"
                )
                return JsonResponse(
                    {
                        "ContainerValue": list(self.cursor.fetchall()),
                        "Result": "Container Updated SuccessFully ...!",
                    }
                )

        elif request.POST.get("Method") == "DELETE":
            self.cursor.execute(
                f"DELETE FROM ContainerDtl where PermitId = '{request.POST.get('PermitId')}' AND RowNo = '{request.POST.get('SNo')}' "
            )
            self.conn.commit()

            self.cursor.execute(
                f"select * from ContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
            )
            c = 1
            for j in self.cursor.fetchall():
                self.cursor.execute(
                    f"UPDATE ContainerDtl SET RowNo = {c} WHERE PermitId = '{j[1]}' AND RowNo = '{j[2]}'"
                )
                c += 1
            self.conn.commit()

            self.cursor.execute(
                f"select * from ContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
            )
            return JsonResponse(
                {
                    "ContainerValue": list(self.cursor.fetchall()),
                    "Result": "Deleted SuccessFully ...!",
                }
            )

        elif request.POST.get("Method") == "CHECKDELETE":
            for ids in json.loads(request.POST.get("IDS")):
                self.cursor.execute(f"DELETE FROM ContainerDtl where id = {ids}")
            self.conn.commit()

            self.cursor.execute(
                f"select * from ContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
            )
            c = 1
            for j in self.cursor.fetchall():
                self.cursor.execute(
                    f"UPDATE ContainerDtl SET RowNo = {c} WHERE PermitId = '{j[1]}' AND RowNo = '{j[2]}'"
                )
                c += 1
            self.conn.commit()

            self.cursor.execute(
                f"select * from ContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
            )
            return JsonResponse(
                {
                    "ContainerValue": list(self.cursor.fetchall()),
                    "Result": "Deleted SuccessFully ...!",
                }
            )

        elif request.POST.get("Method") == "LOAD":
            self.cursor.execute(
                f"select * from ContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
            )
            return JsonResponse(
                {
                    "ContainerValue": list(self.cursor.fetchall()),
                    "Result": "Deleted SuccessFully ...!",
                }
            )

    def get(self, request):
        self.cursor.execute(
            f"select * from ContainerDtl where PermitId = '{request.GET.get('PermitId')}' Order By RowNo"
        )
        return JsonResponse({"ContainerValue": list(self.cursor.fetchall())})


class PartyPage(View, SqlDb):
    def get(self, request):
        SqlDb.__init__(self)
        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM Importer WHERE status = 'Active' ORDER BY Code"
        )
        importer = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM InwardCarrierAgent WHERE status = 'Active' ORDER BY Code"
        )
        inward = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM FreightForwarder WHERE status = 'Active' ORDER BY Code"
        )
        fright = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT Name,Name1,CRUEI,ClaimantName,ClaimantName1,ClaimantCode,Name2 FROM ClaimantParty WHERE status = 'Active' "
        )
        claimant = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM SUPPLIERMANUFACTURERPARTY WHERE status = 'Active' ORDER BY Code"
        )
        supply = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT InhouseCode,HSCode,Description,Brand,Model,DGIndicator,DeclType,ProductCode FROM InhouseItemCode"
        )
        inhouse = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT Id,Sno,Name,ContentType,Data,DocumentType,InPaymentId,FilePath,Size,PermitId,Type FROM InFile WHERE PermitId = '{}' ".format(
                request.session["Permit_Id"]
            )
        )
        inFile = self.cursor.fetchall()

        return JsonResponse(
            {
                "Infile": (
                    pd.DataFrame(
                        list(inFile),
                        columns=[
                            "Id",
                            "Sno",
                            "Name",
                            "ContentType",
                            "Data",
                            "DocumentType",
                            "InPaymentId",
                            "FilePath",
                            "Size",
                            "PermitId",
                            "Type",
                        ],
                    )
                ).to_dict("records"),
                "Importer": (
                    pd.DataFrame(
                        list(importer), columns=["Code", "Name", "Name1", "CRUEI"]
                    )
                ).to_dict("records"),
                "Inward": (
                    pd.DataFrame(
                        list(inward), columns=["Code", "Name", "Name1", "CRUEI"]
                    )
                ).to_dict("records"),
                "Frieght": (
                    pd.DataFrame(
                        list(fright), columns=["Code", "Name", "Name1", "CRUEI"]
                    )
                ).to_dict("records"),
                "Claimant": (
                    pd.DataFrame(
                        list(claimant),
                        columns=[
                            "Name",
                            "Name1",
                            "CRUEI",
                            "ClaimantName",
                            "ClaimantName1",
                            "ClaimantCode",
                            "Name2",
                        ],
                    )
                ).to_dict("records"),
                "Supply": (
                    pd.DataFrame(
                        list(supply), columns=["Code", "Name", "Name1", "CRUEI"]
                    )
                ).to_dict("records"),
                "Inhouse": (
                    pd.DataFrame(
                        list(inhouse),
                        columns=[
                            "InhouseCode",
                            "HSCode",
                            "Description",
                            "Brand",
                            "Model",
                            "DGIndicator",
                            "DeclType",
                            "ProductCode",
                        ],
                    )
                ).to_dict("records"),
            }
        )


class CpcLoadClass(View, SqlDb):
    def get(self, request):
        SqlDb.__init__(self)

        self.cursor.execute(
            "SELECT PermitId,MessageType,RowNo,CpcType,ProcessingCode1,ProcessingCode2,ProcessingCode3 FROM CpcDtl WHERE PermitId = '{}' AND CpcType = 'AEO' ".format(
                request.session["Permit_Id"]
            )
        )
        CpAeo = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT PermitId,MessageType,RowNo,CpcType,ProcessingCode1,ProcessingCode2,ProcessingCode3 FROM CpcDtl WHERE PermitId = '{}' AND CpcType = 'CWC' ".format(
                request.session["Permit_Id"]
            )
        )
        CpCwc = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT PermitId,MessageType,RowNo,CpcType,ProcessingCode1,ProcessingCode2,ProcessingCode3 FROM CpcDtl WHERE PermitId = '{}' AND CpcType = 'SCHEME' ".format(
                request.session["Permit_Id"]
            )
        )
        CpScheme = self.cursor.fetchall()

        return JsonResponse(
            {
                "CpAeo": (
                    pd.DataFrame(
                        list(CpAeo),
                        columns=[
                            "PermitId",
                            "MessageType",
                            "RowNo",
                            "CpcType",
                            "ProcessingCode1",
                            "ProcessingCode2",
                            "ProcessingCode3",
                        ],
                    )
                ).to_dict("records"),
                "CpCwc": (
                    pd.DataFrame(
                        list(CpCwc),
                        columns=[
                            "PermitId",
                            "MessageType",
                            "RowNo",
                            "CpcType",
                            "ProcessingCode1",
                            "ProcessingCode2",
                            "ProcessingCode3",
                        ],
                    )
                ).to_dict("records"),
                "CpScheme": (
                    pd.DataFrame(
                        list(CpScheme),
                        columns=[
                            "PermitId",
                            "MessageType",
                            "RowNo",
                            "CpcType",
                            "ProcessingCode1",
                            "ProcessingCode2",
                            "ProcessingCode3",
                        ],
                    )
                ).to_dict("records"),
            }
        )


def headAttachDownloadFunction(request, ID):
    data = InFile.objects.filter(id=ID)
    for i in data:
        FilePath = i.FilePath
        FileName = i.Name
        FileType = i.ContentType
    response = HttpResponse(open(FilePath + FileName, "rb").read())
    response["Content-Type"] = FileType
    response["Content-Disposition"] = f"attachment; filename={str(FileName)}"
    return response


def ContainerDel(request, arg):
    ContainerDtl.objects.get(id=arg).delete()
    return JsonResponse({"Deleted": "Delete"})


class CascProductCodesViewSets(viewsets.ModelViewSet):
    serializer_class = CascProductCodesSerializer
    queryset = CascProductCodes.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["HSCode", "Description", "CASCCode"]
    search_fields = ["HSCode", "Description", "CASCCode"]
    ordering_fields = "__all__"
    ordering = ["HSCode"]


class HsCodeCodesViewSets(viewsets.ModelViewSet):
    serializer_class = HsCodesSerializer
    queryset = HsCode.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["HSCode", "Description"]
    search_fields = ["HSCode", "Description"]
    ordering_fields = "__all__"
    ordering = ["HSCode"]


class InvoiceInpayment(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request, PermitId):
        self.cursor.execute(
            f"select * from InvoiceDtl WHERE PermitId = '{PermitId}' ORDER BY SNo"
        )
        headers = [i[0] for i in self.cursor.description]
        return JsonResponse(
            {
                "invoice": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )


class ItemInpayment(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request, PermitId):
        cotext = {}
        self.cursor.execute(
            f"select * from ItemDtl WHERE PermitId = '{PermitId}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        cotext.update(
            {
                "item": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        self.cursor.execute(
            f"select * from Cascdtl WHERE PermitId = '{PermitId}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        cotext.update(
            {
                "itemCasc": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        return JsonResponse(cotext)


class InPaymentItemLoad(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

        self.cursor.execute(
            "SELECT InhouseCode,HSCode,Description,Brand,Model,DGIndicator,DeclType,Productcode FROM InhouseItemCode WHERE DeclType = 'INPAYMENT' "
        )
        self.inhouseItemCode = self.cursor.fetchall()

        self.cursor.execute(
            "SELECT HSCode,Description,UOM,Typeid,DUTYTYPID,Inpayment,InnonPayment,Out,Co,Transhipment,RPNEXPORT,DuitableUom,Excisedutyuom,Excisedutyrate,Customsdutyuom,Customsdutyrate,Kgmvisible FROM HSCode"
        )  # ImpControll,OutControll,TransControll <---This Field Add Only Kaizen Portal
        self.hsCode = self.cursor.fetchall()

        self.cursor.execute("SELECT HSCode FROM ChkHsCode ")
        self.chkHsCode = self.cursor.fetchall()

    def get(self, request):
        return JsonResponse(
            {
                "inhouseItemCode": (
                    pd.DataFrame(
                        list(self.inhouseItemCode),
                        columns=[
                            "InhouseCode",
                            "HSCode",
                            "Description",
                            "Brand",
                            "Model",
                            "DGIndicator",
                            "DeclType",
                            "Productcode",
                        ],
                    )
                ).to_dict("records"),
                "hsCode": (
                    pd.DataFrame(
                        list(self.hsCode),
                        columns=[
                            "HSCode",
                            "Description",
                            "UOM",
                            "Typeid",
                            "DUTYTYPID",
                            "Inpayment",
                            "InnonPayment",
                            "Out",
                            "Co",
                            "Transhipment",
                            "RPNEXPORT",
                            "DuitableUom",
                            "Excisedutyuom",
                            "Excisedutyrate",
                            "Customsdutyuom",
                            "Customsdutyrate",
                            "Kgmvisible",
                        ],
                    )
                ).to_dict(
                    "records"
                ),  # ,'ImpControll ,'OutControll','TransControll'<---This Field Add Only Kaizen Portal  '
                "chkHsCode": (
                    pd.DataFrame(list(self.chkHsCode), columns=["HSCode"])
                ).to_dict("records"),
            }
        )


class InPaymentCcp(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request, Data):
        pdfFiles = []
        for ID in Data.split(","):
            self.cursor.execute(
                "SELECT * FROM InHeaderTbl WHERE PermitId = '{}' ".format(ID)
            )

            InNonHeaderData = self.cursor.fetchall()

            PermitValues = (
                pd.DataFrame(
                    list(InNonHeaderData),
                    columns=[i[0] for i in self.cursor.description],
                ).to_dict("records")
            )[0]

            lftcol = 50
            rgtcol = 280
            self.countPage = 1

            if PermitValues["PermitNumber"] == "":
                PermitBar = "DRAFT"
                OldFilename = f"D:/Users/Public/PDFFilesKtt/{PermitBar}1.pdf"

            else:
                PermitBar = PermitValues["PermitNumber"]
                OldFilename = f"D:/Users/Public/PDFFilesKtt/{PermitBar}1.pdf"
                barcode = code39.Standard39(
                    PermitValues["PermitNumber"],
                    barHeight=36.0,
                    barWidth=1.1,
                    baseline=9.0,
                    size=12.0,
                    N=3.0,
                    X=1.0,
                    StartsStopText=False,
                    Extended=False,
                )

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=(595, 841))
            p.setTitle(PermitBar)
            inpstrtdate = ""
            inpEndate = ""

            p.setFont("Courier-Bold", 10)
            p.drawString(480, 750, PermitBar)

            if PermitValues["PermitNumber"] != "":
                barcode.drawOn(p, 330, 760)

            p.setFont("Courier", 10)
            p.drawString(400, 750, "PERMIT NO : ")

            p.drawString(rgtcol, 700, "CARGO CLEARANCE PERMIT")
            p.drawString(460, 700, ("PG : {} OF").format(self.countPage))
            self.countPage += 1

            if PermitValues["prmtStatus"] == "AMD":
                p.drawString(
                    lftcol, 670, "MESSAGE TYPE      : IN-PAYMENT UPDATED PERMIT"
                )
            else:
                p.drawString(lftcol, 670, "MESSAGE TYPE      : IN-PAYMENT PERMIT")

            p.drawString(
                lftcol,
                660,
                "DECLARATION TYPE  : "
                + (str(PermitValues["DeclarationType"])[6:]).upper(),
            )

            p.drawString(lftcol, 630, "IMPORTER:")

            self.cursor.execute(
                f"SELECT Name,Name1,Cruei FROM Importer WHERE code = '{PermitValues['ImporterCompanyCode']}' "
            )
            ImportData = self.cursor.fetchone()
            ImportDataCruei = ImportData[2]
            ImportData = str(ImportData[0]) + str(ImportData[1])

            if len(ImportData) >= 35:
                p.drawString(lftcol, 620, (ImportData[:35]).upper())
                p.drawString(lftcol, 610, (ImportData[35:]).upper())
            else:
                p.drawString(lftcol, 620, (ImportData).upper())
            p.drawString(lftcol, 600, str(ImportDataCruei).upper())

            p.drawString(lftcol, 590, "EXPORTER:")
            # self.cursor.execute(f"SELECT Name,Name1,Cruei FROM InnonExporter WHERE code = '' ")
            # ExportData = self.cursor.fetchone()
            ExportData = None
            if ExportData is not None:
                ExportDataCruei = ExportData[2]
                ExportData = str(ExportData[0]) + str(ExportData[1])

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

            self.cursor.execute(
                f"SELECT PortCode,PortName FROM LoadingPort WHERE PortCode = '{PermitValues['LoadingPortCode']}'"
            )
            NextPort = self.cursor.fetchone()
            if NextPort is not None:
                p.drawString(lftcol, 490, str(NextPort[1]).upper())

            p.drawString(lftcol, 480, "PORT OF DISCHARGE/FINAL PORT OF CALL ")

            # self.cursor.execute(f"SELECT PortCode,PortName FROM LoadingPort WHERE PortCode = '{PermitValues['DischargePort']}'")
            # DischargePort = self.cursor.fetchone()
            DischargePort = None
            if DischargePort is not None:
                p.drawString(lftcol, 470, str(DischargePort[1]).upper())

            p.drawString(lftcol, 460, "COUNTRY OF FINAL DESTINATION:")
            # if PermitValues['FinalDestinationCountry'] != "--Select--":
            #     p.drawString(lftcol, 450, str(PermitValues['FinalDestinationCountry']).split(":")[0])

            p.drawString(lftcol, 440, "INWARD CARRIER AGENT: ")

            InWard = "SELECT Name,Name1 FROM InnonInwardCarrierAgent where Code=%s"
            self.cursor.execute(InWard, (PermitValues["InwardCarrierAgentCode"],))
            InwardData = self.cursor.fetchone()
            if InwardData:
                InwardData = str(InwardData[0]) + str(InwardData[1])

                if len(InwardData) >= 35:
                    p.drawString(
                        lftcol, 430, (InwardData[:35]).upper().replace("\n", " ")
                    )
                    p.drawString(
                        lftcol, 420, (InwardData[35:70]).upper().replace("\n", " ")
                    )
                    p.drawString(
                        lftcol, 410, (InwardData[70:]).upper().replace("\n", " ")
                    )
                else:
                    p.drawString(lftcol, 430, (InwardData).upper().replace("\n", " "))

            p.drawString(lftcol, 400, "OUTWARD CARRIER AGENT: ")

            # OutWard = "SELECT Name,Name1 FROM InnonOutwardCarrierAgent where Code=%s"
            # self.cursor.execute(OutWard,(PermitValues['OutwardCarrierAgentCode'],))
            # OutwardData = self.cursor.fetchone()
            OutwardData = None
            if OutwardData is not None:
                OutwardData = str(OutwardData[0]) + str(OutwardData[1])

                if len(OutwardData) >= 35:
                    p.drawString(
                        lftcol, 390, (OutwardData[:35]).upper().replace("\n", " ")
                    )
                    p.drawString(
                        lftcol, 380, (OutwardData[35:70]).upper().replace("\n", " ")
                    )
                    p.drawString(
                        lftcol, 370, (OutwardData[70:]).upper().replace("\n", " ")
                    )
                else:
                    p.drawString(lftcol, 390, (OutwardData).upper().replace("\n", " "))

            p.drawString(lftcol, 360, "PLACE OF RELEASE: ")

            ReleaseY = 350
            ReleaseX = lftcol
            RelaseVal = str(PermitValues["ReleaseLocName"]).replace("\n", "")

            for Re in range(len(RelaseVal)):
                p.drawString(ReleaseX, ReleaseY, str(RelaseVal[Re]))
                ReleaseX += 6

                if Re % 32 == 0 and Re != 0:
                    ReleaseY -= 10
                    ReleaseX = lftcol

            ReleaseY -= 10

            p.drawString(lftcol, ReleaseY, PermitValues["ReleaseLocation"])
            ReleaseY -= 10
            p.drawString(lftcol, ReleaseY, "LICENCE NO:")
            ReleaseY -= 10

            licence = (str(PermitValues["License"]).upper()).split(",")
            try:
                p.drawString(lftcol, ReleaseY, licence[0])
                ReleaseY -= 10
                p.drawString(lftcol, ReleaseY, licence[1])
                ReleaseY -= 10
                p.drawString(lftcol, ReleaseY, licence[2])
                ReleaseY -= 10
                p.drawString(lftcol, ReleaseY, licence[3])
                ReleaseY -= 10
                p.drawString(lftcol, ReleaseY, licence[4])
                ReleaseY -= 10
            except:
                pass
            p.drawString(
                lftcol,
                50,
                "--------------------------------------------------------------------------------",
            )

            Declarant = "SELECT Cruei FROM DeclarantCompany where tradenetmailboxId=%s"
            self.cursor.execute(Declarant, (PermitValues["TradeNetMailboxID"],))
            DeclarData = self.cursor.fetchone()

            p.drawString(
                lftcol,
                40,
                ("UNIQUE REF : {} {} {}").format(
                    (DeclarData[0]).upper(),
                    str(PermitValues["MSGId"][:8]).upper(),
                    str(PermitValues["MSGId"][8:]).upper(),
                ),
            )

            if PermitValues["prmtStatus"] == "AMD":
                self.cursor.execute(
                    f"SELECT StartDate,EndDate FROM Inpmt where PermitNumber = '{PermitValues['PermitNumber']}' AND MsgId = '{PermitValues['MSGId']}' "
                )
                StartEnd = self.cursor.fetchone()
            else:
                self.cursor.execute(
                    f"SELECT StartDate,EndDate FROM Inpmt where PermitNumber = '{PermitValues['PermitNumber']}' "
                )
                StartEnd = self.cursor.fetchone()

            if StartEnd is not None:
                inpstrtdate = datetime.strptime(str(StartEnd[0]), "%Y-%m-%d").strftime(
                    "%d/%m/%Y"
                )
                inpEndate = datetime.strptime(str(StartEnd[1]), "%Y-%m-%d").strftime(
                    "%d/%m/%Y"
                )

            rgy = 630
            p.drawString(
                rgtcol, rgy, ("VALIDITY PERIOD      : {} - ").format(inpstrtdate)
            )
            rgy -= 10
            p.drawString(rgtcol, rgy, ("                       {}").format(inpEndate))
            rgy -= 20

            totalGross = "{:.3f}".format(float(PermitValues["TotalGrossWeight"]))

            p.drawString(
                rgtcol,
                rgy,
                ("TOTAL GROSS WT/UNIT  : {:>18}/{}").format(
                    totalGross, PermitValues["TotalGrossWeightUOM"]
                ),
            )
            rgy -= 10
            p.drawString(
                rgtcol,
                rgy,
                ("TOTAL OUTER PACK/UNIT: {:>18}/{}").format(
                    PermitValues["TotalOuterPack"], PermitValues["TotalOuterPackUOM"]
                ),
            )
            rgy -= 10
            p.drawString(
                rgtcol,
                rgy,
                ("TOT EXCISE DUT PAYABLE  : S${:>17}").format(
                    PermitValues["TotalExDutyAmt"]
                ),
            )
            rgy -= 10
            p.drawString(
                rgtcol,
                rgy,
                ("TOT CUSTOMS DUT PAYABLE : S${:>17}").format(
                    PermitValues["TotalCusDutyAmt"]
                ),
            )
            rgy -= 10
            p.drawString(
                rgtcol,
                rgy,
                ("TOT OTHER TAX PAYABLE   : S${:>17}").format(
                    PermitValues["TotalODutyAmt"]
                ),
            )
            rgy -= 10
            p.drawString(
                rgtcol,
                rgy,
                ("TOTAL GST AMT           : S${:>17}").format(
                    PermitValues["TotalGSTTaxAmt"]
                ),
            )
            rgy -= 10
            p.drawString(
                rgtcol,
                rgy,
                ("TOTAL AMOUNT PAYABLE    : S${:>17}").format(
                    PermitValues["TotalAmtPay"]
                ),
            )
            rgy -= 10
            p.drawString(
                rgtcol,
                rgy,
                ("CARGO PACKING TYPE: {} ").format(
                    ((PermitValues["CargoPackType"])[3:]).upper()
                ),
            )
            rgy -= 10
            p.drawString(rgtcol, rgy, "IN TRANSPORT IDENTIFIER: ")
            rgy -= 10

            if PermitValues["InwardTransportMode"] == "4 : Air":
                transidval = PermitValues["AircraftRegNo"]
                CoveyanceNo = PermitValues["FlightNO"]
                mastebill = PermitValues["MasterAirwayBill"]
            elif PermitValues["InwardTransportMode"] == "1 : Sea":
                transidval = PermitValues["VesselName"]
                CoveyanceNo = PermitValues["VoyageNumber"]
                mastebill = PermitValues["OceanBillofLadingNo"]
            else:
                transidval = PermitValues["TransportId"]
                CoveyanceNo = PermitValues["ConveyanceRefNo"]
                mastebill = ""

            p.drawString(rgtcol, rgy, transidval.upper())
            rgy -= 10
            p.drawString(
                rgtcol,
                rgy,
                ("CONVEYANCE REFERENCE NO: {} ").format(CoveyanceNo.upper()),
            )
            rgy -= 10
            p.drawString(rgtcol, rgy, "OBL/MAWB NO: ")
            rgy -= 10
            p.drawString(rgtcol, rgy, PermitValues["OceanBillofLadingNo"])
            rgy -= 10
            if str(PermitValues["ArrivalDate"].strftime("%d/%m/%Y")) != "01/01/1900":
                p.drawString(
                    rgtcol,
                    rgy,
                    "ARRIVAL DATE         : {}".format(
                        (PermitValues["ArrivalDate"]).strftime("%d/%m/%Y")
                    ),
                )
            else:
                p.drawString(
                    rgtcol,
                    rgy,
                    "ARRIVAL DATE         : {}".format(
                        (PermitValues["ArrivalDate"]).strftime("%d/%m/%Y")
                    ),
                )

            rgy -= 10
            p.drawString(rgtcol, rgy, "OU TRANSPORT IDENTIFIER: ")
            rgy -= 10

            if PermitValues["InwardTransportMode"] == "4 : Air":
                Outransport = PermitValues["AircraftRegNo"]
                conveno = PermitValues["FlightNO"]
                mastebill = PermitValues["MasterAirwayBill"]

            elif PermitValues["InwardTransportMode"] == "1 : Sea":
                Outransport = PermitValues["VesselName"]
                conveno = PermitValues["VoyageNumber"]
                mastebill = PermitValues["OceanBillofLadingNo"]
            else:
                Outransport = PermitValues["TransportId"]
                conveno = PermitValues["ConveyanceRefNo"]
                mastebill = ""

            # p.drawString(rgtcol, rgy, str(Outransport).upper())
            rgy -= 10
            p.drawString(rgtcol, rgy, "CONVEYANCE REFERENCE NO:  ")
            rgy -= 10
            p.drawString(rgtcol, rgy, "OBL/MAWB/UCR NO: ")
            rgy -= 10
            # p.drawString(rgtcol, rgy, ""+str(mastebill).upper())
            rgy -= 10

            if False:
                p.drawString(
                    rgtcol,
                    rgy,
                    "DEPARTURE DATE       : "
                    + str(PermitValues["DepartureDate"].strftime("%d/%m/%Y")),
                )
            else:
                p.drawString(rgtcol, rgy, "DEPARTURE DATE       : ")
            rgy -= 20

            p.drawString(rgtcol, rgy, "CERTIFICATE NO:  ")
            rgy -= 30

            p.drawString(rgtcol, rgy, "PLACE OF RECEIPT:")
            rgy -= 10

            ReleaseY = rgy
            ReleaseX = rgtcol
            ReciptVal = str(PermitValues["RecepitLocName"]).replace("\n", "")

            for Re in range(len(ReciptVal)):
                p.drawString(ReleaseX, ReleaseY, str(ReciptVal[Re]))
                ReleaseX += 6

                if Re % 32 == 0 and Re != 0:
                    ReleaseY -= 10
                    ReleaseX = rgtcol

            ReleaseY -= 10

            p.drawString(rgtcol, ReleaseY, PermitValues["RecepitLocation"])
            ReleaseY -= 10
            p.drawString(rgtcol, ReleaseY, "CUSTOMS PROCEDURE CODE (CPC) : ")
            ReleaseY -= 10
            rely = ReleaseY

            self.cursor.execute(
                f"SELECT DISTINCT CPCType FROM InNonCPCDtl WHERE PermitId='{PermitValues['PermitId']}' "
            )
            CpcData = self.cursor.fetchall()

            for cpc in CpcData:
                p.drawString(rgtcol, rely, str(cpc[0]))
                rely -= 10

            if PermitValues["Cnb"] == "True" or PermitValues["Cnb"] == "true":
                p.drawString(rgtcol, rely, str("CNB"))

            # -------------------------------------------Heading Page Complete-----------------------------------------------#

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
                    p.setFont("Courier", 10)
                else:
                    itemy -= 10
                if itemy <= 820 and itemy >= 700:
                    p.setFont("Courier", 10)
                    p.drawString(rgtcol, itemy, "CARGO CLEARANCE PERMIT ")
                    p.drawString(460, itemy, ("PG : {} OF ").format(self.countPage))
                    self.countPage += 1
                    itemy -= 10
                    p.drawString(lftcol, itemy, "PERMIT NO : " + str(PermitBar))
                    p.drawString(rgtcol, itemy, "======================")
                    itemy -= 10
                    p.drawString(rgtcol, itemy, "(CONTINUATION PAGE)")
                    itemy -= 20
                    p.drawString(lftcol, itemy, "CONSIGNMENT DETAILS")
                    itemy -= 10
                    p.drawString(
                        lftcol,
                        itemy,
                        "--------------------------------------------------------------------------------",
                    )
                    itemy -= 10

                    p.drawString(
                        lftcol,
                        itemy,
                        "S/NO     HS CODE      CURRENT LOT NO         PREVIOUS LOT NO                ",
                    )
                    itemy -= 10

                    p.drawString(
                        lftcol,
                        itemy,
                        "MARKING    CTY OF ORIGIN    BRAND NAME       MODEL                            ",
                    )
                    itemy -= 10

                    self.cursor.execute(
                        f"SELECT count(InHAWBOBL) FROM ItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '' "
                    )
                    ItemHeadData = self.cursor.fetchone()

                    # if  ItemHeadData[0] is not None:
                    #     p.drawString(lftcol, itemy, "IN HAWB/HUCR/HBL")
                    #     itemy -= 10

                    p.drawString(
                        lftcol,
                        itemy,
                        "PACKING/GOODS DESCRIPTION                    HS QUANTITY & UNIT               ",
                    )
                    itemy -= 10

                    p.drawString(
                        lftcol,
                        itemy,
                        "                                             CIF/FOB VALUE (S$)               ",
                    )
                    itemy -= 10

                    self.cursor.execute(
                        f"SELECT sum(LSPValue) FROM ItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '' "
                    )
                    LspData = self.cursor.fetchone()
                    if str(LspData[0]) != str("0.00") and LspData[0]:
                        p.drawString(
                            lftcol,
                            itemy,
                            "                                             LSP VALUE (S$)                   ",
                        )
                        itemy -= 10

                    p.drawString(
                        lftcol,
                        itemy,
                        "                                             GST AMOUNT (S$)                  ",
                    )
                    itemy -= 10

                    self.cursor.execute(
                        f"SELECT count(DutiableUOM),sum(DutiableQty),sum(UnitPrice),sum(ExciseDutyRate),sum(CustomsDutyAmount) FROM ItemDtl WHERE PermitId = '{PermitValues['PermitId']}' AND InHAWBOBL != '--Select--' "
                    )
                    DutyUom = self.cursor.fetchone()

                    if DutyUom[0] is not None and Decimal(DutyUom[1]) != Decimal(
                        "0.0000"
                    ):
                        p.drawString(
                            lftcol,
                            itemy,
                            "                                             DUT QTY/WT/VOL & UNIT            ",
                        )
                        itemy -= 10

                    if Decimal(DutyUom[2] != Decimal("0.00")):
                        p.drawString(
                            lftcol,
                            itemy,
                            "                                             UNIT PRICE & CODE                 ",
                        )
                        itemy -= 10

                    if Decimal(DutyUom[3] != Decimal("0.00")):
                        p.drawString(
                            lftcol,
                            itemy,
                            "                                             EXCISE DUTY PAYABLE (S$)          ",
                        )
                        itemy -= 10

                    if Decimal(DutyUom[4] != Decimal("0.00")):
                        p.drawString(
                            lftcol,
                            itemy,
                            "                                             CUSTOMS DUTY PAYABLE(S$)          ",
                        )
                        itemy -= 10

                    p.drawString(snox, itemy, "MANUFACTURER'S NAME ")
                    itemy -= 10
                    p.drawString(
                        snox,
                        itemy,
                        "-------------------------------------------------------------------------------",
                    )
                    itemy -= 10
                    p.drawString(
                        lftcol,
                        50,
                        "--------------------------------------------------------------------------------",
                    )
                    p.drawString(
                        lftcol,
                        40,
                        ("UNIQUE REF : {} {} {}").format(
                            str(DeclarData[0]).upper(),
                            str(PermitValues["MSGId"][:8]).upper(),
                            str(PermitValues["MSGId"][8:]).upper(),
                        ),
                    )

                return itemy

            def Cascfunction(Item, CascId, Sno, itemy):
                self.cursor.execute(
                    f"SELECT ProductCode,Quantity,ProductUOM FROM Cascdtl WHERE ItemNo = '{Item['ItemNo']}' AND PermitId = '{Item['PermitId']}' AND CascId = '{CascId}' "
                )
                CascData = self.cursor.fetchone()
                if CascData is not None:
                    p.drawString(
                        lftcol,
                        itemy,
                        "--------------------------------------------------------------------------------",
                    )
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, "S/NO")
                    p.drawString(lftcol + 70, itemy, "CA/SC PRODUCT CODE ")
                    p.drawString(lftcol + 280, itemy, "CA/SC PRODUCT QTY & UNIT")
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, "   {}".format(Sno))
                    p.drawString(lftcol + 70, itemy, str(CascData[0]).upper())
                    if str(CascData[1]) != "0.0000":
                        p.drawString(
                            lftcol + 280,
                            itemy,
                            ("{:10d}.{} {}").format(
                                int(CascData[1]),
                                str(CascData[1]).split(".")[1],
                                CascData[2],
                            ),
                        )
                    itemy = itemyF(itemy)
                    p.drawString(
                        lftcol,
                        itemy,
                        "--------------------------------------------------------------------------------",
                    )

                return itemy

            itemy = itemyF(itemy)
            self.cursor.execute(
                "SELECT * FROM  ItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(
                    PermitValues["PermitId"]
                )
            )
            self.item = self.cursor.fetchall()
            ItemValues = (
                pd.DataFrame(
                    list(self.item), columns=[i[0] for i in self.cursor.description]
                )
            ).to_dict("records")

            for Item in ItemValues:
                p.drawString(
                    lftcol,
                    itemy,
                    f"{'%02d' % Item['ItemNo']}     {Item['HSCode']}      {Item['CurrentLot']}         {Item['PreviousLot']}                ",
                )
                itemy = itemyF(itemy)

                if Item["Making"] != "--Select--":
                    p.drawString(makingx, itemy, (str(Item["Making"])[:2]).upper())
                p.drawString(cityx - 40, itemy, str(Item["Contry"]).upper())
                p.drawString(brandx - 105, itemy, str(Item["Brand"]).upper())
                p.drawString(prviousx, itemy, str(Item["Model"]).upper())
                itemy = itemyF(itemy)

                if Item["InHAWBOBL"] != "":
                    p.drawString(lftcol, itemy, str(Item["InHAWBOBL"]).upper())
                    itemy = itemyF(itemy)

                inp = 0
                if int(Item["OPQty"]) > 0:
                    inp = inp + 10
                    p.drawString(lftcol + 40, itemy, str(Item["OPQty"]).upper())
                    p.drawString(lftcol + 70, itemy, str(Item["OPUOM"]).upper())
                    if int(Item["IPQty"]) > 0:
                        p.drawString(lftcol + 100, itemy, str(Item["IPQty"]).upper())
                        p.drawString(lftcol + 130, itemy, str(Item["IPUOM"]).upper())
                    itemy = itemyF(itemy)

                if int(Item["InPqty"]) > 0:
                    inp = inp + 10
                    p.drawString(lftcol + 40, itemy, str(Item["InPqty"]).upper())
                    p.drawString(lftcol + 70, itemy, str(Item["InPUOM"]).upper())
                    if int(Item["ImPQty"]) > 0:
                        p.drawString(lftcol + 100, itemy, str(Item["ImPQty"]).upper())
                        p.drawString(lftcol + 130, itemy, str(Item["ImPUOM"]).upper())
                    itemy = itemyF(itemy)

                def Inf(iny):
                    return inp + iny

                DescriptionItem = Item["Description"].upper()
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
                    DescX += 6
                    if "\n" == DescriptionItem[D]:
                        DescX = lftcol
                        itemy = itemyF(itemy)
                        Dcount += 1
                    if (D + 1) % 50 == 0:
                        DescX = lftcol
                        itemy = itemyF(itemy)
                        Dcount += 1

                    if Dcount == 1 and HSQtyName:
                        p.drawString(
                            prviousx + 100,
                            Inf(itemy),
                            ("{:8d}.{} {}").format(
                                int(Item["HSQty"]),
                                str(Item["HSQty"]).split(".")[1],
                                Item["HSUOM"],
                            ),
                        )
                        HSQtyName = False

                    if Dcount == 2 and CiFob:
                        p.drawString(
                            prviousx + 100,
                            Inf(itemy),
                            ("{:10d}.{}").format(
                                int(Item["CIFFOB"]), str(Item["CIFFOB"]).split(".")[1]
                            ),
                        )
                        CiFob = False

                    if Dcount == 3 and Lsp:
                        Dcount += 1
                        if Decimal(Item["LSPValue"]) != Decimal("0.00"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:10d}.{}").format(
                                    int(Item["LSPValue"]),
                                    str(Item["LSPValue"]).split(".")[1],
                                ),
                            )
                            Lsp = False
                    if Dcount == 4 and GstAmd:
                        p.drawString(
                            prviousx + 100,
                            Inf(itemy),
                            ("{:10d}.{}").format(
                                int(Item["GSTAmount"]),
                                str(Item["GSTAmount"]).split(".")[1],
                            ),
                        )
                        GstAmd = False

                    if Dcount == 5 and TotDutiable:
                        Dcount += 1
                        if Decimal(Item["DutiableQty"]) != Decimal("0.0000"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:8d}.{} {}").format(
                                    int(Item["DutiableQty"]),
                                    str(Item["DutiableQty"]).split(".")[1],
                                    Item["DutiableUOM"],
                                ),
                            )
                            TotDutiable = False

                    if Dcount == 6 and ExciseAmd:
                        Dcount += 1
                        if Decimal(Item["ExciseDutyAmount"]) != Decimal("0.00"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:10d}.{}").format(
                                    int(Item["ExciseDutyAmount"]),
                                    str(Item["ExciseDutyAmount"]).split(".")[1],
                                ),
                            )
                            ExciseAmd = False

                    if Dcount == 7 and CustomDuty:
                        Dcount += 1
                        if Decimal(Item["CustomsDutyAmount"]) != Decimal("0.00"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:10d}.{}").format(
                                    int(Item["CustomsDutyAmount"]),
                                    str(Item["CustomsDutyAmount"]).split(".")[1],
                                ),
                            )

                    if Dcount == 8 and OtherDuty:
                        Dcount += 1
                        if Decimal(Item["OtherTaxAmount"]) != Decimal("0.00"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:10d}.{}").format(
                                    int(Item["OtherTaxAmount"]),
                                    str(Item["OtherTaxAmount"]).split(".")[1],
                                ),
                            )
                            OtherDuty = False
                else:
                    if Dcount <= 1:
                        p.drawString(
                            prviousx + 100,
                            Inf(itemy),
                            ("{:8d}.{} {}").format(
                                int(Item["HSQty"]),
                                str(Item["HSQty"]).split(".")[1],
                                Item["HSUOM"],
                            ),
                        )
                        itemy = itemyF(itemy)
                    if Dcount <= 2:
                        p.drawString(
                            prviousx + 100,
                            Inf(itemy),
                            ("{:10d}.{}").format(
                                int(Item["CIFFOB"]), str(Item["CIFFOB"]).split(".")[1]
                            ),
                        )
                        itemy = itemyF(itemy)

                    if Dcount <= 3:
                        if Decimal(Item["LSPValue"]) != Decimal("0.00"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:10d}.{}").format(
                                    int(Item["LSPValue"]),
                                    str(Item["LSPValue"]).split(".")[1],
                                ),
                            )
                            itemy = itemyF(itemy)

                    if Dcount <= 4:
                        p.drawString(
                            prviousx + 100,
                            Inf(itemy),
                            ("{:10d}.{}").format(
                                int(Item["GSTAmount"]),
                                str(Item["GSTAmount"]).split(".")[1],
                            ),
                        )
                        itemy = itemyF(itemy)

                    if Dcount <= 5:
                        if Decimal(Item["DutiableQty"]) != Decimal("0.0000"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:8d}.{} {}").format(
                                    int(Item["DutiableQty"]),
                                    str(Item["DutiableQty"]).split(".")[1],
                                    Item["DutiableUOM"],
                                ),
                            )
                            itemy = itemyF(itemy)

                    if Dcount <= 6:
                        if Decimal(Item["ExciseDutyAmount"]) != Decimal("0.00"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:10d}.{}").format(
                                    int(Item["ExciseDutyAmount"]),
                                    str(Item["ExciseDutyAmount"]).split(".")[1],
                                ),
                            )
                            itemy = itemyF(itemy)

                    if Dcount <= 7:
                        if Decimal(Item["CustomsDutyAmount"]) != Decimal("0.00"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:10d}.{}").format(
                                    int(Item["CustomsDutyAmount"]),
                                    str(Item["CustomsDutyAmount"]).split(".")[1],
                                ),
                            )
                            itemy = itemyF(itemy)

                    if Dcount <= 8:
                        if Decimal(Item["OtherTaxAmount"]) != Decimal("0.00"):
                            p.drawString(
                                prviousx + 100,
                                Inf(itemy),
                                ("{:10d}.{}").format(
                                    int(Item["OtherTaxAmount"]),
                                    str(Item["OtherTaxAmount"]).split(".")[1],
                                ),
                            )
                            itemy = itemyF(itemy)

                itemy = itemyF(itemy + inp + 10)
                self.cursor.execute(
                    f"SELECT SupplierCode FROM InvoiceDtl WHERE PermitId = '{Item['PermitId']}' AND InvoiceNo = '{Item['InvoiceNo']}' "
                )
                InvoiceData = self.cursor.fetchone()
                if InvoiceData != "":
                    self.cursor.execute(
                        f"SELECT Name,Name1 FROM SUPPLIERMANUFACTURERPARTY WHERE code = '{InvoiceData[0]}' "
                    )
                    SupplyData = self.cursor.fetchone()
                    if SupplyData is not None:
                        SupplyData = (str(SupplyData[0]) + str(SupplyData[1])).upper()
                        p.drawString(lftcol, itemy, (SupplyData)[:50])
                        itemy = itemyF(itemy)
                        if len(SupplyData) >= 50:
                            p.drawString(lftcol, itemy, (SupplyData)[50:])
                            itemy = itemyF(itemy)

                self.cursor.execute(
                    f"SELECT * FROM Cascdtl WHERE ItemNo = '{Item['ItemNo']}' AND PermitId = '{Item['PermitId']}'"
                )
                CascCheck = self.cursor.fetchall()

                if len(CascCheck) != 0:
                    itemy = Cascfunction(Item, "Casc1", "01", itemy)
                    itemy = Cascfunction(Item, "Casc2", "02", itemy)
                    itemy = Cascfunction(Item, "Casc3", "03", itemy)
                    itemy = Cascfunction(Item, "Casc4", "04", itemy)
                    itemy = Cascfunction(Item, "Casc5", "05", itemy)

                if (
                    str(Item["EngineCapcity"]) != str("0.00")
                    and str(Item["EngineCapcity"]) != ""
                ):
                    p.drawString(
                        snox,
                        itemy,
                        "-------------------------------------------------------------------------------",
                    )
                    itemy = itemyF(itemy)
                    p.drawString(lftcol, itemy, "S/NO")
                    p.drawString(lftcol + 70, itemy, "ENGINE NO/CHASSIS NO ")
                    itemy = itemyF(itemy)
                    p.drawString(
                        lftcol, itemy, ("   {}").format("%02d" % Item["ItemNo"])
                    )
                    p.drawString(lftcol + 70, itemy, str(Item["EngineCapcity"]))
                    itemy = itemyF(itemy)
                    p.drawString(
                        snox,
                        itemy,
                        "-------------------------------------------------------------------------------",
                    )

                p.drawString(
                    snox,
                    itemy,
                    "-------------------------------------------------------------------------------",
                )
                itemy = itemyF(itemy) - 20
                p.drawString(
                    snox,
                    itemy,
                    "-------------------------------------------------------------------------------",
                )
                itemy = itemyF(itemy)

            def itemyF1(itemy):
                if itemy <= 60:
                    itemy = 820
                    p.showPage()
                    p.setFont("Courier", 10)
                else:
                    itemy -= 10
                if itemy <= 820 and itemy >= 780:
                    p.setFont("Courier", 10)
                    p.drawString(rgtcol, itemy, "CARGO CLEARANCE PERMIT ")
                    p.drawString(460, itemy, ("PG : {} OF").format(self.countPage))
                    self.countPage += 1
                    itemy -= 10
                    p.drawString(lftcol, itemy, "PERMIT NO : " + PermitBar)
                    p.drawString(rgtcol, itemy, "======================")
                    itemy -= 10
                    p.drawString(rgtcol, itemy, "(CONTINUATION PAGE)")
                    itemy -= 20
                    p.drawString(lftcol, itemy, "CONSIGNMENT DETAILS")
                    itemy -= 10
                    p.drawString(
                        lftcol,
                        itemy,
                        "--------------------------------------------------------------------------------",
                    )
                    itemy -= 10
                    p.drawString(
                        lftcol,
                        50,
                        "--------------------------------------------------------------------------------",
                    )
                    p.drawString(
                        lftcol,
                        40,
                        ("UNIQUE REF : {} {} {}").format(
                            (DeclarData[0]).upper(),
                            str(PermitValues["MSGId"][:8]).upper(),
                            str(PermitValues["MSGId"][8:]).upper(),
                        ),
                    )
                return itemy

            TradeRemark = str(PermitValues["TradeRemarks"]).upper()
            # itemy = itemyF1(itemy)
            if TradeRemark != "":
                p.drawString(lftcol, itemy, "TRADER’s REMARKS")
                itemy = itemyF1(itemy)
            TradeX = lftcol
            for Tr in range(len(TradeRemark)):
                if TradeRemark[Tr] != "\n":
                    p.drawString(TradeX, itemy, TradeRemark[Tr])
                TradeX += 6
                if (Tr + 1) % 80 == 0 or TradeRemark[Tr] == "\n":
                    TradeX = lftcol
                    itemy = itemyF1(itemy)

            else:
                itemy = itemyF1(itemy)
            p.drawString(
                lftcol,
                itemy,
                "-------------------------------------------------------------------------------",
            )

            self.cursor.execute(
                f"SELECT RowNo,ContainerNo,size,weight,SealNo FROM ContainerDtl WHERE PermitId = '{PermitValues['PermitId']}' "
            )
            ContainerData = self.cursor.fetchall()

            if len(ContainerData) != 0:
                itemy = itemyF1(itemy)
                p.drawString(lftcol, itemy, "CONTAINER IDENTIFIERS")
                itemy = itemyF1(itemy)
                p.drawString(
                    lftcol,
                    itemy,
                    "-------------------------------------------------------------------------------",
                )
                itemy = itemyF1(itemy)
                for Cont in ContainerData:
                    p.drawString(lftcol, itemy, ("   {})").format("%02d" % Cont[0]))
                    p.drawString(lftcol + 50, itemy, str(Cont[1]).upper())
                    p.drawString(
                        lftcol + 130,
                        itemy,
                        ("{}  {}").format(Cont[2][:3], Cont[2][3:5]),
                    )
                    p.drawString(lftcol + 200, itemy, (str(Cont[3]))[:3])
                    p.drawString(lftcol + 240, itemy, str(Cont[4]))
                    itemy = itemyF1(itemy)

            p.drawString(
                lftcol,
                itemy,
                "-------------------------------------------------------------------------------",
            )
            itemy = itemyF1(itemy)
            p.drawString(
                lftcol,
                itemy,
                "NO UNAUTHORISED ADDITION/AMENDMENT TO THIS PERMIT MAY BE MADE AFTER APPROVAL",
            )
            itemy = itemyF1(itemy)
            p.drawString(
                lftcol,
                itemy,
                "-------------------------------------------------------------------------------",
            )
            itemy = itemyF1(itemy - 10)
            p.drawString(lftcol, itemy, "NAME OF COMPANY:")
            Declarant = "SELECT name,DeclarantName,DeclarantCode,DeclarantTel FROM DeclarantCompany where tradenetmailboxId=%s"
            self.cursor.execute(Declarant, (PermitValues["TradeNetMailboxID"],))
            DeclarData = self.cursor.fetchone()
            p.drawString(lftcol + 110, itemy, (DeclarData[0])[:67])
            itemy = itemyF1(itemy)
            p.drawString(lftcol + 110, itemy, (DeclarData[0])[67:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "DECLARANT NAME :")
            p.drawString(lftcol + 110, itemy, (DeclarData[1])[:67])
            itemy = itemyF1(itemy)
            p.drawString(lftcol + 110, itemy, (DeclarData[1])[67:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "DECLARANT CODE :")
            p.drawString(lftcol + 110, itemy, "XXXX" + (DeclarData[2])[-5:])
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "TEL NO         : ")
            p.drawString(lftcol + 110, itemy, (DeclarData[3]))
            itemy = itemyF1(itemy)
            p.drawString(
                lftcol,
                itemy,
                "-------------------------------------------------------------------------------",
            )
            itemy = itemyF1(itemy)
            p.drawString(lftcol, itemy, "CONTROLLING AGENCY/CUSTOMS CONDITIONS ")
            itemy = itemyF1(itemy)

            if PermitValues["prmtStatus"] == "AMD":
                self.cursor.execute(
                    f"SELECT Conditioncode,ConditionDescription FROM Inpmt WHERE PermitNumber = '{PermitValues['PermitNumber']}' AND MsgId = '{PermitValues['MSGId']}' ORDER BY SNO"
                )
            else:
                self.cursor.execute(
                    f"SELECT Conditioncode,ConditionDescription FROM Inpmt WHERE PermitNumber = '{PermitValues['PermitNumber']}' ORDER BY SNO"
                )
            ControllingData = self.cursor.fetchall()

            for Control in ControllingData:
                p.setFont("Courier-Bold", 10)
                p.drawString(lftcol, itemy, Control[0])
                p.drawString(lftcol + 30, itemy, "-")
                p.setFont("Courier", 10)

                p.drawString(lftcol + 40, itemy, (Control[1])[:73])
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

            draft = PermitBar
            if draft == "DRAFT":
                draft = f"Draft_{PermitValues['MSGId']}"
                filename = f"D:/Users/Public/PDFFilesKtt/1{draft}.pdf"
            else:
                filename = f"D:/Users/Public/PDFFilesKtt/1{draft}.pdf"
            p.setTitle(draft)

            p.save()

            try:
                with open(filename, "wb") as f:
                    f.write(buffer.getbuffer())
            except Exception as e:
                pass
            buffer.seek(0)
            buffer.close()

            existing_pdf = PdfFileReader(open(filename, "rb"))
            output = PdfFileWriter()

            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(595, 841))
            can.setFont("Courier", 10)
            can.drawString(520, 700, str(len(existing_pdf.pages)))
            can.showPage()
            can.setFont("Courier", 10)
            can.drawString(520, 810, str(len(existing_pdf.pages)))
            can.showPage()
            can.setFont("Courier", 10)
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

            output_stream = open(
                f"D:/Users/Public/PDFFilesKtt/{draft}.pdf", "wb"
            )  # f"D:/Users/Public/PDFFilesKtt/{draft}.pdf
            output.write(output_stream)
            output_stream.close()

            file_path = f"D:/Users/Public/PDFFilesKtt/{draft}1.pdf"

            if os.path.exists(file_path):
                os.remove(file_path)

            pdfFiles.append(f"D:/Users/Public/PDFFilesKtt/{draft}.pdf")

        pdfWriter = PdfFileWriter()

        for file in pdfFiles:
            pdfFile = open(file, "rb")
            pdfReader = PdfFileReader(pdfFile)

            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                pdfWriter.addPage(pageObj)

        pdfOutputFile = open("D:/Users/Public/PDFFilesKtt/MergedFiles.pdf", "wb")
        pdfWriter.write(pdfOutputFile)

        pdfOutputFile.close()
        pdfFile.close()

        with open(f"D:/Users/Public/PDFFilesKtt/MergedFiles.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()

        response = HttpResponse(pdf_data, content_type="application/pdf")
        if len(pdfFiles) > 1:
            response[
                "Content-Disposition"
            ] = f'attachment; filename="InpayMultiply.pdf"'
        else:
            response["Content-Disposition"] = f'attachment; filename="{draft}.pdf"'

        return response
