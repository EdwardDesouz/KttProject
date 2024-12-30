const NowDate = new Date();
const TOUCHTIME = NowDate.toISOString().slice(0, 19).replace("T", " ");

$(document).ready(function () {
  $("#COOLIST").css("background-color", "white");
  $("#COOLIST a").css("color", "green");
  $("#INPAYMENT").css("background-color", "rgb(25, 135, 84)");
  $("#INPAYMENT a").css("color", "white");
  $('#declarationType').focus();
  $("#Loading").hide()
});

var ItemData = [];

$(document).ready(() => {
  $.ajax({
    url: "/cooitemsave/" + $("#PermitIDInNon").val() + '/',
    success: (response) => {
      ItemData = response.item;
      console.log('ItemData:',ItemData)
      ItemLoad()
    }
  })
})

var HsCodeData = []
var hsCodeData = fetch('/CooHsCodeUrl/').then(function (res) {
  return res.json()
}, function (err) {
  return "error"
})
hsCodeData.then(function (response) {
  HsCodeData = response.hscode
  // console.log(HsCodeData)
  ItemLoad()
})

function ItemLoad(){
  $("#ItemNumbereCoo").val(ItemData.length + 1)
  var ItemCurrAmd = []
  var Cifob = 0
  var td = ""
  ItemData.forEach((item) => {
    var Color = HsCodeData.filter((data) => {

      if (data.HSCode == item.HSCode && data.Co == '1') {
        return true
      }
    })

    if (Color.length != 0) {
      Color = "red"
    }
    else {
      Color = '#000'
    }
    td += `<tr style="color:${Color}">
    <td><input type="checkbox" name="ItemDeleteCheckbox" value = "${item.ItemNo}"></td>
    <td><i class="fa-regular fa-pen-to-square" style="color: #ff0000;" onclick = "ItemEdit('${item.ItemNo}')"></i></td>
    <td>${item.ItemNo}</td>
    <td>${item.HSCode}</td>
    <td>${item.Description}</td>
    <td>${item.Contry}</td>
    <td>${item.UnitPriceCurrency}</td>
    <td>${item.CIFFOB}</td>
    <td>${item.HSQTY}</td>
    <td>${item.HSUOM}</td>
    <td>${item.TotalLineAmount}</td>
    <td>${item.CerItemQty}</td>
    <td>${item.CerItemUOM}</td>
    <td>${item.ItemValue}</td>
    </tr>
    `
    Cifob += Number(item.CIFFOB);
    ItemCurrAmd.push([item.UnitPriceCurrency, Number(item.TotalLineAmount)]);
    console.log('test:',test)
  })
  if (ItemData.length == 0) {
    td = `<tr>
            <td colspan=14 style='text-align:center'>No Record</td>
          </tr>`
  }
  $('#TotalCIFFOBValue').val(Cifob)
  $('#NumberOfItems').val(ItemData.length)
  $("#ItemTable tbody").html(td)
  SummarySumofItemAmd(ItemCurrAmd)
}
function SummarySumofItemAmd(itemcorrectamount) {
  document.getElementById("summaryNoOfItemValue").innerHTML = "";
  let a = itemcorrectamount;
  let k = [];
  let c = [];
  let j = 0;

  for (let i = 0; i < a.length; i++) {
    if (i == 0) {
      k.push(a[i][0]);
      c.push(a[i]);
    } else {
      if (k.includes(a[i][0])) {
        let n1 = k.indexOf(a[i][0]);
        let m = c[n1][1] + a[i][1];
        c[n1][1] = m;
      } else {
        k.push(a[i][0]);
        c.push(a[i]);
      }
    }
  }
  for (let y = 0; y < c.length; y++) {
    var x = document.createElement("INPUT");
    x.setAttribute("type", "text");
    x.setAttribute("class", "inputStyle");
    x.setAttribute("disabled", false);
    x.setAttribute("value", `${c[y][0]} : ${c[y][1].toFixed(2)}`);
    x.setAttribute("name", 'summaryNoOfItemValue');
    document.getElementById('summaryNoOfItemValue').appendChild(x);
  }
  let artst = c.toString()
  document.getElementById('SummaryItemAmount').innerHTML = artst.replaceAll(",", " ");
}

function TabHead(ID) {
  $("#HeaderTab").removeClass("HeadTabStyleChange");
  $("#PartyTab").removeClass("HeadTabStyleChange");
  $("#CargoTab").removeClass("HeadTabStyleChange");
  $("#ItemTab").removeClass("HeadTabStyleChange");
  $("#SummaryTab").removeClass("HeadTabStyleChange");
  $("#CancelTab").removeClass("HeadTabStyleChange");
  $("#Header").hide();
  $("#Party").hide();
  $("#Cargo").hide();
  $("#Item").hide();
  $("#Summary").hide();
  $("#Amend").hide();

  if (ID == "HeaderTab") {
    $("#HeaderTab").addClass("HeadTabStyleChange");
    $("#Header").show();
    $('#declarationType').focus();
  }
  if (ID == "PartyTab") {
    $("#PartyTab").addClass("HeadTabStyleChange");
    $("#Party").show();
    $('#InNonImporterCode').focus();
  }
  if (ID == "CargoTab") {
    $("#CargoTab").addClass("HeadTabStyleChange");
    $("#Cargo").show();
    $('#InNonTotOuterPackInput').focus();
  }
  if (ID == "ItemTab") {
    $("#ItemTab").addClass("HeadTabStyleChange");
    $("#Item").show();

  }
  if (ID == "SummaryTab") {
    $("#SummaryTab").addClass("HeadTabStyleChange");
    $("#Summary").show();
    //SummaryLoadInNon()
    SummaryPage();
    $('#SummaryPreviousPermitBtn').focus()
  }
  if (ID == "AmendTab") {
    $("#AmendTab").addClass("HeadTabStyleChange");
    $("#Amend").show();
  }
}

function DeclarationChange() {
  var val = $("#declarationType").val()
  $('#InwardTransportModeShowHide').show();
  $('#claimantPartyId').hide();
  if (val == 'BKT : Blanket' || val == 'GST : GST (Including Duty Exemption)') {
    if (val == 'BKT : Blanket') {
      $('#InwardTransportModeShowHide').hide();
      $('#inwardTranseportMode').val('--Select--');
    }
    $('#claimantPartyId').show();
  }
}

function OutwardChange() {
  // below the val is outward select tags id we have to select the value after that we need to give the conditions like this
  var val = $("#OutwardTranseportMode").val();
  console.log(val)
  // var vll=$('#FinalDestinationSelect').val()
  // console.log(vll)

  // below the id is from cargo outward deatails mode's value


  $('#OutwardVisibile').show()
  
  $('#CargoPageDetails').show()
  $('#InNonOutMode').val(val)

  $('#VoyageNumberID').hide()
  $('#VoyageNumberID input').val('')


  $('#veseeleid').hide()
  $('#veseeleid input').val('')


  $('#conveyancerailid').hide()
  $('#conveyancerailid input').val('')


  $('#transportrailid').hide()
  $('#transportrailid input').val('')


  $('#flightnoid').hide()
  $('#flightnoid input').val('')


  $('#aircraftregnoid').hide()
  $('#aircraftregnoid input').val('')


  $('#conveyancemailid').hide()
  $('#conveyancemailid input').val('')


  $('#transportmailid').hide()
  $('#transportmailid  input').val('')


  $('#conveyancemmodelid').hide()
  $('#conveyancemmodelid  input').val('')


  $('#transportmmodelid').hide()
  $('#transportmmodelid input').val('')


  $('#conveyancepipeid').hide()
  $('#conveyancepipeid input').val('')


  $('#transportpipeid').hide()
  $('#transportpipeid input').val('')


  $('#conveyanceroadid').hide()
  $('#conveyanceroadid input').val('')


  $('#transportroadid').hide()
  $('#transportroadid input').val('')


  if (val == '--Select--') {
    $('#InNonOutMode').val('')
    
  }


  if (val == '1 : Sea') {
    $('#VoyageNumberID').show()
    $('#veseeleid').show()
  }
  else if (val == '2 : Rail') {
    $('#conveyancerailid').show()
    $('#transportrailid').show()


  }
  else if (val == '3 : Road') {
    $('#conveyanceroadid').show()
    $('#transportroadid').show()


  }
  else if (val == '4 : Air') {
    $('#flightnoid').show()
    $('#aircraftregnoid').show()


  }
  else if (val == '5 : Mail') {
    $('#conveyancemailid').show()
    $('#transportmailid').show()


  }
  else if (val == '6 : Multi-model(Not in use)') {
    $('#conveyancemmodelid').show()
    $('#transportmmodelid').show()
  }
  else if (val == '7 : Pipeline') {
    $('#conveyancepipeid').show()
    $('#transportpipeid').show()
  }
  else if (val == 'N : Not Required') {
    $('#OutwardVisibile').hide()
   
  }
   CargoResetCoo()
}

var Exporter = [];
$(document).ready(() => {
  $.ajax({
    url: "/exporterurl/",
    success: (response) => {
      Exporter = response.exporter;
      ExportFocusOut()
      // console.log(Exporter)
    }
  })
})

var Outwardcarrieragent = [];
$(document).ready(() => {
  $.ajax({
    url: "/Outwardurl/",
    success: (response) => {
      Outwardcarrieragent = response.outwardcarrier;
      // console.log(Outwardcarrieragent)
      OutwardFocusOut()
    }
  })
})
// doubt have to ask
var Fforwarder = [];
$(document).ready(() => {
  $.ajax({
    url: "/Fforwarderurl/",
    success: (response) => {
      Fforwarder = response.freforwarder;
      FrightFocusOut()
      // console.log(Fforwarder)

    }
  })
})

var Cons = [];
$(document).ready(() => {
  $.ajax({
    url: "/Consigneeurl/",
    success: (response) => {
      Cons = response.consignee;
      // console.log(Cons)
      ConsigneeFocusOut()
      // console.log('Congine:',Cons)

    }
  })
})


var MFact = [];
$(document).ready(() => {
  $.ajax({
    url: "/Manfact/",
    success: (response) => {
      MFact = response.Mfactutrer;
      // console.log(MFact)
      ManfactutrerOut()
    }
  })
})




var DCPORTcode = [];
$(document).ready(() => {
  $.ajax({
    url: "/Cargodcportcode/",
    success: (response) => {
      DCPORTcode = response.Dcportcode;
      // console.log(DCPORTcode)
      InNonDisachargePortFocusOut()

    }
  })
})

var ITEMHScode = [];
$(document).ready(() => {
  $.ajax({
    url: "/ItemHscode/",
    success: (response) => {
      ITEMHScode = response.ItemHscode;
      // console.log(ITEMHScode)

    }
  })
})


var COOcode = [];
$(document).ready(() => {
  $.ajax({
    url: "/ItemCooCode/",
    success: (response) => {
      COOcode = response.CooCode;
      // console.log(COOcode)

    }
  })
})



/*------------------------------------------AUTO-COMPLETE---------------------------------*/
function Autocomplete1(myValues, idName) {
  $(idName)
    .autocomplete({
      source: function (request, response) {
        var term = request.term.toLowerCase();
        var matches = $.grep(myValues, function (value) {
          var k = value.split(":");
          for (var i = 0; i < value.length; i++) {
            if (k[0].toLowerCase().startsWith(term)) {
              return k[0].toLowerCase().startsWith(term);
            } else {
              return k[1].toLowerCase().startsWith(term);
            }
          }
        });
        matches.sort();
        matches = matches.slice(0, 100);
        response(matches);
      },
      autoFocus: true,
      maxShowItems: 10,
      scroll: true,
    })
    .focusout(function () {
      var selectedValue = $(this).val();
      var splittedValue = selectedValue.split(":");
      if (splittedValue.length > 0) {
        $(this).val(splittedValue[0]);
      }
    });
}



function ExportFocusIn() {
  var myValues = [];
  for (var i of Exporter) {
    
    myValues.push(i.Code + ":" + i.Name);
    // console.log(i.Name)
  }
  Autocomplete1(myValues,"#ExporterCode");
  // console.log($("#ExporterCode").val())
}
function ExportFocusOut() {
   let Code = $("#ExporterCode").val().trim().toUpperCase()
  //  console.log(Code)
   if (Code != "") {
    var data = Exporter.filter((obj) => {
      
      return (obj.Code).trim().toUpperCase() == Code
    })
    // console.log('Filtered Data:', data);
   
    
    $("#ExporterCruei").val(data[0].CRUEI)
    $("#ExporterName").val(data[0].Name)
    $("#ExporterName1").val(data[0].Name1)
    $("#ExporterAddress1").val(data[0].Address)
    $("#ExporterAddress2").val(data[0].Address1)
    $("#ExporterAddress3").val(data[0].Address2)
  }
  else {
    $("#ExporterCruei").val("")
    $("#ExporterName").val("")
    $("#ExporterName1").val("")
    $("#ExporterAddress1").val("")
    $("#ExporterAddress2").val("")
    $("#ExporterAddress3").val("")
  }
// console.log($("#ExporterCode").val())
// console.log($("#ExporterCruei").val())
// console.log($("#ExporterName").val())
// console.log($("#ExporterName1").val())
// console.log($("#ExporterAddress1").val())
// console.log($("#ExporterAddress2").val())
// console.log($("#ExporterAddress3").val())
}




function OutwardFocusIN() {
  var OFvalue = [];
  for (var i of Outwardcarrieragent) {
    OFvalue.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(OFvalue, "#OutwardCarrierAgentCode");
  console.log('OFvalue:',OFvalue)
 
}

function OutwardFocusOut() {
  let Code = $("#OutwardCarrierAgentCode").val().trim().toUpperCase()
  console.log('OutwardCarrierAgentCode:',Code)
  
  if (Code != "") {
    var data = Outwardcarrieragent.filter((obj) => {
      // console.log('OutwardFocusOut:',obj)
      return (obj.Code).trim().toUpperCase() == Code
    })
    // console.log('Filtered Data:', data);
    $("#OutwardCarrierAgentCruei").val(data[0].CRUEI)
    $("#OutwardCarrierAgentName").val(data[0].Name)
    $("#OutwardCarrierAgentName1").val(data[0].Name1)
   
  }
  else {
    $("#OutwardCarrierAgentCruei").val("")
    $("#OutwardCarrierAgentName").val("")
    $("#OutwardCarrierAgentName1").val("")
  }
}




function FrightFrwdFocusIN() {
  var FFvalue = [];
  for (var i of Fforwarder) {
    FFvalue.push(i.Code + ":" + i.Name);
    console.log(FFvalue)
  }


  Autocomplete1(FFvalue, "#FreightForwarderCode");
}
function FrightFocusOut() {
  let Code = $("#FreightForwarderCode").val().trim().toUpperCase()
  console.log("FreightForwarderCode:", Code);

  if (Code != "") {
    var data = Fforwarder.filter((obj) => {
      // console.log('fforwarder:',obj)
      return (obj.Code).trim().toUpperCase() == Code
    })
  //  console.log("FreightForwarderCruei:",data[0].CRUEI)
  //  console.log("FreightForwarderName:",data[0].Name)
  //  console.log("FreightForwarderName1:",data[0].Name1)
    $("#FreightForwarderCruei").val(data[0].CRUEI)
    $("#FreightForwarderName").val(data[0].Name)
    $("#FreightForwarderName1").val(data[0].Name1)
  }
  else {
    $("#FreightForwarderCruei").val("")
    $("#FreightForwarderName").val("")
    $("#FreightForwarderName1").val("")
  }

}




function ConsigneeFocusIN() {
  var Consigneevalue = [];
  for (var i of Cons) {
    Consigneevalue.push(i.ConsigneeCode + ":" + i.ConsigneeName);
  }
  Autocomplete1(Consigneevalue, "#ConsigneeCode");
  // console.log('Consigneevalue:',Consigneevalue)
}
function ConsigneeFocusOut() {
  let Code = $("#ConsigneeCode").val().trim().toUpperCase();
  console.log("ConsigneeCode:", Code);

  if (Code != "") {
    var data = Cons.filter((obj) => {
    //   console.log('ConsigneeFocusOut:',obj)
      return (obj.ConsigneeCode).trim().toUpperCase() == Code
    });
    // console.log('Filtered Data:', data);


    $("#ConsigneeCruei").val(data[0].ConsigneeCRUEI)
    $("#ConsigneeName").val(data[0].ConsigneeName)
    $("#ConsigneeName1").val(data[0].ConsigneeName1)
    $("#ConsigneeAdress").val(data[0].ConsigneeAddress)
    $("#ConsigneeAdress1").val(data[0].ConsigneeAddress1)
    $("#ConsigneeAdress2").val(data[0].ConsigneeAddress2)

  }
  else {
    $("#ConsigneeCruei").val("")
    $("#ConsigneeName").val("")
    $("#ConsigneeName1").val("")
    $("#ConsigneeAdress").val("")
    $("#ConsigneeAdress1").val("")
    $("#ConsigneeAdress2").val("")
  }

}



function ManfactutrerIN() {
  var Mfactvalue = [];
  for (var i of MFact) {
    Mfactvalue.push(i.ManufacturerCode + ":" + i.ManufacturerName);
  }
  Autocomplete1(Mfactvalue, "#ManfactutrerCode");
}
function ManfactutrerOut() {
  let Code = $("#ManfactutrerCode").val().trim().toUpperCase()

  if (Code != "") {
    var data = MFact.filter((obj) => {
    //   console.log('ManfactutrerIN:',obj)
      return (obj.ManufacturerCode).trim().toUpperCase() == Code
    })
    // console.log('Filtered Data:', data);


    $("#ManfactutrerCruei").val(data[0].ManufacturerCRUEI)
    $("#ManfactutrerName").val(data[0].ManufacturerName)
    $("#ManfactutrerName1").val(data[0].ManufacturerName1)
    $("#ManfactutrerAddress").val(data[0].ManufacturerAddress)
    $("#ManfactutrerAddress1").val(data[0].ManufacturerAddress1)
    $("#ManfactutrerCity").val(data[0].ManufacturerCity)
    $("#ManfactutrerSubcode").val(data[0].ManufacturerSub)
    $("#ManfactutrerSubDivision").val(data[0].ManufacturerSubDivi)
    $("#ManfactutrerCountry").val(data[0].ManufacturerCountry)
    $("#ManfactutrerPostalcode").val(data[0].ManufacturerPostal)

  }
  else {
    $("#ManfactutrerCruei").val("")
    $("#ManfactutrerName").val("")
    $("#ManfactutrerName1").val("")
    $("#ManfactutrerAddress").val("")
    $("#ManfactutrerAddress1").val("")
    $("#ManfactutrerCity").val("")
    $("#ManfactutrerSubcode").val("")
    $("#ManfactutrerSubDivision").val("")
    $("#ManfactutrerCountry").val("")
    $("#ManfactutrerPostalcode").val("")

  }

}






// Cargo page discargeport

function InNonDisachargePortFocusIn() {
  var Dcportvalue = [];
  for (var i of DCPORTcode) {
    Dcportvalue.push(i.PortCode + ":" + i.PortName);
  }
  Autocomplete1(Dcportvalue, "#CargoDisachargeInput");
}
function InNonDisachargePortFocusOut() {
  let Code = $("#CargoDisachargeInput").val().trim().toUpperCase()

  if (Code != "") {
    var data = DCPORTcode.filter((obj) => {
      // console.log(obj)
      return (obj.PortCode).trim().toUpperCase() == Code
    })
    $("#CargoDisachargeText").val(data[0].PortName)


  }
  else {
    $("#CargoDisachargeText").val("")


  }

}


//  Item page HSCODE 

function ItemHscodeFocusIn() {
  var Hscodevalue = [];
  for (var i of ITEMHScode) {
    Hscodevalue.push(i.HSCode + ":" + i.Description);

  }

  Autocomplete1(Hscodevalue, "#ItemHsCodeCoo");
}
// function ItemHscodeFocusOut() {
//   let Code = $("#ItemHsCodeCoo").val().trim().toUpperCase()

//   if (Code != "") {
//     var data = ITEMHScode.filter((obj) => {
//       // console.log(obj)
//       return (obj.HSCode).trim().toUpperCase() == Code
//     })
//     $("#ItemDescriptioncoo").val(data[0].Description)


//   }
//   else {
//     $("#ItemDescriptioncoo").val("")


//   }

// }
function ItemHscodeFocusOut() {
 
  $("#ItemHsQtyUom").val('--Select--')

  let typeid = 0
  let code = $('#ItemHsCodeCoo').val().trim().toUpperCase()
  if (code != "") {
      var HsCodeF = ITEMHScode.filter((hs) => {
          if (code == (hs.HSCode).toUpperCase()) {
              return hs
          }
      })
      HsCodeF = HsCodeF[0]
      let hsdesc = true;
      InhouseItemCode.filter((hsd) => {
          if (hsd.HSCode == code) {
              hsdesc = false;

              $('#ItemDescriptioncoo').val(hsd.Description)
          }
      })
      try {
          if (hsdesc) {
              $('#ItemDescriptioncoo').val(HsCodeF.Description)
          }
          typeid = HsCodeF.DUTYTYPID
          $("#ItemHsQtyUom").val(HsCodeF.UOM)
          var uom = HsCodeF.DuitableUom
          if (Number(HsCodeF.Transhipment) == 1) {
              $("#HscodeControl").show()
              $('#itemCascID').prop('checked', true)
              ItemCascShowAll('#itemCascID', '.OutItemCascHide')
          }
          else {
              $('#itemCascID').prop('checked', false)
              ItemCascShowAll('#itemCascID', '.OutItemCascHide')
          }
          var HSQTYUOM = $("#ItemHsQtyUom").val()
          if ((typeid == 62 || typeid == 63)) {
              if (typeid == 62 && HSQTYUOM == "LTR") {
                  $("#itemDutiableQtyNone").show()
                  $("#itemAlchoholNone").show()
              }
              if (typeid == 63 && HSQTYUOM == "KGM") {
                  $("#itemDutiableQtyNone").show()
                  $("#itemAlchoholNone").hide()
              }
              else if (typeid == 62 && HSQTYUOM != "LTR") {
                  $("#itemDutiableQtyNone").show()
                  $("#itemAlchoholNone").hide()
              }
              else {
                  $("#itemDutiableQtyNone").show()
                  $("#itemAlchoholNone").show()
              }
              if (uom == "A") {
                  $("#ItemHsQtyUom").val('--Select--')
                  $("#ddptotDutiableQty").val('--Select--')
              }
              else {
                  $("#ItemHsQtyUom").val(uom)
                  $("#ddptotDutiableQty").val(uom)
              }
          }
          else if (typeid == 64) {
              if (HSQTYUOM != "LTR") {
                  $("#itemDutiableQtyNone").show()
                  $("#itemAlchoholNone").hide()
              }
              else {
                  $("#itemDutiableQtyNone").show()
                  $("#itemAlchoholNone").show()
              }
              if (uom == "A") {
                  $("#ItemHsQtyUom").val('--Select--')
                  $("#ddptotDutiableQty").val('--Select--')
              }
              else {
                  $("#ItemHsQtyUom").val(uom)
                
              }
          }
          else if (typeid == 61 && HSQTYUOM == "LTR") {
             
              
              if (uom == "A") {
                  $("#ItemHsQtyUom").val('--Select--')
                  
              }
              else {
                  $("#ItemHsQtyUom").val(uom)
                  
              }
          }
          else if (typeid == 61 && HSQTYUOM == "KGM") {
              
              if (uom == "A") {
                  $("#ItemHsQtyUom").val('--Select--')
                 
              }
              else {
                  $("#ItemHsQtyUom").val(uom)
                 
              }
          }
          else {
             
              $("#ItemHsQtyUom").val('--Select--')
             
          }
      }
      catch (err) {
          console.log("error : ", err)
      }
  }
}


// Invoice hs code
function TxtInvQtyOut() {
  console.log('edward')
let code = $('#ItemHsCodeCoo').val().trim().toUpperCase()
var HsCodeF = ITEMHScode.filter((hs) => {
  if (code == (hs.HSCode).toUpperCase()) {
    return hs
  }
})
HsCodeF = HsCodeF[0]
var UOm = HsCodeF.UOM
$("#ItemHsQtyInput").val($('#itemInvoiceQuantity').val());
  if (UOm == "TEN" || UOm == "TPR") {
    var a = $('#itemInvoiceQuantity').val()
    $("#ItemHsQtyInput").val(a / 10)
  }
  else if (UOm == "CEN") {
    var a = $('#itemInvoiceQuantity').val()
    $("#ItemHsQtyInput").val(Number(a) / 100)
  }
  else if (UOm == "MIL" || UOm == "TNE") {
    var a = $('#itemInvoiceQuantity').val()
    $("#ItemHsQtyInput").val(Number(a) / 1000)
  }
  else if (UOm == "MTK") {
    var a = $('#itemInvoiceQuantity').val()
    $("#ItemHsQtyInput").val(a * 3.213)
  }
  else if (UOm == "LTR") {
    var a = $('#itemInvoiceQuantity').val()
    $("#ItemHsQtyInput").val(a * 1)
  }
  else if (UOm == "KGM" || UOm == "NMB" || UOm == "-") {
    var a = $('#itemInvoiceQuantity').val()
    $("#ItemHsQtyInput").val(a)
  }

  if ($('#itemInvoiceQuantity').val() == "") {
    $('#itemInvoiceQuantity').val("0.00")
  }
  if ($('#ItemHsQtyInput').val() == "0") {
    $('#ItemHsQtyInput').val('0.00')
  }
}

// Item page COO


function ItemCooIn() {
  var Coovalue = [];
  for (var i of COOcode) {
    Coovalue.push(i.CountryCode + ":" + i.Description);
  }
  Autocomplete1(Coovalue, "#ItemCooInput");
}
function ItemCooOut() {
  let Code = $("#ItemCooInput").val().trim().toUpperCase()

  if (Code != "") {
    var data = COOcode.filter((obj) => {
      // console.log(obj)
      return (obj.CountryCode).trim().toUpperCase() == Code
    })
    $("#ItemCooInputText").val(data[0].Description)
  }
  else {
    $("#ItemCooInputText").val("")
  }
}

//  Item page multiplying currentunit price * Total line amount

function CooInvoiceCalculation() {
  let result = $("#TxtExchangeRate").val() * $("#iteminCooTotalLineAmount").val()
  $("#iteminvoiceCIFFOB").val(result.toFixed(2))
}


// Item page when we click add item page the mandatory fields 


function CootItemSave() {
  let CooItemCheck = true;
  $('#ItemHsCodeInNonSpan').hide()
  $('#ItemDescriptionInNonSpan').hide()
  $('#ItemCooInputSpan').hide()
  $('#ItemHsQtyInputSpan').hide()
  $('#ItemInvoiceCurrencyDropSpan').hide()
  $('#itemCooTotalLineAmountSpan').hide()


  if ($('#ItemHsCodeCoo').val() == "") {
    CooItemCheck = false;

    $('#ItemHsCodeInNonSpan').show()

  }

  if ($('#ItemDescriptioncoo').val() == "") {
    CooItemCheck = false;

    $('#ItemDescriptionInNonSpan').show()
  }
  if ($('#ItemCooInput').val() == "") {
    CooItemCheck = false;

    $('#ItemCooInputSpan').show()
  }
  if ($('#ItemHsQtyInput').val() == "0.00") {

    CooItemCheck = false;

    $('#ItemHsQtyInputSpan').show()
  }

  if ($('#TxtExchangeRate').val() == "0.00") {
    CooItemCheck = false;

    $('#ItemInvoiceCurrencyDropSpan').show()
  }
  if ($('#iteminCooTotalLineAmount').val() == "0.00") {
    CooItemCheck = false;

    $('#itemCooTotalLineAmountSpan').show()
  }

  if ($('#ItemValueOnCertificate').val() == "") {
    $("#ItemValueOnCertificate").val("0.00");
}
if ($('#CooTextileQuoQnt').val() == "") {
  $("#CooTextileQuoQnt").val("0.00");
}
if ($('#CooItemInvoicenoInput').val() == "") {
  $("#CooItemInvoicenoInput").val("0.00");
}




  // console.log('ITEM NUMBER:',$("#ItemNumbereCoo").val())
  // console.log('ITEM CODE:',$("#ItemCodeCoo").val())
  // console.log('HS CODE:',$("#ItemHsCodeCoo").val())
  console.log('DESCRIPTION:',$("#ItemDescriptioncoo").val())
  // console.log('COO:',$("#ItemCooInput").val())
  // console.log('ItemCooInputText:',$("#ItemCooInputText").val())
  // console.log('INVOICE QUANTITY:',$("#itemInvoiceQuantity").val())
  // console.log('HS QUANTITY:',$("#ItemHsQtyInput").val())
  // console.log('ItemHsQtyUom:',$("#ItemHsQtyUom").val())
  // console.log('CURR:',$("#DRPCurrency").val())
  // console.log(' TxtExchangeRate:',$("#TxtExchangeRate").val())
  // console.log(' TOTAL LINE AMOUNT:',$("#iteminCooTotalLineAmount").val())
  // console.log(' CIF/FOB (SGD):',$("#iteminvoiceCIFFOB").val())
  // console.log(' SHIPPING MARKS:',$("#shippingmarks").val())
  // console.log(' CERTIFICATE ITEM QUANTITY:',$("#ItemCertificateHsQtyInput").val())
  // console.log(' CERTIFICATE ITEM QUANTITY Uom:',$("#ItemCFQtyUom").val())
  // console.log(' MANUFACTURING COST DATE:',$("#ItemManCostDate").val())
  // console.log(' TEXTILE CATEGORY:',$("#CooItemTextInput").val())
  // console.log(' TEXTILE QUOTA QUANTITY:',$("#CooTextileQuoQnt").val())
  // console.log(' CooTextileQuoQntUom:',$("#CooTextileQuoQntUom").val())
  // console.log(' INVOICE NUMBER:',$("#CooItemInvoicenoInput").val())
  // console.log(' ORIGIN CRITERION:',$("#CooOrgin1").val())
  // console.log('ORIGIN CRITERION :',$("#CooOrgin2").val())
  // console.log('ORIGIN CRITERION :',$("#CooOrgin3").val())
  // console.log(' INVOICE DATE:',$("#ItemInVoDate").val())
  // console.log(' HS CODE ON CERTIFICATE:',$("#ItemHsCodeCertificateCoo").val())
  // console.log('PERCENTAGE CONTENT OF ORIGIN CRITERION :',$("#ItemHsCodePerContent").val())
  // console.log(' CIF/FOB ITEM VALUE ON CERTIFICATE:',$("#ItemValueOnCertificate").val())



  var newDate = ""
  const originalDate = $("#ItemInVoDate").val();
  if (originalDate != "") {
    const parts = originalDate.split("/");
    newDate = `${parts[2]}/${parts[1]}/${parts[0]}`;
  }

  var NEWDATE = ""
  const MFCostDate = $("#ItemManCostDate").val();
  if (MFCostDate != "") {
    var Parts = originalDate.split("/");
    NEWDATE = `${Parts[2]}/${Parts[1]}/${Parts[0]}`;
  }

  let ItemNumberEdit = $("#ItemNumbereCoo").val()
  if (CooItemCheck) {
    $("#Loading").show()
    $.ajax({
      url: "/cooitemsave/",
      type: "POST",
      data: {
        ItemNo: $("#ItemNumbereCoo").val().trim(),
        PermitId: $("#PermitIDInNon").val(),
        MessageType: "COODEC",
        HSCode: $("#ItemHsCodeCoo").val().trim(),
        Description: $("#ItemDescriptioncoo").val().trim(),
        Contry: $("#ItemCooInput").val().trim(),
        UnitPrice: $("#TxtExchangeRate").val().trim(),
        UnitPriceCurrency: $("#DRPCurrency").val().trim(),
        ExchangeRate: "0.00",
        SumExchangeRate: "0.00",
        TotalLineAmount: $("#iteminCooTotalLineAmount").val().trim(),
        CIFFOB: $("#iteminvoiceCIFFOB").val().trim(),
        InvoiceQty: $("#itemInvoiceQuantity").val().trim(),
        HSQTY: $("#ItemHsQtyInput").val().trim(),
        HSUOM: $("#ItemHsQtyUom").val().trim(),
        ShippingMark: $("#shippingmarks").val().trim(),
        CerItemQty: $("#ItemCertificateHsQtyInput").val().trim(),
        CerItemUOM: $("#ItemCFQtyUom").val().trim(),
        ManfCostDate: NEWDATE,
        TextileCat: $("#CooItemTextInput").val().trim(),
        TextileQuotaQty: $("#CooTextileQuoQnt").val().trim(),
        TextileQuotaQtyUOM: $("#CooTextileQuoQntUom").val().trim(),
        ItemValue: $("#ItemValueOnCertificate").val().trim(),
        InvoiceNumber: $("#CooItemInvoicenoInput").val().trim(),
        InvoiceDate: newDate,
        HSOnCer: $("#ItemHsCodeCertificateCoo").val().trim(),
        OriginCriterion: $("#CooOrgin1").val().trim() + "-" + $("#CooOrgin2").val().trim() + "-" + $("#CooOrgin3").val().trim(),
        PerOrgainCRI: $("#ItemHsCodePerContent").val().trim(),
        CertificateDes: $("#ItemDescriptionCoo").val().trim(),
        Touch_user: "",
        TouchTime: "",


        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        
      },
      



      success: (data) => {
        ItemResetCoo()
        ItemData = data.item
        console.log('ItemData=:',ItemData)
        ItemLoad()
        $("#Loading").hide()
        $('#ItemHsCodeCoo').focus()
      }

    })
  }
  else {
    alert("PLEASE CHECK THE ALL MANDATORY ")
  }

}

function NextItem() {
  if ($('#ItemNextItemID').val() != "" ) {
    var ItemNum = Number($('#ItemNextItemID').val()) + 1;
    if (ItemNum > 1) {
      ItemEdit(ItemNum);
    }
  }
}



function PreviousItem() {
  if ($('#ItemNextItemID').val() != "" && Number($('#ItemNextItemID').val()) > 1) {
    var ItemNum = Number($('#ItemNextItemID').val()) - 1;
    ItemEdit(ItemNum);
  }
}




// When we click the add item button then all item going to save the page end

function ItemLoad() {
  let TotalLineAmd = 0;
  let Itemval= 0;


  $("#ItemNumbereCoo").val(ItemData.length + 1)
  // console.log('hello:',ItemData.length)
  var ItemCurrAmd = []
  var Cifob = 0
  var td = ""
  ItemData.forEach((item) => {
    var Color = HsCodeData.filter((data) => {
      // console.log('Color:',Color)

      if (data.HSCode == item.HSCode && data.Co == '1') {
        return true
      }
    })

    if (Color.length != 0) {
      console.log('Color.length:',Color.length)
      Color = "black"

    }
    else {
      Color = '#000'
    }
    td += `<tr style="color:${Color}">
    <td><input type="checkbox" name="ItemDeleteCheckbox" value = "${item.ItemNo}"></td>
    <td><i class="fa-regular fa-pen-to-square" style="color: #ff0000;" onclick = "ItemEdit('${item.ItemNo}')"></i></td>
    <td>${item.ItemNo}</td>
    <td>${item.HSCode}</td>
    <td>${item.Description}</td>
    <td>${item.Contry}</td>
    <td>${item.UnitPriceCurrency}</td>
    <td>${item.CIFFOB}</td>
    <td>${item.HSQTY}</td>
    <td>${item.HSUOM}</td>
    <td>${item.TotalLineAmount}</td>
    <td>${item.CerItemQty}</td>
    <td>${item.CerItemUOM}</td>
    <td>${item.ItemValue}</td>
    </tr>
    `
    Cifob += Number(item.CIFFOB);
    ItemCurrAmd.push([item.UnitPriceCurrency, Number(item.TotalLineAmount)]);

    TotalLineAmd += Number(item.TotalLineAmount);
    Itemval +=Number(item.ItemValue);
    
   

  })
  if (ItemData.length == 0) {
    td = `<tr>
            <td colspan=14 style='text-align:center'>No Record</td>
          </tr>`
  }
  $('#summaryNoOfItemValue').val(TotalLineAmd.toFixed(2));
  $('#summaryTotalInvoiceCIFValue').val(Itemval.toFixed(2));
  $('#TotalCIFFOBValue').val(Cifob)
  $('#summaryNoOfItems').val(ItemData.length)
  $("#ItemTable tbody").html(td)
  // SummarySumofItemAmd(ItemCurrAmd)
}




// Save Permit funtions in summary page




function CooSavePermit(){
  $('#Header span1').hide()
  $('#Cargo span1').hide()
  $('#Party span1').hide()
  $('#Summary span1').hide()
  let HeaderCheck = true;
  let PartyCheck = true;
  let CargoCheck = true;
  let SummaryCheck = true;
  let FinalCheck = true;

  const HeaderId = [
    ['OutwardTranseportMode', 'OutwardTranseportModeSpan'],
    ['DeclaringFor', 'DeclaringForSpan'],
    ['cotypeTranseportMode', 'inwardTranseportModeSpan'],
    ['Certificate1TranseportMode', 'Certificate1TranseportModeSpan']
  ]
  const PartyId = [
    ['ExporterCruei', 'ExporterCrueiError'],
    ['ExporterName', 'ExporterNameError'],
    ['OutwardCarrierAgentCruei', 'OutwardCarrierAgentCrueiError'],
    ['OutwardCarrierAgentName', 'OutwardCarrierAgentNameError'],
    ['ConsigneeCruei', 'ConsigneeCrueiError'],
    ['ConsigneeName', 'ConsigneeNameError'],
    ['ManfactutrerCruei', 'ManfactutrerCrueiError'],
    ['ManfactutrerName', 'ManfactutrerNameError'],
    
  ]

  const CargoID = [
    ['InNonOutMode', 'InNonOutModeSpan'],
    ['DepartureDate', 'DepartureDateSpan'],
    ['ExporterName', 'ExporterNameError'],
    ['CargoDisachargeInput', 'CooCargoDPSpan'],
    ['FinalDestinationSelect', 'FinalDestinationCountryModeSpan'],
    ]

    const SummaryID = [
      ['SummaryMRD', 'SummaryMRDSpan'],
      ['SummaryTIME', 'SummaryTIMESpan'],
      ]
  for (let i of HeaderId) {
    if ($(`#${i[0]}`).val() == "--Select--") {
      $(`#${i[1]}`).show()
      HeaderCheck = false
    }
  }
  for (let i of PartyId) {
    if ($(`#${i[0]}`).val() == "") {
      $(`#${i[1]}`).show()
      PartyCheck = false
    }
  }
    for (let i of CargoID) {
      if ($(`#${i[0]}`).val() == "" || $(`#${i[0]}`).val() == "--Select--") {
        $(`#${i[1]}`).show()
        CargoCheck = false
      }
    }
    for (let i of SummaryID) {
      if ($(`#${i[0]}`).val() == "" ) {
        $(`#${i[1]}`).show()
        SummaryCheck = false
      }
    }

    let Tag = "";
    if (!HeaderCheck) {
      FinalCheck = false
      Tag += "<h1 class='FinalH1'>PLEASE CHECK THE HEADER PAGE</h1><hr>"
    }
    if (!PartyCheck) {
      FinalCheck = false
      Tag += "<h1 class='FinalH1'>PLEASE CHECK THE PARTY PAGE</h1><hr>"
    }

    if (!CargoCheck) {
      FinalCheck = false
      Tag += "<h1 class='FinalH1'>PLEASE CHECK THE CARGO PAGE</h1><hr>"
    }

    if (ItemData.length == 0) {
      FinalCheck = false
      Tag += "<h1 class='FinalH1'>PLEASE CHECK THE ITEM PAGE</h1><hr>"
    }

    if (!SummaryCheck) {
      FinalCheck = false
      Tag += "<h1 class='FinalH1'>PLEASE CHECK THE SUMMARY PAGE</h1><hr>"
    }
    if (!$('#DeclareIndicator').prop("checked")) {
      FinalCheck = false
      Tag += "<h1 class='FinalH1'>PLEASE CHECK THE DECLARATION INDICATOR</h1><hr>"
    }

    if (FinalCheck) {
      AllCooSavePermit()
    }
    else {
      // alert("PLEASE FILL THE ALL DATA")
      ValidationPopUp(Tag)
    }

}

function ValidationPopUp(Tag) {
  $("#InNonImporterSerchId").show();
  $("#InNonImporterSerchId").html(`
  <div class="FinalValidationBG">
        <div class="FinalValidationBox">
            <h1 class="FinalHead">PLEASE FILL THE MANDATORY</h1>
            <hr class = "FinalValidationBGhr">
            ${Tag}
            <button type="button" class="ButtonClick" style="margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
        </div>
    </div>
    `
  );
}


function AllCooSavePermit() {
  let DepartureDate = ""
  if ($('#DepartureDate').val() != "") {
    DepartureDate = $("#DepartureDate").val().split("/");
    DepartureDate = `${DepartureDate[2]}/${DepartureDate[1]}/${DepartureDate[0]}`;
  }
  let MRDate = ""
  if ($('#SummaryMRD').val() != "") {
    MRDate = $("#SummaryMRD").val().split("/");
    MRDate = `${MRDate[2]}/${MRDate[1]}/${MRDate[0]}`;
  }
  $("#Loading").show();
  try{
  $.ajax({
    url: '/CooSavePermit/',
    type: "POST",
    data: {
      Refid: $('#REFID').val(),
      JobId: $('#JOBID').val(),
      MSGId: $('#MSGID').val(),
      PermitId: $('#PermitIDInNon').val(),
      TradeNetMailboxID: $('#MailBoxId').val(),
      MessageType: $('#MsgType').val(),
      ApplicationType: $('#ApplicationType').val(),
      PreviousPermitNo: $('#PreviousPermitNo').val(),
      OutwardTransportMode: $('#OutwardTranseportMode').val(),
      ReferenceDocuments: $('#ReferenceDocuments').val(),
      COType: $('#cotypeTranseportMode').val(),
      CerDtlType1: $('#Certificate1TranseportMode').val(),
      CerDtlCopy1: $('#CooCopies1').val(),
      CerDtlType2: $('#Certificate2TranseportMode').val(),
      CerDtlCopy2: $('#CooCopies2').val(),
      CurrencyCode: $('#CurrencyTranseportMode').val(),
      AdditionalCer: $("#AdditionalCer1").val() + "-" + $("#AdditionalCer2").val() + "-" + $("#AdditionalCer3").val()+ "-" + $("#AdditionalCer4").val(),
      TransportDtl: $("#TransportDtl1").val() + "-" + $("#TransportDtl2").val() + "-" + $("#TransportDtl3").val()+ "-" + $("#TransportDtl4").val(),
      PerferenceContent: $('#CooCommonPerinput').val(),
      DeclarantCompanyCode: $('#DeclarantCode').val(),
      ExporterCompanyCode: $('#ExporterCode').val(),
      OutwardCarrierAgentCode: $('#OutwardCarrierAgentCode').val(),
      FreightForwarderCode: $('#FreightForwarderCode').val(),
      CONSIGNEECode: $('#ConsigneeCode').val(),
      Manufacturer: $('#ManfactutrerCode').val(),
      DepartureDate: DepartureDate,
      DischargePort: $('#CargoDisachargeInput').val(),
      FinalDestinationCountry: $('#FinalDestinationSelect').val(),
      OutVoyageNumber: $('#VoyageNumberValue').val(),
      OutVesselName: $('#veseeleValue').val(),
      OutConveyanceRefNo: $('#conveyancevalue').val(),
      OutTransportId: $('#transportValue').val(),
      OutFlightNO: $('#FlightNoValueId').val(),
      OutAircraftRegNo: $('#aircraftregnoValue').val(),
      TotalOuterPack:"",
      TotalOuterPackUOM: "",
      TotalGrossWeight: "",
      TotalGrossWeightUOM: "",
      DeclareIndicator: $('#DeclareIndicator').val(),
      NumberOfItems:ItemData.length,
      InternalRemarks: $('#summaryInternalRemarks').val(),
      TradeRemarks: $('#summaryTradeRemarks').val(),
      Status: "NEW",
      TouchUser: $('#INONUSERNAME').val(),
      TouchTime: TOUCHTIME,
      prmtStatus:"",
      PermitNumber: $('#PermitNumberId').val(),
      EntryYear: $('#CooEntryInput').val(),
      Percomwealth: $('#CooCommonPerinput').val(),
      Gpsdonorcountry: $('#GSPCurrencyUOM').val(),
      Additionalrecieptant:  $("#Recipient1").val() + "-" + $("#Recipient2").val() + "-" + $("#Recipient3").val(),
      GrossReference: $('#SummaryCrossReference').val(),
      DeclarningFor: $('#DeclaringFor').val(),
      CertificateNumber: "",
      MRDate: MRDate,
      MRTime: $('#SummaryTIME').val(),

      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    },
    success: (data) => {
      ItemData = data.Item
      console.log(ItemData)
      console.log("print")
      window.location.href = '/coolist/'
    }
  })
}catch (error) {
  
  console.error('Error in AJAX request:', error);
  
}
}


//  COO Summary Page Declatrion Company


function COOCoType() {
  var COType = $("#cotypeTranseportMode").val();
  var final=COType.split(":")[0].trim();

  $("#SummaryCoType").html("<p>" + final + "</p>");
}

function CooCerti1() {
  $("#SummaryCertificateType").html("<p>" + $("#Certificate1TranseportMode").val() + "</p>");
}

function SummaryPage() {
  $("#SummaryExporter").html("<p>" + $("#ExporterCruei").val() + " - " + $("#ExporterName").val() + "</p>");
  $("#SummaryItemAmount").html("<p>" + $("#summaryNoOfItemValue").val() + "</p>");
}

function CooCurrencyCode() {

  var currencyOption = $("#CurrencyTranseportMode").val();
  var currencyValue = currencyOption.split(":")[0].trim();
    

    var currencycode = $("#CurrencyTranseportMode").val();
    console.log("currencycode:",currencycode)

  $("#SummaryCurrencyCode").html("<p>" + currencyValue+ "</p>");
  console.log("SummaryCurrencyCode:",$("#SummaryCurrencyCode").val())
}

function CooPreviousPermit() {
    
    var previouspermit = $("#PreviousPermitNo").val();
    console.log("previouspermit:",previouspermit)
    $("#SummaryPrevioursPermit").html("<p>" + previouspermit + "</p>");
    console.log("SummaryPrevioursPermit:",$("#SummaryPrevioursPermit").val())
    
    
}

function CooTransportMode() {
  var outwardTransportMode = $("#OutwardTranseportMode").val();
  var final=outwardTransportMode.split(":")[1].trim();
  
  $("#SummaryTransportMode").html("<p>" + final + "</p>");

  if (outwardTransportMode == '--Select--') {
    $("#SummaryTransportMode").html('');
  }
}



// function ExportFocusOut() {
//   $("#SummaryExporter").html("<p>" + $("#ExporterCode").val() + "</p>");
// }

// Coo Item page reset Function

function CooHeaderReset() {
  $("#PreviousPermitNo").val("");
  $("#OutwardTranseportMode").val("--Select--");
  $("#DeclaringFor").val("--Select--");
  $("#OverRideExchangeRate").val("");
  $("#REFERENCE DOCUMENT").val("");
  $("#Recipient1").val("");
  $("#Recipient2").val("");
  $("#Recipient3").val("");
  $("#cotypeTranseportMode").val("--Select--");
  $("#Certificate1TranseportMode").val("--Select--");
  $("#Certificate2TranseportMode").val("--Select--");
  $("#CurrencyVisible").val("");
  $("#CurrencyTranseportMode").val("--Select--");
  $("#CooEntryInput").val("");
  $("#GSPCurrencyUOM").val("--Select--");
  $("#CooCommonPerinput").val("");
  $("#AdditionalCer1").val("");
  $("#AdditionalCer2").val("");
  $("#AdditionalCer3").val("");
  $("#AdditionalCer4").val("");
  $("#TransportDtl1").val("");
  $("#TransportDtl2").val("");
  $("#TransportDtl3").val("");
  $("#TransportDtl4").val("");
  $("#CooCopies1").val("");
  $("#CooCopies2").val("");


  CERTTUFCATE1Change()
  CooTypeChage()
 }

//  coo cargo reset Funtion
function CargoResetCoo(){

 
  $("#DepartureDate").val("");
  $("#CargoDisachargeInput").val("");
  $("#CargoDisachargeText").val("");
  $("#FinalDestinationSelect").val("--Select--");
  $("#VoyageNumberValue").val("");
  $("#veseeleValue").val("");
  $("#CargoDisachargeText").val("");
  $("#CargoDisachargeText").val("");
  $("#CargoDisachargeText").val("");
  $("#CargoDisachargeText").val("");


  
  
}



// Coo Item page reset Function

function ItemResetCoo() {
  $("#ItemNumbereCoo").val("");
  $("#ItemCodeCoo").val("");
  $("#ItemHsCodeCoo").val("");
  $("#CooItemTextInput").val("");
  $("#CooTextileQuoQnt").val("0.00");
  $("#CooTextileQuoQntUom").val("--Select--");
  $("#CooItemInvoiceno").val("");
  $("#CooOrgin1").val("");
  $("#CooOrgin2").val("");
  $("#CooOrgin3").val("");
  $("#ItemDescriptioncoo").val("");
  $("#ItemCooInput").val("");
  $("#ItemCooInputText").val("");
  $("#itemInvoiceQuantity").val("0.00");
  $("#ItemHsQtyInput").val("0.00");
  $("#ItemHsQtyUom").val("--Select--");
  $("#DRPCurrency").val("--Select--");
  $("#TxtExchangeRate").val("0.00");
  $("#iteminCooTotalLineAmount").val("0.00");
  $("#iteminvoiceCIFFOB").val("0.00");
  $("#shippingmarks").val("");
  $("#ItemHsCodePerContent").val("");
  $("#ItemCertificateHsQtyInput").val("0.00");
  $("#ItemCFQtyUom").val("--Select--");
  $("#ItemManCostDate").val("");
  $("#ItemInVoDate").val("");
  $("#ItemHsCodeCertificateCoo").val("");
  $("#ItemHsCodePerContent").val("");
  $("#ItemDescriptionCoo").val("");
  $("#ItemValueOnCertificate").val("");
  $("#CooItemInvoicenoInput").val("");
  $("span1").hide();
  $("#ItemNumbereCoo").val(ItemData.length + 1)

}

// Item page list view edit functions

function ItemEdit(arg) {
  // console.log("The Item No is : ", arg)
  ItemResetCoo()
  CERTTUFCATE1Change()
  
  for (var item of ItemData) {

    let Origincriterion=item.OriginCriterion.split('-');
   
    if (item.ItemNo == arg) {
  
      var manDate = (item.ManfCostDate).split('-')
      
      manDate = `${manDate[2]}/${manDate[1]}/${manDate[0]}`

      var indate = (item.InvoiceDate).split('-')
      indate = `${indate[2]}/${indate[1]}/${indate[0]}`

      if ("01/01/1900" == indate) { indate = "" }

      if ("01/01/1900" == manDate) {  manDate = "" }
      
      $("#ItemNumbereCoo").val(item.ItemNo);
      $("#ItemNextItemID").val(item.ItemNo);

      $("#ItemHsCodeCoo").val(item.HSCode);
      $("#ItemDescriptioncoo").val(item.Description);
      console.log($("#ItemDescriptioncoo").val())
      $("#ItemCooInput").val(item.Contry);
      $("#iteminvoiceCIFFOB").val(item.CIFFOB);
      $("#ItemHsQtyInput").val(item.HSQTY);
      $("#ItemHsQtyUom").val(item.HSUOM);
      $("#iteminCooTotalLineAmount").val(item.TotalLineAmount);
      $("#ItemCertificateHsQtyInput").val(item.CerItemQty);
      $("#ItemCFQtyUom").val(item.CerItemUOM);
      $("#ItemCertificateHsQtyInput").val(item.CerItemQty);
      $("#ItemCFQtyUom").val(item.CerItemUOM);
      $("#itemInvoiceQuantity").val(item.InvoiceQty);
      $("#DRPCurrency").val(item.UnitPriceCurrency);
      $("#TxtExchangeRate").val(item.ExchangeRate);
      $('#shippingmarks').val(item.ShippingMark);
      $('#ItemManCostDate').val(manDate);
      $("#ItemValueOnCertificate").val(item.ItemValue);
      $("#CooItemTextInput").val(item.TextileCat);
      $("#CooTextileQuoQnt").val(item.TextileQuotaQty);
      $("#CooTextileQuoQntUom").val(item.TextileQuotaQtyUOM);
      $("#CooItemInvoicenoInput").val(item.InvoiceNumber);
      $('#CooOrgin1').val(Origincriterion[0]);
      $('#CooOrgin2').val(Origincriterion[1]);
      $('#CooOrgin3').val(Origincriterion[2]); 
      $('#ItemInVoDate').val(indate);
      $('#ItemHsCodeCertificateCoo').val(item.HSOnCer);
      $('#ItemHsCodePerContent').val(item.PerOrgainCRI);
      $('#ItemDescriptionCoo').val(item.CertificateDes);
    
      

      DRPCurrencyChange()
      ItemCooOut()

      $("#ItemDescriptioncoo").focus();
    }
// console.log('ItemeditedDatas:',ItemData)
  }
}






// upload data

function ItemUploadInNon() {
  
  var fileInput = document.getElementById("InpaymentFile");
  if (fileInput.value != "") {
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append("file", file);
    formData.append("PermitId", $("#PermitIDInNon").val());
    formData.append("MsgType", $("#MsgType").val());
    formData.append("UserName", $("#INONUSERNAME").val());
    formData.append("TouchTime", TOUCHTIME);
    formData.append(
      "csrfmiddlewaretoken",
      $("[name=csrfmiddlewaretoken]").val()
    );
    $("#Loading").show();
    $.ajax({
      type: "POST",
      url: "/ItemCooExcelUpload/",
      dataType: "json",
      processData: false,
      contentType: false,
      data: formData,
      mimeType: "multipart/form-data",
      success: function (response) {
        ItemData = response.item;
        ItemLoad();
        $("#Loading").hide();
      },
      error: function (response) {
        $("#Loading").hide();
      },
    });
  }
}


// when we click the edit button after we typing the updated value and give the add item in itempage

function ItemEditAllInNon() {
  $('#EditAllItemBtn').prop('disabled', true)
  // $("#Loading").show();
  var ItemAllDataInNon = [];

  for (var item of ItemData) {
    ItemEditInNon(item.ItemNo);
    var Echeck = true;


    if (Echeck) {
      ItemAllDataInNon.push({

        HSCode: $("#ItemHsCodeCoo").val().trim(),
        Description: $("#ItemDescriptioncoo").val().trim(),
        Contry: $("#ItemCooInput").val().trim(),
        TotalLineAmount: $("#iteminCooTotalLineAmount").val().trim(),
        HSQty: $("#ItemHsQtyInput").val().trim(),
        HSUOM: $("#ItemHsQtyUom").val(),
        CIFFOB: $("#iteminvoiceCIFFOB").val().trim(),

      });
      console.log(HSCode)
    }
    CooPartyReset();
  }
  // $("#Loading").show();
  // $.ajax({
  //   type: "POST",
  //   url: "/AllItemUpdateInNon/",
  //   data: {
  //     Item: JSON.stringify(ItemAllDataInNon),
  //     PermitId: $("#PermitIDInNon").val(),
  //     csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
  //   },
  //   success: function (response) {
  //     ItemData = response.item;
  //     ItemLoad();
  //     $("#Loading").hide();
  //   },
  // });
}


// Party page Reset functions

function CooPartyReset() {
  $("#ExporterCode").val("");
  $("#ExporterCruei").val("");
  $("#ExporterName").val("");
  $("#ExporterName1").val("");
  $("#ExporterAddress1").val("");
  $("#ExporterAddress2").val("");
  $("#ExporterAddress3").val("");
  $("#OutwardCarrierAgentCode").val("");
  $("#OutwardCarrierAgentCruei").val("");
  $("#OutwardCarrierAgentName").val("");
  $("#OutwardCarrierAgentName1").val("");
  $("#FreightForwarderCode").val("");
  $("#FreightForwarderCruei").val("");
  $("#FreightForwarderName").val("");
  $("#FreightForwarderName1").val("");
  $("#ConsigneeCode").val("");
  $("#ConsigneeCruei").val("");
  $("#ConsigneeName").val("");
  $("#ConsigneeName1").val("");
  $("#ConsigneeAdress").val("");
  $("#ConsigneeAdress1").val("");
  $("#ConsigneeAdress2").val("");
  $("#ManfactutrerCode").val("");
  $("#ManfactutrerCruei").val("");
  $("#ManfactutrerName").val("");
  $("#ManfactutrerName1").val("");
  $("#ManfactutrerAddress").val("");
  $("#ManfactutrerAddress1").val("");
  $("#ManfactutrerCity").val("");
  $("#ManfactutrerSubcode").val("");
  $("#ManfactutrerSubDivision").val("");
  $("#ManfactutrerCountry").val("");
  $("#ManfactutrerPostalcode").val("");

}


// Item Page Date Function this is for common


function CooDateFunction(Arg) {
  $('#CooDateCodeSpan').hide();
  $('#CooDateInvoiceCodeSpan').hide();

  let x = document.getElementById(Arg);
  // console.log(x)
  if (x.value.length != 0) {
    if (x.value.length == 8) {
      if (x.value[0] + x.value[1] <= 31 && x.value[2] + x.value[3] <= 12) {
        x.value =
          `${x.value[0] + x.value[1]}/${x.value[2] + x.value[3]}/${x.value[4] + x.value[5] + x.value[6] + x.value[7]}`
      }
      else {
        x.value = DateTimeCalculation();
      }
    }
    else if (x.value.length == 10) {
    }
    else {
      x.value = DateTimeCalculation();
    }
  }
}

function DateTimeCalculation() {
  let today = new Date();
  let day = today.getDate().toString().padStart(2, '0');
  let month = (today.getMonth() + 1).toString().padStart(2, '0');
  let year = today.getFullYear().toString();
  let formattedDate = `${day}/${month}/${year}`;
  return formattedDate;
}

// Date Functions

$(function () {

  $("#ItemManCostDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#ItemInVoDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#DepartureDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#SummaryMRD").datepicker({ dateFormat: "dd/mm/yy" });


  $('#ItemManCostDate').keydown(function (event) {
    if (event.keyCode == 32) { // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#ItemManCostDate").val(currentDate);
    }
  });

  $('#ItemInVoDate').keydown(function (event) {
    if (event.keyCode == 32) { // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#ItemInVoDate").val(currentDate);
    }
  });

  $('#DepartureDate').keydown(function (event) {
    if (event.keyCode == 32) { // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#DepartureDate").val(currentDate);
    }
  });

  $('#SummaryMRD').keydown(function (event) {
    if (event.keyCode == 32) { // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#SummaryMRD").val(currentDate);
    }
  });
});

// Coo MRTime Function

function MrtTimeOut() {
  const Val = $('#SummaryTIME').val()

  if (Val.length == 6 || Val.length == 7 || Val.length == 8) {
    const regex = /^\d{2}:(AM|PM)$/i;
    const regex2 = /^\d{2}\d{2} (AM|PM)$/i;
    const regex3 = /^\d{2}:\d{2} (AM|PM)$/i; 
    if (regex.test(Val)) {
      $("#SummaryTIME").val(
        `${Val[0]}${Val[1]}:${Val[2]}${Val[3]} ${Val[4]}${Val[5]}`
      );
    } else if(regex2.test(Val)){
      $("#SummaryTIME").val( `${Val[0]}${Val[1]}:${Val[2]}${Val[3]} ${Val[4]}${Val[5]}${Val[6]}`
      );
    }else if (regex3.test(Val)) {
      $("#SummaryTIME").val(Val);
    }else{
      $("#SummaryTIME").val("");
    } 
  } else {
    $("#SummaryTIME").val("");
  }
}



// Item page Checkbox Delete Function

function ItemDeleteInNon() {
  $("#Loading").show();
  var CheckArray = [];
  var CheckBoxName = document.getElementsByName("ItemDeleteCheckbox");
  for (var i of CheckBoxName) {
    if (i.checked) {
      CheckArray.push(i.value);
    }
  }
  if (CheckArray != "") {
    $("#Loading").show();
    $.ajax({
      url: "/cooitemdelete/",
      type: "GET",
      data: {
        PermitId: $("#PermitIDInNon").val(),
        // here this stringfy is used for convert the data to
        ItemNo: JSON.stringify(CheckArray),
      },
      success: function (response) {
        ItemData = response.item;
        ItemLoad();
        $('#ItemHeadCheck').prop('checked', false);
        $("#Loading").hide();
        alert("Deleted Records Succssfully...!");
      },
    });
  }
}

function ItemDelAllCheckBox() {
  if ($("#ItemHeadCheck").prop("checked")) {
    $("#ItemTable input").prop("checked", true);
  } else {
    $("#ItemTable input").prop("checked", false);
  }
}

function TrimKeyUp(Val) {
  $("#" + Val).keyup(function (event) {
    if (event.keyCode != 32) {
      let Value = $("#" + Val).val();
      $("#" + Val).val(Value.trim());
    }
  });
}


// connectivity between header and item page

function CERTTUFCATE1Change(){
  var val = $("#Certificate1TranseportMode").val();
  // console.log(val)

  $('#CooEntryYear').hide()
  $('#CooItemInvoiceno').hide()
  $('#CooItemInvoicenoInput').val('')
  $('#CooItemOrginCriterion').hide()
  $('#CooOrgin1').val('')
  $('#CooOrgin2').val('')
  $('#CooOrgin3').val('')
  $('#CooItemCifFobItemValue').hide()
  $('#CooCommonHealth').hide()
  $('#CooGPS').hide()
 
  
  if (val != '--Select--') {
    $('#CooEntryYear').show()
    
  }
  if (val == '1 : Generalised System of Preferences (GSP) Form A') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooEntryYear').hide()
  }
  if (val == '5 : Commonwealth Preference Certificate') {
    $('#CooCommonHealth').show()
    $('#CooEntryYear').hide()
    
  }
  if (val == '12 : Global System of Trade Preference (GSTP)') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooEntryYear').hide()
    
  }
 
  if (val == '16 : ASEAN Trade in Goods Agreement (ATIGA)') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooEntryYear').hide()
    
  }
  if (val == '17 : Back to Back ATIGA Form D') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooEntryYear').hide()
    
  }
  if (val == '18 : Preferential Certificate of Origin for FTA') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooEntryYear').hide()
    
  }
  if (val == '19 : Asean-China FTA Form E') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooEntryYear').hide()
  }
  if (val == '2 : GSP Form A under Cumulative ASEAN') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').show()
    $('#CooEntryYear').hide()
  }
  if (val == '20 : Back-to-Back ACFTA Form E') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '21 : India Singapore CECA CO') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '22 : Back-to-Back AKFTA Form AK') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '23 : Asean-Korea FTA Form AK') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '24 : Certificate of Origin Generic Form Z') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '25 : Asean Japan CEP Form AJ') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '26 : Back-to-Back AJCEP Form AJ') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '27 : Asean India FTA Form AI') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '28 : Back-to-Back AIFTA Form AI') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '29 : Asean-Australia-New Zealand FTA Form AANZ') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '3 : Back to Back GSP Form A') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').hide()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '30 : Back-to-Back AANZFTA Form AANZ') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '31 : ASEAN-Hong Kong FTA Form AHK') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '32 : Back-to-Back AHKFTA Form AHK') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '33 : Regional Comprehensive Economic Partnership (RCEP) Form RCEP') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '34 : Back-to-Back Form RCEP') {
    $('#CooItemInvoiceno').show()
    $('#CooItemOrginCriterion').show()
    $('#CooItemCifFobItemValue').hide()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '4 : Ordinary Certificate of Origin') {
    $('#CooItemInvoiceno').hide()
    $('#CooItemOrginCriterion').hide()
    $('#CooItemCifFobItemValue').hide()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '4A : Certificate of Processing') {
    $('#CooItemInvoiceno').hide()
    $('#CooItemOrginCriterion').hide()
    $('#CooItemCifFobItemValue').hide()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '7 : Form W (reserve)') {
    $('#CooItemInvoiceno').hide()
    $('#CooItemOrginCriterion').hide()
    $('#CooItemCifFobItemValue').hide()
    $('#CooGPS').hide()
    $('#CooEntryYear').hide()
    $('#CooCommonHealth').hide()
  }
  if (val == '9 : Ordinary Certificate of Origin for textile products to EU countries only') {
    $('#CooItemInvoiceno').hide()
    $('#CooItemOrginCriterion').hide()
    $('#CooItemCifFobItemValue').show()
    $('#CooGPS').hide()
    $('#CooEntryYear').show()
    $('#CooCommonHealth').hide()
  } 
}



function CooTypeChage(){
  var val = $("#cotypeTranseportMode").val();
  console.log(val)

  $("#CooItemTextCate").hide()
  $("#CooItemTextQuta").hide()
  $("#CooItemTextInput").val('')
  $("#CooTextileQuoQnt").val('0.00')
  $("#CooTextileQuoQntUom").val('--Select--')

  

  if(val=='TX : Application for textile products'){
    $("#CooItemTextCate").show()
    $("#CooItemTextQuta").show()
  }

}

function SummaryLoadInNon(){
    console.log('hello summary')
    var money = $("#DRPCurrency").val()
  $("#summaryNoOfItemValue").val("0.00");
  $("#summaryTotalInvoiceCIFValue").val("0.00");

  ItemData.forEach((element) => {

    TotalLineAmd += Number(element.TotalLineAmount);
    var money=$("#DRPCurrency").val()
    // Itemval += Number(item.ItemValue);
  });

  $("#summaryNoOfItemValue").val("0.00");
  if (TotalLineAmd != 0) {
    $("#summaryNoOfItemValue").val(money+ +TotalLineAmd.toFixed(2));
    $('#SummaryItemAmount').html($("#summaryNoOfItemValue").val());
   
  }
  $("#summaryTotalInvoiceCIFValue").val("0.00");
  if (Itemval != 0) {
    $("#summaryTotalInvoiceCIFValue").val(Itemval.toFixed(2));
  }
  

}




// Header page reference document


function CooReferenceDocument() {
  if ($("#ReferenceDocuments").prop("checked")) {
    $("#ReferenceShow").show();
    $("#ReferenceDocuments").val("True")
  }
  else {
    $("#ReferenceDocuments").val("False")
    $("#ReferenceShow").hide();
    $(".LicenceHide").val("");
    $.ajax({
      url: "/AttachOut/",
      data: {
        Method: "ALLDELETE",
        PermitId: $("#PermitId").val(),
      },
      success: function (response) {
        AttachData = response.attachFile;
        AttachLoad(AttachData);
      },
    });
  }
}


function HeaderDocumentAttch() {
  let check = true;
  if ($("#HeaddocumentType").val() == "--Select--") {
    check = false;
  }
  if ($("#HeadAttach").val() == "") {
    check = false;
  }
  if (check) {
    var FileName = "HeadAttach";
    var MeesageID = $("#MSGID").val();
    var PermitId = $("#PermitIDInNon").val();
    var UserName = $("#INONUSERNAME").val();
    var name = document.getElementById(FileName);
    var type1 = name.files.item(0).type;
    var size = name.files.item(0).size / 1024;
    size = Math.round(size * 100) / 100;
    name = name.files.item(0).name.split(".");
    name = name[0].replaceAll(" ", "_");
    name = name.replaceAll("-", "_");
    name = name + MeesageID + UserName;
    var fileInput = document.getElementById(FileName);
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append("file", file);
    formData.append("Sno", 1);
    formData.append("Name", name);
    formData.append("ContentType", type1);
    formData.append("DocumentType", $("#HeaddocumentType").val());
    formData.append("InPaymentId", MeesageID);
    formData.append("FilePath", "D:/Users/Public/IMG/");
    formData.append("Size", size + " KB");
    formData.append("PermitId", PermitId);
    formData.append("UserName", UserName);
    formData.append("TouchTime", TOUCHTIME);
    formData.append("Type", "NEW");
    formData.append(
      "csrfmiddlewaretoken",
      $("[name=csrfmiddlewaretoken]").val()
    );
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      },
    });
    $("#Loading").show();
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/AttachCoo/",
      processData: false,
      contentType: false,
      mimeType: "multipart/form-data",
      data: formData,
      success: function (response) {
        $("#Loading").hide();
        AttachData = response.attachFile;
        AttachLoad(AttachData);
      },
    });
  } else {
    alert("PLEASE SELECT THE DOCUMENT TYPE OR INSERT THE FILE ");
  }
}


/*------------------------------Party Searching-------------------------------------------*/
/*------------------------------EXPORTER-------------------------------------------*/
function EXPORTERSearch() {
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Exporter) {
   
    tag += `
      <tr onclick="CooExporterSearchSelectRow(this)" style="cursor: pointer;">
          <td>${i.Code}</td>
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.CRUEI}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>EXPORTER</h1>
                  <input type="text" id="InNonSearchImg" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonImporterTable').DataTable().search($('#InNonSearchImg').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonImporterTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonImporterTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}
function CooExporterSearchSelectRow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  $("#ExporterCode").val(col1);

  ExportFocusOut();

  $("#InNonImporterSerchId").hide();
}


/*------------------------------OUTWARD CARRIER AGENT-------------------------------------------*/

function OUTWARDSearch() {
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Outwardcarrieragent) {
    console.log('code is:', i.Code);
    console.log('name is:', i.Name);
    console.log('name1 is:', i.Name1);
    console.log('CRUEI is:', i.CRUEI);
   

    tag += `
      <tr onclick="CooOutwardSearchSelectRow(this)" style="cursor: pointer;">
          <td>${i.Code}</td>
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.CRUEI}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>OUTWARD CARRIER AGENT</h1>
                  <input type="text" id="InNonSearchImg" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonImporterTable').DataTable().search($('#InNonSearchImg').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonImporterTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonImporterTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}
function CooOutwardSearchSelectRow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  $("#OutwardCarrierAgentCode").val(col1);

  OutwardFocusOut();


  $("#InNonImporterSerchId").hide();
}

/*---------------------------FREIGHT FORWARDER-------------------------------------------*/

function FREIGHTSearch(){
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Fforwarder) { 
    tag += `
      <tr  onclick="CooFreightImgSelectRow(this)"style="cursor: pointer;">
          <td>${i.Code}</td>
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.CRUEI}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>FREIGHT FORWARDER</h1>
                  <input type="text" id="InNonSearchImg" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonImporterTable').DataTable().search($('#InNonSearchImg').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonImporterTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonImporterTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}
function CooFreightImgSelectRow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  
  $("#FreightForwarderCode").val(col1);

  FrightFocusOut();

  $("#InNonImporterSerchId").hide();
}
/*---------------------------Consignee-------------------------------------------*/

function CONSIGNEESearch(){
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Cons) { 
    tag += `
      <tr  onclick="CooConsigneImgSelectRow(this)"style="cursor: pointer;">
          <td>${i.ConsigneeCode}</td>
          <td>${i.ConsigneeName}</td>
          <td>${i.ConsigneeName1}</td>
          <td>${i.ConsigneeCRUEI}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>CONSIGNEE</h1>
                  <input type="text" id="InNonSearchImg" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonImporterTable').DataTable().search($('#InNonSearchImg').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonImporterTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonImporterTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}
function CooConsigneImgSelectRow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  
  $("#ConsigneeCode").val(col1);

  ConsigneeFocusOut();

  $("#InNonImporterSerchId").hide();
}


/*---------------------------MANUFACTURER-------------------------------------------*/

function MANFACTUTRERSearch(Model){
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Model) { 
    tag += `
      <tr  onclick="CooManFactImgSelectRow(this)"style="cursor: pointer;">
          <td>${i.ManufacturerCode}</td>
          <td>${i.ManufacturerName}</td>
          <td>${i.ManufacturerName1}</td>
          <td>${i.ManufacturerCRUEI}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>MANUFACTURER</h1>
                  <input type="text" id="InNonSearchImg" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonImporterTable').DataTable().search($('#InNonSearchImg').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonImporterTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonImporterTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}
function CooManFactImgSelectRow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  
  $("#ManfactutrerCode").val(col1);

  ManfactutrerOut();

  $("#InNonImporterSerchId").hide();
}



/*-------------------------------Party  page+ button functions -----------------------------*/ 
function ExporterSave() {
  $("#ExportCodeSpan").hide();
  if ($('#ExporterCode').val() == "") {
    $("#ExportCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CooPartySave/',
      data: {
        ModelName: 'ExporterModel',
        code: ($("#ExporterCode").val()).trim(),
        cruei: ($("#ExporterCruei").val()).trim(),
        name: ($("#ExporterName").val()).trim(),
        name1: ($("#ExporterName1").val()).trim(),
        TouchUser: $("#INONUSERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        Exporter = response.Exporter;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

function OutwardCarrierSave() {
  $("#OutwardCodeSpan").hide();
  if ($('#OutwardCarrierAgentCode').val() == "") {
    $("#OutwardCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CooPartySave/',
      data: {
        ModelName: 'OutwardModel',
        code: ($("#OutwardCarrierAgentCode").val()).trim(),
        cruei: ($("#OutwardCarrierAgentCruei").val()).trim(),
        name: ($("#OutwardCarrierAgentName").val()).trim(),
        name1: ($("#OutwardCarrierAgentName1").val()).trim(),
        TouchUser: $("#INONUSERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        Outwardcarrieragent = response.Outward;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

function FrightSave() {
  $("#FrightCodeSpan").hide();
  if ($('#FreightForwarderCode').val() == "") {
    $("#FrightCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CooPartySave/',
      data: {
        ModelName: 'FreightModel',
        code: ($("#FreightForwarderCode").val()).trim(),
        cruei: ($("#FreightForwarderCruei").val()).trim(),
        name: ($("#FreightForwarderName").val()).trim(),
        name1: ($("#FreightForwarderName1").val()).trim(),
        TouchUser: $("#INONUSERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        Fforwarder = response.FreightForwarder;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

function Consignsave() {
  $("#ConsigneeCodeSpan").hide();
  if ($('#ConsigneeCode').val() == "") {
    $("#ConsigneeCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CooPartySave/',
      data: {
        ModelName: 'CONSIGNE',
        ConsigneeCode: ($("#ConsigneeCode").val()).trim(),
        ConsigneeCRUEI: ($("#ConsigneeCruei").val()).trim(),
        ConsigneeName: ($("#ConsigneeName").val()).trim(),
        ConsigneeName1: ($("#ConsigneeName1").val()).trim(),
        ConsigneeAddress:($("#ConsigneeAdress").val()).trim(),
        ConsigneeAddress1:($("#ConsigneeAdress1").val()).trim(),
        TouchUser: $("#INONUSERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        Cons = response.consign;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

function ManufactSave() {
  $("#ManfactutrerCodeSpan").hide();
  if ($('#ManfactutrerCode').val() == "") {
    $("#ManfactutrerCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CooPartySave/',
      data: {
        ModelName: 'MANFACTUTRER',
        ManufacturerCode: ($("#ManfactutrerCode").val()).trim(),
        ManufacturerCRUEI: ($("#ManfactutrerCruei").val()).trim(),
        ManufacturerName: ($("#ManfactutrerName").val()).trim(),
        ManufacturerName1: ($("#ManfactutrerName1").val()).trim(),
        ManufacturerAddress:($("#ManfactutrerAddress").val()).trim(),
        ManufacturerAddress1:($("#ManfactutrerAddress1").val()).trim(),
        ManufacturerCity:($("#ManfactutrerCity").val()).trim(),
        TouchUser: $("#INONUSERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        MFact = response.Manufact;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

/*-------------------------Cargopage loading port ------------------------------------*/

function ItemLoadingSearchImg(){
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of DCPORTcode) { 
    tag += `
      <tr  onclick="CooCargoImgSelectRow(this)"style="cursor: pointer;">
          <td>${i.PortCode}</td>
          <td>${i.PortName}</td>
          <td>${i.Country}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>DISCHARGE PORT</h1>
                  <input type="text" id="InNonSearchImg" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonImporterTable').DataTable().search($('#InNonSearchImg').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonImporterTable">
                      <thead>
                          <th>PORTCODE</th>
                          <th>	PORT NAME</th>
                          <th>COUNTRY</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonImporterTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}
function CooCargoImgSelectRow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  
  $("#CargoDisachargeInput").val(col1);

  InNonDisachargePortFocusOut();

  $("#InNonImporterSerchId").hide();
}

/*-------------------------Itempage Coo Search------------------------------------*/

function ItemCooSearch(){
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of COOcode) { 
    tag += `
      <tr  onclick="CooItemImgSelectRow(this)"style="cursor: pointer;">
          <td>${i.CountryCode}</td>
          <td>${i.Description}</td>
          
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>ORIGIN COUNTRY</h1>
                  <input type="text" id="InNonSearchImg" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonImporterTable').DataTable().search($('#InNonSearchImg').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonImporterTable">
                      <thead>
                          <th>COUNTRYCODE</th>
                          <th>DESCRIPTION</th>
                        </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonImporterTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}
function CooItemImgSelectRow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  
  $("#ItemCooInput").val(col1);

  ItemCooOut();

  $("#InNonImporterSerchId").hide();
}

/*-------------------------------------------------------------------------------------------------------*/

// item page edit all item

async function ItemEditAllCoo() {
  // $('#editAllitemBtn').prop('disabled', true)
  $('#Loading').show();
  setTimeout(ItemEditAllCoo1, 1000);
}


function ItemEditAllCoo1() {
  // console.log('hello')
  // $('#EditAllItemBtn').prop('disabled', true)
  // $("#Loading").show();
  var ItemAllDataInNon = [];
  for (var item of ItemData) {
    ItemEdit(item.ItemNo);
    var Echeck = true;
    console.log("Echeck:",Echeck)
    if (Echeck == false){
      console.log('error');

    }

    var newDate = ""
    const originalDate = $("#ItemInVoDate").val();
    if (originalDate != "") {
      const parts = originalDate.split("/");
      newDate = `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
  
    var NEWDATE = ""
    const MFCostDate = $("#ItemManCostDate").val();
    if (MFCostDate != "") {
      var Parts = originalDate.split("/");
      NEWDATE = `${Parts[2]}/${Parts[1]}/${Parts[0]}`;
    }
  

 
    
    if (Echeck) {
      ItemAllDataInNon.push({
        ItemNo: $("#ItemNumbereCoo").val().trim(),
        PermitId: $("#PermitIDInNon").val(),
        MessageType: "COODEC",
        HSCode: $("#ItemHsCodeCoo").val().trim(),
        Description: $("#ItemDescriptioncoo").val().trim(),
        Contry: $("#ItemCooInput").val().trim(),
        UnitPrice: $("#TxtExchangeRate").val().trim(),
        UnitPriceCurrency: $("#DRPCurrency").val().trim(),
        ExchangeRate: "0.00",
        SumExchangeRate: "0.00",
        TotalLineAmount: $("#iteminCooTotalLineAmount").val().trim(),
        CIFFOB: $("#iteminvoiceCIFFOB").val().trim(),
        InvoiceQty: $("#itemInvoiceQuantity").val().trim(),
        HSQTY: $("#ItemHsQtyInput").val().trim(),
        HSUOM: $("#ItemHsQtyUom").val().trim(),
        ShippingMark: $("#shippingmarks").val().trim(),
        CerItemQty: $("#ItemCertificateHsQtyInput").val().trim(),
        CerItemUOM: $("#ItemCFQtyUom").val().trim(),
        ManfCostDate: NEWDATE,
        TextileCat: $("#CooItemTextInput").val().trim(),
        TextileQuotaQty: $("#CooTextileQuoQnt").val().trim(),
        TextileQuotaQtyUOM: $("#CooTextileQuoQntUom").val().trim(),
        ItemValue: $("#ItemValueOnCertificate").val().trim(),
        InvoiceNumber: $("#CooItemInvoicenoInput").val().trim(),
        InvoiceDate:  newDate,
        HSOnCer: $("#ItemHsCodeCertificateCoo").val().trim(),
        OriginCriterion: $("#CooOrgin1").val().trim() + "-" + $("#CooOrgin2").val().trim() + "-" + $("#CooOrgin3").val().trim(),
        PerOrgainCRI: $("#ItemHsCodePerContent").val().trim(),
        CertificateDes: $("#ItemDescriptionCoo").val().trim(),
        Touch_user: $("#INONUSERNAME").val().trim(),
        TouchTime: TOUCHTIME,
      });
    }
    else{
    $('#Loading').hide()
    
    }
   
  }
if(ItemAllDataInNon !=0){

  console.log('ItemAllDataInNon:',ItemAllDataInNon.length);
  console.log('ItemAllDataInNon:',ItemAllDataInNon);
  $.ajax({
    url: "/AllItemUpdateCoo/",
    method: "POST",
    data: {
      'ItemAllDataInNon': JSON.stringify(ItemAllDataInNon),
      'PermitId': $('#PermitIDInNon').val().toUpperCase(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      ItemData = response.item;
      console.log('the edited datas:',ItemData)
      alert(response.Result);
      ItemLoad();
      $("#Loading").hide();
      ItemResetCoo();

    },
    error: (er) => {
      $('#Loading').hide();
      console.log('error',er)
      ItemResetCoo();
    }
  })
}
}


/*-------------------Item page Item Code-------------------------------------------------*/ 
var InhouseItemCode = [];
var HsCode = [];
var ChkHsCode = [];
var HsCodeLoading = [];
$(document).ready(function () {
  $.ajax({
    url: "/CooItemCode/",
    data: {
      PermitId: $("#PermitIDInNon").val(),
    },
    success: function (response) {
      console.log("Item Page Loaded ...!");
      InhouseItemCode = response.inhouseItemCode;
      console.log("inhousedatas are:",InhouseItemCode)
      HsCode = response.hsCode;
      ChkHsCode = response.chkHsCode;
      ItemLoad()
      console.log(HsCode)
      for (var i of HsCode) {
        HsCodeLoading.push(i.HSCode + ":" + i.Description);
      }
      $('#HsCodeLoadingId').hide()
      document.getElementById('ItemHsCodeCoo').addEventListener('input', function () {
        Autocomplete1(HsCodeLoading, "#ItemHsCodeCoo");
      })
    },
  });
});

function ItemcodeFocusIn(){
  var myValues = [];
  for (var i of InhouseItemCode) {
    console.log("my datas are:",i)
    myValues.push(i.InhouseCode + ":" + i.HsCode );
  }
  Autocomplete1(myValues, "#ItemCodeCoo");

}

function ItemcodeFocusOut(val){
  if (val == "") {
    $("#ItemHsCodeCoo").val("");
    $("#ItemDescriptioncoo").val("");
  }else{
    for (var i of InhouseItemCode) {
      console.log("datas are:",i)
      if (val == i.InhouseCode) {
        $("#ItemHsCodeCoo").val(i.HsCode);
        $("#ItemDescriptioncoo").val(i.Description);
      }
    }
  }
  ItemHscodeFocusOut()
}


function ItemCodeSave() {
  $('#Loading').show();
  $("#ItemCodeSpan").hide()
  $("#ItemHouseHscode").hide()
  $("#ItemDescriptionInNonSpan").hide()
  $("#HsCodeLoadingId").hide()
  if (($('#ItemHsCodeCoo').val() != "") && ($('#ItemDescriptioncoo').val() != "") && ($("#ItemCodeCoo")
      .val() != "")) {
      $.ajax({
          type: "POST",
          url: "/CooItemCodeSave/",
          data: {
              ModelName: 'COOInhouseItemModel',
              InhouseCode: $("#ItemCodeCoo").val(),
              HsCode: $("#ItemHsCodeCoo").val(),
              Description: $("#ItemDescriptioncoo").val(),
              cooCode:"",
              CooName: "",
              manufactdate: "",
              OrginCert:"",
              CertificateHscode: "",
              PerCentOrgCert: "",
              CertficateDescrp: "",
              ShippingMarks: "",
              TouchUser: $("#INONUSERNAME").val().toUpperCase(),
              TouchTime: TOUCHTIME,
              csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
          },
          success: function (data) {
              alert(data.Result);
              $('#Loading').hide();
          }
      })
  } else {
      if ($('#ItemHsCodeCoo').val() == "") {
          $("#ItemHsCodeInNonSpan").show()
      }
      if ($('#ItemDescriptioncoo').val() == "") {
          $("#ItemDescriptionInNonSpan").show()
      }
      if ($('#ItemCodeCoo').val() == "") {
          $("#ItemCodeSpan").show()
      }
  }
}

function CheckFunction(ID) {
  if ($("#" + ID).prop("checked")) {
    $("#" + ID).val("True");
    if ("itemUnBrand" == ID) {
      $("#itemBrandInput").val("UNBRANDED");
    }
  } else {
    $("#" + ID).val("False");
    if ("itemUnBrand" == ID) {
      $("#itemBrandInput").val("");
    }
  }
}








  
