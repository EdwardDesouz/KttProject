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


def OutList(request):
    context = {}
    Username = request.session["Username"]
    context.update({"UserName": Username})
    return render(request, "Out/OutList.html", context)


class outListTable(View, SqlDb):
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
            "SELECT t1.Id as 'ID', t1.JobId as 'JOB ID', t1.MSGId as 'MSG ID',CONVERT(varchar, t1.TouchTime, 105) AS 'DEC DATE', SUBSTRING(t1.DeclarationType, 1, CHARINDEX(':', t1.DeclarationType) - 1) AS 'DEC TYPE', t1.TouchUser AS 'CREATE', t2.TradeNetMailboxID AS 'DEC ID', CONVERT(varchar, t1.DepartureDate, 105) AS ETD,t1.PermitNumber AS 'PERMIT NO',  t3.OutUserName + ' ' + t3.OutUserName1 AS 'EXPORTER',  STUFF((SELECT distinct(', ' + US.OutHAWBOBL) FROM OutItemDtl US   WHERE US.PermitId = t1.PermitId  FOR XML PATH('')), 1, 1, '') 'HAWB',CASE WHEN  t1.OutwardTransportMode = '4 : Air' THEN t1.OutMasterAirwayBill WHEN t1.OutwardTransportMode = '1 : Sea' THEN t1.OutOceanBillofLadingNo ELSE ''  END AS 'MAWB/OBL',t1.DischargePort as POD,CASE WHEN  t1.COType = '--Select--' THEN ''    WHEN t1.COType != '' THEN t1.COType ELSE ''  END as 'CO TYPE',CASE WHEN  t1.CerDetailtype1 = '--Select--' THEN '-' WHEN t1.CerDetailtype1 != ''  THEN t1.CerDetailtype1 ELSE ''  END as 'CERT TYPE',t1.CertificateNumber as 'CERT NO', t1.MessageType as 'MSG TYPE', t1.OutwardTransportMode as TPT,t1.PreviousPermit as 'PRE PMT',t1.GrossReference as 'X REF', t1.InternalRemarks as 'INT REM', t1.Status as 'STATUS' FROM OutHeaderTbl AS t1 INNER JOIN DeclarantCompany AS t2   ON t1.DeclarantCompanyCode = t2.Code  INNER JOIN OutExporter AS t3 ON t1.ExporterCompanyCode = t3.OutUserCode    INNER JOIN OutInvoiceDtl AS t5 ON t1.PermitId = t5.PermitId  INNER JOIN ManageUser AS t6 ON t6.UserId = t1.TouchUser  where t6.AccountId = '"
            + AccountId
            + "' and convert(varchar,t1.TouchTime,111)>='"
            + nowdata.strftime("%Y/%m/%d")
            + "' GROUP BY t1.Id, t1.JobId, t1.MSGId, t1.TouchTime, t1.TouchUser, t1.DeclarationType,  t1.DepartureDate, t1.PermitId,t1.PermitNumber,t1.PreviousPermit, t1.OutwardTransportMode, t1.OutMasterAirwayBill, t1.OutOceanBillofLadingNo, t1.DischargePort, t1.MessageType, t1.InwardTransportMode, t1.PreviousPermit,t1.COType,t1.CerDetailtype1,t1.CurrencyCode, t1.InternalRemarks,t1.CertificateNumber, t1.Status, t2.TradeNetMailboxID, t3.OutUserName, t3.OutUserName1,t6.AccountId,t2.DeclarantName,t1.InwardTransportMode, t1.ReleaseLocation,t1.RecepitLocation ,t1.DeclarningFor ,t1.InwardTransportMode,t1.License ,t1.GrossReference,t1.INHAWB, t1.DischargePort ,t1.MasterAirwayBill,t1.OceanBillofLadingNo order by t1.Id Desc"
        )  # t1.Status != 'DEL' AND

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
                    "HAWB",
                    "MAWBOBL",
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

        return JsonResponse(result, safe=False)


class OutNew(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request):
        Username = request.session["Username"]

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))

        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) + 1  FROM OutHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'OUTDEC' ".format(refDate))
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
            "DeclarationType": CommonMaster.objects.filter(TypeId=15, StatusId=1).order_by("Name"),
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
        return render(request, "Out/OutNew.html", context)


class OutParty(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT OutUserCode,OutUserName,OutUserName1,OutUserCRUEI,OutUserAddress,OutUserAddress1,OutUserCity,OutUserSubCode,OutUserSub,OutUserPostal,OutUserCountry FROM OutExporter WHERE Status = 'Active' "
        )
        self.Partycontext.update(
            {
                "exporter": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=[
                            "OutUserCode",
                            "OutUserName",
                            "OutUserName1",
                            "OutUserCRUEI",
                            "OutUserAddress",
                            "OutUserAddress1",
                            "OutUserCity",
                            "OutUserSubCode",
                            "OutUserSub",
                            "OutUserPostal",
                            "OutUserCountry",
                        ],
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)


class PartyLoad(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute(
            "SELECT Code,Name,Name1,CRUEI FROM OutImporter WHERE status = 'Active' ORDER BY Name "
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
            "SELECT Code,Name,Name1,CRUEI FROM InwardCarrierAgent WHERE status = 'Active' ORDER BY Name"
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
            "SELECT Code,Name,Name1,CRUEI FROM OutwardCarrierAgent WHERE status = 'Active' ORDER BY Name"
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
            "SELECT Code,Name,Name1,CRUEI FROM FreightForwarder WHERE status = 'Active' ORDER BY Name"
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
            "SELECT ConsigneeCode,ConsigneeName,ConsigneeName1,ConsigneeCRUEI,ConsigneeAddress,ConsigneeAddress1,ConsigneeCity,ConsigneeSub,ConsigneeSubDivi,ConsigneePostal,ConsigneeCountry FROM OutConsignee ORDER BY ConsigneeName"
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


class ParytManFacture(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}
        self.cursor.execute(
            "SELECT ManufacturerCode,ManufacturerName,ManufacturerName1,ManufacturerCRUEI,ManufacturerAddress,ManufacturerAddress1,ManufacturerCity,ManufacturerSubDivi,ManufacturerSub,ManufacturerPostal,ManufacturerCountry FROM OutManufacturer where Status = 'Active' "
        )
        self.Partycontext.update(
            {
                "manfacture": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()),
                        columns=[
                            "ManufacturerCode",
                            "ManufacturerName",
                            "ManufacturerName1",
                            "ManufacturerCRUEI",
                            "ManufacturerAddress",
                            "ManufacturerAddress1",
                            "ManufacturerCity",
                            "ManufacturerSubDivi",
                            "ManufacturerSub",
                            "ManufacturerPostal",
                            "ManufacturerCountry",
                        ],
                    )
                ).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)


class CargoLocations(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

        self.cursor.execute("SELECT Code,Description,LocationCode FROM ReleaseLocation order by Id")
        self.Partycontext.update(
            {
                "releaseLocation": (pd.DataFrame(list (self.cursor.fetchall()), columns=["Code", "Description","LocationCode"])).to_dict("records")
            }
        )

        self.cursor.execute("SELECT Code,Description,LocationCode FROM ReceiptLocation order by Id")
        self.Partycontext.update(
            {
                "reciptLocation": (
                    pd.DataFrame(
                        list(self.cursor.fetchall()), columns=["Code", "Description",'LocationCode']
                    )
                ).to_dict("records")
            }
        )

        self.cursor.execute("select * from LoadingPort")
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "loadingPort": (pd.DataFrame(list(self.cursor.fetchall()), columns=headers)).to_dict("records")
            }
        )

    def get(self, request):
        return JsonResponse(self.Partycontext)


class OutInvoice(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
        self.Partycontext = {}

    def get(self, request, Permit):
        self.cursor.execute(
            f"select * from OutInvoiceDtl WHERE PermitId = '{Permit}' ORDER BY SNo"
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "invoice": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        return JsonResponse(self.Partycontext)

    def post(self, request):
        SNo = request.POST.get("SNo")
        PermitId = request.POST.get("PermitId")
        message = ""
        if request.POST.get("method") == "DELETE":
            self.cursor.execute(
                "DELETE FROM OutInvoiceDtl WHERE PermitId = '{}' AND SNo = {}".format(
                    request.POST.get("PermitId"), request.POST.get("SNo")
                )
            )
            self.conn.commit()

            self.cursor.execute(
                "SELECT SNo ,PermitId FROM OutInvoiceDtl WHERE PermitId = '{}' ORDER BY SNo".format(
                    request.POST.get("PermitId")
                )
            )
            for ind in range(1, len(self.cursor.fetchall()) + 1):
                self.cursor.execute(
                    "UPDATE OutInvoiceDtl SET SNo = '{}' WHERE PermitId = '{}' ".format(
                        ind, request.POST.get("PermitId")
                    )
                )
            self.conn.commit()
        else:
            try:
                self.cursor.execute(
                    f"SELECT PermitId,SNo FROM OutInvoiceDtl WHERE PermitId = '{PermitId}' AND SNo = '{SNo}'"
                )
                if self.cursor.fetchone():
                    InvoiceUpd = f"UPDATE OutInvoiceDtl SET SNo = %s ,InvoiceNo = %s ,InvoiceDate = %s ,TermType = %s ,AdValoremIndicator = %s ,PreDutyRateIndicator = %s ,SupplierImporterRelationship = %s ,SupplierCode = %s ,ExportPartyCode = %s ,TICurrency = %s ,TIExRate = %s ,TIAmount = %s ,TISAmount = %s ,OTCCharge = %s ,OTCCurrency = %s ,OTCExRate = %s ,OTCAmount = %s ,OTCSAmount = %s ,FCCharge = %s ,FCCurrency = %s ,FCExRate = %s ,FCAmount = %s ,FCSAmount = %s ,ICCharge = %s ,ICCurrency = %s ,ICExRate = %s ,ICAmount = %s ,ICSAmount = %s ,CIFSUMAmount = %s ,GSTPercentage = %s ,GSTSUMAmount = %s ,MessageType = %s ,PermitId = %s ,TouchUser = %s ,TouchTime = %s WHERE PermitId = '{PermitId}' AND SNo = '{SNo}' "
                    InvoiceVal = (
                        request.POST.get("SNo"),
                        request.POST.get("InvoiceNo"),
                        request.POST.get("InvoiceDate"),
                        request.POST.get("TermType"),
                        request.POST.get("AdValoremIndicator"),
                        request.POST.get("PreDutyRateIndicator"),
                        request.POST.get("SupplierImporterRelationship"),
                        request.POST.get("SupplierCode"),
                        request.POST.get("ExportPartyCode"),
                        request.POST.get("TICurrency"),
                        request.POST.get("TIExRate"),
                        request.POST.get("TIAmount"),
                        request.POST.get("TISAmount"),
                        request.POST.get("OTCCharge"),
                        request.POST.get("OTCCurrency"),
                        request.POST.get("OTCExRate"),
                        request.POST.get("OTCAmount"),
                        request.POST.get("OTCSAmount"),
                        request.POST.get("FCCharge"),
                        request.POST.get("FCCurrency"),
                        request.POST.get("FCExRate"),
                        request.POST.get("FCAmount"),
                        request.POST.get("FCSAmount"),
                        request.POST.get("ICCharge"),
                        request.POST.get("ICCurrency"),
                        request.POST.get("ICExRate"),
                        request.POST.get("ICAmount"),
                        request.POST.get("ICSAmount"),
                        request.POST.get("CIFSUMAmount"),
                        request.POST.get("GSTPercentage"),
                        request.POST.get("GSTSUMAmount"),
                        request.POST.get("MessageType"),
                        request.POST.get("PermitId"),
                        str(request.session["Username"]).upper(),
                        request.POST.get("TouchTime"),
                    )
                    self.cursor.execute(InvoiceUpd, InvoiceVal)
                    message = "Successfully Inserted"
                else:
                    InvoiceData = "INSERT INTO OutInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ExportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    InvoiceVal = (
                        request.POST.get("SNo"),
                        request.POST.get("InvoiceNo"),
                        request.POST.get("InvoiceDate"),
                        request.POST.get("TermType"),
                        request.POST.get("AdValoremIndicator"),
                        request.POST.get("PreDutyRateIndicator"),
                        request.POST.get("SupplierImporterRelationship"),
                        request.POST.get("SupplierCode"),
                        request.POST.get("ExportPartyCode"),
                        request.POST.get("TICurrency"),
                        request.POST.get("TIExRate"),
                        request.POST.get("TIAmount"),
                        request.POST.get("TISAmount"),
                        request.POST.get("OTCCharge"),
                        request.POST.get("OTCCurrency"),
                        request.POST.get("OTCExRate"),
                        request.POST.get("OTCAmount"),
                        request.POST.get("OTCSAmount"),
                        request.POST.get("FCCharge"),
                        request.POST.get("FCCurrency"),
                        request.POST.get("FCExRate"),
                        request.POST.get("FCAmount"),
                        request.POST.get("FCSAmount"),
                        request.POST.get("ICCharge"),
                        request.POST.get("ICCurrency"),
                        request.POST.get("ICExRate"),
                        request.POST.get("ICAmount"),
                        request.POST.get("ICSAmount"),
                        request.POST.get("CIFSUMAmount"),
                        request.POST.get("GSTPercentage"),
                        request.POST.get("GSTSUMAmount"),
                        request.POST.get("MessageType"),
                        request.POST.get("PermitId"),
                        str(request.session["Username"]).upper(),
                        request.POST.get("TouchTime"),
                    )
                    self.cursor.execute(InvoiceData, InvoiceVal)
                    message = "Successfully Insertd"
                self.conn.commit()
            except:
                message = "Sorry Did not saved somthing error"

        self.cursor.execute(
            f"select * from OutInvoiceDtl WHERE PermitId = '{PermitId}' ORDER BY SNo"
        )
        headers = [i[0] for i in self.cursor.description]
        self.Partycontext.update(
            {
                "invoice": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records"),
                "message": message,
            }
        )
        return JsonResponse(self.Partycontext)


class OutItemInhouse(View, SqlDb):
    def get(self, request):
        SqlDb.__init__(self)
        context = {}
        self.cursor.execute("select * from InhouseItemCode where DeclType='OUT'")
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "inhouse": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )
        self.cursor.execute("select * from ChkHsCode")
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "ChkHsCode": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )

        self.cursor.execute("select * from Country")
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "country": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )

        return JsonResponse(context)


class OutHscode(View, SqlDb):
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


class OutItem(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request, Permit):
        context = {}

        self.cursor.execute(
            f"select * from OutCASCDtl WHERE PermitId = '{Permit}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "casc": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )

        self.cursor.execute(
            f"select * from OutItemDtl WHERE PermitId = '{Permit}' ORDER BY ItemNo"
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
        self.cursor.execute(
            f"DELETE FROM OutCASCDtl WHERE ItemNo = '{request.POST.get('ItemNo')}' AND PermitId = '{request.POST.get('PermitId')}'"
        )
        self.conn.commit()

        context = {}
        message = ""

        cascQry = "INSERT INTO OutCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId,EndUserDes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
            f"select * from OutCASCDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "casc": (pd.DataFrame(list(self.cursor.fetchall()), columns=headers)).to_dict("records")
            }
        )

        self.cursor.execute(
            f"SELECT ItemNo,PermitId FROM OutItemDtl WHERE ItemNo = '{request.POST.get('ItemNo')}' AND PermitId = '{request.POST.get('PermitId')}' "
        )
        if self.cursor.fetchone() is None:
            try:
                Qry = "INSERT INTO OutItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,EndUserDescription,Brand,Model,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,CerItemQty,CerItemUOM,CIFValOfCer,ManufactureCostDate,TexCat,TexQuotaQty,TexQuotaUOM,CerInvNo,CerInvDate,OriginOfCer,HSCodeCer,PerContent,CertificateDescription,TouchUser,TouchTime,VehicleType,OptionalChrgeUOM,EngineCapcity,Optioncahrge,OptionalSumtotal,OptionalSumExchage,EngineCapUOM,orignaldatereg) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (
                    request.POST.get("ItemNo"),
                    request.POST.get("PermitId"),
                    request.POST.get("MessageType"),
                    request.POST.get("HSCode"),
                    request.POST.get("Description"),
                    request.POST.get("DGIndicator"),
                    request.POST.get("Contry"),
                    request.POST.get("EndUserDescription"),
                    request.POST.get("Brand"),
                    request.POST.get("Model"),
                    request.POST.get("InHAWBOBL"),
                    request.POST.get("OutHAWBOBL"),
                    request.POST.get("DutiableQty"),
                    request.POST.get("DutiableUOM"),
                    request.POST.get("TotalDutiableQty"),
                    request.POST.get("TotalDutiableUOM"),
                    request.POST.get("InvoiceQuantity"),
                    request.POST.get("HSQty"),
                    request.POST.get("HSUOM"),
                    request.POST.get("AlcoholPer"),
                    request.POST.get("InvoiceNo"),
                    request.POST.get("ChkUnitPrice"),
                    request.POST.get("UnitPrice"),
                    request.POST.get("UnitPriceCurrency"),
                    request.POST.get("ExchangeRate"),
                    request.POST.get("SumExchangeRate"),
                    request.POST.get("TotalLineAmount"),
                    request.POST.get("InvoiceCharges"),
                    request.POST.get("CIFFOB"),
                    request.POST.get("OPQty"),
                    request.POST.get("OPUOM"),
                    request.POST.get("IPQty"),
                    request.POST.get("IPUOM"),
                    request.POST.get("InPqty"),
                    request.POST.get("InPUOM"),
                    request.POST.get("ImPQty"),
                    request.POST.get("ImPUOM"),
                    request.POST.get("PreferentialCode"),
                    request.POST.get("GSTRate"),
                    request.POST.get("GSTUOM"),
                    request.POST.get("GSTAmount"),
                    request.POST.get("ExciseDutyRate"),
                    request.POST.get("ExciseDutyUOM"),
                    request.POST.get("ExciseDutyAmount"),
                    request.POST.get("CustomsDutyRate"),
                    request.POST.get("CustomsDutyUOM"),
                    request.POST.get("CustomsDutyAmount"),
                    request.POST.get("OtherTaxRate"),
                    request.POST.get("OtherTaxUOM"),
                    request.POST.get("OtherTaxAmount"),
                    request.POST.get("CurrentLot"),
                    request.POST.get("PreviousLot"),
                    request.POST.get("Making"),
                    request.POST.get("ShippingMarks1"),
                    request.POST.get("ShippingMarks2"),
                    request.POST.get("ShippingMarks3"),
                    request.POST.get("ShippingMarks4"),
                    request.POST.get("CerItemQty"),
                    request.POST.get("CerItemUOM"),
                    request.POST.get("CIFValOfCer"),
                    request.POST.get("ManufactureCostDate"),
                    request.POST.get("TexCat"),
                    request.POST.get("TexQuotaQty"),
                    request.POST.get("TexQuotaUOM"),
                    request.POST.get("CerInvNo"),
                    request.POST.get("CerInvDate"),
                    request.POST.get("OriginOfCer"),
                    request.POST.get("HSCodeCer"),
                    request.POST.get("PerContent"),
                    request.POST.get("CertificateDescription"),
                    str(request.session["Username"]).upper(),
                    datetime.now(),
                    request.POST.get("VehicleType"),
                    request.POST.get("OptionalChrgeUOM"),
                    request.POST.get("EngineCapcity"),
                    request.POST.get("Optioncahrge"),
                    request.POST.get("OptionalSumtotal"),
                    request.POST.get("OptionalSumExchage"),
                    request.POST.get("EngineCapUOM"),
                    request.POST.get("orignaldatereg"),
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
                    request.POST.get("DGIndicator"),
                    request.POST.get("Contry"),
                    request.POST.get("EndUserDescription"),
                    request.POST.get("Brand"),
                    request.POST.get("Model"),
                    request.POST.get("InHAWBOBL"),
                    request.POST.get("OutHAWBOBL"),
                    request.POST.get("DutiableQty"),
                    request.POST.get("DutiableUOM"),
                    request.POST.get("TotalDutiableQty"),
                    request.POST.get("TotalDutiableUOM"),
                    request.POST.get("InvoiceQuantity"),
                    request.POST.get("HSQty"),
                    request.POST.get("HSUOM"),
                    request.POST.get("AlcoholPer"),
                    request.POST.get("InvoiceNo"),
                    request.POST.get("ChkUnitPrice"),
                    request.POST.get("UnitPrice"),
                    request.POST.get("UnitPriceCurrency"),
                    request.POST.get("ExchangeRate"),
                    request.POST.get("SumExchangeRate"),
                    request.POST.get("TotalLineAmount"),
                    request.POST.get("InvoiceCharges"),
                    request.POST.get("CIFFOB"),
                    request.POST.get("OPQty"),
                    request.POST.get("OPUOM"),
                    request.POST.get("IPQty"),
                    request.POST.get("IPUOM"),
                    request.POST.get("InPqty"),
                    request.POST.get("InPUOM"),
                    request.POST.get("ImPQty"),
                    request.POST.get("ImPUOM"),
                    request.POST.get("PreferentialCode"),
                    request.POST.get("GSTRate"),
                    request.POST.get("GSTUOM"),
                    request.POST.get("GSTAmount"),
                    request.POST.get("ExciseDutyRate"),
                    request.POST.get("ExciseDutyUOM"),
                    request.POST.get("ExciseDutyAmount"),
                    request.POST.get("CustomsDutyRate"),
                    request.POST.get("CustomsDutyUOM"),
                    request.POST.get("CustomsDutyAmount"),
                    request.POST.get("OtherTaxRate"),
                    request.POST.get("OtherTaxUOM"),
                    request.POST.get("OtherTaxAmount"),
                    request.POST.get("CurrentLot"),
                    request.POST.get("PreviousLot"),
                    request.POST.get("Making"),
                    request.POST.get("ShippingMarks1"),
                    request.POST.get("ShippingMarks2"),
                    request.POST.get("ShippingMarks3"),
                    request.POST.get("ShippingMarks4"),
                    request.POST.get("CerItemQty"),
                    request.POST.get("CerItemUOM"),
                    request.POST.get("CIFValOfCer"),
                    request.POST.get("ManufactureCostDate"),
                    request.POST.get("TexCat"),
                    request.POST.get("TexQuotaQty"),
                    request.POST.get("TexQuotaUOM"),
                    request.POST.get("CerInvNo"),
                    request.POST.get("CerInvDate"),
                    request.POST.get("OriginOfCer"),
                    request.POST.get("HSCodeCer"),
                    request.POST.get("PerContent"),
                    request.POST.get("CertificateDescription"),
                    str(request.session["Username"]).upper(),
                    datetime.now(),
                    request.POST.get("VehicleType"),
                    request.POST.get("OptionalChrgeUOM"),
                    request.POST.get("EngineCapcity"),
                    request.POST.get("Optioncahrge"),
                    request.POST.get("OptionalSumtotal"),
                    request.POST.get("OptionalSumExchage"),
                    request.POST.get("EngineCapUOM"),
                    request.POST.get("orignaldatereg"),
                )
                PermitId = request.POST.get("PermitId")
                ItemNo = request.POST.get("ItemNo")
                Qry = f"UPDATE OutItemDtl SET ItemNo = %s,PermitId = %s,MessageType = %s,HSCode = %s,Description = %s,DGIndicator = %s,Contry = %s,EndUserDescription = %s,Brand = %s,Model = %s,InHAWBOBL = %s,OutHAWBOBL = %s,DutiableQty = %s,DutiableUOM = %s,TotalDutiableQty = %s,TotalDutiableUOM = %s,InvoiceQuantity = %s,HSQty = %s,HSUOM = %s,AlcoholPer = %s,InvoiceNo = %s,ChkUnitPrice = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,InvoiceCharges = %s,CIFFOB = %s,OPQty = %s,OPUOM = %s,IPQty = %s,IPUOM = %s,InPqty = %s,InPUOM = %s,ImPQty = %s,ImPUOM = %s,PreferentialCode = %s,GSTRate = %s,GSTUOM = %s,GSTAmount = %s,ExciseDutyRate = %s,ExciseDutyUOM = %s,ExciseDutyAmount = %s,CustomsDutyRate = %s,CustomsDutyUOM = %s,CustomsDutyAmount = %s,OtherTaxRate = %s,OtherTaxUOM = %s,OtherTaxAmount = %s,CurrentLot = %s,PreviousLot = %s,Making = %s,ShippingMarks1 = %s,ShippingMarks2 = %s,ShippingMarks3 = %s,ShippingMarks4 = %s,CerItemQty = %s,CerItemUOM = %s,CIFValOfCer = %s,ManufactureCostDate = %s,TexCat = %s,TexQuotaQty = %s,TexQuotaUOM = %s,CerInvNo = %s,CerInvDate = %s,OriginOfCer = %s,HSCodeCer = %s,PerContent = %s,CertificateDescription = %s,TouchUser = %s,TouchTime = %s,VehicleType = %s,OptionalChrgeUOM = %s,EngineCapcity = %s,Optioncahrge = %s,OptionalSumtotal = %s,OptionalSumExchage = %s,EngineCapUOM = %s,orignaldatereg = %s WHERE PermitId = '{PermitId}' AND ItemNo = '{ItemNo}'  "
                self.cursor.execute(Qry, Val)
                message = "Updated Successfully...!"
            except Exception as e:
                message = "Did not Updated"
        self.conn.commit()

        context.update({"message": message})

        self.cursor.execute(
            f"select * from OutItemDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
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


def outItemDelete(request):
    data = json.loads(request.POST.get("Ids"))
    db = SqlDb()
    try:
        db.cursor.execute("DELETE FROM OutItemDtl WHERE Id ")
    except:pass

    ItemValue = json.loads(request.POST.get("Ids"))

    values_str = ", ".join(map(str, ItemValue))

    query1 = f"DELETE FROM OutItemDtl WHERE ItemNo IN ({values_str}) AND PermitId = '{request.POST.get('PermitId')}' "
    db.cursor.execute(query1)

    query2 = f"DELETE FROM OutCASCDtl WHERE ItemNo IN ({values_str}) AND PermitId = '{request.POST.get('PermitId')}' "
    db.cursor.execute(query2)

    db.conn.commit()

    db.cursor.execute(
        "SELECT ItemNo,PermitId FROM OutItemDtl WHERE PermitId = '{}' ORDER BY ItemNo".format(
            request.POST.get("PermitId")
        )
    )

    Ic = 1
    for itm in db.cursor.fetchall():
        db.cursor.execute(
            "UPDATE OutItemDtl SET ItemNo = '{}' WHERE PermitId = '{}' AND  ItemNo = '{}' ".format(
                Ic, request.POST.get("PermitId"), itm[0]
            )
        )
        db.cursor.execute(
            "UPDATE OutCASCDtl SET ItemNo = '{}' WHERE PermitId = '{}' AND  ItemNo = '{}' ".format(
                Ic, request.POST.get("PermitId"), itm[0]
            )
        )
        Ic += 1

    db.conn.commit()

    context = {}
    db.cursor.execute(
        f"select * from OutCASCDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
    )
    headers = [i[0] for i in db.cursor.description]
    context.update(
        {
            "casc": (pd.DataFrame(list(db.cursor.fetchall()), columns=headers)).to_dict(
                "records"
            )
        }
    )

    db.cursor.execute(
        f"select * from OutItemDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
    )
    headers = [i[0] for i in db.cursor.description]
    context.update(
        {
            "item": (pd.DataFrame(list(db.cursor.fetchall()), columns=headers)).to_dict(
                "records"
            )
        }
    )
    return JsonResponse(context)


class AttachDocument(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self, request):
        if request.GET.get("Method") == "DELETE":
            self.cursor.execute(
                "DELETE FROM OutFile WHERE Id = '{}' ".format(request.GET.get("Data"))
            )
        elif request.GET.get("Method") == "ALLDELETE":
            self.cursor.execute(
                "DELETE FROM OutFile WHERE PermitId = '{}' AND Type = 'NEW' ".format(
                    request.GET.get("PermitId")
                )
            )

        self.conn.commit()

        self.cursor.execute(
            f"SELECT Id,Sno,Name,ContentType,DocumentType,Size,PermitId,Type FROM OutFile where PermitId = '{request.GET.get('PermitId')}' AND Type = '{request.GET.get('Type')}' Order By Sno "
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
            }
        )

    def post(self, request):
        Result = ""
        try:
            self.cursor.execute(
                "SELECT COUNT(PermitId) AS MaxItem FROM OutFile  where PermitId='"
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
            Qry = "INSERT INTO OutFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
            f"SELECT Id,Sno,Name,ContentType,DocumentType,Size,PermitId,Type FROM OutFile where PermitId = '{request.POST.get('PermitId')}' AND Type = '{request.POST.get('Type')}'  Order By Sno "
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
                    f"select RowNo , PermitId from OutContainerDtl where RowNo = '{request.POST.get('RowNo')}' AND PermitId = '{request.POST.get('PermitId')}'"
                )
                result = self.cursor.fetchall()
                if not (result):
                    self.cursor.execute(
                        f"INSERT INTO OutContainerDtl (PermitId, RowNo,ContainerNo, size, weight,SealNo, MessageType,TouchUser,TouchTime) VALUES ('{request.POST.get('PermitId')}','{request.POST.get('RowNo')}','{request.POST.get('ContainerNo')}','{request.POST.get('size')}','{request.POST.get('weight')}','{request.POST.get('SealNo')}','{request.POST.get('MessageType')}','{str(request.session['Username']).upper()}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')"
                    )
                    self.conn.commit()
                    Result = "Saved SuccessFully....!"
                else:
                    self.cursor.execute(
                        f"Update OutContainerDtl set ContainerNo = '{request.POST.get('ContainerNo')}',size = '{request.POST.get('size')}',weight =  '{request.POST.get('weight')}',SealNo = '{request.POST.get('SealNo')}',MessageType = '{request.POST.get('MessageType')}',TouchUser = '{str(request.session['Username']).upper()}',TouchTime = '{datetime.now()}' where RowNo = '{request.POST.get('RowNo')}' AND PermitId = '{request.POST.get('PermitId')}'"
                    )
                    self.conn.commit()
                    Result = "Update SuccessFully....!"

            elif request.POST.get("Method") == "DELETE":
                self.cursor.execute(
                    f"DELETE FROM OutContainerDtl where PermitId = '{request.POST.get('PermitId')}' AND RowNo = '{request.POST.get('SNo')}' "
                )
                self.conn.commit()

                self.cursor.execute(
                    f"select * from OutContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
                )
                c = 1
                for j in self.cursor.fetchall():
                    self.cursor.execute(
                        f"UPDATE OutContainerDtl SET RowNo = {c} WHERE PermitId = '{j[1]}' AND RowNo = '{j[2]}'"
                    )
                    c += 1
                self.conn.commit()
                Result = "Deleted SuccessFully....!"

            elif request.POST.get("Method") == "CHECKDELETE":
                for ids in json.loads(request.POST.get("IDS")):
                    self.cursor.execute(f"DELETE FROM OutContainerDtl where id = {ids}")
                self.conn.commit()

                self.cursor.execute(
                    f"select * from OutContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
                )
                c = 1
                for j in self.cursor.fetchall():
                    self.cursor.execute(
                        f"UPDATE OutContainerDtl SET RowNo = {c} WHERE PermitId = '{j[1]}' AND RowNo = '{j[2]}'"
                    )
                    c += 1
                self.conn.commit()
                Result = "Deleted SuccessFully....!"

            elif request.POST.get("Method") == "LOAD":
                pass
        except Exception as e:
            Result = "Somthing Error"

        self.cursor.execute(
            f"select * from OutContainerDtl where PermitId = '{request.POST.get('PermitId')}' Order By RowNo "
        )
        return JsonResponse(
            {"ContainerValue": list(self.cursor.fetchall()), "Result": Result}
        )

    def get(self, request):
        SqlDb.__init__(self)
        self.cursor.execute(
            f"select * from OutContainerDtl where PermitId = '{request.GET.get('PermitId')}' Order By RowNo"
        )
        return JsonResponse({"ContainerValue": list(self.cursor.fetchall())})


class outSaveSubmit(View, SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def post(self, request):

        self.cursor.execute(f"DELETE FROM OutCPCDtl WHERE PermitId = '{request.POST.get("PermitId")}'")
        self.conn.commit()

        cpcData = json.loads(request.POST.get('cpcData1'))
        cpcQry = "INSERT INTO OutCPCDtl(PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for i in cpcData:
            cpcVal = (request.POST.get("PermitId"),"OUTDEC",i[0],i[1],i[2],i[3],i[4],str(request.session['Username']).upper(),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.cursor.execute(cpcQry,cpcVal)

        data = {
            "Refid": request.POST.get("Refid"),
            "JobId": request.POST.get("JobId"),
            "MSGId": request.POST.get("MSGId"),
            "PermitId": request.POST.get("PermitId"),
            "TradeNetMailboxID": request.POST.get("TradeNetMailboxID"),
            "MessageType": request.POST.get("MessageType"),
            "DeclarationType": request.POST.get("DeclarationType"),
            "PreviousPermit": request.POST.get("PreviousPermit"),
            "CargoPackType": request.POST.get("CargoPackType"),
            "InwardTransportMode": request.POST.get("InwardTransportMode"),
            "OutwardTransportMode": request.POST.get("OutwardTransportMode"),
            "BGIndicator": request.POST.get("BGIndicator"),
            "SupplyIndicator": request.POST.get("SupplyIndicator"),
            "ReferenceDocuments": request.POST.get("ReferenceDocuments"),
            "License": request.POST.get("License"),
            "COType": request.POST.get("COType"),
            "Entryyear": request.POST.get("Entryyear"),
            "GSPDonorCountry": request.POST.get("GSPDonorCountry"),
            "CerDetailtype1": request.POST.get("CerDetailtype1"),
            "CerDetailCopies1": request.POST.get("CerDetailCopies1"),
            "CerDetailtype2": request.POST.get("CerDetailtype2"),
            "CerDetailCopies2": request.POST.get("CerDetailCopies2"),
            "PerCommon": request.POST.get("PerCommon"),
            "CurrencyCode": request.POST.get("CurrencyCode"),
            "AddCerDtl": request.POST.get("AddCerDtl"),
            "TransDtl": request.POST.get("TransDtl"),
            "Recipient": request.POST.get("Recipient"),
            "DeclarantCompanyCode": request.POST.get("DeclarantCompanyCode"),
            "ExporterCompanyCode": request.POST.get("ExporterCompanyCode"),
            "Inwardcarriercode": request.POST.get("Inwardcarriercode"),
            "OutwardCarrierAgentCode": request.POST.get("OutwardCarrierAgentCode"),
            "FreightForwarderCode": request.POST.get("FreightForwarderCode"),
            "ImporterCompanyCode": request.POST.get("ImporterCompanyCode"),
            "InwardCarrierAgentCode": request.POST.get("InwardCarrierAgentCode"),
            "CONSIGNEECode": request.POST.get("CONSIGNEECode"),
            "EndUserCode": request.POST.get("EndUserCode"),
            "Manufacturer": request.POST.get("Manufacturer"),
            "ArrivalDate": request.POST.get("ArrivalDate"),
            "ArrivalTime": request.POST.get("ArrivalTime"),
            "LoadingPortCode": request.POST.get("LoadingPortCode"),
            "VoyageNumber": request.POST.get("VoyageNumber"),
            "VesselName": request.POST.get("VesselName"),
            "OceanBillofLadingNo": request.POST.get("OceanBillofLadingNo"),
            "ConveyanceRefNo": request.POST.get("ConveyanceRefNo"),
            "TransportId": request.POST.get("TransportId"),
            "FlightNO": request.POST.get("FlightNO"),
            "AircraftRegNo": request.POST.get("AircraftRegNo"),
            "MasterAirwayBill": request.POST.get("MasterAirwayBill"),
            "ReleaseLocation": request.POST.get("ReleaseLocation"),
            "RecepitLocation": request.POST.get("RecepitLocation"),
            "StorageLocation": request.POST.get("StorageLocation"),
            "BlanketStartDate": request.POST.get("BlanketStartDate"),
            "DepartureDate": request.POST.get("DepartureDate"),
            "DepartureTime": request.POST.get("DepartureTime"),
            "DischargePort": request.POST.get("DischargePort"),
            "FinalDestinationCountry": request.POST.get("FinalDestinationCountry"),
            "OutVoyageNumber": request.POST.get("OutVoyageNumber"),
            "OutVesselName": request.POST.get("OutVesselName"),
            "OutOceanBillofLadingNo": request.POST.get("OutOceanBillofLadingNo"),
            "VesselType": request.POST.get("VesselType"),
            "VesselNetRegTon": request.POST.get("VesselNetRegTon"),
            "VesselNationality": request.POST.get("VesselNationality"),
            "TowingVesselID": request.POST.get("TowingVesselID"),
            "TowingVesselName": request.POST.get("TowingVesselName"),
            "NextPort": request.POST.get("NextPort"),
            "LastPort": request.POST.get("LastPort"),
            "OutConveyanceRefNo": request.POST.get("OutConveyanceRefNo"),
            "OutTransportId": request.POST.get("OutTransportId"),
            "OutFlightNO": request.POST.get("OutFlightNO"),
            "OutAircraftRegNo": request.POST.get("OutAircraftRegNo"),
            "OutMasterAirwayBill": request.POST.get("OutMasterAirwayBill"),
            "TotalOuterPack": request.POST.get("TotalOuterPack"),
            "TotalOuterPackUOM": request.POST.get("TotalOuterPackUOM"),
            "TotalGrossWeight": request.POST.get("TotalGrossWeight"),
            "TotalGrossWeightUOM": request.POST.get("TotalGrossWeightUOM"),
            "GrossReference": request.POST.get("GrossReference"),
            "TradeRemarks": request.POST.get("TradeRemarks"),
            "InternalRemarks": request.POST.get("InternalRemarks"),
            "DeclareIndicator": "True",
            "NumberOfItems": request.POST.get("NumberOfItems"),
            "TotalCIFFOBValue": request.POST.get("TotalCIFFOBValue"),
            "TotalGSTTaxAmt": request.POST.get("TotalGSTTaxAmt"),
            "TotalExDutyAmt": request.POST.get("TotalExDutyAmt"),
            "TotalCusDutyAmt": request.POST.get("TotalCusDutyAmt"),
            "TotalODutyAmt": request.POST.get("TotalODutyAmt"),
            "TotalAmtPay": request.POST.get("TotalAmtPay"),
            "Status": "NEW",
            "TouchUser": str(request.session['Username']).upper(),
            "TouchTime": datetime.now(),
            "PermitNumber": '',
            "prmtStatus": 'NEW',
            "ResLoaName": request.POST.get("ResLoaName"),
            "RepLocName": request.POST.get("RepLocName"),
            "RecepitLocName": request.POST.get("RecepitLocName"),
            "outHAWB": request.POST.get("outHAWB"),
            "INHAWB": request.POST.get("INHAWB"),
            "CertificateNumber": request.POST.get("CertificateNumber"),
            "Defrentprinting": request.POST.get("Defrentprinting"),
            "Cnb": request.POST.get("Cnb"),
            "DeclarningFor": request.POST.get("DeclarningFor"),
            "MRDate": request.POST.get("MRDate"),
            "MRTime": request.POST.get("MRTime"),
        }
        self.cursor.execute(f"SELECT * FROM OutHeaderTbl WHERE PermitId = '{request.POST.get("PermitId")}' AND  MSGId = '{ request.POST.get("MSGId")}' AND JobId = '{request.POST.get("JobId")}' AND Refid = '{request.POST.get("Refid")}' ")
        result = self.cursor.fetchall()
        print("The Result Is : ",result)
        try:
            if result:
                columns = ', '.join([f'{key} = %s' for key in data.keys()])
                
                qry = f"UPDATE OutHeaderTbl SET {columns} WHERE PermitId = '{request.POST.get("PermitId")}' AND  MSGId = '{ request.POST.get("MSGId")}' AND JobId = '{request.POST.get("JobId")}' AND Refid = '{request.POST.get("Refid")}'"
                self.cursor.execute(qry, tuple(data.values()))
                self.conn.commit()
                print("Updated")
                return  JsonResponse({"message":"Success"}) 
            else:
                columns = ', '.join([f'[{key}]' for key in data.keys()])
                values = ', '.join(['%s' for _ in range(len(data))])
                insert_statement = f'INSERT INTO OutHeaderTbl ({columns}) VALUES ({values})'

                self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(str(request.session['Username']).upper()))
                ManageUserVal = self.cursor.fetchone()
                AccountId = ManageUserVal[0]

                # Execute the INSERT statement
                self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{request.POST.get("PermitId")}','OUTDEC','{AccountId}','{request.POST.get("MSGId")}','{str(request.session['Username']).upper()}','{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')")
                self.cursor.execute(insert_statement, tuple(data.values()))
                self.conn.commit()
                return  JsonResponse({"message":"Success"}) 
        except:
            return  JsonResponse({"message":"Did not Saved"}) 


class CopyOutPayment(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)

    def get(self,request,id):
        query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'OutCPCDtl'"
        self.cursor.execute(query)
            
        result = self.cursor.fetchall()
        for i in result:
            print(i[0],end=',')

        Username = request.session['Username'] 

        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute(f"SELECT PermitId FROM OutHeaderTbl WHERE Id = '{id}' ")

        CopyPermitId = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(Username))
        ManageUserVal = self.cursor.fetchone()
        AccountId = ManageUserVal[0]
        self.cursor.execute("SELECT COUNT(*) + 1  FROM OutHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'OUTDEC' ".format(refDate))
        self.RefId = ("%03d" % self.cursor.fetchone()[0])

        self.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        self.JobIdCount = self.cursor.fetchone()[0]

        self.JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % self.JobIdCount}" 
        self.MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % self.JobIdCount}"
        self.PermitIdInNon = f"{Username}{refDate}{self.RefId}"

        NowDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.cursor.execute(f"INSERT INTO OutHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,COType,Entryyear,GSPDonorCountry,CerDetailtype1,CerDetailCopies1,CerDetailtype2,CerDetailCopies2,PerCommon,CurrencyCode,AddCerDtl,TransDtl,Recipient,DeclarantCompanyCode,ExporterCompanyCode,Inwardcarriercode,OutwardCarrierAgentCode,FreightForwarderCode,ImporterCompanyCode,InwardCarrierAgentCode,CONSIGNEECode,EndUserCode,Manufacturer,ArrivalDate,ArrivalTime,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,BlanketStartDate,DepartureDate,DepartureTime,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ResLoaName,RepLocName,RecepitLocName,outHAWB,INHAWB,CertificateNumber,Defrentprinting,Cnb,DeclarningFor,MRDate,MRTime,CondColor) SELECT '{self.RefId}','{self.JobId}','{self.MsgId}','{self.PermitIdInNon}','{ManageUserVal[1]}',MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,COType,Entryyear,GSPDonorCountry,CerDetailtype1,CerDetailCopies1,CerDetailtype2,CerDetailCopies2,PerCommon,CurrencyCode,AddCerDtl,TransDtl,Recipient,DeclarantCompanyCode,ExporterCompanyCode,Inwardcarriercode,OutwardCarrierAgentCode,FreightForwarderCode,ImporterCompanyCode,InwardCarrierAgentCode,CONSIGNEECode,EndUserCode,Manufacturer,ArrivalDate,ArrivalTime,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,BlanketStartDate,DepartureDate,DepartureTime,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,'DRF','{Username}','{NowDate}','','COPY',ResLoaName,RepLocName,RecepitLocName,outHAWB,INHAWB,CertificateNumber,Defrentprinting,Cnb,'--Select--',MRDate,MRTime,CondColor FROM OutHeaderTbl WHERE Id = '{id}'")

        self.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{self.PermitIdInNon}','OUTDEC','{AccountId}','{self.MsgId}','{Username}','{NowDate}')")

        self.cursor.execute(f"INSERT INTO OutInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ExportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) SELECT SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ExportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,'{self.PermitIdInNon}','{Username}','{NowDate}' FROM OutInvoiceDtl WHERE PermitId = '{CopyPermitId}' ") 
        
        self.cursor.execute(f"INSERT INTO OutItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,EndUserDescription,Brand,Model,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,CerItemQty,CerItemUOM,CIFValOfCer,ManufactureCostDate,TexCat,TexQuotaQty,TexQuotaUOM,CerInvNo,CerInvDate,OriginOfCer,HSCodeCer,PerContent,CertificateDescription,TouchUser,TouchTime,VehicleType,OptionalChrgeUOM,EngineCapcity,Optioncahrge,OptionalSumtotal,OptionalSumExchage,EngineCapUOM,orignaldatereg) SELECT ItemNo,'{self.PermitIdInNon}',MessageType,HSCode,Description,DGIndicator,Contry,EndUserDescription,Brand,Model,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,CerItemQty,CerItemUOM,CIFValOfCer,ManufactureCostDate,TexCat,TexQuotaQty,TexQuotaUOM,CerInvNo,CerInvDate,OriginOfCer,HSCodeCer,PerContent,CertificateDescription,'{Username}','{NowDate}',VehicleType,OptionalChrgeUOM,EngineCapcity,Optioncahrge,OptionalSumtotal,OptionalSumExchage,EngineCapUOM,orignaldatereg FROM OutItemDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO OutCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId,EndUserDes) SELECT ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,'{self.PermitIdInNon}',MessageType,'{Username}','{NowDate}',CASCId,EndUserDes FROM OutCASCDtl WHERE PermitId = '{CopyPermitId}'")
        
        self.cursor.execute(f"INSERT INTO OutContainerDtl (PermitId,RowNo,ContainerNo,Size,Weight,SealNo,MessageType,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}',RowNo,ContainerNo,Size,Weight,SealNo,MessageType,'{Username}','{NowDate}' FROM OutContainerDtl WHERE PermitId = '{CopyPermitId}'")

        self.cursor.execute(f"INSERT INTO OutFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) SELECT Sno,Name,ContentType,Data,DocumentType,InPaymentId,'{Username}','{NowDate}',Size,'{self.PermitIdInNon}',Type FROM OutFile WHERE PermitId = '{CopyPermitId}' ")
        
        self.cursor.execute(f"INSERT INTO OutCPCDtl(PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) SELECT '{self.PermitIdInNon}',MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,'{Username}','{NowDate}'  FROM OutCPCDtl WHERE PermitId = '{CopyPermitId}'")
        
        self.conn.commit()

        self.cursor.execute(f"SELECT Id FROM OutHeaderTbl WHERE PermitId = '{self.PermitIdInNon}' ")
        
        return redirect('/outEdit/'+str(self.cursor.fetchone()[0])+'/')


class OutEdit(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)


    def get(self, request,id):
        Username = request.session["Username"]

        self.cursor.execute(f"SELECT * FROM OutHeaderTbl WHERE id = {id}")
        headers = [i[0] for i in self.cursor.description]
        outAll = list(self.cursor.fetchall())

        self.cursor.execute("SELECT AccountId FROM ManageUser WHERE UserName = '{}' ".format(Username))

        AccountId = self.cursor.fetchone()[0]

        self.cursor.execute("select Top 1 manageuser.LoginStatus,manageuser.DateLastUpdated,manageuser.MailBoxId,manageuser.SeqPool,SequencePool.StartSequence,DeclarantCompany.TradeNetMailboxID,DeclarantCompany.DeclarantName,DeclarantCompany.DeclarantCode,DeclarantCompany.DeclarantTel,DeclarantCompany.CRUEI,DeclarantCompany.Code,DeclarantCompany.name,DeclarantCompany.name1 from manageuser inner join SequencePool on manageuser.SeqPool=SequencePool.Description inner join DeclarantCompany on DeclarantCompany.TradeNetMailboxID=ManageUser.MailBoxId where ManageUser.UserId='"+ Username+ "'")
        InNonHeadData = self.cursor.fetchone()
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
            "DeclarationType": CommonMaster.objects.filter(TypeId=15, StatusId=1).order_by("Name"),
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
            "OutData" : (pd.DataFrame(outAll, columns=headers)).to_dict("records"),
        })
        return render(request, "Out/OutNew.html", context)


def ItemExcelDownload(request):
    response = HttpResponse(
        open(
            "D:\\New folder\\NNR REPORT FILE\\OUT & COO Type Changes\\RET\\RET\\ExcelTemplate\\OutExcelTemplate.xlsx",
            "rb",
        ).read()
    )
    response["Content-Type"] = "text/csv"
    response["Content-Disposition"] = f"attachment; filename=OutExcelTemplate.xlsx"
    return response  


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

        ItemColumns ={
            'CountryofOrigin' : '' ,
            'HSCode' : '' ,
            'HSQty' : '0.00' ,
            'TotalLineAmount' : '0.00' ,
            'ItemCode' : '' ,
            'Description' : '' ,
            'DGIndicator' : 'False' ,
            'Brand' : '' ,
            'Model' : '' ,
            'InHAWBOBL' : '' ,
            'OutHAWBOBL' : '' ,
            'HSUOM' : '--Select--' ,
            'InvoiceNumber' : '' ,
            'ItemCurrency' : '--Select--' ,
            'UnitPrice' : '0.00' ,
            'TotalDutiableQty' : '0.00' ,
            'TotalDutiableUOM' : '--Select--' ,
            'DutiableQty' : '0.00' ,
            'DutiableUOM' : '--Select--' ,
            'OuterPackQty' : '0.00' ,
            'OuterPackUOM' : '--Select--' ,
            'InPackQty' : '0.00' ,
            'InPackUOM' : '--Select--' ,
            'InnerPackQty' : '0.00' ,
            'InnerPackUOM' : '--Select--' ,
            'InmostPackQty' : '0.00' ,
            'InmostPackUOM' : '--Select--' ,
            'TarrifPreferentialCode' : '--Select--' ,
            'OtherTaxRate' : '0.00' ,
            'OtherTaxUOM' : '--Select--' ,
            'OtherTaxAmount' : '0.00' ,
            'CurrentLot' : '' ,
            'PreviousLot' : '' ,
            'AlcoholPercentage' : '0.00' ,
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
            'VehicleType' : '--Select--' ,
            'OptionalChrgeUOM' : '--Select--' ,
            'EngineCapcity' : '0.00' ,
            'Optioncahrge' : '0.00' ,
            'OptionalSumtotal' : '0.00' ,
            'OptionalSumExchange' : '0.00' ,
            'EngineCapUOM' : '--Select--' ,
            'originaldatereg' : '' ,
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

        self.cursor.execute(f"SELECT max(ItemNo) PermitId FROM OutItemDtl WHERE PermitId = '{PermitId}'")
        
        itemLen = self.cursor.fetchone()
        if str(itemLen[0]) == "None":
            itemLen = 0
        else:
            itemLen = itemLen[0]
        # print("The Final" , itemLen)

        # query = f"SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'OutItemDtl'"
        # self.cursor.execute(query)
          
        # result = self.cursor.fetchall()
        # for i in result:
        #     print(f"'{i[0]}' : {i[1]}")


        for index, row in ItemInfo.iterrows():
            itemLen += 1
            data = {
                'ItemNo' : itemLen,
                'PermitId' : PermitId,
                'MessageType' : MsgType,
                'HSCode' : row['HSCode'],
                'Description' : row['Description'],
                'DGIndicator' : row['DGIndicator'],
                'Contry' : row['CountryofOrigin'],
                'EndUserDescription' : '',
                'Brand' : row['Brand'],
                'Model' : row['Model'],
                'InHAWBOBL' : row['InHAWBOBL'],
                'OutHAWBOBL' : row['OutHAWBOBL'],
                'DutiableQty' : row['DutiableQty'],
                'DutiableUOM' : row['DutiableUOM'],
                'TotalDutiableQty' : row['TotalDutiableQty'],
                'TotalDutiableUOM' : row['TotalDutiableUOM'],
                'InvoiceQuantity' : '0.00',
                'HSQty' : row['HSQty'],
                'HSUOM' : row['HSUOM'],
                'AlcoholPer' : row['AlcoholPercentage'],
                'InvoiceNo' : row['InvoiceNumber'],
                'ChkUnitPrice' : 'False',
                'UnitPrice' : row['UnitPrice'],
                'UnitPriceCurrency' : row['ItemCurrency'],
                'ExchangeRate' : '0.00',
                'SumExchangeRate' : '0.00',
                'TotalLineAmount' : row['TotalLineAmount'],
                'InvoiceCharges' : '0.00',
                'CIFFOB' : '0.00',
                'OPQty' : row['OuterPackQty'],
                'OPUOM' : row['OuterPackUOM'],
                'IPQty' : row['InPackQty'],
                'IPUOM' : row['InPackUOM'],
                'InPqty' : row['InnerPackQty'],
                'InPUOM' : row['InnerPackUOM'],
                'ImPQty' : row['InmostPackQty'],
                'ImPUOM' : row['InmostPackUOM'],
                'PreferentialCode' : row['TarrifPreferentialCode'],
                'GSTRate' : '0.00',
                'GSTUOM' : '--Select--',
                'GSTAmount' : '0.00',
                'ExciseDutyRate' : '0.00',
                'ExciseDutyUOM' : '--Select--',
                'ExciseDutyAmount' : '0.00',
                'CustomsDutyRate' : '0.00',
                'CustomsDutyUOM' : '--Select--',
                'CustomsDutyAmount' : '0.00',
                'OtherTaxRate' : row['OtherTaxRate'],
                'OtherTaxUOM' : row['OtherTaxUOM'],
                'OtherTaxAmount' : row['OtherTaxAmount'],
                'CurrentLot' : row['CurrentLot'],
                'PreviousLot' : row['PreviousLot'],
                'Making' : '--Select--',
                'ShippingMarks1' : row['ShippingMarks1'],
                'ShippingMarks2' : row['ShippingMarks2'],
                'ShippingMarks3' : row['ShippingMarks3'],
                'ShippingMarks4' : row['ShippingMarks4'],
                'CerItemQty' : row['CerItemQty'],
                'CerItemUOM' : row['CerItemUOM'],
                'CIFValOfCer' : row['CIFValOfCer'],
                'ManufactureCostDate' : row['ManufactureCostDate'],
                'TexCat' : row['TexCat'],
                'TexQuotaQty' : row['TexQuotaQty'],
                'TexQuotaUOM' : row['TexQuotaUOM'],
                'CerInvNo' : row['CerInvNo'],
                'CerInvDate' : row['CerInvDate'],
                'OriginOfCer' : row['OriginOfCer'],
                'HSCodeCer' : row['HSCodeCer'],
                'PerContent' : row['PerContent'],
                'CertificateDescription' : row['CertificateDescription'],
                'TouchUser' : userName,
                'TouchTime' : TouchTime,
                'VehicleType' : row['VehicleType'],
                'OptionalChrgeUOM' : row['OptionalChrgeUOM'],
                'EngineCapcity' : row['EngineCapcity'],
                'Optioncahrge' : row['Optioncahrge'],
                'OptionalSumtotal' : row['OptionalSumtotal'],
                'OptionalSumExchage' : row['OptionalSumExchange'],
                'EngineCapUOM' : row['EngineCapUOM'],
                'orignaldatereg' : row['originaldatereg'],
            } 
            try:
                columns = ', '.join([f'[{key}]' for key in data.keys()])
                values = ', '.join(['%s' for _ in range(len(data))])
                insert_statement = f'INSERT INTO OutItemDtl ({columns}) VALUES ({values})'  
                self.cursor.execute(insert_statement, tuple(data.values()))  
                self.conn.commit()
            except Exception as e:
                print(e)     

        context = {}
        self.cursor.execute(
            f"select * from OutItemDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "item": (
                    pd.DataFrame(list(self.cursor.fetchall()), columns=headers)
                ).to_dict("records")
            }
        )

        self.cursor.execute(
        f"select * from OutCASCDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
        )
        headers = [i[0] for i in self.cursor.description]
        context.update(
            {
                "casc": (pd.DataFrame(list(self.cursor.fetchall()), columns=headers)).to_dict(
                    "records"
                )
            }
        )
        
        return JsonResponse(context)            


def outEditItemall(request):
    db = SqlDb()
    

    print("hello ")

    PermitId = request.POST.get('PermitId')

    ItemValue = json.loads(request.POST.get('editItemData'))

    qry = "UPDATE OutItemDtl SET MessageType = %s,HSCode = %s,Description = %s,DGIndicator = %s,Contry = %s,EndUserDescription = %s,Brand = %s,Model = %s,InHAWBOBL = %s,OutHAWBOBL = %s,DutiableQty = %s,DutiableUOM = %s,TotalDutiableQty = %s,TotalDutiableUOM = %s,InvoiceQuantity = %s,HSQty = %s,HSUOM = %s,AlcoholPer = %s,InvoiceNo = %s,ChkUnitPrice = %s,UnitPrice = %s,UnitPriceCurrency = %s,ExchangeRate = %s,SumExchangeRate = %s,TotalLineAmount = %s,InvoiceCharges = %s,CIFFOB = %s,OPQty = %s,OPUOM = %s,IPQty = %s,IPUOM = %s,InPqty = %s,InPUOM = %s,ImPQty = %s,ImPUOM = %s,PreferentialCode = %s,GSTRate = %s,GSTUOM = %s,GSTAmount = %s,ExciseDutyRate = %s,ExciseDutyUOM = %s,ExciseDutyAmount = %s,CustomsDutyRate = %s,CustomsDutyUOM = %s,CustomsDutyAmount = %s,OtherTaxRate = %s,OtherTaxUOM = %s,OtherTaxAmount = %s,CurrentLot = %s,PreviousLot = %s,Making = %s,ShippingMarks1 = %s,ShippingMarks2 = %s,ShippingMarks3 = %s,ShippingMarks4 = %s,CerItemQty = %s,CerItemUOM = %s,CIFValOfCer = %s,ManufactureCostDate = %s,TexCat = %s,TexQuotaQty = %s,TexQuotaUOM = %s,CerInvNo = %s,CerInvDate = %s,OriginOfCer = %s,HSCodeCer = %s,PerContent = %s,CertificateDescription = %s,TouchUser = %s,TouchTime = %s,VehicleType = %s,OptionalChrgeUOM = %s,EngineCapcity = %s,Optioncahrge = %s,OptionalSumtotal = %s,OptionalSumExchage = %s,EngineCapUOM = %s,orignaldatereg = %s  WHERE ItemNo = %s AND PermitId = %s"
    
    
    for i in ItemValue:
        val = (i['MessageType'],i['HSCode'],i['Description'],i['DGIndicator'],i['Contry'],i['EndUserDescription'],i['Brand'],i['Model'],i['InHAWBOBL'],i['OutHAWBOBL'],i['DutiableQty'],i['DutiableUOM'],i['TotalDutiableQty'],i['TotalDutiableUOM'],i['InvoiceQuantity'],i['HSQty'],i['HSUOM'],i['AlcoholPer'],i['InvoiceNo'],i['ChkUnitPrice'],i['UnitPrice'],i['UnitPriceCurrency'],i['ExchangeRate'],i['SumExchangeRate'],i['TotalLineAmount'],i['InvoiceCharges'],i['CIFFOB'],i['OPQty'],i['OPUOM'],i['IPQty'],i['IPUOM'],i['InPqty'],i['InPUOM'],i['ImPQty'],i['ImPUOM'],i['PreferentialCode'],i['GSTRate'],i['GSTUOM'],i['GSTAmount'],i['ExciseDutyRate'],i['ExciseDutyUOM'],i['ExciseDutyAmount'],i['CustomsDutyRate'],i['CustomsDutyUOM'],i['CustomsDutyAmount'],i['OtherTaxRate'],i['OtherTaxUOM'],i['OtherTaxAmount'],i['CurrentLot'],i['PreviousLot'],i['Making'],i['ShippingMarks1'],i['ShippingMarks2'],i['ShippingMarks3'],i['ShippingMarks4'],i['CerItemQty'],i['CerItemUOM'],i['CIFValOfCer'],i['ManufactureCostDate'],i['TexCat'],i['TexQuotaQty'],i['TexQuotaUOM'],i['CerInvNo'],i['CerInvDate'],i['OriginOfCer'],i['HSCodeCer'],i['PerContent'],i['CertificateDescription'],request.session["Username"],datetime.now(),i['VehicleType'],i['OptionalChrgeUOM'],i['EngineCapcity'],i['Optioncahrge'],i['OptionalSumtotal'],i['OptionalSumExchage'],i['EngineCapUOM'],i['orignaldatereg'],i['ItemNo'],PermitId)
        db.cursor.execute(qry,val)
        db.conn.commit()

    context = {}
    db.cursor.execute(
        f"select * from OutItemDtl WHERE PermitId = '{request.POST.get('PermitId')}' ORDER BY ItemNo"
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
    

def outTransmit(request):
    permitNumber1 = json.loads(request.GET.get("PermitNumber"))
    s = SqlDb('SecondDb')
    s1 = SqlDb('default')

    


    for ID in permitNumber1:
        s1.cursor.execute(f"SELECT * FROM OutHeaderTbl WHERE Id='{ID}' ")
        permitNumber = s1.cursor.fetchone()[4]
        TouchUser = str(request.session['Username']).upper() 
        refDate = datetime.now().strftime("%Y%m%d")
        jobDate = datetime.now().strftime("%Y-%m-%d")
        print(permitNumber)

        s.cursor.execute("SELECT AccountId,MailBoxId FROM ManageUser WHERE UserName = '{}' ".format(TouchUser))
        ManageUserVal = s.cursor.fetchone()
        AccountId = ManageUserVal[0]
        MailId = ManageUserVal[1]

        s.cursor.execute("SELECT COUNT(*) + 1  FROM OutHeaderTbl WHERE MSGId LIKE '%{}%' AND MessageType = 'OUTDEC' ".format(refDate))
        RefId = ("%03d" % s.cursor.fetchone()[0])

        s.cursor.execute("SELECT COUNT(*) + 1  FROM PermitCount WHERE TouchTime LIKE '%{}%' AND AccountId = '{}' ".format(jobDate,AccountId))
        JobIdCount = s.cursor.fetchone()[0]

        JobId = f"K{datetime.now().strftime('%y%m%d')}{'%05d' % JobIdCount}" 
        MsgId = f"{datetime.now().strftime('%Y%m%d')}{'%04d' % JobIdCount}"
        NewPermitId = f"{TouchUser}{refDate}{RefId}"

        TouchTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        try:
            s1.cursor.execute(f"SELECT * FROM OutHeaderTbl WHERE PermitId='{permitNumber}' ")
            Heading = [i[0] for i in s1.cursor.description]
            HeadData = [dict(zip(Heading,row)) for row in s1.cursor.fetchall()]
            HeadQry = ("INSERT INTO OutHeaderTbl (Refid,JobId,MSGId,PermitId,TradeNetMailboxID,MessageType,DeclarationType,PreviousPermit,CargoPackType,InwardTransportMode,OutwardTransportMode,BGIndicator,SupplyIndicator,ReferenceDocuments,License,COType,Entryyear,GSPDonorCountry,CerDetailtype1,CerDetailCopies1,CerDetailtype2,CerDetailCopies2,PerCommon,CurrencyCode,AddCerDtl,TransDtl,Recipient,DeclarantCompanyCode,ExporterCompanyCode,Inwardcarriercode,OutwardCarrierAgentCode,FreightForwarderCode,ImporterCompanyCode,InwardCarrierAgentCode,CONSIGNEECode,EndUserCode,Manufacturer,ArrivalDate,ArrivalTime,LoadingPortCode,VoyageNumber,VesselName,OceanBillofLadingNo,ConveyanceRefNo,TransportId,FlightNO,AircraftRegNo,MasterAirwayBill,ReleaseLocation,RecepitLocation,StorageLocation,BlanketStartDate,DepartureDate,DepartureTime,DischargePort,FinalDestinationCountry,OutVoyageNumber,OutVesselName,OutOceanBillofLadingNo,VesselType,VesselNetRegTon,VesselNationality,TowingVesselID,TowingVesselName,NextPort,LastPort,OutConveyanceRefNo,OutTransportId,OutFlightNO,OutAircraftRegNo,OutMasterAirwayBill,TotalOuterPack,TotalOuterPackUOM,TotalGrossWeight,TotalGrossWeightUOM,GrossReference,TradeRemarks,InternalRemarks,DeclareIndicator,NumberOfItems,TotalCIFFOBValue,TotalGSTTaxAmt,TotalExDutyAmt,TotalCusDutyAmt,TotalODutyAmt,TotalAmtPay,Status,TouchUser,TouchTime,PermitNumber,prmtStatus,ResLoaName,RepLocName,RecepitLocName,outHAWB,INHAWB,CertificateNumber,Defrentprinting,Cnb,DeclarningFor,MRDate,MRTime,CondColor) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
            for head in HeadData:
                headVal = (RefId,JobId,MsgId,NewPermitId,MailId,head['MessageType'],head['DeclarationType'],head['PreviousPermit'],head['CargoPackType'],head['InwardTransportMode'],head['OutwardTransportMode'],head['BGIndicator'],head['SupplyIndicator'],head['ReferenceDocuments'],head['License'],head['COType'],head['Entryyear'],head['GSPDonorCountry'],head['CerDetailtype1'],head['CerDetailCopies1'],head['CerDetailtype2'],head['CerDetailCopies2'],head['PerCommon'],head['CurrencyCode'],head['AddCerDtl'],head['TransDtl'],head['Recipient'],head['DeclarantCompanyCode'],head['ExporterCompanyCode'],head['Inwardcarriercode'],head['OutwardCarrierAgentCode'],head['FreightForwarderCode'],head['ImporterCompanyCode'],head['InwardCarrierAgentCode'],head['CONSIGNEECode'],head['EndUserCode'],head['Manufacturer'],head['ArrivalDate'],head['ArrivalTime'],head['LoadingPortCode'],head['VoyageNumber'],head['VesselName'],head['OceanBillofLadingNo'],head['ConveyanceRefNo'],head['TransportId'],head['FlightNO'],head['AircraftRegNo'],head['MasterAirwayBill'],head['ReleaseLocation'],head['RecepitLocation'],head['StorageLocation'],head['BlanketStartDate'],head['DepartureDate'],head['DepartureTime'],head['DischargePort'],head['FinalDestinationCountry'],head['OutVoyageNumber'],head['OutVesselName'],head['OutOceanBillofLadingNo'],head['VesselType'],head['VesselNetRegTon'],head['VesselNationality'],head['TowingVesselID'],head['TowingVesselName'],head['NextPort'],head['LastPort'],head['OutConveyanceRefNo'],head['OutTransportId'],head['OutFlightNO'],head['OutAircraftRegNo'],head['OutMasterAirwayBill'],head['TotalOuterPack'],head['TotalOuterPackUOM'],head['TotalGrossWeight'],head['TotalGrossWeightUOM'],head['GrossReference'],head['TradeRemarks'],head['InternalRemarks'],head['DeclareIndicator'],head['NumberOfItems'],head['TotalCIFFOBValue'],head['TotalGSTTaxAmt'],head['TotalExDutyAmt'],head['TotalCusDutyAmt'],head['TotalODutyAmt'],head['TotalAmtPay'],head['Status'],TouchUser,TouchTime,head['PermitNumber'],head['prmtStatus'],head['ResLoaName'],head['RepLocName'],head['RecepitLocName'],head['outHAWB'],head['INHAWB'],head['CertificateNumber'],head['Defrentprinting'],head['Cnb'],head['DeclarningFor'],head['MRDate'],head['MRTime'],head['CondColor'])
                s.cursor.execute(HeadQry,headVal)

            s.cursor.execute(f"INSERT INTO PermitCount (PermitId,MessageType,AccountId,MsgId,TouchUser,TouchTime) VALUES ('{NewPermitId}','OUTDEC','{AccountId}','{MsgId}','{TouchUser}','{TouchTime}') ")

            InvoiceQry = "INSERT INTO OutInvoiceDtl (SNo,InvoiceNo,InvoiceDate,TermType,AdValoremIndicator,PreDutyRateIndicator,SupplierImporterRelationship,SupplierCode,ExportPartyCode,TICurrency,TIExRate,TIAmount,TISAmount,OTCCharge,OTCCurrency,OTCExRate,OTCAmount,OTCSAmount,FCCharge,FCCurrency,FCExRate,FCAmount,FCSAmount,ICCharge,ICCurrency,ICExRate,ICAmount,ICSAmount,CIFSUMAmount,GSTPercentage,GSTSUMAmount,MessageType,PermitId,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM OutInvoiceDtl WHERE PermitId='{permitNumber}' ")
            InvoiceHead = [i[0] for i in s1.cursor.description]
            InvoiceData = [dict(zip(InvoiceHead,row)) for row in s1.cursor.fetchall()] 
            for head in InvoiceData:
                InvoiceVal= (head['SNo'],head['InvoiceNo'],head['InvoiceDate'],head['TermType'],head['AdValoremIndicator'],head['PreDutyRateIndicator'],head['SupplierImporterRelationship'],head['SupplierCode'],head['ExportPartyCode'],head['TICurrency'],head['TIExRate'],head['TIAmount'],head['TISAmount'],head['OTCCharge'],head['OTCCurrency'],head['OTCExRate'],head['OTCAmount'],head['OTCSAmount'],head['FCCharge'],head['FCCurrency'],head['FCExRate'],head['FCAmount'],head['FCSAmount'],head['ICCharge'],head['ICCurrency'],head['ICExRate'],head['ICAmount'],head['ICSAmount'],head['CIFSUMAmount'],head['GSTPercentage'],head['GSTSUMAmount'],head['MessageType'],NewPermitId,TouchUser,TouchTime)
                s.cursor.execute(InvoiceQry,InvoiceVal)

            ItemQry = "INSERT INTO OutItemDtl (ItemNo,PermitId,MessageType,HSCode,Description,DGIndicator,Contry,EndUserDescription,Brand,Model,InHAWBOBL,OutHAWBOBL,DutiableQty,DutiableUOM,TotalDutiableQty,TotalDutiableUOM,InvoiceQuantity,HSQty,HSUOM,AlcoholPer,InvoiceNo,ChkUnitPrice,UnitPrice,UnitPriceCurrency,ExchangeRate,SumExchangeRate,TotalLineAmount,InvoiceCharges,CIFFOB,OPQty,OPUOM,IPQty,IPUOM,InPqty,InPUOM,ImPQty,ImPUOM,PreferentialCode,GSTRate,GSTUOM,GSTAmount,ExciseDutyRate,ExciseDutyUOM,ExciseDutyAmount,CustomsDutyRate,CustomsDutyUOM,CustomsDutyAmount,OtherTaxRate,OtherTaxUOM,OtherTaxAmount,CurrentLot,PreviousLot,Making,ShippingMarks1,ShippingMarks2,ShippingMarks3,ShippingMarks4,CerItemQty,CerItemUOM,CIFValOfCer,ManufactureCostDate,TexCat,TexQuotaQty,TexQuotaUOM,CerInvNo,CerInvDate,OriginOfCer,HSCodeCer,PerContent,CertificateDescription,TouchUser,TouchTime,VehicleType,OptionalChrgeUOM,EngineCapcity,Optioncahrge,OptionalSumtotal,OptionalSumExchage,EngineCapUOM,orignaldatereg) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM OutItemDtl WHERE PermitId='{permitNumber}' ")
            ItemHead = [i[0] for i in s1.cursor.description]
            ItemData = [dict(zip(ItemHead,row)) for row in s1.cursor.fetchall()]
            for head in ItemData:
                ItemVal= (head['ItemNo'],NewPermitId,head['MessageType'],head['HSCode'],head['Description'],head['DGIndicator'],head['Contry'],head['EndUserDescription'],head['Brand'],head['Model'],head['InHAWBOBL'],head['OutHAWBOBL'],head['DutiableQty'],head['DutiableUOM'],head['TotalDutiableQty'],head['TotalDutiableUOM'],head['InvoiceQuantity'],head['HSQty'],head['HSUOM'],head['AlcoholPer'],head['InvoiceNo'],head['ChkUnitPrice'],head['UnitPrice'],head['UnitPriceCurrency'],head['ExchangeRate'],head['SumExchangeRate'],head['TotalLineAmount'],head['InvoiceCharges'],head['CIFFOB'],head['OPQty'],head['OPUOM'],head['IPQty'],head['IPUOM'],head['InPqty'],head['InPUOM'],head['ImPQty'],head['ImPUOM'],head['PreferentialCode'],head['GSTRate'],head['GSTUOM'],head['GSTAmount'],head['ExciseDutyRate'],head['ExciseDutyUOM'],head['ExciseDutyAmount'],head['CustomsDutyRate'],head['CustomsDutyUOM'],head['CustomsDutyAmount'],head['OtherTaxRate'],head['OtherTaxUOM'],head['OtherTaxAmount'],head['CurrentLot'],head['PreviousLot'],head['Making'],head['ShippingMarks1'],head['ShippingMarks2'],head['ShippingMarks3'],head['ShippingMarks4'],head['CerItemQty'],head['CerItemUOM'],head['CIFValOfCer'],head['ManufactureCostDate'],head['TexCat'],head['TexQuotaQty'],head['TexQuotaUOM'],head['CerInvNo'],head['CerInvDate'],head['OriginOfCer'],head['HSCodeCer'],head['PerContent'],head['CertificateDescription'],TouchUser,TouchTime,head['VehicleType'],head['OptionalChrgeUOM'],head['EngineCapcity'],head['Optioncahrge'],head['OptionalSumtotal'],head['OptionalSumExchage'],head['EngineCapUOM'],head['orignaldatereg'])
                s.cursor.execute(ItemQry,ItemVal)

            ItemCascQry = "INSERT INTO OutCASCDtl (ItemNo,ProductCode,Quantity,ProductUOM,RowNo,CascCode1,CascCode2,CascCode3,PermitId,MessageType,TouchUser,TouchTime,CASCId,EndUserDes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM OutCASCDtl WHERE PermitId='{permitNumber}' ")
            ItemCascHead = [i[0] for i in s1.cursor.description]
            ItemCascData = [dict(zip(ItemCascHead,row)) for row in s1.cursor.fetchall()]
            for head in ItemCascData:
                ItemCascVal= (head['ItemNo'],head['ProductCode'],head['Quantity'],head['ProductUOM'],head['RowNo'],head['CascCode1'],head['CascCode2'],head['CascCode3'],NewPermitId,head['MessageType'],TouchUser,TouchTime,head['CASCId'],head['EndUserDes'])
                s.cursor.execute(ItemCascQry,ItemCascVal)

            ContainerQry = "INSERT INTO OutContainerDtl (PermitId,RowNo,ContainerNo,Size,Weight,SealNo,MessageType,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM OutContainerDtl WHERE PermitId='{permitNumber}' ")
            ContainerHead = [i[0] for i in s1.cursor.description]
            ContainerData = [dict(zip(ContainerHead,row)) for row in s1.cursor.fetchall()]
            for head in ContainerData:
                ContainerVal= (NewPermitId,head['RowNo'],head['ContainerNo'],head['Size'],head['Weight'],head['SealNo'],head['MessageType'],TouchUser,TouchTime)
                s.cursor.execute(ContainerQry,ContainerVal)

            CpcQry = "INSERT INTO OutCPCDtl (PermitId,MessageType,RowNo,CPCType,ProcessingCode1,ProcessingCode2,ProcessingCode3,TouchUser,TouchTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM OutCPCDtl WHERE PermitId='{permitNumber}' ")
            CpcHead = [i[0] for i in s1.cursor.description]
            CpcData = [dict(zip(CpcHead,row)) for row in s1.cursor.fetchall()]
            for head in CpcData:
                CpcVal= (NewPermitId,head['MessageType'],head['RowNo'],head['CPCType'],head['ProcessingCode1'],head['ProcessingCode2'],head['ProcessingCode3'],TouchUser,TouchTime)
                s.cursor.execute(CpcQry,CpcVal) 

            InfileQry = "INSERT INTO OutFile (Sno,Name,ContentType,Data,DocumentType,InPaymentId,TouchUser,TouchTime,Size,PermitId,Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  
            s1.cursor.execute(f"SELECT * FROM OutFile WHERE PermitId='{permitNumber}' ")
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
 

class CpcFIlter(View,SqlDb):
    def __init__(self):
        SqlDb.__init__(self)
    def get(self,request,permitId):
        self.cursor.execute(f"select * from OutCPCDtl Where PermitId = '{permitId}' ")
        headers = [i[0] for i in self.cursor.description]
        return JsonResponse({'cpc':(pd.DataFrame(list(self.cursor.fetchall()), columns=headers)).to_dict("records")})