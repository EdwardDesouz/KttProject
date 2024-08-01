def ItemExcelUpload(request):
    xlsx_file = request.FILES["file"]

    PermitId = request.POST.get("PermitId")
    MsgType = request.POST.get("MsgType")
    userName = request.POST.get("UserName")
    TouchTime = request.POST.get("TouchTime")

    
    

    ItemInfo = pd.read_excel(xlsx_file, sheet_name="ItemInfo")

    casc = False
    contain = False
    if "Casccodes" in pd.ExcelFile(xlsx_file).sheet_names:
        CascInfo = pd.read_excel(xlsx_file, sheet_name="Sheet3")
        casc = True
    
    ItemData = []
    CascData = []
  
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

    CascColumn = {			 	 	

        "DESCRIPTION": "",
        "HSCODE": "",
        "HSC": "--Select--",
        "PRODUCT CODE": "--Select--",
        "PRDT UOM": "--Select--",
       
    }

 

    ItemInfo.fillna(ItemColumns, inplace=True)
    
    
    if casc and contain:
        for index, row in ItemInfo.iterrows():
            ItemLen = len(ItemDtl.objects.filter(PermitId=PermitId)) + (index + 1)
            try:
                ItemData.append(
                    ItemDtl(
                        Description=row["Description"],
                        HSCode=row["HSCode"],
                        HSUOM=row["HSUOM"],
                        Contry=row["CountryofOrigin"],
                        InvoiceQuantity=["INV QTY"],
                        HSQty=row["HSQty"],
                        ProductCode=row["ProductCode"],
                        Quantity=row["Quantity"],
                        ProductUOM=row["ProductUOM"],
                        Contry=row["CountryofOrigin"],
                        RowNo=str(int(row["RowNo"])),
                        TotalLineAmount=row["TotalLineAmount"],
                        
                        DGIndicator=row["DGIndicator"],
                        Brand=row["Brand"],
                        Model=row["Model"],
                        InHAWBOBL=row["InHAWBOBL"],
                        
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
                print("ItemData:",ItemData)
            except Exception as e:
                pass
        
        ItemDtl.objects.bulk_create(ItemData)  
    else:
        ItemColumns = {
    
        }                       
        ItemInfo.fillna(ItemColumns, inplace=True)
        
        for index, row in ItemInfo.iterrows():
            ItemLen = len(ItemDtl.objects.filter(PermitId=PermitId))+1
            print ("itemlen:",ItemLen)
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
                            UnitPriceCurrency= "--Select--",
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
    # print("Item Data:")
    # for item in Item:
    #     print(item)


    # print("\nItem Casc Data:")
    # for item_casc in ItemCasc:
    #     print(item_casc)
    return JsonResponse({"Item": Item, "ItemCasc": ItemCasc,"message": "All Item Inserted Successfully", "Result": "Deleted"})
