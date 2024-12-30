from typing import Any
from django.shortcuts import render,redirect
from KttApp.views import SqlDb
from django.views import View
from datetime import *
import pandas as pd
from KttApp.models import *
from django.http import JsonResponse 
from django.http import HttpResponse
import json
import re
from PyPDF2 import PdfReader
from django.urls import reverse


class TransHome(View):
    def get(self, request):
        context = {
            "CustomiseReport": CustomiseReport.objects.filter(ReportName="IPT", UserName=request.session["Username"]).exclude(FiledName="id"),
            "ManageUserMail": ManageUser.objects.filter(Status="Active").order_by("MailBoxId").values_list("MailBoxId", flat=True).distinct(),
            "UserName": request.session["Username"],
        }
        return render(request, "Transhipment/Listpage.html", context)


class TranshList(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request):
        Username = request.session["Username"]

        self.cursor.execute(
            "SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username)
        )
        AccountId = self.cursor.fetchone()[0]

        nowdata = datetime.now() - timedelta(days=60)
        self.cursor.execute(
            "SELECT t1.Id as 'ID', t1.JobId as 'JOB ID', t1.MSGId as 'MSG ID', CONVERT(varchar, t1.TouchTime, 105) AS 'DEC DATE',SUBSTRING(t1.DeclarationType, 1, CHARINDEX(':', t1.DeclarationType) - 1) AS 'DEC TYPE', t1.TouchUser AS 'CREATE', t2.TradeNetMailboxID AS 'DEC ID', CONVERT(varchar, t1.ArrivalDate, 105) AS ETA, t1.PermitNumber AS 'PERMIT NO', t3.Name+' '+t3.Name1 AS 'IMPORTER',STUFF((SELECT distinct(', ' +  US.InHAWBOBL)  FROM TranshipmentItemDtl  US  WHERE US.PermitId = t1.PermitId FOR XML PATH('')), 1, 1, '') 'HAWB',CASE   WHEN  t1.InwardTransportMode = '4 : Air' THEN t1.MasterAirwayBill WHEN t1.InwardTransportMode = '1 : Sea'  THEN t1.OceanBillofLadingNo  ELSE ''  END AS 'MAWB/OBL',t1.LoadingPortCode as POL,t1.MessageType as 'MSG TYPE', t1.InwardTransportMode as TPT,t1.PreviousPermit as 'PRE PMT',t1.GrossReference as 'X REF', t1.InternalRemarks as 'INT REM',t1.Status as 'STATUS' FROM  TranshipmentHeader AS t1 INNER JOIN DeclarantCompany AS t2 ON t1.DeclarantCompanyCode = t2.Code INNER JOIN transImporter AS t3 ON t1.ImporterCompanyCode = t3.Code INNER JOIN ManageUser AS t6 ON t6.UserId=t1.TouchUser  where   t6.AccountId='"
            + AccountId
            + "'  GROUP BY t1.Id, t1.JobId, t1.MSGId, t1.TouchTime, t1.TouchUser,t1.DeclarationType, t1.ArrivalDate, t1.PermitId,t1.PermitNumber, t1.InwardTransportMode, t1.MasterAirwayBill,t1.OceanBillofLadingNo, t1.LoadingPortCode, t1.MessageType, t1.InwardTransportMode,  t1.PreviousPermit,t1.InternalRemarks, t1.Status, t2.TradeNetMailboxID, t3.Name,t3.Name1,t6.AccountId,t1.License ,t1.GrossReference , t1.ReleaseLocation, t1.DischargePort ,t1.RecepitLocation ,t1.OutwardTransportMode ,t1.DeclarningFor ,t2.DeclarantName order by t1.Id Desc"
        )#t1.Status != 'DEL' and

        # heading = self.cursor.description
        headers = [i[0] for i in self.cursor.description]
        return JsonResponse(
            (pd.DataFrame(list(self.cursor.fetchall()), columns=headers)).to_dict(
                "records"
            ),
            safe=False,
        )


class TranshListnew(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request):
        Username = request.session["Username"]

        refDate = datetime.now().strftime("%Y%m%d")
    
        jobDate = datetime.now().strftime("%Y-%m-%d")

        currentDate = datetime.now().strftime("%d/%m/%Y")

        self.cursor.execute(
            "SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username)
        )

        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute( "SELECT COUNT(*) + 1  FROM TranshipmentHeader WHERE MSGId LIKE '%{}%' AND MessageType = 'TNPDEC' ".format(refDate))
        self.RefId = "%03d" % self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(
                jobDate, AccountId
            )
        )
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}"

        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"

        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        self.cursor.execute(
            "select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"
            + Username
            + "'"
        )
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
            "DeclarationType": CommonMaster.objects.filter(
                TypeId=18, StatusId=1
            ).order_by("Name"),
            "CargoType": CommonMaster.objects.filter(TypeId=2, StatusId=1),
            "OutWardTransportMode": CommonMaster.objects.filter(
                TypeId=3, StatusId=1
            ).order_by("Name"),
            "DeclaringFor": CommonMaster.objects.filter(TypeId=81, StatusId=1).order_by(
                "Name"
            ),
            "BgIndicator": CommonMaster.objects.filter(TypeId=4, StatusId=1).order_by(
                "Name"
            ),
            "DocumentAttachmentType": CommonMaster.objects.filter(
                TypeId=5, StatusId=1
            ).order_by("Name"),
            "CoType": CommonMaster.objects.filter(TypeId=16, StatusId=1).order_by(
                "Name"
            ),
            "CertificateType": CommonMaster.objects.filter(
                TypeId=17, StatusId=1
            ).order_by("Name"),
            "Currency": Currency.objects.filter().order_by("Currency"),
            "Container": CommonMaster.objects.filter(TypeId=6, StatusId=1).order_by(
                "Name"
            ),
            "TotalOuterPack": CommonMaster.objects.filter(
                TypeId=10, StatusId=1
            ).order_by("Name"),
            "InvoiceTermType": CommonMaster.objects.filter(
                TypeId=7, StatusId=1
            ).order_by("Name"),
            "Making": CommonMaster.objects.filter(TypeId=12, StatusId=1).order_by(
                "Name"
            ),
            "VesselType": CommonMaster.objects.filter(TypeId=14, StatusId=1).order_by(
                "Name"
            ),
             "currentDate": currentDate 
        }
        return render(request, "Transhipment/Newpage.html", context)


class PartyLoad(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM transImporter WHERE status = 'Active' ORDER BY Name "
        )
        self.Partycontext.update(
            {
                "importer": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=["Code", "Name", "Name1", "CRUEI"],
                    )
                ).to_dict("records"),
            }
        )

        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM transInwardcarrier WHERE status = 'Active' ORDER BY Name"
        )
        self.Partycontext.update(
            {
                "inward": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=["Code", "Name", "Name1", "CRUEI"],
                    )
                ).to_dict("records"),
            }
        )

        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM transOutward WHERE status = 'Active' ORDER BY Name"
        )
        self.Partycontext.update(
            {
                "outward": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=["Code", "Name", "Name1", "CRUEI"],
                    )
                ).to_dict("records"),
            }
        )

        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM transfreight WHERE status = 'Active' ORDER BY Name"
        )
        self.Partycontext.update(
            {
                "fright": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=["Code", "Name", "Name1", "CRUEI"],
                    )
                ).to_dict("records")
            }
        )

        self.cursor.execute(
            "SELECT ConsigneeCode,ConsigneeName,ConsigneeName1,ConsigneeCRUEI,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSub,ConsigneeSubDivi,ConsigneePostal,ConsigneeCountry FROM transConsignee ORDER BY ConsigneeName"
        )
        self.Partycontext.update(
            {
                "consign": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=[
                            "ConsigneeCode",
                            "ConsigneeName",
                            "ConsigneeName1",
                            "ConsigneeCRUEI",
                            "ConsigneeAddress",
                            "ConsigneeAddress1",
                            "ConsigneeCity",
                            "ConsigneeSub",
                            "ConsigneeSubDivi",
                            "ConsigneePostal",
                            "ConsigneeCountry",
                        ],
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)


class TranshItem(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request, permit):
        self.cursor.execute(
            "SELECT * FROM TranshipmentItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(
                permit
            )
        )
        headers = [i[0] for i in self.cursor.description]
        itemData = self.cursor.fetchall()
        context = {
            "item": (pd.DataFrame(list(itemData), columns=headers).to_dict("records"))
        }
        self.cursor.execute(
            f"select * from TCASCDtl WHERE PermitId = '{permit}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "casc": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        return JsonResponse(context)

    def post(self, request):
        ItemNo = request.POST.get("ItemNo")
        PermitId = request.POST.get("PermitId")
        MessageType = request.POST.get("MessageType")
        HSCode = request.POST.get("HSCode")
        Description = request.POST.get("Description")
        DGIndicator = request.POST.get("DGIndicator")
        Contry = request.POST.get("Contry")
        Brand = request.POST.get("Brand")
        Model = request.POST.get("Model")
        InHAWBOBL = request.POST.get("InHAWBOBL")
        InMAWBOBL = request.POST.get("InMAWBOBL")
        OutHAWBOBL = request.POST.get("OutHAWBOBL")
        OutMAWBOBL = request.POST.get("OutMAWBOBL")
        DutiableQty = request.POST.get("DutiableQty")
        DutiableUOM = request.POST.get("DutiableUOM")
        TotalDutiableQty = request.POST.get("TotalDutiableQty")
        TotalDutiableUOM = request.POST.get("TotalDutiableUOM")
        InvoiceQuantity = request.POST.get("InvoiceQuantity")
        HSQty = request.POST.get("HSQty")
        HSUOM = request.POST.get("HSUOM")
        AlcoholPer = request.POST.get("AlcoholPer")
        ChkUnitPrice = request.POST.get("ChkUnitPrice")
        UnitPrice = request.POST.get("UnitPrice")
        UnitPriceCurrency = request.POST.get("UnitPriceCurrency")
        ExchangeRate = request.POST.get("ExchangeRate")
        SumExchangeRate = request.POST.get("SumExchangeRate")
        TotalLineAmount = request.POST.get("TotalLineAmount")
        InvoiceCharges = request.POST.get("InvoiceCharges")
        CIFFOB = request.POST.get("CIFFOB")
        OPQty = request.POST.get("OPQty")
        OPUOM = request.POST.get("OPUOM")
        IPQty = request.POST.get("IPQty")
        IPUOM = request.POST.get("IPUOM")
        InPqty = request.POST.get("InPqty")
        InPUOM = request.POST.get("InPUOM")
        ImPQty = request.POST.get("ImPQty")
        ImPUOM = request.POST.get("ImPUOM")
        PreferentialCode = request.POST.get("PreferentialCode")
        GSTRate = request.POST.get("GSTRate")
        GSTUOM = request.POST.get("GSTUOM")
        GSTAmount = request.POST.get("GSTAmount")
        ExciseDutyRate = request.POST.get("ExciseDutyRate")
        ExciseDutyUOM = request.POST.get("ExciseDutyUOM")
        ExciseDutyAmount = request.POST.get("ExciseDutyAmount")
        CustomsDutyRate = request.POST.get("CustomsDutyRate")
        CustomsDutyUOM = request.POST.get("CustomsDutyUOM")
        CustomsDutyAmount = request.POST.get("CustomsDutyAmount")
        OtherTaxRate = request.POST.get("OtherTaxRate")
        OtherTaxUOM = request.POST.get("OtherTaxUOM")
        OtherTaxAmount = request.POST.get("OtherTaxAmount")
        CurrentLot = request.POST.get("CurrentLot")
        PreviousLot = request.POST.get("PreviousLot")
        Making = request.POST.get("Making")
        ShippingMarks1 = request.POST.get("ShippingMarks1")
        ShippingMarks2 = request.POST.get("ShippingMarks2")
        ShippingMarks3 = request.POST.get("ShippingMarks3")
        ShippingMarks4 = request.POST.get("ShippingMarks4")
        TouchUser = request.session["Username"]
        TouchTime = datetime.now()
        DrpVehicleType = request.POST.get("DrpVehicleType")
        Enginecapacity = request.POST.get("EngineCapcity")
        Engineuom = request.POST.get("Engineuom")
        Orginregdate = request.POST.get("orignaldatereg")
        OptionalChrgeUOM = request.POST.get("OptionalChrgeUOM")
        Optioncahrge = request.POST.get("Optioncahrge")
        OptionalSumtotal = request.POST.get("OptionalSumtotal")
        OptionalSumExchage = request.POST.get("OptionalSumExchage")

        self.cursor.execute(
            f"DELETE FROM TCASCDtl WHERE ItemNo = '{ItemNo}' AND PermitId = '{PermitId}'"
        )
        self.conn.commit()

        cascQry = "INSERT INTO TCASCDtl(ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId,Enduserdesc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for casc in json.loads(request.POST.get("CascDatas")):
            cascVal = (
                request.POST.get("ItemNo"),
                casc["ProductCode"],
                casc["Quantity"],
                casc["ProductUOM"],
                casc["RowNo"],
                casc["CascCode1"],
                casc["CascCode2"],
                casc["CascCode3"],
                request.POST.get("PermitId"),
                request.POST.get("MessageType"),
                str(request.session["Username"]).upper(),
                datetime.now(),
                casc["CASCId"],
                casc["EndUserDes"],
            )
            self.cursor.execute(cascQry, cascVal)
        self.conn.commit()
        self.cursor.execute(
            "SELECT * FROM TranshipmentItemDtl WHERE PermitId = '{}' AND ItemNo = '{}' ".format(
                PermitId, ItemNo
            )
        )
        result = self.cursor.fetchall()
        # data = (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,InMAWBOBL,OutHAWBOBL,OutMAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,DrpVehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage)
        # for i in data:
        #     print(i)
        Val = (
            ItemNo,
            PermitId,
            MessageType,
            HSCode,
            Description,
            DGIndicator,
            Contry,
            Brand,
            Model,
            InHAWBOBL,
            InMAWBOBL,
            OutHAWBOBL,
            OutMAWBOBL,
            DutiableQty,
            DutiableUOM,
            TotalDutiableQty,
            TotalDutiableUOM,
            InvoiceQuantity,
            HSQty,
            HSUOM,
            AlcoholPer,
            ChkUnitPrice,
            UnitPrice,
            UnitPriceCurrency,
            ExchangeRate,
            SumExchangeRate,
            TotalLineAmount,
            InvoiceCharges,
            CIFFOB,
            OPQty,
            OPUOM,
            IPQty,
            IPUOM,
            InPqty,
            InPUOM,
            ImPQty,
            ImPUOM,
            PreferentialCode,
            GSTRate,
            GSTUOM,
            GSTAmount,
            ExciseDutyRate,
            ExciseDutyUOM,
            ExciseDutyAmount,
            CustomsDutyRate,
            CustomsDutyUOM,
            CustomsDutyAmount,
            OtherTaxRate,
            OtherTaxUOM,
            OtherTaxAmount,
            CurrentLot,
            PreviousLot,
            Making,
            ShippingMarks1,
            ShippingMarks2,
            ShippingMarks3,
            ShippingMarks4,
            TouchUser,
            TouchTime,
            DrpVehicleType,
            Enginecapacity,
            Engineuom,
            Orginregdate,
            OptionalChrgeUOM,
            Optioncahrge,
            OptionalSumtotal,
            OptionalSumExchage,
        )
        message = ""
        if result:
            Qry = "UPDATE TranshipmentItemDtl SET ItemNo = %s,PermitId = %s,MessageType = %s,HSCode = %s,Description = %s,DGIndicator = %s,Contry = %s,Brand = %s,Model = %s,InHAWBOBL = %s,InMAWBOBL = %s,OutHAWBOBL = %s,OutMAWBOBL = %s,DutiableQty = %s,DutiableUOM = %s,TotalDutiableQty = %s,TotalDutiableUOM = %s,InvoiceQuantity = %s,HSQty = %s,HSUOM = %s,AlcoholPer = %s,ChkUnitPrice = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,InvoiceCharges = %s,CIFFOB = %s,OPQty = %s,OPUOM = %s,IPQty = %s,IPUOM = %s,InPqty = %s,InPUOM = %s,ImPQty = %s,ImPUOM = %s,PreferentialCode = %s,GSTRate = %s,GSTUOM = %s,GSTAmount = %s,ExciseDutyRate = %s,ExciseDutyUOM = %s,ExciseDutyAmount = %s,CustomsDutyRate = %s,CustomsDutyUOM = %s,CustomsDutyAmount = %s,OtherTaxRate = %s,OtherTaxUOM = %s,OtherTaxAmount = %s,CurrentLot = %s,PreviousLot = %s,Making = %s,ShippingMarks1 = %s,ShippingMarks2 = %s,ShippingMarks3 = %s,ShippingMarks4 = %s,TouchUser = %s,TouchTime = %s,DrpVehicleType = %s,Enginecapacity = %s,Engineuom = %s,Orginregdate = %s,OptionalChrgeUOM = %s,Optioncahrge = %s,OptionalSumtotal = %s,OptionalSumExchage = %s WHERE PermitId = '{}' AND ItemNo = '{}'".format(PermitId, ItemNo)
            try:
                self.cursor.execute(Qry, Val)
                self.conn.commit()
                message = "updated Successfully"
            except Exception as e:
                print(e)
                message = "Did not updated Successfully"
        else:
            try:
                Qry = "INSERT INTO TranshipmentItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,InMAWBOBL,OutHAWBOBL,OutMAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,DrpVehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                # Val = (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,InMAWBOBL,OutHAWBOBL,OutMAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,DrpVehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage)
                self.cursor.execute(Qry, Val)
                self.conn.commit()
                message = "Item Saved"
            except Exception as e:
                print("The error is : ", e)
                message = "Item Did not Saved"

        self.cursor.execute(
            "SELECT * FROM TranshipmentItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(
                PermitId
            )
        )
        headers = [i[0] for i in self.cursor.description]  # list comprehension

        itemData = self.cursor.fetchall()
        context = {
            "item": (pd.DataFrame(list(itemData), columns=headers).to_dict("records")),
            "message": message,
        }

        self.cursor.execute(
            f"select * from TCASCDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "casc": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )

        return JsonResponse(context)


def TransEditItemall(request):
    db = SqlDb()
    

    print("hello ")

    PermitId = request.POST.get('PermitId')

    ItemValue = json.loads(request.POST.get('editItemData'))

    qry = "UPDATE TranshipmentItemDtl SET MessageType = %s,HSCode = %s,Description = %s,DGIndicator = %s,Contry = %s,Brand = %s,Model = %s,InHAWBOBL = %s,InMAWBOBL = %s,OutHAWBOBL = %s,OutMAWBOBL = %s,DutiableQty = %s,DutiableUOM = %s,TotalDutiableQty = %s,TotalDutiableUOM = %s,InvoiceQuantity = %s,HSQty = %s,HSUOM = %s,AlcoholPer = %s,ChkUnitPrice = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,InvoiceCharges = %s,CIFFOB = %s,OPQty = %s,OPUOM = %s,IPQty = %s,IPUOM = %s,InPqty = %s,InPUOM = %s,ImPQty = %s,ImPUOM = %s,PreferentialCode = %s,GSTRate = %s,GSTUOM = %s,GSTAmount = %s,ExciseDutyRate = %s,ExciseDutyUOM = %s,ExciseDutyAmount = %s,CustomsDutyRate = %s,CustomsDutyUOM = %s,CustomsDutyAmount = %s,OtherTaxRate = %s,OtherTaxUOM = %s,OtherTaxAmount = %s,CurrentLot = %s,PreviousLot = %s,Making = %s,ShippingMarks1 = %s,ShippingMarks2 = %s,ShippingMarks3 = %s,ShippingMarks4 = %s,TouchUser = %s,TouchTime = %s,DrpVehicleType = %s,Enginecapacity = %s,Engineuom = %s,Orginregdate = %s,OptionalChrgeUOM = %s,Optioncahrge = %s,OptionalSumtotal = %s,OptionalSumExchage = %s WHERE ItemNo = %s AND PermitId = %s"
    
    
    for i in ItemValue:
        val = (i['MessageType'],i['HSCode'],i['Description'],i['DGIndicator'],i['Contry'],i['Brand'],i['Model'],i['InHAWBOBL'],i['InMAWBOBL'],i['OutHAWBOBL'],i['OutMAWBOBL'],i['DutiableQty'],i['DutiableUOM'],i['TotalDutiableQty'],i['TotalDutiableUOM'],i['InvoiceQuantity'],i['HSQty'],i['HSUOM'],i['AlcoholPer'],i['ChkUnitPrice'],i['UnitPrice'],i['UnitPriceCurrency'],i['ExchangeRate'],i['SumExchangeRate'],i['TotalLineAmount'],i['InvoiceCharges'],i['CIFFOB'],i['OPQty'],i['OPUOM'],i['IPQty'],i['IPUOM'],i['InPqty'],i['InPUOM'],i['ImPQty'],i['ImPUOM'],i['PreferentialCode'],i['GSTRate'],i['GSTUOM'],i['GSTAmount'],i['ExciseDutyRate'],i['ExciseDutyUOM'],i['ExciseDutyAmount'],i['CustomsDutyRate'],i['CustomsDutyUOM'],i['CustomsDutyAmount'],i['OtherTaxRate'],i['OtherTaxUOM'],i['OtherTaxAmount'],i['CurrentLot'],i['PreviousLot'],i['Making'],i['ShippingMarks1'],i['ShippingMarks2'],i['ShippingMarks3'],i['ShippingMarks4'],request.session["Username"],datetime.now(),i['DrpVehicleType'],i['Enginecapacity'],i['Engineuom'],i['Orginregdate'],i['OptionalChrgeUOM'],i['Optioncahrge'],i['OptionalSumtotal'],i['OptionalSumExchage'],i['ItemNo'],PermitId)
        db.cursor.execute(qry,val)
        db.conn.commit()

    context = {}
    db.cursor.execute(
        f"select * from TranshipmentItemDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
    )
    headers = [i[0] for i in db.cursor.description]
    context.update(
        {
            "item": (
                pd.DataFrame(list(db.cursor.fetchall()), columns=headers)
            ).to_dict("records")
        }
    )
    
    return JsonResponse(context)


class TransDelHblHawb(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,PermitId):

        self.cursor.execute("update TranshipmentItemDtl  set InHAWBOBL='',OutHAWBOBL=''  where  MessageType='TNPDEC' AND PermitId='" + PermitId + "' ")
        self.conn.commit()

        self.cursor.execute("SELECT ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,InMAWBOBL,OutHAWBOBL,OutMAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,DrpVehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage  FROM  TranshipmentItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(PermitId))
        self.item = self.cursor.fetchall()

        return JsonResponse({
            "item" : (pd.DataFrame(list(self.item), columns=['ItemNo','PermitId','MessageType','HSCode','Description','DGIndicator','Contry','Brand','Model','InHAWBOBL','InMAWBOBL','OutHAWBOBL','OutMAWBOBL','DutiableQty','DutiableUOM','TotalDutiableQty','TotalDutiableUOM','InvoiceQuantity','HSQty','HSUOM','AlcoholPer','ChkUnitPrice','UnitPrice','UnitPriceCurrency','ExchangeRate','SumExchangeRate','TotalLineAmount','InvoiceCharges','CIFFOB','OPQty','OPUOM','IPQty','IPUOM','InPqty','InPUOM','ImPQty','ImPUOM','PreferentialCode','GSTRate','GSTUOM','GSTAmount','ExciseDutyRate','ExciseDutyUOM','ExciseDutyAmount','CustomsDutyRate','CustomsDutyUOM','CustomsDutyAmount','OtherTaxRate','OtherTaxUOM','OtherTaxAmount','CurrentLot','PreviousLot','Making','ShippingMarks1','ShippingMarks2','ShippingMarks3','ShippingMarks4','TouchUser','TouchTime','DrpVehicleType','Enginecapacity','Engineuom','Orginregdate','OptionalChrgeUOM','Optioncahrge','OptionalSumtotal','OptionalSumExchage'])).to_dict('records'),
        }) 
  


class AttachDocument(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request):
        if request.GET.get("Method") == "DELETE":
            self.cursor.execute(
                "DELETE FROM transhipfile WHERE Id = '{}' ".format(
                    request.GET.get("Data")
                )
            )
            self.conn.commit()
        elif request.GET.get("Method") == "ALLDELETE":
            self.cursor.execute(
                "DELETE FROM transhipfile WHERE PermitId = '{}' AND Type = 'NEW' ".format(
                    request.GET.get("PermitId")
                )
            )

            self.conn.commit()

        self.cursor.execute(
            f"SELECT Id,Sno,Name,ContentType,DocumentType,Size,PermitId,Type FROM transhipfile where PermitId = '{request.GET.get('PermitId')}' Order By Sno "
        )
        print("hello Welcome : ", request.GET.get("PermitId"))

        return JsonResponse(
            {
                "attachFile": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=[
                            "Id",
                            "Sno",
                            "Name",
                            "ContentType",
                            "DocumentType",
                            "Size",
                            "PermitId",
                            "Type",
                        ],
                    )
                ).to_dict("records"),
            }
        )

    def post(self, request):
        Result = ""
        try:
            self.cursor.execute(
                "SELECT COUNT(PermitId) AS MaxItem FROM transhipfile  where PermitId='"
                + request.POST.get("PermitId")
                + "' AND Type = '"
                + request.POST.get("Type")
                + "'"
            )

            myfile = request.FILES.get("file")
            path1 = request.POST.get("FilePath")
            fileFormat = request.POST.get("ContentType").split("/")

            with open(
                path1 + request.POST.get("Name") + "." + fileFormat[1], "wb+"
            ) as destination:
                for chunk in myfile.chunks():
                    destination.write(chunk)

            lenFile = int((self.cursor.fetchone())[0]) + 1
            Qry = "INSERT INTO transhipfile (Sno,Name,ContentType,Data,DocumentType,TranshipId,TouchUser,TouchTime,Size,PermitId,Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            Val = (
                lenFile,
                request.POST.get("Name") + "." + fileFormat[1],
                request.POST.get("ContentType"),
                None,
                request.POST.get("DocumentType"),
                request.POST.get("InPaymentId"),
                request.POST.get("UserName"),
                request.POST.get("TouchTime"),
                request.POST.get("Size"),
                request.POST.get("PermitId"),
                request.POST.get("Type"),
            )
            self.cursor.execute(Qry, Val)
            self.conn.commit()
            Result = "SAVED SUCCESSFULLY...!"

        except Exception as E:
            Result = "DID NOT SAVED...!"

        self.cursor.execute(
            f"SELECT Id,Sno,Name,ContentType,DocumentType,Size,PermitId,Type FROM transhipfile where PermitId = '{request.POST.get('PermitId')}' AND Type = '{request.POST.get('Type')}'  Order By Sno "
        )
        return JsonResponse(
            {
                "attachFile": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=[
                            "Id",
                            "Sno",
                            "Name",
                            "ContentType",
                            "DocumentType",
                            "Size",
                            "PermitId",
                            "Type",
                        ],
                    )
                ).to_dict("records"),
                "Result": Result,
            }
        )


class ContainerSave(View, SqlDb):
    def post(self, request):
        SqlDb.__init__(self)
        Result = ""
        try:
            if request.POST.get("Method") == "SAVE":
                self.cursor.execute(
                    f"select RowNo , PermitId from TranshipmentContainerDtl where RowNo = '{request.POST.get('RowNo')}' AND PermitId = '{request.POST.get('PermitId')}'"
                )
                result = self.cursor.fetchall()
                if not (result):
                    self.cursor.execute(
                        f"INSERT INTO TranshipmentContainerDtl (PermitId, RowNo,ContainerNo, size, weight,SealNo, MessageType,TouchUser,TouchTime) VALUES ('{request.POST.get('PermitId')}','{request.POST.get('RowNo')}','{request.POST.get('ContainerNo')}','{request.POST.get('size')}','{request.POST.get('weight')}','{request.POST.get('SealNo')}','{request.POST.get('MessageType')}','{str(request.session['Username']).upper()}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
                    )
                    self.conn.commit()
                    Result = "Saved SuccessFully....!"
                else:
                    self.cursor.execute(
                        f"Update TranshipmentContainerDtl set ContainerNo = '{request.POST.get('ContainerNo')}',size = '{request.POST.get('size')}',weight =  '{request.POST.get('weight')}',SealNo = '{request.POST.get('SealNo')}',MessageType = '{request.POST.get('MessageType')}',TouchUser = '{str(request.session['Username']).upper()}',TouchTime = '{datetime.now()}' where RowNo = '{request.POST.get('RowNo')}' AND PermitId = '{request.POST.get('PermitId')}'"
                    )
                    self.conn.commit()
                    Result = "Update SuccessFully....!"

            elif request.POST.get("Method") == "DELETE":
                self.cursor.execute(
                    f"DELETE FROM TranshipmentContainerDtl where PermitId = '{request.POST.get('PermitId')}' AND RowNo = '{request.POST.get('SNo')}' "
                )
                self.conn.commit()

                self.cursor.execute(
                    f"select * from TranshipmentContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
                )
                c = 1
                for j in self.cursor.fetchall():
                    self.cursor.execute(
                        f"UPDATE TranshipmentContainerDtl SET RowNo = {c} WHERE PermitId = '{j[1]}' AND RowNo = '{j[2]}'"
                    )
                    c += 1
                self.conn.commit()
                Result = "Deleted SuccessFully....!"

            elif request.POST.get("Method") == "CHECKDELETE":
                for ids in json.loads(request.POST.get("IDS")):
                    self.cursor.execute(f"DELETE FROM TranshipmentContainerDtl where id = {ids}")
                self.conn.commit()

                self.cursor.execute(
                    f"select * from TranshipmentContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
                )
                c = 1
                for j in self.cursor.fetchall():
                    self.cursor.execute(
                        f"UPDATE TranshipmentContainerDtl SET RowNo = {c} WHERE PermitId = '{j[1]}' AND RowNo = '{j[2]}'"
                    )
                    c += 1
                self.conn.commit()
                Result = "Deleted SuccessFully....!"

            elif request.POST.get("Method") == "LOAD":
                pass
        except Exception as e:
            Result = "Somthing Error"

        self.cursor.execute(
            f"select * from TranshipmentContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
        )
        return JsonResponse(
            {"ContainerValue": list(self.cursor.fetchall()), "Result": Result}
        )

    def get(self, request):
        SqlDb.__init__(self)
        self.cursor.execute(
            f"select * from TranshipmentContainerDtl where PermitId = '{request.GET.get('PermitId')}' Order By RowNo"
        )
        return JsonResponse({"ContainerValue": list(self.cursor.fetchall())})


# class TransSave(View, SqlDb):
#     def __init__(self):
#         SqlDb.__init__(self)
#     def get(self, request):
        
#         query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TranshipmentItemDtl'"
#         self.cursor.execute(query) 

#         result = self.cursor.fetchall()
#         for i in result:
#             print(f"{i[0]}",end=',')
#         return JsonResponse({"message": "loading"})
    
#     def post(self, request):

#         self.cursor.execute("DELETE FROM TranshipmentCPCDtl WHERE PermitId = '{}' ".format(request.POST.get('PermitId')))
#         self.conn.commit()


#         cpcData = json.loads(request.POST.get('cpcData1'))
#         cpcQry = "INSERT INTO TranshipmentCPCDtl(PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
       
       
#         for i in cpcData:
#             cpcVal = (request.POST.get("PermitId"),"TNPDEC",i[0],i[1],i[2],i[3],i[4],str(request.session['Username']).upper(),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#             self.cursor.execute(cpcQry,cpcVal)

        
#         Refid = request.POST.get('Refid')
#         JobId = request.POST.get('JobId')
#         MSGId = request.POST.get('MSGId')
#         PermitId = request.POST.get('PermitId')
#         TradeNetMailboxID = request.POST.get('TradeNetMailboxID')
#         MessageType = request.POST.get('MessageType')
#         DeclarationType = request.POST.get('DeclarationType')
#         PreviousPermit = request.POST.get('PreviousPermit')
#         CargoPackType = request.POST.get('CargoPackType')
#         InwardTransportMode = request.POST.get('InwardTransportMode')
#         OutwardTransportMode = request.POST.get('OutwardTransportMode')
#         BGIndicator = request.POST.get('BGIndicator')
#         SupplyIndicator = request.POST.get('SupplyIndicator')
#         ReferenceDocuments = request.POST.get('ReferenceDocuments')
#         License = request.POST.get('License')
#         # Correct
#         Recipient = request.POST.get('Recipient')
#         DeclarantCompanyCode = request.POST.get('DeclarantCompanyCode')
#         ImporterCompanyCode = request.POST.get('ImporterCompanyCode')
#         HandlingAgentCode = request.POST.get('HandlingAgentCode')
#         InwardCarrierAgentCode = request.POST.get('InwardCarrierAgentCode')
#         OutwardCarrierAgentCode = request.POST.get('OutwardCarrierAgentCode')
#         FreightForwarderCode = request.POST.get('FreightForwarderCode')
#         ClaimantPartyCode = request.POST.get('ClaimantPartyCode')
#         EndUserCode = request.POST.get('EndUserCode')
#         ArrivalDate = request.POST.get('ArrivalDate')
#         LoadingPortCode = request.POST.get('LoadingPortCode')
#         VoyageNumber = request.POST.get('VoyageNumber')
#         VesselName = request.POST.get('VesselName')
#         OceanBillofLadingNo = request.POST.get('OceanBillofLadingNo')
#         ConveyanceRefNo = request.POST.get('ConveyanceRefNo')
#         TransportId = request.POST.get('TransportId')
#         FlightNO = request.POST.get('FlightNO')
#         AircraftRegNo = request.POST.get('AircraftRegNo')
#         MasterAirwayBill = request.POST.get('MasterAirwayBill')
#         ReleaseLocation = request.POST.get('ReleaseLocation')
#         RecepitLocation = request.POST.get('RecepitLocation')
#         StorageLocation = request.POST.get('StorageLocation')
#         RemovalStartDate = request.POST.get('RemovalStartDate')
#         DepartureDate = request.POST.get('DepartureDate')
#         DischargePort = request.POST.get('DischargePort')
#         FinalDestinationCountry = request.POST.get('FinalDestinationCountry')
#         OutVoyageNumber = request.POST.get('OutVoyageNumber')
#         OutVesselName = request.POST.get('OutVesselName')
#         OutOceanBillofLadingNo = request.POST.get('OutOceanBillofLadingNo')
#         VesselType = request.POST.get('VesselType')
#         VesselNetRegTon = request.POST.get('VesselNetRegTon')
#         VesselNationality = request.POST.get('VesselNationality')
#         TowingVesselID = request.POST.get('TowingVesselID')
#         TowingVesselName = request.POST.get('TowingVesselName')
#         NextPort = request.POST.get('NextPort')
#         LastPort = request.POST.get('LastPort')
#         OutConveyanceRefNo = request.POST.get('OutConveyanceRefNo')
#         OutTransportId = request.POST.get('OutTransportId')
#         OutFlightNO = request.POST.get('OutFlightNO')
#         OutAircraftRegNo = request.POST.get('OutAircraftRegNo')
#         OutMasterAirwayBill = request.POST.get('OutMasterAirwayBill')
#         TotalOuterPack = request.POST.get('TotalOuterPack')
#         TotalOuterPackUOM = request.POST.get('TotalOuterPackUOM')
#         TotalGrossWeight = request.POST.get('TotalGrossWeight')
#         TotalGrossWeightUOM = request.POST.get('TotalGrossWeightUOM')
#         GrossReference = request.POST.get('GrossReference')
#         TradeRemarks = request.POST.get('TradeRemarks')
#         InternalRemarks = request.POST.get('InternalRemarks')
#         DeclareIndicator = request.POST.get('DeclareIndicator')
#         NumberOfItems = request.POST.get('NumberOfItems')
#         TotalCIFFOBValue = request.POST.get('TotalCIFFOBValue')
#         TotalGSTTaxAmt = request.POST.get('TotalGSTTaxAmt')
#         TotalExDutyAmt = request.POST.get('TotalExDutyAmt')
#         TotalCusDutyAmt = request.POST.get('TotalCusDutyAmt')
#         TotalODutyAmt = request.POST.get('TotalODutyAmt')
#         TotalAmtPay = request.POST.get('TotalAmtPay')
#         Status = request.POST.get('Status')


#         TouchUser = request.session["Username"]
#         TouchTime = datetime.now()


#         PermitNumber = request.POST.get('PermitNumber')
#         prmtStatus = request.POST.get('prmtStatus')
#         ReleaseLocName = request.POST.get('ReleaseLocName')
#         RecepitLocName = request.POST.get('RecepitLocName')


#         Cnb = request.POST.get('Cnb')
#         DeclarningFor = request.POST.get('DeclarningFor')
#         INHAWB = request.POST.get('INHAWB')
#         outHAWB = request.POST.get('outHAWB')
#         MRDate = request.POST.get('MRDate')
#         MRTime = request.POST.get('MRTime')
#         CondColor = ""

        
        
#         # query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TranshipmentHeader'"
#         # self.cursor.execute(query)

#         # result = self.cursor.fetchall()
#         # for i in result:
#         #     print("%s",end=',')

#         values = (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,HandlingAgentCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,EndUserCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,RemovalStartDate,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocName,RecepitLocName,Cnb,DeclarningFor,INHAWB,outHAWB,MRDate,MRTime)
#         print(values)

#         self.cursor.execute("select * from TranshipmentHeader where PermitId = '{}' ".format(PermitId))
#         result = self.cursor.fetchall()
       
#         try:
#             if len(result)==0:
                
#                 Qry = "INSERT INTO TranshipmentHeader (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,HandlingAgentCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,EndUserCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,RemovalStartDate,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocName,RecepitLocName,Cnb,DeclarningFor,INHAWB,outHAWB,MRDate,MRTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#                 self.cursor.execute(Qry,values)
                
#                 self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(str(request.session['Username']).upper()))
#                 ManageUserVal = self.cursor.fetchone()
#                 AccountId = ManageUserVal[0]
#                 # self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{PermitId}','TNPDEC','{AccountId}','{MSGId}','{str(request.session['Username']).upper()}','{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')")
#                 self.cursor.execute("INSERT INTO PermitCount (PermitId, MessageType, AccountId, MsgId, TouchUser, TouchTime) VALUES ('{}', 'TNPDEC', '{}', '{}', '{}', '{}')".format(PermitId,AccountId,MSGId,str(request.session['Username']).upper(),datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#                 print('Updated values:', values)
#                 self.conn.commit()
#                 print("Saved New Record")
#             else:
#                 print("Its A update code")
#                 Qry=f"Update TranshipmentHeader set Refid=%s,JobId=%s,MSGId=%s,PermitId=%s,TradeNetMailboxID=%s,MessageType=%s,DeclarationType=%s,PreviousPermit=%s,CargoPackType=%s,InwardTransportMode=%s,OutwardTransportMode=%s,BGIndicator=%s,SupplyIndicator=%s,ReferenceDocuments=%s,License=%s,Recipient=%s,DeclarantCompanyCode=%s,ImporterCompanyCode=%s,HandlingAgentCode=%s,InwardCarrierAgentCode=%s,OutwardCarrierAgentCode=%s,FreightForwarderCode=%s,ClaimantPartyCode=%s,EndUserCode=%s,ArrivalDate=%s,LoadingPortCode=%s,VoyageNumber=%s,VesselName=%s,OceanBillofLadingNo=%s,ConveyanceRefNo=%s,TransportId=%s,FlightNO=%s,AircraftRegNo=%s,MasterAirwayBill=%s,ReleaseLocation=%s,RecepitLocation=%s,StorageLocation=%s,RemovalStartDate=%s,DepartureDate=%s,DischargePort=%s,FinalDestinationCountry=%s,OutVoyageNumber=%s,OutVesselName=%s,OutOceanBillofLadingNo=%s,VesselType=%s,VesselNetRegTon=%s,VesselNationality=%s,TowingVesselID=%s,TowingVesselName=%s,NextPort=%s,LastPort=%s,OutConveyanceRefNo=%s,OutTransportId=%s,OutFlightNO=%s,OutAircraftRegNo=%s,OutMasterAirwayBill=%s,TotalOuterPack=%s,TotalOuterPackUOM=%s,TotalGrossWeight=%s,TotalGrossWeightUOM=%s,GrossReference=%s,TradeRemarks=%s,InternalRemarks=%s,DeclareIndicator=%s,NumberOfItems=%s,TotalCIFFOBValue=%s,TotalGSTTaxAmt=%s,TotalExDutyAmt=%s,TotalCusDutyAmt=%s,TotalODutyAmt=%s,TotalAmtPay=%s,Status=%s,TouchUser=%s,TouchTime=%s,PermitNumber=%s,prmtStatus=%s,ReleaseLocName=%s,RecepitLocName=%s,Cnb=%s,DeclarningFor=%s,INHAWB=%s,outHAWB=%s,MRDate=%s,MRTime=%s WHERE PermitId = '{PermitId}'"
#                 self.cursor.execute(Qry,values)
#             print('Updated values:', values) 
#             self.conn.commit()
            

#         except Exception as e:
#             print("Its a Error Code ...",e)
#             return  JsonResponse({"message":"Failed"}) 
        
#         return  JsonResponse({"message":"Success"}) 
    




class TransSave(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
    

    def post(self, request):

        self.cursor.execute("DELETE FROM TranshipmentCPCDtl WHERE PermitId = '{}' ".format(request.POST.get('PermitId')))
        self.conn.commit()

        cpcData = json.loads(request.POST.get('cpcData1'))

        print("CPC Data to be saved:", cpcData) 

        cpcQry = "INSERT INTO TranshipmentCPCDtl(PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
       
       
        for i in cpcData:
            cpcVal = (request.POST.get("PermitId"),"TNPDEC",i[0],i[1],i[2],i[3],i[4],str(request.session['Username']).upper(),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.cursor.execute(cpcQry,cpcVal)
            print("Inserting:", cpcVal)

        data = {
            "Refid" : request.POST.get('Refid'),
            "JobId" : request.POST.get('JobId'),
            "MSGId" : request.POST.get('MSGId'),
            "PermitId" : request.POST.get('PermitId'),
            "TradeNetMailboxID" :request.POST.get('TradeNetMailboxID'),
            "MessageType" : request.POST.get('MessageType'),
            "DeclarationType" : request.POST.get('DeclarationType'),
            "PreviousPermit" : request.POST.get('PreviousPermit'),
            "CargoPackType" : request.POST.get('CargoPackType'),
            "InwardTransportMode" : request.POST.get('InwardTransportMode'),
            "OutwardTransportMode" : request.POST.get('OutwardTransportMode'),
            "BGIndicator" : request.POST.get('BGIndicator'),
            "SupplyIndicator" : request.POST.get('SupplyIndicator'),
            "ReferenceDocuments" : request.POST.get('ReferenceDocuments'),
            "License" : request.POST.get('License'),
            "Recipient" : request.POST.get('Recipient'),
            "DeclarantCompanyCode" : request.POST.get('DeclarantCompanyCode'),
            "ImporterCompanyCode": request.POST.get('ImporterCompanyCode'),
            "HandlingAgentCode" : request.POST.get('HandlingAgentCode'),
            "InwardCarrierAgentCode" : request.POST.get('InwardCarrierAgentCode'),
            "OutwardCarrierAgentCode" : request.POST.get('OutwardCarrierAgentCode'),
            "FreightForwarderCode" : request.POST.get('FreightForwarderCode'),
            "ClaimantPartyCode" : request.POST.get('ClaimantPartyCode'),
            "EndUserCode" : request.POST.get('EndUserCode'),
            "ArrivalDate" : request.POST.get('ArrivalDate'),
            "LoadingPortCode" : request.POST.get('LoadingPortCode'),
            "VoyageNumber" : request.POST.get('VoyageNumber'),
            "VesselName" : request.POST.get('VesselName'),
            "OceanBillofLadingNo" : request.POST.get('OceanBillofLadingNo'),
            "ConveyanceRefNo" : request.POST.get('ConveyanceRefNo'),
            "TransportId" : request.POST.get('TransportId'),
            "FlightNO" : request.POST.get('FlightNO'),
            "AircraftRegNo" : request.POST.get('AircraftRegNo'),
            "MasterAirwayBill" : request.POST.get('MasterAirwayBill'),
            "ReleaseLocation" : request.POST.get('ReleaseLocation'),
            "RecepitLocation" : request.POST.get('RecepitLocation'),
            "StorageLocation" : request.POST.get('StorageLocation'),
            "RemovalStartDate" : request.POST.get('RemovalStartDate'),
            "DepartureDate" : request.POST.get('DepartureDate'),
            "DischargePort" : request.POST.get('DischargePort'),
            "FinalDestinationCountry" : request.POST.get('FinalDestinationCountry'),
            "OutVoyageNumber" : request.POST.get('OutVoyageNumber'),
            "OutVesselName" : request.POST.get('OutVesselName'),
            "OutOceanBillofLadingNo" : request.POST.get('OutOceanBillofLadingNo'),
            "VesselType" : request.POST.get('VesselType'),
            "VesselNetRegTon" : request.POST.get('VesselNetRegTon'),
            "VesselNationality" : request.POST.get('VesselNationality'),
            "TowingVesselID" : request.POST.get('TowingVesselID'),
            "TowingVesselName" : request.POST.get('TowingVesselName'),
            "NextPort" : request.POST.get('NextPort'),
            "LastPort" : request.POST.get('LastPort'),
            "OutConveyanceRefNo" : request.POST.get('OutConveyanceRefNo'),
            "OutTransportId" : request.POST.get('OutTransportId'),
            "OutFlightNO" : request.POST.get('OutFlightNO'),
            "OutAircraftRegNo" : request.POST.get('OutAircraftRegNo'),
            "OutMasterAirwayBill" : request.POST.get('OutMasterAirwayBill'),
            "TotalOuterPack" : request.POST.get('TotalOuterPack'),
            "TotalOuterPackUOM" : request.POST.get('TotalOuterPackUOM'),
            "TotalGrossWeight" : request.POST.get('TotalGrossWeight'),
            "TotalGrossWeightUOM" : request.POST.get('TotalGrossWeightUOM'),
            "GrossReference" : request.POST.get('GrossReference'),
            "TradeRemarks" : request.POST.get('TradeRemarks'),
            "InternalRemarks" : request.POST.get('InternalRemarks'),
            "DeclareIndicator" : request.POST.get('DeclareIndicator'),
            "NumberOfItems" : request.POST.get('NumberOfItems'),
            "TotalCIFFOBValue" : request.POST.get('TotalCIFFOBValue'),
            "TotalGSTTaxAmt" : request.POST.get('TotalGSTTaxAmt'),
            "TotalExDutyAmt" : request.POST.get('TotalExDutyAmt'),
            "TotalCusDutyAmt" : request.POST.get('TotalCusDutyAmt'),
            "TotalODutyAmt" : request.POST.get('TotalODutyAmt'),
            "TotalAmtPay" : request.POST.get('TotalAmtPay'),
            "Status" : request.POST.get('Status'),
            "TouchUser" : request.session["Username"],
            "TouchTime" : datetime.now(),
            "PermitNumber" : request.POST.get('PermitNumber'),
            "prmtStatus" : request.POST.get('prmtStatus'),
            'ReleaseLocName' : request.POST.get('ReleaseLocName'),
            "RecepitLocName" : request.POST.get('RecepitLocName'),
            "Cnb" : request.POST.get('Cnb'),
            "DeclarningFor" : request.POST.get('DeclarningFor'),
            "INHAWB" : request.POST.get('INHAWB'),
            "outHAWB" : request.POST.get('outHAWB'),
            "MRDate" : request.POST.get('MRDate'),
            "MRTime" : request.POST.get('MRTime'),
            "CondColor" : ""
        }
      
        
        self.cursor.execute("SELECT * FROM TranshipmentHeader WHERE PermitId = '{}' AND MSGId = '{}' AND JobId = '{}' AND Refid = '{}'".format(request.POST.get("PermitId"), request.POST.get("MSGId"),request.POST.get("JobId"),request.POST.get("Refid")))

        result = self.cursor.fetchall()
        
 
        print("The Result Is : ",result)
        try:
            if result:
                columns = ', '.join([f'{key} = %s' for key in data.keys()])
                qry = "UPDATE TranshipmentHeader SET {} WHERE PermitId = '{}' AND MSGId = '{}' AND JobId = '{}' AND Refid = '{}'".format(columns,request.POST.get("PermitId"),request.POST.get("MSGId"),request.POST.get("JobId"),request.POST.get("Refid"))

                self.cursor.execute(qry, tuple(data.values()))
                self.conn.commit()
                print("Updated")
                return  JsonResponse({"message":"Success"}) 
            else:
                columns = ', '.join([f'[{key}]' for key in data.keys()])
                values = ', '.join(['%s' for _ in range(len(data))])
                insert_statement = f'INSERT INTO TranshipmentHeader ({columns}) VALUES ({values})'

                self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(str(request.session['Username']).upper()))
                ManageUserVal = self.cursor.fetchone()
                AccountId = ManageUserVal[0]

                self.cursor.execute("INSERT INTO PermitCount (PermitId, MessageType, AccountId, MsgId, TouchUser, TouchTime) VALUES ('{}', 'TNPDEC', '{}', '{}', '{}', '{}')".format(request.POST.get("PermitId"),AccountId,request.POST.get("MSGId"),str(request.session['Username']).upper(),datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self.cursor.execute(insert_statement, tuple(data.values()))
                self.conn.commit()
                
                return  JsonResponse({"message":"Success"}) 
        except:
            return  JsonResponse({"message":"Did not Saved"}) 


def Transmit(request):
    permitNumber1 = json.loads(request.GET.get("PermitNumber"))# this Records Select check boxes id's

    s = SqlDb('SecondDb')
    s1 = SqlDb('default')
    for ID in permitNumber1:
        s1.cursor.execute(f"SELECT * FROM TranshipmentHeader WHERE Id='{ID}' ") #this get selected permit id
        permitNumber = s1.cursor.fetchone()[4]
        TouchUser = str(request.session['Username']).upper() 
        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        s.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(TouchUser))
        ManageUserVal = s.cursor.fetchone()
        AccountId = ManageUserVal[0]
        MailId = ManageUserVal[1]

        s.cursor.execute("SELECT COUNT(*) + 1  FROM TranshipmentHeader WHERE MSGId LIKE '%{}%' AND MessageType = 'INPDEC' ".format(refDate))
        RefId = ("%03d" % s.cursor.fetchone()[0])

        s.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        JobIdCount = s.cursor.fetchone()[0]

        JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % JobIdCount}" 
        MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % JobIdCount}"
        NewPermitId = f"{TouchUser}{refDate}{RefId}"

        TouchTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        try:
            s1.cursor.execute(f"SELECT * FROM TranshipmentHeader WHERE PermitId='{permitNumber}' ")
            Heading = [i[0] for i in s1.cursor.description] #This only print for table headings (column names)
            HeadData = [dict(zip(Heading,row)) for row in s1.cursor.fetchall()]
            HeadQry = ("INSERT INTO TranshipmentHeader(Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,HandlingAgentCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,EndUserCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,RemovalStartDate,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocName,RecepitLocName,Cnb,DeclarningFor,INHAWB,outHAWB,MRDate,MRTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
            for head in HeadData:
                headVal = (RefId,JobId,MsgId,NewPermitId,MailId,head['MessageType'],head['DeclarationType'],head['PreviousPermit'],head['CargoPackType'],head['InwardTransportMode'],head['OutwardTransportMode'],head['BGIndicator'],head['SupplyIndicator'],head['ReferenceDocuments'],head['License'],head['Recipient'],head['DeclarantCompanyCode'],head['ImporterCompanyCode'],head['HandlingAgentCode'],head['InwardCarrierAgentCode'],head['OutwardCarrierAgentCode'],head['FreightForwarderCode'],head['ClaimantPartyCode'],head['EndUserCode'],head['ArrivalDate'],head['LoadingPortCode'],head['VoyageNumber'],head['VesselName'],head['OceanBillofLadingNo'],head['ConveyanceRefNo'],head['TransportId'],head['FlightNO'],head['AircraftRegNo'],head['MasterAirwayBill'],head['ReleaseLocation'],head['RecepitLocation'],head['StorageLocation'],head['RemovalStartDate'],head['DepartureDate'],head['DischargePort'],head['FinalDestinationCountry'],head['OutVoyageNumber'],head['OutVesselName'],head['OutOceanBillofLadingNo'],head['VesselType'],head['VesselNetRegTon'],head['VesselNationality'],head['TowingVesselID'],head['TowingVesselName'],head['NextPort'],head['LastPort'],head['OutConveyanceRefNo'],head['OutTransportId'],head['OutFlightNO'],head['OutAircraftRegNo'],head['OutMasterAirwayBill'],head['TotalOuterPack'],head['TotalOuterPackUOM'],head['TotalGrossWeight'],head['TotalGrossWeightUOM'],head['GrossReference'],head['TradeRemarks'],head['InternalRemarks'],head['DeclareIndicator'],head['NumberOfItems'],head['TotalCIFFOBValue'],head['TotalGSTTaxAmt'],head['TotalExDutyAmt'],head['TotalCusDutyAmt'],head['TotalODutyAmt'],head['TotalAmtPay'],head['Status'],TouchUser,TouchTime,head['PermitNumber'],head['prmtStatus'],head['ReleaseLocName'],head['RecepitLocName'],head['Cnb'],head['DeclarningFor'],head['INHAWB'],head['outHAWB'],head['MRDate'],head['MRTime'])
                s.cursor.execute(HeadQry,headVal)

            s.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{NewPermitId}','TNPDEC','{AccountId}','{MsgId}','{TouchUser}','{TouchTime}') ")

            ItemQry = "INSERT INTO TranshipmentItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,Vehicletype,Enginecapacity,Engineuom,Orginregdate,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,LSPValue,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM TranshipmentItemDtl WHERE PermitId='{permitNumber}' ")
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
 

 
class TranshipmentEdit(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request,id):

        print("The id is :",id)

        Username = request.session["Username"]
        self.cursor.execute(f"SELECT * FROM TranshipmentHeader WHERE id = {id}")
        headers = [i[0] for i in self.cursor.description]
        transAll = list(self.cursor.fetchall())

        for i in transAll:
            print("test ans :",i)
    
        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))

        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate, AccountId))

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"
            + Username
            + "'"
        )
        InNonHeadData = self.cursor.fetchone()
        context = {
            "UserName": Username,
            "PermitId": transAll[0][4],
            "JobId": transAll[0][2],
            "RefId": transAll[0][1],
            "MsgId": transAll[0][3],
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

        context.update({
            "OutData" : (pd.DataFrame(transAll, columns=headers)).to_dict("records"),
        })
        for item in context["OutData"]:
            print("Row:")
            for key, value in item.items():
                print(f"  {key}: {value}")
        return render(request, "Transhipment/Newpage.html", context)


class Transshow(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request,id):

        print("The id is :",id)

        Username = request.session["Username"]
        self.cursor.execute(f"SELECT * FROM TranshipmentHeader WHERE id = {id}")
        headers = [i[0] for i in self.cursor.description]
        transAll = list(self.cursor.fetchall())

        for i in transAll:
            print("test ans :",i)
    
        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))

        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate, AccountId))

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"
            + Username
            + "'"
        )
        InNonHeadData = self.cursor.fetchone()
        context = {
            "UserName": Username,
            "PermitId": transAll[0][4],
            "JobId": transAll[0][2],
            "RefId": transAll[0][1],
            "MsgId": transAll[0][3],
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

        context.update({
            "Show" : (pd.DataFrame(transAll, columns=headers)).to_dict("records"),
        })

        status = transAll[0][72]

        if status == 'REJ':
        
            msgid = transAll[0][3]  
            chkMailId = InNonHeadData[2]  

            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ErrorID as Code, 
                    ErrorDescription as Description 
                FROM TransRejectStatus 
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
            msgid = transAll[0][3]  
            chkMailId = InNonHeadData[2] 
        
            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ErrorID as Code, 
                    ErrorDescription as Description 
                FROM TransRejectStatus 
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
                    FROM transpmt 
                    WHERE permitnumber = %s 
                    ORDER BY Sno
                """, [transAll[0][75]])
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
        
            msgid = transAll[0][3]  
            chkMailId = InNonHeadData[2]  

            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ErrorCode  as Code, 
                    ErrorDescription+' '+ErrorTrace as Description 
                FROM TransErrorStatus 
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
        
            msgid = transAll[0][3]  
            chkMailId = InNonHeadData[2]  

            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ConditionCde  as Code, 
                    ConditionDes as Description 
                FROM TransCancelPermit 
                WHERE permitnumber = %s
                AND MsgID = %s 
                AND MailBoxId = %s  
                ORDER BY Sno
            """, [transAll[0][75],msgid, chkMailId])

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
        
            msgid = transAll[0][3]  
            chkMailId = InNonHeadData[2]  

            self.cursor.execute("""
                SELECT 
                    Sno as SNo, 
                    ConditionCode as Code, 
                    ConditionDescription as Description 
                FROM TransAMDPMT 
                 WHERE permitnumber = %s
                AND MsgID = %s 
                AND MailBoxId = %s  
                ORDER BY Sno
            """, [transAll[0][75],msgid, chkMailId])

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
        return render(request, "Transhipment/Newpage.html", context)



class TranshipmentCopy(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,id):
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TranshipmentCPCDtl'"
        self.cursor.execute(query)

        result = self.cursor.fetchall()
        for i in result:
            print(i[0],end=',')

        Username = request.session['Username'] 

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")


        self.cursor.execute(f"SELECT outHAWB  FROM TranshipmentHeader WHERE Id = '{id}' ")
        previous_out_hawb = self.cursor.fetchone()[0]

        print("Previous OutHAWB:", previous_out_hawb)

        self.cursor.execute(f"SELECT outHAWB FROM TranshipmentHeader WHERE Id = '{id}' ")
        current_out_hawb = self.cursor.fetchone()[0]
        
        print("Current OutHAWB:", current_out_hawb)

        if previous_out_hawb == current_out_hawb:
            print("outHAWB values are the same")
            message= 'DUPLICATE HAWB/HBL FOUND. PLEASE VERIFY AND PROCEED'
        else:
            print("outHAWB values are different")

        self.cursor.execute(f"SELECT PermitId FROM TranshipmentHeader WHERE Id = '{id}' ")

        CopyPermitId = self.cursor.fetchone()[0]


        self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        ManageUserVal = self.cursor.fetchone()
        AccountId = ManageUserVal[0]
        self.cursor.execute("SELECT COUNT(*) + 1  FROM TranshipmentHeader WHERE MSGId LIKE '%{}%' AND MessageType = 'TNPDEC' ".format(refDate))
        self.RefId = ("%03d" % self.cursor.fetchone()[0])

        self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         
        self.cursor.execute(f"INSERT INTO TranshipmentHeader (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,HandlingAgentCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,EndUserCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,RemovalStartDate,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocName,RecepitLocName,Cnb,DeclarningFor,INHAWB,outHAWB,MRDate,MRTime) SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{ManageUserVal[1]}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,HandlingAgentCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,EndUserCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,RemovalStartDate,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{Username}','{NowDate}','','COPY',ReleaseLocName,RecepitLocName,Cnb,'--Select--',INHAWB,outHAWB,MRDate,MRTime FROM TranshipmentHeader WHERE Id = '{id}'")

        self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','TNPDEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')") 
        
        self.cursor.execute(f"INSERT INTO TranshipmentItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,InMAWBOBL,OutHAWBOBL,OutMAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,DrpVehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,InMAWBOBL,OutHAWBOBL,OutMAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,'{Username}','{NowDate}',DrpVehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM TranshipmentItemDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO TCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId,Enduserdesc) SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,'{self.PermitIdInNon}',MessageType,'{Username}','{NowDate}',CASCId,Enduserdesc FROM TCASCDtl WHERE PermitId = '{CopyPermitId}'")
        
        self.cursor.execute(f"INSERT INTO TranshipmentContainerDtl (PermitId,RowNo,ContainerNo,Size,Weight,SealNo,MessageType,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}',RowNo,ContainerNo,Size,Weight,SealNo,MessageType,'{Username}','{NowDate}' FROM TranshipmentContainerDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO transhipfile (Sno,Name,ContentType,Data,DocumentType,TranshipId,TouchUser,TouchTime,PermitId,Size,Type) SELECT Sno,Name,ContentType,Data,DocumentType,TranshipId,'{Username}','{NowDate}','{self.PermitIdInNon}',Size,Type FROM transhipfile WHERE PermitId = '{CopyPermitId}' ")
        
        self.cursor.execute(f"INSERT INTO TranshipmentCPCDtl(PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}',MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,'{Username}','{NowDate}'  FROM TranshipmentCPCDtl WHERE PermitId = '{CopyPermitId}'")
        
        self.conn.commit()

       
        self.cursor.execute(f"SELECT Id FROM TranshipmentHeader WHERE PermitId = '{self.PermitIdInNon}' ")
        new_permit_id = self.cursor.fetchone()[0]
            
     
        return redirect(reverse('trans_edit', kwargs={'id': new_permit_id}) + '?message='+ message)

        # return render(request, "Transhipment/Newpage.html")



class TransMailTransmitData(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request):

        maiId = request.GET.get('mailId')

        self.cursor.execute("SELECT TOP 1 TouchUser FROM TranshipmentHeader WHERE TradeNetMailboxID = '{}' ".format(maiId))
       
       
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
            self.cursor.execute(f"SELECT PermitId FROM TranshipmentHeader WHERE Id = '{Id}'")
            CopyPermitId = self.cursor.fetchone()[0]
            print("copypermit:", CopyPermitId)


            self.cursor.execute("SELECT COUNT(*) + 1  FROM TranshipmentHeader WHERE MSGId LIKE '%{}%' AND MessageType = 'TNPDEC' ".format(refDate))
            self.RefId = ("%03d" % self.cursor.fetchone()[0])

            self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
            self.JobIdCount = self.cursor.fetchone()[0]

            self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
            self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
            self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"
            print("permit id:",self.PermitIdInNon)


            NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("nowdate:",NowDate)

            id = Id
            self.cursor.execute(f"INSERT INTO TranshipmentHeader (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,HandlingAgentCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,EndUserCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,RemovalStartDate,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ReleaseLocName,RecepitLocName,Cnb,DeclarningFor,INHAWB,outHAWB,MRDate,MRTime,CondColor,TransmitId) SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{ManageUserVal[1]}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,Recipient,DeclarantCompanyCode,ImporterCompanyCode,HandlingAgentCode,InwardCarrierAgentCode,OutwardCarrierAgentCode,FreightForwarderCode,ClaimantPartyCode,EndUserCode,ArrivalDate,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,RemovalStartDate,DepartureDate,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{Username}','{NowDate}','','NEW',ReleaseLocName,RecepitLocName,Cnb,'--Select--',INHAWB,outHAWB,MRDate,MRTime,CondColor,TransmitId FROM TranshipmentHeader WHERE Id = '{id}'")

            self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','TNPDEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')") 
            
            self.cursor.execute(f"INSERT INTO TranshipmentItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,InMAWBOBL,OutHAWBOBL,OutMAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,TouchUser,TouchTime,DrpVehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage) SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,DGIndicator,Contry,Brand,Model,InHAWBOBL,InMAWBOBL,OutHAWBOBL,OutMAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,'{Username}','{NowDate}',DrpVehicleType,Enginecapacity,Engineuom,Orginregdate,OptionalChrgeUOM,Optioncahrge,OptionalSumtotal,OptionalSumExchage FROM TranshipmentItemDtl WHERE PermitId = '{CopyPermitId}'")

            self.cursor.execute(f"INSERT INTO TCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId,Enduserdesc) SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,'{self.PermitIdInNon}',MessageType,'{Username}','{NowDate}',CASCId,Enduserdesc FROM TCASCDtl WHERE PermitId = '{CopyPermitId}'")
            
            self.cursor.execute(f"INSERT INTO TranshipmentContainerDtl (PermitId,RowNo,ContainerNo,Size,Weight,SealNo,MessageType,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}',RowNo,ContainerNo,Size,Weight,SealNo,MessageType,'{Username}','{NowDate}' FROM TranshipmentContainerDtl WHERE PermitId = '{CopyPermitId}'")

            self.cursor.execute(f"INSERT INTO transhipfile (Sno,Name,ContentType,Data,DocumentType,TranshipId,TouchUser,TouchTime,PermitId,Size,Type) SELECT Sno,Name,ContentType,Data,DocumentType,TranshipId,'{Username}','{NowDate}','{self.PermitIdInNon}',Size,Type FROM transhipfile WHERE PermitId = '{CopyPermitId}' ")
            
            self.cursor.execute(f"INSERT INTO TranshipmentCPCDtl(PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}',MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,'{Username}','{NowDate}'  FROM TranshipmentCPCDtl WHERE PermitId = '{CopyPermitId}'")
            
            self.conn.commit()

        
        return JsonResponse({"SUCCESS" : 'COPY ITEM'})



class TranshipListDelete(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,ID):
        print("The Id is  : ",ID)
        self.cursor.execute("UPDATE TranshipmentHeader SET STATUS = 'DEL' WHERE Id = '{}' ".format(ID))
        self.conn.commit()
        return JsonResponse({'message' : 'Deleted : '+ str(ID)})
    

    
class CpcFIlter(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
    def get(self,request,permitId):
        print('CpcFIlter:',permitId)
        self.cursor.execute(f"select * from TranshipmentCPCDtl Where PermitId = '{permitId}' ")
        headers = [i[0] for i in self.cursor.description]
        return JsonResponse({'cpc':(pd.DataFrame(list(self.cursor.fetchall()), columns=headers)).to_dict("records")})
    

