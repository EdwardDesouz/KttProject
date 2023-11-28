const NowDate = new Date();
const TOUCHTIME = NowDate.toISOString().slice(0, 19).replace("T", " ");

var InvoiceData = [];

$(document).ready(function () {
  $("#OUT").css("background-color", "white");
  $("#OUT a").css("color", "green");
  $("#INPAYMENT").css("background-color", "rgb(25, 135, 84)");
  $("#INPAYMENT a").css("color", "white");
  $('.EndUserHide').hide()
});
const a = fetch('/OutInvoice/' + $('#PermitId').val() + "/")
//promise objects return two things one on successfull one on error 
var response = a.then(function (res) {
  return res.json()
}, function (err) {
  return "error"
})
response.then(function (response) {
  InvoiceData = response.invoice
  InvoiceLoadData()
  $("#Loading").hide();
})

function TabHead(ID) {
  $("#PartyTab").removeClass("HeadTabStyleChange");
  $("#CargoTab").removeClass("HeadTabStyleChange");
  $("#InvoiceTab").removeClass("HeadTabStyleChange");
  $("#ItemTab").removeClass("HeadTabStyleChange");
  $("#CpcTab").removeClass("HeadTabStyleChange");
  $("#SummaryTab").removeClass("HeadTabStyleChange");
  $("#RefundTab").removeClass("HeadTabStyleChange");
  $("#AmendTab").removeClass("HeadTabStyleChange");
  $("#CancelTab").removeClass("HeadTabStyleChange");
  $("#HeaderTab").removeClass("HeadTabStyleChange");
  $("#Header").hide();
  $("#Party").hide();
  $("#Cargo").hide();
  $("#Invoice").hide();
  $("#Item").hide();
  $("#Cpc").hide();
  $("#Summary").hide();
  $("#Refund").hide();
  $("#Amend").hide();
  $("#Cancel").hide();
  if (ID == "HeaderTab") {
    $("#HeaderTab").addClass("HeadTabStyleChange");
    $("#Header").show();
  }
  if (ID == "PartyTab") {
    $("#PartyTab").addClass("HeadTabStyleChange");
    $("#Party").show();
  }
  if (ID == "CargoTab") {
    $("#CargoTab").addClass("HeadTabStyleChange");
    $("#Cargo").show();
  }
  if (ID == "InvoiceTab") {
    $("#InvoiceTab").addClass("HeadTabStyleChange");
    $("#Invoice").show();
  }
  if (ID == "ItemTab") {
    $("#ItemTab").addClass("HeadTabStyleChange");
    $("#Item").show();
  }
  if (ID == "CpcTab") {
    $("#CpcTab").addClass("HeadTabStyleChange");
    $("#Cpc").show();
  }
  if (ID == "SummaryTab") {
    $("#SummaryTab").addClass("HeadTabStyleChange");
    $("#Summary").show();
  }
  if (ID == "AmendTab") {
    $("#AmendTab").addClass("HeadTabStyleChange");
    $("#Amend").show();
  }
  if (ID == "CancelTab") {
    $("#CancelTab").addClass("HeadTabStyleChange");
    $("#Cancel").show();
  }
  if (ID == "RefundTab") {
    $("#RefundTab").addClass("HeadTabStyleChange");
    $("#Refund").show();
  }
}

function ContainerValidSize(selector, value) {
  $(selector).next("span").hide();
  if (value == "--Select--" || value == "") {
    $(selector).next("span").show();
  }
}

function containerValidNum(Select, value) {
  $(Select).next("span").hide();
  var regex = /^[A-Za-z]{4}\d{7}$/;
  if (!regex.test(value)) {
    $(Select).next("span").show();
  }
}

function OutItemAddCasc(Table, Cascname) {
  var rowAdd = `
    <tr>
      <td><input type="text" class="inputStyle" name="${Cascname}"></td>
      <td><input type="text" class="inputStyle" name="${Cascname}"></td>
      <td><input type="text" class="inputStyle" name="${Cascname}"></td>
      <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCasc(this)"></i></td>
    </tr>`;
  $(`${Table} tbody`).append(rowAdd);
}

function DeleteCasc(event) {
  let tr = $(event).closest("tr")
  if (tr.index() == 0) {
    tr.find("input:eq(0)").val("")
    tr.find("input:eq(1)").val("")
    tr.find("input:eq(2)").val("")
  }
  else {
    tr.remove()
  }
}


function ItemCascShow(ID, CLASS) {
  if ($(ID).prop("checked")) {
    $(CLASS).show();
  } else {
    $(CLASS).hide();
  }
}
function ItemCascShowAll(ID, CLASS) {
  if ($(ID).prop("checked")) {
    $(CLASS).show();
  } else {
    $(CLASS).hide();
    $(CLASS + " input").prop("checked", false);
    $(CLASS + " select").val("--Select--")
    $(CLASS + " textarea").val("")
    $(`${CLASS} :input[type="number"]`).val("0.00");
    $(`${CLASS} :input[type="text"]`).val("");
  }
}

function OutCpcADD(Table, NAME, CLASS) {
  if ($(`${Table} tr`).length < 6) {
    var rowAdd = `
      <tr>
        <td><input type="text" class="inputStyle"  name = "${NAME}"></td>
        <td><input type="text" class="inputStyle" name = "${NAME}"></td>
        <td><input type="text" class="inputStyle" name = "${NAME}"></td>
        <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCasc(this)"></i></td>
      </tr>`;
    $(`${Table} tbody`).append(rowAdd);
    $(CLASS).hide();
  } else {
    $(CLASS).show();
  }
  var TableValues = [];
  var Name = document.getElementsByName(NAME);
  for (var i = 0; i < Name.length; i = i + 3) {
    TableValues.push([Name[i].value, Name[i + 1].value, Name[i + 2].value]);
  }
}

function OutCpcHideShow(ID, CLASS, Name) {
  if ($(ID).prop("checked")) {
    $(CLASS).show();
  } else {
    $(CLASS).hide();
  }
}

/*--------------------------------Out Change Select Boxes --------------------------------*/

function OutDeclarationChange() {
  var DeclarationVal = $("#DeclarationType").val();
  $("#InwardTransportModeShowHide").show();
  $("#CoTypeShow").show();
  if (DeclarationVal == "BKT : BLANKET") {
    $("#InwardTransportModeShowHide").hide();
    $("#CoTypeShow").hide();
  } else if (DeclarationVal == "DRT : DIRECT (INCLUDING STORAGE IN FTZ)") {
    $("#InwardTransportModeShowHide").show();
  } else if (DeclarationVal == "--Select--") {
  } else {
    $("#InwardTransportModeShowHide").hide();
  }
}

function OutInwardTrasnPortModeChange() {
  var OutTransPort = $("#OutInwardTransportMode").val();
  $('#InwardMode').val(OutTransPort)
  $('#OutWardDetailsShow').show();
  $("#OutCargoImporterShow").hide();
  $("#OutInwardCarrierShow").hide();
  $("#OutCargoImporterShow input").val("");
  $("#OutInwardCarrierShow input").val("");
  $(".CargoSeaShow").hide();
  $(".CargoRailShow").hide();
  $(".CargoAirShow").hide();
  $('#OutCargoOblShow').hide();
  $('#OutCargoHblShow').hide();
  $(".CargoSeaShow input").val('');
  $(".CargoRailShow input").val('');
  $(".CargoAirShow input").val('');
  if (OutTransPort == "1 : Sea" || OutTransPort == "4 : Air") {
    $("#OutCargoImporterShow").show();
    $("#OutInwardCarrierShow").show();
  }
  else {
    $("#OutCargoImporterShow").show();
  }
  if (OutTransPort == "1 : Sea") {
    $('#OutCargoObl').html('OBL');
    $('#OutCargoHbl').html('HBL');
    $('#OutCargoOblShow').show();
    $('#OutCargoHblShow').show();
    $(".CargoSeaShow").show();
  }
  else if (OutTransPort == "4 : Air") {
    $(".CargoAirShow").show();
    $('#OutCargoObl').html('MAWB');
    $('#OutCargoHbl').html('HAWB');
    $('#OutCargoOblShow').show();
    $('#OutCargoHblShow').show();
  }
  else if (OutTransPort == "N : Not Required" || OutTransPort == "--Select--") {
    $("#OutWardDetailsShow").hide();
    $("#OutWardDetailsShow input").val('');
  }
  else {
    $(".CargoRailShow").show();
    $('#OutCargoObl').html('OBL');
    $('#OutCargoOblShow').show();
  }
}

function OutOutwardTrasnPortModeChange() {
  var OutTransPort = $("#OutOutwardTransportMode").val();
  $('#OutwardMode').val(OutTransPort)
  $('#OutOutWardDetailShow').show();
  $("#OutWardCarrierAgentShow").hide();
  $("#OutWardCarrierAgentShow input").val("");
  $('#OutOutwardSeaShow').hide();
  $('#OutOutwardSeaShow input').val('');
  $('#OutOutRailShow').hide();
  $('#OutOutRailShow input').val('');
  $('#OutOutAirShow').hide();
  $('#OutOutAirShow input').val('');
  if (OutTransPort == "1 : Sea" || OutTransPort == "4 : Air" || OutTransPort == "7 : Pipeline") {
    $("#OutWardCarrierAgentShow").show();
  }
  if (OutTransPort == "1 : Sea") {
    $("#OutOutwardSeaShow").show();
  }
  else if (OutTransPort == "N : Not Required" || OutTransPort == "--Select--") {
    $('#OutOutWardDetailShow').hide();
    $('#OutOutWardDetailShow input').val("");
  }
  else if (OutTransPort == "4 : Air") {
    $('#OutOutAirShow').show();
  }
  else {
    $('#OutOutRailShow').show();
  }
}

function OutCoTypeChange() {
  var CoType = $("#CoType").val();
  $(".PartyManufacturer").hide();
  if (CoType != "--Select--") {
    $(".PartyManufacturer").show();
    $('.CoTxtile').hide()
    if (CoType == "TX : Application for textile products") {
      $('.CoTxtile').show()
    }
    else {
      $('.CoTxtile').hide()
      $("TexCat").val("")
      $('TexQuotaQty').val('0.00')
      $('TexQuotaUOM').val('--Select--')
    }
  } else {
    $(".CoTypeEmpty").val("");
    $(".CoTypeEmptySelect").val("--Select--");
  }
}

function OutReferenceDocument() {
  if ($("#ReferenceDocuments").prop("checked")) {
    $("#OutReferenceShow").show();
  } else {
    $("#OutReferenceShow").hide();
    $(".LicenceHide").val("");
  }
}

function OutCargoPackTypeChange() {
  var PackVal = $('#CargoPackType').val();
  if (PackVal == '9: Containerized') {
    $('#OutContainerShow').show()
  }
  else {
    $('#OutContainerShow').hide()
    $('#OutContainerShow span').hide()
    $('#OutContainerShow input').val("")
    $('#OutContainerShow Select').val("--Select--");
  }
}

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

/*------------------------------------------PARTY PAGE ---------------------------------*/
var Exporter = [];
var Fright = [];
var Consign = [];
var Importer = [];
var Inward = [];
var OutWard = [];
var Frieght = [];
var ManFacture = [];

$(document).ready(() => {
  $.ajax({
    url: "/OutParty/",
    success: (response) => {
      Exporter = response.exporter;
    }
  })
})

$(document).ready(() => {
  $.ajax({
    url: "/OutParty1/",
    success: (response) => {
      Importer = response.importer;
      Inward = response.inward;
      OutWard = response.outward;
      Frieght = response.fright;
      Consign = response.consign;
    }
  })
})

$(document).ready(() => {
  $.ajax({
    url: "/ParytManFacture/",
    success: (response) => {
      ManFacture = response.manfacture;
    }
  })
})

var ReleaseLocation = [];
var ReciptLocation = [];
var LoadingPort = []
$(document).ready(() => {
  $.ajax({
    url: "/CargoLocations/",
    success: (response) => {
      ReleaseLocation = response.releaseLocation;
      ReciptLocation = response.reciptLocation;
      LoadingPort = response.loadingPort;
    }
  })
})

function ExportFocusIn() {
  var myValues = [];
  for (var i of Exporter) {
    myValues.push(i.OutUserCode + ":" + i.OutUserName);
  }
  Autocomplete1(myValues, "#ExporterCode");
}

function ExportFocusOut() {
  let Code = $("#ExporterCode").val().trim()

  if (Code != "") {
    var data = Exporter.filter((obj) => {
      return obj.OutUserCode == Code
    })
    $("#ExporterCruei").val(data[0].OutUserCRUEI)
    $("#ExporterName").val(data[0].OutUserName)
    $("#ExporterName1").val(data[0].OutUserName1)
    $("#ExporterAddress").val(data[0].OutUserAddress)
    $("#ExporterAddress1").val(data[0].OutUserAddress1)
    $("#ExporterCity").val(data[0].OutUserCity)
    $("#ExporterSubCode").val(data[0].OutUserSubCode)
    $("#ExporterSubDivison").val(data[0].OutUserSub)
    $("#ExporterCountry").val(data[0].OutUserCountry)
    $("#ExporterPostalCode").val(data[0].OutUserPostal)
  }
  else {
    $("#ExporterCruei").val("")
    $("#ExporterName").val("")
    $("#ExporterName1").val("")
    $("#ExporterAddress").val("")
    $("#ExporterAddress1").val("")
    $("#ExporterCity").val("")
    $("#ExporterSubCode").val("")
    $("#ExporterSubDivison").val("")
    $("#ExporterCountry").val("")
    $("#ExporterPostalCode").val("")
  }
}

function ImportFocusIn() {
  var myValues = [];
  for (var i of Importer) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#ImporterCode");
}

function ImportFocusOut() {
  let Code = $("#ImporterCode").val().trim()
  if (Code != "") {
    Importer.filter((obj) => {
      if (obj.Code == Code) {
        $("#ImporterCruei").val(obj.CRUEI)
        $("#ImporterName").val(obj.Name)
        $("#ImporterName1").val(obj.Name1)
      }
    })
  }
  else {
    $("#ImporterCruei").val('')
    $("#ImporterName").val('')
    $("#ImporterName1").val('')
  }
}

function InwardFocusIn() {
  var myValues = [];
  for (var i of Inward) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#InwardCode");
}

function InwardFocusOut() {
  let Code = $("#InwardCode").val().trim()
  if (Code != "") {
    Inward.filter((obj) => {
      if (obj.Code == Code) {
        $("#InwardCruei").val(obj.CRUEI)
        $("#InwardName").val(obj.Name)
        $("#InwardName1").val(obj.Name1)
      }
    })
  }
  else {
    $("#InwardCruei").val('')
    $("#InwardName").val('')
    $("#InwardName1").val('')
  }
}

function OutwardFocusIn() {
  var myValues = [];
  for (var i of OutWard) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#OutwardCode");
}

function OutwardFocusOut() {
  let Code = $("#OutwardCode").val().trim()
  if (Code != "") {
    OutWard.filter((obj) => {
      if (obj.Code == Code) {
        $("#OutwardCruei").val(obj.CRUEI)
        $("#OutwardName").val(obj.Name)
        $("#OutwardName1").val(obj.Name1)
      }
    })
  }
  else {
    $("#OutwardCruei").val('')
    $("#OutwardName").val('')
    $("#OutwardName1").val('')
  }
}

function FrieghtFocusIn() {
  var myValues = [];
  for (var i of Frieght) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#FrieghtCode");
}

function FrieghtFocusOut() {
  let Code = $("#FrieghtCode").val().trim()
  if (Code != "") {
    Frieght.filter((obj) => {
      if (obj.Code == Code) {
        $("#FrieghtCruei").val(obj.CRUEI)
        $("#FrieghtName").val(obj.Name)
        $("#FrieghtName1").val(obj.Name1)
      }
    })
  }
  else {
    $("#FrieghtCruei").val('')
    $("#FrieghtName").val('')
    $("#FrieghtName1").val('')
  }
}

function ConsigneFocusIn() {
  var myValues = [];
  for (var i of Consign) {
    myValues.push(i.ConsigneeCode + ":" + i.ConsigneeName);
  }
  Autocomplete1(myValues, "#ConsigneCode");
}

function ConsigneFocusOut() {
  let Code = $("#ConsigneCode").val().trim()

  if (Code != "") {
    var data = Consign.filter((obj) => {
      if (obj.ConsigneeCode == Code) {
        $("#ConsigneCruei").val(obj.ConsigneeCRUEI)
        $("#ConsigneConName").val(obj.ConsigneeName)
        $("#ConsigneName1").val(obj.ConsigneeName1)
        $("#ConsigneAddress").val(obj.ConsigneeAddress)
        $("#ConsigneAddress1").val(obj.ConsigneeAddress1)
        $("#ConsigneCity").val(obj.ConsigneeCity)
        $("#ConsigneSubCountry").val(obj.ConsigneeSub)
        $("#ConsigneSubDivison").val(obj.ConsigneeSubDivi)
        $("#ConsigneCountry").val(obj.ConsigneeCountry)
        $("#ConsignePostal").val(obj.ConsigneePostal)
      }
    })
  }
  else {
    $("#ConsigneCruei").val("")
    $("#ConsigneConName").val("")
    $("#ConsigneName1").val("")
    $("#ConsigneAddress").val("")
    $("#ConsigneAddress1").val("")
    $("#ConsigneCity").val("")
    $("#ConsigneSubCountry").val("")
    $("#ConsigneSubDivison").val("")
    $("#ConsigneCountry").val("")
    $("#ConsignePostal").val("")
  }
}

function EndUserClick() {
  if ($("#EndUserID").prop('checked')) {
    $('.EndUserHide').show()
  }
  else {
    $('.EndUserHide').hide()
    $('.EndUserHide input').val("")
  }
}

function EndConsigneFocusIn() {
  var myValues = [];
  for (var i of Consign) {
    myValues.push(i.ConsigneeCode + ":" + i.ConsigneeName);
  }
  Autocomplete1(myValues, "#EndConsigneCode");
}

function EndConsigneFocusOut() {
  let Code = $("#EndConsigneCode").val().trim()

  if (Code != "") {
    var data = Consign.filter((obj) => {
      if (obj.ConsigneeCode == Code) {
        $("#EndConsigneCruei").val(obj.ConsigneeCRUEI)
        $("#EndConsigneUserName").val(obj.ConsigneeName)
        $("#EndConsigneName1").val(obj.ConsigneeName1)
        $("#EndConsigneAddress").val(obj.ConsigneeAddress)
        $("#EndConsigneAddress1").val(obj.ConsigneeAddress1)
        $("#EndConsigneCity").val(obj.ConsigneeCity)
        $("#EndConsigneSubCode").val(obj.ConsigneeSub)
        $("#EndConsigneSubDivison").val(obj.ConsigneeSubDivi)
        $("#EndConsigneCountry").val(obj.ConsigneeCountry)
        $("#EndConsignePostal").val(obj.ConsigneePostal)
      }
    })
  }
  else {
    $("#EndConsigneCruei").val("")
    $("#EndConsigneUserName").val("")
    $("#EndConsigneName1").val("")
    $("#EndConsigneAddress").val("")
    $("#EndConsigneAddress1").val("")
    $("#EndConsigneCity").val("")
    $("#EndConsigneSubCode").val("")
    $("#EndConsigneSubDivison").val("")
    $("#EndConsigneCountry").val("")
    $("#EndConsignePostal").val("")
  }
}

function CopyConsigne() {
  $("#EndConsigneCode").val($("#ConsigneCode").val())
  $("#EndConsigneCruei").val($("#ConsigneCruei").val())
  $("#EndConsigneUserName").val($("#ConsigneConName").val())
  $("#EndConsigneName1").val($("#ConsigneName1").val())
  $("#EndConsigneAddress").val($("#ConsigneAddress").val())
  $("#EndConsigneAddress1").val($("#ConsigneAddress1").val())
  $("#EndConsigneCity").val($("#ConsigneCity").val())
  $("#EndConsigneSubCode").val($("#ConsigneSubCountry").val())
  $("#EndConsigneSubDivison").val($("#ConsigneSubDivison").val())
  $("#EndConsigneCountry").val($("#ConsigneCountry").val())
  $("#EndConsignePostal").val($("#ConsignePostal").val())
}

function ManFactureFocusIn() {
  var myValues = [];
  for (var i of ManFacture) {
    myValues.push(i.ManufacturerCode + ":" + i.ManufacturerName);
  }
  Autocomplete1(myValues, "#ManuFactureCode");
}

function ManFactureFocusOut() {
  let Code = $("#ManuFactureCode").val().trim()

  if (Code != "") {
    ManFacture.filter((obj) => {
      if (obj.ManufacturerCode == Code) {
        $("#ManuFactureCruei").val(obj.ManufacturerCRUEI)
        $("#ManuFactureName").val(obj.ManufacturerName)
        $("#ManuFactureName1").val(obj.ManufacturerName1)
        $("#ManuFactureAddress").val(obj.ManufacturerAddress)
        $("#ManuFactureAddress1").val(obj.ManufacturerAddress1)
        $("#ManuFactureCity").val(obj.ManufacturerCity)
        $("#ManuFactureSubCode").val(obj.ManufacturerSub)
        $("#ManuFactureSubDivision").val(obj.ManufacturerSubDivi)
        $("#ManuFactureCountry").val(obj.ManufacturerCountry)
        $("#ManuFacturePostal").val(obj.ManufacturerPostal)
      }
    })
  }
  else {
    $("#ManuFactureCruei").val("")
    $("#ManuFactureName").val("")
    $("#ManuFactureName1").val("")
    $("#ManuFactureAddress").val("")
    $("#ManuFactureAddress1").val("")
    $("#ManuFactureCity").val("")
    $("#ManuFactureSubCode").val("")
    $("#ManuFactureSubDivision").val("")
    $("#ManuFactureCountry").val("")
    $("#ManuFacturePostal").val("")
  }
}

function ReleaseLocationFocusIn() {
  var myValues = [];
  for (var i of ReleaseLocation) {
    myValues.push(i.Code + ":" + i.Description);
  }
  Autocomplete1(myValues, "#ReleaseLocaName");
}

function ReleaseLocationFocusOut() {
  let Code = $("#ReleaseLocaName").val().trim().toUpperCase()
  ReleaseLocation.filter((obj) => {
    if (obj.Code == Code) {
      $('#ReleaseLocText').val(obj.Description)
    }
  })
}

function ReciptFocusIn() {
  var myValues = [];
  for (var i of ReciptLocation) {
    myValues.push(i.Code + ":" + i.Description);
  }
  Autocomplete1(myValues, "#ReciptLocationCode");
}

function ReciptFocusOut() {
  let Code = $("#ReciptLocationCode").val().trim().toUpperCase()
  ReciptLocation.filter((obj) => {
    if (obj.Code == Code) {
      $('#RecepitLocName').val(obj.Description)
    }
  })
}

function LoadingPortFocusIn() {
  var myValues = [];
  for (var i of LoadingPort) {
    myValues.push(i.Country + ":" + i.PortName);
  }
  Autocomplete1(myValues, "#LoadingPortCode");
}

function LoadingPortFocusOut() {
  let Code = $("#LoadingPortCode").val().trim().toUpperCase()
  LoadingPort.filter((obj) => {
    if (obj.Country == Code) {
      $('#LoadingPortCodeText').val(obj.PortName)
    }
  })
}
function DischargePortFocusIn() {
  var myValues = [];
  for (var i of LoadingPort) {
    myValues.push(i.Country + ":" + i.PortName);
  }
  Autocomplete1(myValues, "#DischargePort");
}

function DischargePortFocusOut() {
  let Code = $("#DischargePort").val().trim().toUpperCase()
  LoadingPort.filter((obj) => {
    if (obj.Country == Code) {
      $('#DischargePortText').val(obj.PortName)
    }
  })
}

function StorageFocusIn() {
  var myValues = [];
  for (var i of ReciptLocation) {
    myValues.push(i.Code + ":" + i.Description);
  }
  Autocomplete1(myValues, "#StorageCode");
}

function StorageFocusOut() {
  let Code = $("#StorageCode").val().trim().toUpperCase()
  ReciptLocation.filter((obj) => {
    if (obj.Code == Code) {
      $('#StorageText').val(obj.Description)
    }
  })
}
function NextPortFocusIn() {
  var myValues = [];
  for (var i of LoadingPort) {
    myValues.push(i.Country + ":" + i.PortName);
  }
  Autocomplete1(myValues, "#NextPort");
}

function NextPortFocusOut() {
  let Code = $("#NextPort").val().trim().toUpperCase()
  LoadingPort.filter((obj) => {
    if (obj.Country == Code) {
      $('#NextPortText').val(obj.PortName)
    }
  })
}

function LastPortFocusIn() {
  var myValues = [];
  for (var i of LoadingPort) {
    myValues.push(i.Country + ":" + i.PortName);
  }
  Autocomplete1(myValues, "#LastPort");
}

function LastPortFocusOut() {
  let Code = $("#LastPort").val().trim().toUpperCase()
  LoadingPort.filter((obj) => {
    if (obj.Country == Code) {
      $('#LastPortText').val(obj.PortName)
    }
  })
}

function InvoiceCalculation() {
  let result = $("#InvoiceExRate").val() * $("#InvoiceAmount").val()
  $("#InvoiceSumAmount").val(result.toFixed(2))
  $("#InvoiceCifSumAmount").val(result.toFixed(2))
}

function InvoiceExporterFocusIn() {
  var myValues = [];
  for (var i of Exporter) {
    myValues.push(i.OutUserCode + ":" + i.OutUserName);
  }
  Autocomplete1(myValues, "#InviceExporterCode");
}
function InvoiceExporterFocusOut() {
  let Code = $("#InviceExporterCode").val().trim().toUpperCase()

  if (Code != "") {
    var data = Exporter.filter((obj) => {
      return obj.OutUserCode == Code
    })
    $("#InviceExporterCruei").val(data[0].OutUserCRUEI)
    $("#InviceExporterName").val(data[0].OutUserName)
    $("#InviceExporterName1").val(data[0].OutUserName1)
  }
  else {
    $("#InviceExporterCruei").val("")
    $("#InviceExporterName").val("")
    $("#InviceExporterName1").val("")
  }
}

$(function () {
  $("#InvoiceDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#InvoiceDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#InvoiceDate").val(currentDate);
    }
  });
});

$(function () {
  $("#InvDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#InvDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#InvDate").val(currentDate);
    }
  });
});

$(function () {
  $("#ManuDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#ManuDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#ManuDate").val(currentDate);
    }
  });
});


$(function () {
  $("#orignaldatereg").datepicker({ dateFormat: "dd/mm/yy" });
  $("#orignaldatereg").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#orignaldatereg").val(currentDate);
    }
  });
});

$(function () {
  $("#ArrivalDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#ArrivalDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#ArrivalDate").val(currentDate);
    }
  });
});

$(function () {
  $("#BlanketStartDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#BlanketStartDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#BlanketStartDate").val(currentDate);
    }
  });
});

$(function () {
  $("#DepartureDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#DepartureDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#DepartureDate").val(currentDate);
    }
  });
});


function InvoiceDateFunction(Arg) {
  if (Arg == "InvoiceDateInNon") {
    $("#InvoiceDateSpan").hide();
  }
  let x = document.getElementById(Arg);

  if (x.value.length != 0) {
    if (x.value.length == 8) {
      if (x.value[0] + x.value[1] <= 31 && x.value[2] + x.value[3] <= 12) {
        x.value = `${x.value[0] + x.value[1]}/${x.value[2] + x.value[3]}/${x.value[4] + x.value[5] + x.value[6] + x.value[7]
          }`;
      } else {
        x.value = DateTimeCalculation();
      }
    } else if (x.value.length == 10) {
    } else {
      x.value = DateTimeCalculation();
    }
  }
}

function InvoiceSave() {
  let check = true;
  $("#InviceExporterNameSpan").hide()
  $("#InvoiceNumberSpan").hide()
  $("#InvoiceDateSpan").hide()
  $("#InvoiceCurrencySpan").hide()

  if ($("#InviceExporterName").val() == "") {
    $("#InviceExporterNameSpan").show()
    check = false;
  }
  if ($("#InvoiceNumber").val() == "") {
    $("#InvoiceNumberSpan").show()
    check = false;
  }
  if ($("#InvoiceDate").val() == "") {
    $("#InvoiceDateSpan").show()
    check = false;
  }
  if ($("#InvoiceCurrency").val() == "--Select--") {
    $("#InvoiceCurrencySpan").show()
    check = false;
  }

  let InvoiceDate = $("#InvoiceDate").val().split("/");
  InvoiceDate = `${InvoiceDate[2]}/${InvoiceDate[1]}/${InvoiceDate[0]}`;

  $("#Loading").show();

  $.ajax({
    url: "/OutInvoice/",
    type: 'POST',
    data: {
      SNo: $('#InvoiceSerialNumber').val(),
      InvoiceNo: $('#InvoiceNumber').val(),
      InvoiceDate: InvoiceDate,
      TermType: $('#InvoiceTermType').val(),
      AdValoremIndicator: $('#AdValoremIndicator').val(),
      PreDutyRateIndicator: $('#PreferentialDutyRateIndicator').val(),
      SupplierImporterRelationship: $('#InvoiceSupplierImporter').val(),
      SupplierCode: "",
      ExportPartyCode: $('#InviceExporterCode').val(),
      TICurrency: $('#InvoiceCurrency').val(),
      TIExRate: $('#InvoiceExRate').val(),
      TIAmount: $('#InvoiceAmount').val(),
      TISAmount: $('#InvoiceSumAmount').val(),
      OTCCharge: "0.00",
      OTCCurrency: "--Select--",
      OTCExRate: "0.00",
      OTCAmount: "0.00",
      OTCSAmount: "0.00",
      FCCharge: "0.00",
      FCCurrency: "--Select--",
      FCExRate: "0.00",
      FCAmount: "0.00",
      FCSAmount: "0.00",
      ICCharge: "0.00",
      ICCurrency: "--Select--",
      ICExRate: "0.00",
      ICAmount: "0.00",
      ICSAmount: "0.00",
      CIFSUMAmount: $('#InvoiceCifSumAmount').val(),
      GSTPercentage: "8",
      GSTSUMAmount: "0.00",
      MessageType: $('#MessageType').val(),
      PermitId: $('#PermitId').val(),
      TouchTime: TOUCHTIME,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      $("#Loading").hide();
      alert(response.message)
      InvoiceData = response.invoice
      InvoiceReset()
      InvoiceLoadData()
      $('[tabindex="14"]').focus();
    }
  })

}

function InvoiceLoadData() {

  $("#InvoiceSerialNumber").val(Number(InvoiceData.length) + 1).toString().padStart(3, "0")
  var InvData = ''
  var DrpInvoice = '<option>--Select--</option>'
  InvoiceData.forEach((data) => {
    InvData += `<tr>
      <td><i class="fa-regular fa-pen-to-square" style="color: #ff0000;" onclick = "InvoiceEditInNon('${data.SNo}')"></i></td>
      <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick = "InvoiceDeleteInNon('${data.SNo}')"></i></td>
      <td>${data.SNo}</td>
      <td>${data.InvoiceNo}</td>
      <td>${data.InvoiceDate}</td>
      <td>${data.TICurrency}</td>
      <td>${data.TISAmount}</td>
      <td>${data.CIFSUMAmount}</td>
    </tr>`
    DrpInvoice += `<option>${data.InvoiceNo}</option>`
  })

  if (InvoiceData.length == 0) {
    InvData = `<tr>
  <td colspan=8 style='text-align:center'>No Record</td>
  </tr>`
  }
  $('#InvoiceTable tbody').html(InvData)
  $('#DrpInvoiceNo').html(DrpInvoice)
}
function InvoiceDeleteInNon(Id) {
  $("#Loading").show();
  $.ajax({
    url: "/OutInvoice/",
    type: "POST",
    data: {
      method: "DELETE",
      SNo: Id,
      PermitId: $('#PermitId').val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: (response) => {
      $("#Loading").hide();
      InvoiceData = response.invoice
      InvoiceReset()
      InvoiceLoadData()
    }
  })
}

function InvoiceEditInNon(SNO) {
  InvoiceData.filter(
    (data) => {
      if (SNO == data.SNo) {
        $("#InvoiceDate").val(formatDate(data.InvoiceDate));
        $('#InvoiceSerialNumber').val(data.SNo)
        $('#InvoiceNumber').val(data.InvoiceNo)
        $('#InvoiceTermType').val(data.TermType)
        $('#AdValoremIndicator').val(data.AdValoremIndicator)
        if (data.AdValoremIndicator == "True") {
          $('#AdValoremIndicator').prop('checked', true)
        }
        else {
          $('#AdValoremIndicator').prop('checked', false)
        }
        $('#PreferentialDutyRateIndicator').val(data.PreDutyRateIndicator)
        if (data.PreDutyRateIndicator == "True") {
          $('#PreferentialDutyRateIndicator').prop('checked', true)
        }
        else {
          $('#PreferentialDutyRateIndicator').prop('checked', false)
        }
        $('#InvoiceSupplierImporter').val(data.SupplierImporterRelationship)
        $('#InviceExporterCode').val(data.ExportPartyCode)
        $('#InvoiceCurrency').val(data.TICurrency)
        $('#InvoiceExRate').val(data.TIExRate)
        $('#InvoiceAmount').val(data.TIAmount)
        $('#InvoiceSumAmount').val(data.TISAmount)
        $('#InvoiceCifSumAmount').val(data.CIFSUMAmount)
        InvoiceExporterFocusOut()
      }
    }
  )
}

function InvoiceReset() {
  $("#Invoice span").hide();
  $("#Invoice input").val("");
  $("#Invoice select").val("--Select--");
  $("#InvoiceCalculationTable input").val("0.00");
  $("#Invoice input").prop("checked", false);
  $("#AdValoremIndicator").val("False");
  $("#PreferentialDutyRateIndicator").val("False");
  $("#InvoiceSerialNumber").val((Number(InvoiceData.length) + 1).toString().padStart(3, "0")
  );
}

function formatDate(inputDate) {
  const [year, month, day] = inputDate.split("-");
  const formattedDate = `${day}/${month}/${year}`;
  return formattedDate;
}

function CheckFunction(ID) {
  if ($("#" + ID).prop("checked")) {
    $("#" + ID).val("True");
    if ("ItemUnBrand" == ID) {
      $("#Brand").val("UNBRANDED");
    }
  } else {
    $("#" + ID).val("False");
    if ("ItemUnBrand" == ID) {
      $("#Brand").val("");
    }
  }
}

function InNonImporeterSearch(Model1, Head, Code, Cruei, Name, Name1) {
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Model1) {
    tag += `
      <tr onclick="InNonImporeterSearchSelectRow(this,'${Code}','${Cruei}','${Name}','${Name1}')" style="cursor: pointer;">
          <td>${i.OutUserCode}</td>
          <td>${i.OutUserName}</td>
          <td>${i.OutUserName1}</td>
          <td>${i.OutUserCRUEI}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>${Head}</h1>
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

function InNonImporeterSearchSelectRow(Arg, Code, Cruei, Name, Name1) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  let col2 = SelectRow.find("td:eq(1)").text();
  let col3 = SelectRow.find("td:eq(2)").text();
  let col4 = SelectRow.find("td:eq(3)").text();

  $("#" + Code).val(col1);
  $("#" + Name).val(col2);
  $("#" + Name1).val(col3);
  $("#" + Cruei).val(col4);

  $("#InNonImporterSerchId").hide();
}
function CopyExporter(){
  $('#InviceExporterCode').val($('#ExporterCode').val())
  InvoiceExporterFocusOut()
}
var InhouseData = [];
var ChkHsCode = [];
var Country = [];
var inhouseData = fetch('/OutItemInhouse/').then(function (res) {
  return res.json()
}, function (err) {
  return "error"
})
inhouseData.then(function (response) {
  InhouseData = response.inhouse
  ChkHsCode = response.ChkHsCode
  Country = response.country
})

function FinalDestinationfocusin() {
  let tag = " <option>--Select--</option>"
  Country.filter((c) => {
    tag += ` <option>${c.CountryCode} : ${c.Description}</option>`
  })
  $("#FinalDestinationCountry").html(tag)
}

function VesselNationalityFocusIn() {
  let tag = " <option>--Select--</option>"
  Country.filter((c) => {
    tag += ` <option>${c.CountryCode} : ${c.Description}</option>`
  })
  $("#VesselNationality").html(tag)
}

function FinalDestinationfocusout() {
  const DrpFinalDesCountry = $('#FinalDestinationCountry').val()
  if (DrpFinalDesCountry != "--Select--") {
    if (DrpFinalDesCountry == "IR : IRAN (ISLAMIC REP OF)" || DrpFinalDesCountry == "IQ : IRAQ" || DrpFinalDesCountry == "CD : DEMOCRATIC REPUBLIC OF THE CONGO" ||
      DrpFinalDesCountry == "CG : CONGO" || DrpFinalDesCountry == "CI : COTE D'IVOIRE" || DrpFinalDesCountry == "ER : ERITREA" || DrpFinalDesCountry == "KP : KOREA, DEM PEO REP OF" || DrpFinalDesCountry == "LR : LIBERIA" || DrpFinalDesCountry == "SL : SIERRA LEONE") {
      $("#FinalDestinationCountrySpan").html("You have Selected Controlled Country");
    }
    else {
      $("#FinalDestinationCountrySpan").html("");
    }
  }
  else {
    $("#FinalDestinationCountrySpan").html("");
  }
}

function InhouseFocusIn() {
  var myValues = [];
  for (var i of InhouseData) {
    myValues.push(i.InhouseCode + ":" + i.HSCode);
  }
  Autocomplete1(myValues, "#ItemCode");
}

function InhouseFocusOut() {
  let code = $('#ItemCode').val().trim().toUpperCase()
  InhouseData.filter((ans) => {
    if (code == (ans.InhouseCode).trim().toUpperCase()) {
      $('#ItemHsCode').val(ans.HSCode)
      $('#ItmeDescription').val(ans.Description)
      if (ans.Brand == "UNBRANDED") {
        $('#ItemUnBrand').prop("checked", true)
      }
    }
  })
  HsCodeFocusOut()
}

var HsCodeData = []
var hsCodeData = fetch('/OutHscode/').then(function (res) {
  return res.json()
}, function (err) {
  return "error"
})
hsCodeData.then(function (response) {
  HsCodeData = response.hscode
  console.log(HsCodeData)
})

function HsCodeFocusIn() {
  var myValues = [];
  for (var i of HsCodeData) {
    myValues.push(i.HSCode + ":" + i.Description);
  }
  Autocomplete1(myValues, "#ItemHsCode");
}

function HsCodeFocusOut() {
  $("#itemDutiableQtyNone").hide()
  $("#itemAlchoholNone").hide()
  $("#TDQUOM").val('--Select--')
  $("#ddptotDutiableQty").val('--Select--')
  $("#HscodeControl").text('')
  let typeid = 0
  let code = $('#ItemHsCode').val().trim().toUpperCase()
  var HsCodeF = HsCodeData.filter((hs) => {
    if (code == (hs.HSCode).toUpperCase()) {
      return hs
    }
  })
  HsCodeF = HsCodeF[0]
  let hsdesc = true;
  InhouseData.filter((hsd) => {
    if (hsd.HSCode == code) {
      hsdesc = false;
      $('#ItmeDescription').val(hsd.Description)
    }
  })
  try {
    if (hsdesc) {
      $('#ItmeDescription').val(HsCodeF.Description)
    }
    typeid = HsCodeF.DUTYTYPID
    $("#HSQTYUOM").val(HsCodeF.UOM)
    var uom = HsCodeF.DuitableUom
    if (HsCodeF.Out == 1) {
      $("#HscodeControl").text("CONTROLLED ITEM")
    }
    var HSQTYUOM = $("#HSQTYUOM").val()
    if (code.startsWith('87')) {
      var chkhs = ChkHsCode.filter((ch) => {
        if (ch.HsCode == code) {
          return true
        }
      })
      if (chkhs.length > 0) {
        $('#VehicalTypeShow').show()
        $('#EngineCapacityShow').show()
        $('#OriginalShow').show()
      }
      else {
        $('#VehicalTypeShow').hide()
        $('#EngineCapacityShow').hide()
        $('#OriginalShow').hide()
      }
    }
    else {
      $('#VehicalTypeShow').hide()
      $('#EngineCapacityShow').hide()
      $('#OriginalShow').hide()
    }
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
        $("#TDQUOM").val('--Select--')
        $("#ddptotDutiableQty").val('--Select--')
      }
      else {
        $("#TDQUOM").val(uom)
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
        $("#TDQUOM").val('--Select--')
        $("#ddptotDutiableQty").val('--Select--')
      }
      else {
        $("#TDQUOM").val(uom)
        $("#ddptotDutiableQty").val(uom)
      }
    }
    else if (typeid == 61 && HSQTYUOM == "LTR") {
      $("#itemDutiableQtyNone").show()
      $("#itemAlchoholNone").show()
      if (uom == "A") {
        $("#TDQUOM").val('--Select--')
        $("#ddptotDutiableQty").val('--Select--')
      }
      else {
        $("#TDQUOM").val(uom)
        $("#ddptotDutiableQty").val(uom)
      }
    }
    else if (typeid == 61 && HSQTYUOM == "KGM") {
      $("#itemDutiableQtyNone").show()
      if (uom == "A") {
        $("#TDQUOM").val('--Select--')
        $("#ddptotDutiableQty").val('--Select--')
      }
      else {
        $("#TDQUOM").val(uom)
        $("#ddptotDutiableQty").val(uom)
      }
    }
    else {
      $("#itemDutiableQtyNone").hide()
      $("#itemAlchoholNone").hide()

      $('#TxtTotalDutiableQuantity').val("0.00");
      $("#TDQUOM").val('--Select--')
      $('#txtAlcoholPer').val("0.00");
    }
  }
  catch (err) {
    console.log("error")
  }
}

function DutiableQuantityOut() {

  let code = $('#ItemHsCode').val().trim().toUpperCase()
  var HsCodeF = HsCodeData.filter((hs) => {
    if (code == (hs.HSCode).toUpperCase()) {
      return hs
    }
  })
  HsCodeF = HsCodeF[0]
  var kgmvis = HsCodeF.Kgmvisible
  if ($('#TxtTotalDutiableQuantity').val() != "") {
    var T1 = Number($('#TxtIPQty').val())
    var T2 = Number($('#TxtOPQty').val())
    var T3 = Number($('#TxtTotalDutiableQuantity').val())
    var T4 = Number($('#TxtIMPQty').val())
    var T8 = Number($('#TxtINPQty').val())
    var pckqty = 0;
    if (T1 > 0) {
      pckqty = T1;
    }
    if (T2 > 0) {
      if (pckqty > 0) {
        pckqty = pckqty * T2;
      }
      else {
        pckqty = T2;
      }
    }
    if (T4 > 0) {
      if (pckqty > 0) {
        pckqty = pckqty * T4;
      }
      else {
        pckqty = T4;
      }
    }
    if (T8 > 0) {
      if (pckqty > 0) {
        pckqty = pckqty * T8;
      }
      else {
        pckqty = T8;
      }
    }
    var TDQUOM = $("#TDQUOM").val()
    if (T4 == 0 && T8 == 0) {
      if (TDQUOM == "LTR") {
        $('#txttotDutiableQty').val(pckqty * T3)
        $('#TxtHSQuantity').val(pckqty * T3)
      }
      else if (TDQUOM == "KGM" && kgmvis == "MULTIPLE") {
        $('#txttotDutiableQty').val((pckqty * T3))
      }
      else if (TDQUOM == "KGM" && kgmvis == "DIVIDE") {

        $('#txttotDutiableQty').val((pckqty * T3) / 1000)

      }
      else if (TDQUOM == "STK") {
        $('#txttotDutiableQty').val((pckqty * T3) / 1000)
        $('#TxtHSQuantity').val((pckqty * T3) / 1000)
      }
      else if (TDQUOM == "DAL") {
        $('#txttotDutiableQty').val((pckqty * T3))
      }
    }
    else if (T1 != 0 && T2 != 0 && T4 != 0 && T8 != 0) {
      if (TDQUOM == "LTR") {
        $('#txttotDutiableQty').val(T1 * T2 * T3 * T4 * T8)
        $('#TxtHSQuantity').val(T1 * T2 * T3 * T4 * T8)

      }
      else if (TDQUOM == "KGM" && kgmvis == "MULTIPLE") {
        $('#txttotDutiableQty').val((T1 * T2 * T3 * T4 * T8))
      }
      else if (TDQUOM == "KGM" && kgmvis == "DIVIDE") {

        $('#txttotDutiableQty').val((T1 * T2 * T3 * T4 * T8) / 1000)

      }
      else if (TDQUOM == "STK") {

        $('#txttotDutiableQty').val((T1 * T2 * T3 * T4 * T8) / 1000)
        $('#TxtHSQuantity').val((T1 * T2 * T3 * T8 * T4) / 1000)

      }
      else if (TDQUOM == "DAL") {
        $('#txttotDutiableQty').val((T1 * T2 * T3 * T4 * T8))
      }
    }
    else if (T4 != 0 && T8 == 0) {
      if (TDQUOM == "LTR") {
        $('#txttotDutiableQty').val(T1 * T2 * T3 * T4)
        $('#TxtHSQuantity').val(T1 * T2 * T3 * T4)
      }
      else if (TDQUOM == "KGM" && kgmvis == "MULTIPLE") {
        $('#txttotDutiableQty').val((T1 * T2 * T3 * T4))
      }
      else if (TDQUOM == "KGM" && kgmvis == "DIVIDE") {
        $('#txttotDutiableQty').val((T1 * T2 * T3 * T4) / 1000)
      }
      else if (TDQUOM == "STK") {
        $('#txttotDutiableQty').val((T1 * T2 * T3 * T4) / 1000)
        $('#TxtHSQuantity').val((T1 * T2 * T3 * T4) / 1000)

      }
      else if (TDQUOM == "DAL") {
        $('#txttotDutiableQty').val((T1 * T2 * T3 * T4))
      }
    }
    else if (T4 == 0 && T8 != 0) {
      if (TDQUOM == "LTR") {

        $('#txttotDutiableQty').val(T1 * T2 * T3 * T8)
        $('#TxtHSQuantity').val(T1 * T2 * T3 * T8)

      }
      else if (TDQUOM == "KGM" && kgmvis == "MULTIPLE") {

        $('#txttotDutiableQty').val((T1 * T2 * T3 * T8))

      }
      else if (TDQUOM == "KGM" && kgmvis == "DIVIDE") {

        $('#txttotDutiableQty').val((T1 * T2 * T3 * T8) / 1000)

      }
      else if (TDQUOM == "STK") {

        $('#txttotDutiableQty').val((T1 * T2 * T3 * T8) / 1000)
        $('#TxtHSQuantity').val((T1 * T2 * T3 * T8) / 1000)

      }
      else if (TDQUOM == "DAL") {

        $('#txttotDutiableQty').val((T1 * T2 * T3 * T8))

      }
    }
  }
}

function TxtInvQtyOut() {
  let code = $('#ItemHsCode').val().trim().toUpperCase()
  var HsCodeF = HsCodeData.filter((hs) => {
    if (code == (hs.HSCode).toUpperCase()) {
      return hs
    }
  })
  HsCodeF = HsCodeF[0]

  var UOm = HsCodeF.UOM
  $("#TxtHSQuantity").val($('#TxtInvQty').val());
  if (UOm == "TEN" || UOm == "TPR") {
    var a = $('#TxtInvQty').val()
    $("#TxtHSQuantity").val(a / 10)
  }

  else if (UOm == "CEN") {
    var a = $('#TxtInvQty').val()
    $("#TxtHSQuantity").val(Number(a) / 100)
  }
  else if (UOm == "MIL" || UOm == "TNE") {
    var a = $('#TxtInvQty').val()
    $("#TxtHSQuantity").val(Number(a) / 1000)
  }
  else if (UOm == "MTK") {
    var a = $('#TxtInvQty').val()
    $("#TxtHSQuantity").val(a * 3.213)
  }
  else if (UOm == "LTR") {
    var a = $('#TxtInvQty').val()
    $("#TxtHSQuantity").val(a * 1)
  }
  else if (UOm == "KGM" || UOm == "NMB" || UOm == "-") {
    var a = $('#TxtInvQty').val()
    $("#TxtHSQuantity").val(a)
  }

  if ($('#TxtInvQty').val() == "") {
    $('#TxtInvQty').val("0.00")
  }
  if ($('#TxtHSQuantity').val() == "0") {
    $('#TxtHSQuantity').val('0.00')
  }
}

function TxtHSQuantityOut() {
  if ($('#TxtHSQuantity').val() == '') {
    $('#TxtHSQuantity').val('0.00')
  }
}

function DrpInvoiceNoChange() {
  var drop = $('#DrpInvoiceNo').val()
  if (drop == "--Select--") {
    $('#DRPCurrency').val('--Select--')
    $('#TxtExchangeRate').val('0.00')
  }
  InvoiceData.map((e) => {
    if (e.InvoiceNo == drop) {
      $('#DRPCurrency').val(e.TICurrency)
      DRPCurrencyChange()
    }
  })

}

function TxtTotalLineAmountOut() {
  if ($('#TxtTotalLineAmount').val() != "") {

    var T1 = Number($('#TxtTotalLineAmount').val())
    var T2 = Number($('#TxtExchangeRate').val())

    if (T1 != "" && T2 != '') {
      $('#TxtTotalLineCharges').val((T1 * T2).toFixed(2))
    }
  }
  else {
    $('TxtTotalLineAmount').val('0.00')
  }
  if ($('#TxtTotalLineAmount').val() != "") {
    var T1 = Number($('#TxtTotalLineAmount').val())
    var T2 = Number($('#TxtExchangeRate').val())
    var T3 = Number($('#TxtTotalLineCharges').val())



    if (T1 != "" && T2 != "" && T3 != "") {
      $('#TxtCIFFOB').val((T1 * T2).toFixed(2))
    }
  }
  else {
    $('#TxtTotalLineAmount').val('0.00')
  }
}

function ItemCooIn() {
  var myValues = [];
  for (var i of Country) {
    myValues.push(i.CountryCode + ":" + i.Description);
  }
  Autocomplete1(myValues, "#ItemCooInput");
}

function ItemCooOut() {
  let Val = $("#ItemCooInput").val().trim().toUpperCase()
  for (var i of Country) {
    if (i.CountryCode == Val) {
      $("#ItemCooInputText").val(i.Description);
      break;
    }
  }
}

function CooSelectRow(Tag) {
  let SelectRow = $(Tag).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  let col2 = SelectRow.find("td:eq(1)").text();
  $("#ItemCooInput").val(col1);
  $("#ItemCooInputText").val(col2);
  $("#InNonImporterSerchId").hide();
}

function CopyOfHsQty(Input, Uom) {
  $(Input).val($("#TxtHSQuantity").val())
  $(Uom).val($("#HSQTYUOM").val())
}
function ItemCooSearch() {
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Country) {
    tag += `
      <tr onclick="CooSelectRow(this)" style="cursor: pointer;">
          <td>${i.CountryCode}</td>
          <td>${i.Description}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>COUNTRY OF ORGIN</h1>
                  <input type="text" id="CooSearchInputImg" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#CooTable').DataTable().search($('#CooSearchInputImg').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "CooTable">
                      <thead>
                          <th>COUNTRY CODE</th>
                          <th>DESCRIPTION</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#CooTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}

var ItemData = [];
var CascData = [];
var itemfetch = fetch('/OutItem/' + $('#PermitId').val() + "/").then(function (res) {
  return res.json()
}, function (err) {
  return "error"
})

itemfetch.then(function (itemfetch) {
  ItemData = itemfetch.item
  CascData = itemfetch.casc
  ItemLoad()
  $("#Loading").hide();
})

function ItemLoad() {
  $("#ItemNo").val(ItemData.length + 1)
  var td = ""
  ItemData.forEach((item) => {
    td += `<tr>
    <td><input type="checkbox" name="ItemDeleteCheckbox" value = "${item.ItemNo}"></td>
    <td><i class="fa-regular fa-pen-to-square" style="color: #ff0000;" onclick = "ItemEdit('${item.ItemNo}')"></i></td>
    <td>${item.ItemNo}</td>
    <td>${item.HSCode}</td>
    <td>${item.Description}</td>
    <td>${item.Contry}</td>
    <td>${item.InHAWBOBL}</td>
    <td>${item.OutHAWBOBL}</td>
    <td>${item.UnitPriceCurrency}</td>
    <td>${item.CIFFOB}</td>
    <td>${item.HSQty}</td>
    <td>${item.HSUOM}</td>
    <td>${item.TotalLineAmount}</td>
    </tr>
    `
  })
  if (ItemData.length == 0) {
    td = `<tr>
            <td colspan=14 style='text-align:center'>No Record</td>
          </tr>`
  }
  $("#ItemTable tbody").html(td)
}

function OutItemSave() {

  let ItmCheck = true;
  $('#ItemHsCodeSpan').hide()
  $('#ItmeDescriptionSpan').hide()
  $('#ItemCooInputSpan').hide()
  $('#BrandSpan').hide()
  $('#TxtHSQuantitySpan').hide()
  $('#TxtTotalLineAmountSpan').hide()

  if ($('#ItemHsCode').val() == "") {
    ItmCheck = false;
    $('#ItemHsCodeSpan').show()
  }

  if ($('#ItmeDescription').val() == "") {
    ItmCheck = false;
    $('#ItmeDescriptionSpan').show()
  }

  if ($('#ItemCooInput').val() == "") {
    ItmCheck = false;
    $('#ItemCooInputSpan').show()
  }

  if ($('#Brand').val() == "") {
    ItmCheck = false;
    $('#BrandSpan').show()
  }

  if ($('#Brand').val() == "") {
    ItmCheck = false;
    $('#BrandSpan').show()
  }

  if ($('#TxtHSQuantity').val() <= 0) {
    ItmCheck = false;
    $('#TxtHSQuantitySpan').show()
  }

  if ($('#TxtTotalLineAmount').val() <= 0) {
    ItmCheck = false;
    $('#TxtTotalLineAmountSpan').show()
  }

  let OrginalDate = ""
  if ($('#orignaldatereg').val() != "") {
    OrginalDate = $("#orignaldatereg").val().split("/");
    OrginalDate = `${OrginalDate[2]}/${OrginalDate[1]}/${OrginalDate[0]}`;
  }

  let InvDate = ""
  if ($('#orignaldatereg').val() != "") {
    InvDate = $("#orignaldatereg").val().split("/");
    InvDate = `${InvDate[2]}/${InvDate[1]}/${InvDate[0]}`;
  }

  let ManuDate = ""
  if ($('#orignaldatereg').val() != "") {
    ManuDate = $("#orignaldatereg").val().split("/");
    ManuDate = `${ManuDate[2]}/${ManuDate[1]}/${ManuDate[0]}`;
  }
  if (ItmCheck) {
    $("#Loading").show()
    $.ajax({
      url: "/OutItem/",
      type: "POST",
      data: {
        CascDatas: JSON.stringify(CascSave()),
        ItemNo: $('#ItemNo').val().trim().toUpperCase(),
        PermitId: $('#PermitId').val().trim().toUpperCase(),
        MessageType: $('#MessageType').val().trim().toUpperCase(),
        HSCode: $('#ItemHsCode').val().trim().toUpperCase(),
        Description: $('#ItmeDescription').val().trim().toUpperCase(),
        DGIndicator: $('#ItemDgIndicator').val().trim().toUpperCase(),
        Contry: $('#ItemCooInput').val().trim().toUpperCase(),
        EndUserDescription: "",//$('#EndUserDescription').val().trim().toUpperCase(),
        Brand: $('#Brand').val().trim().toUpperCase(),
        Model: $('#Model').val().trim().toUpperCase(),
        InHAWBOBL: $('#InHAWBOBL').val(),
        OutHAWBOBL: $('#OutHAWBOBL').val(),
        DutiableQty: $('#TxtTotalDutiableQuantity').val().trim().toUpperCase(),
        DutiableUOM: $('#TDQUOM').val().trim(),
        TotalDutiableQty: $('#txttotDutiableQty').val().trim().toUpperCase(),
        TotalDutiableUOM: $('#ddptotDutiableQty').val().trim().toUpperCase(),
        InvoiceQuantity: $('#TxtInvQty').val().trim().toUpperCase(),
        HSQty: $('#TxtHSQuantity').val().trim().toUpperCase(),
        HSUOM: $('#HSQTYUOM').val().trim(),
        AlcoholPer: $('#txtAlcoholPer').val().trim().toUpperCase(),
        InvoiceNo: $('#DrpInvoiceNo').val().trim().toUpperCase(),
        ChkUnitPrice: $('#itemCheckUnitPrice').val().trim().toUpperCase(),
        UnitPrice: $('#UnitPrice').val().trim().toUpperCase(),
        UnitPriceCurrency: $('#DRPCurrency').val().trim().toUpperCase(),
        ExchangeRate: $('#TxtExchangeRate').val().trim().toUpperCase(),
        SumExchangeRate: $('#SumExchangeRate').val().trim().toUpperCase(),
        TotalLineAmount: $('#TxtTotalLineAmount').val().trim().toUpperCase(),
        InvoiceCharges: $('#TxtTotalLineCharges').val().trim().toUpperCase(),
        CIFFOB: $('#TxtCIFFOB').val().trim().toUpperCase(),
        OPQty: $('#TxtOPQty').val().trim().toUpperCase(),
        OPUOM: $('#OPUOM').val().trim(),
        IPQty: $('#TxtIPQty').val().trim().toUpperCase(),
        IPUOM: $('#IPUOM').val().trim(),
        InPqty: $('#TxtINPQty').val().trim().toUpperCase(),
        InPUOM: $('#TxtINPQtyUom').val().trim(),
        ImPQty: $('#TxtIMPQty').val().trim().toUpperCase(),
        ImPUOM: $('#ImPUOM').val().trim(),
        PreferentialCode: $('#itemPreferntialCode').val(),
        GSTRate: 7,
        GSTUOM: "PER",
        GSTAmount: "0.00",
        ExciseDutyRate: "0.00",
        ExciseDutyUOM: "--Select--",
        ExciseDutyAmount: "0.00",
        CustomsDutyRate: "0.00",
        CustomsDutyUOM: "--Select--",
        CustomsDutyAmount: "0.00",
        OtherTaxRate: "0.00",
        OtherTaxUOM: "--Select--",
        OtherTaxAmount: "0.00",
        CurrentLot: $('#TxtCurrentLot').val().trim().toUpperCase(),
        PreviousLot: $('#TxtPreviousLot').val().trim().toUpperCase(),
        Making: $('#DrpMaking').val(),
        ShippingMarks1: $('#txtShippingMarks1').val().trim().toUpperCase(),
        ShippingMarks2: $('#txtShippingMarks2').val().trim().toUpperCase(),
        ShippingMarks3: $('#txtShippingMarks3').val().trim().toUpperCase(),
        ShippingMarks4: $('#txtShippingMarks4').val().trim().toUpperCase(),
        CerItemQty: $('#TxtCerItemQty').val().trim().toUpperCase(),
        CerItemUOM: $('#DrpCerItemUOM').val().trim(),
        CIFValOfCer: $('#TxtCIFCer').val().trim().toUpperCase(),
        ManufactureCostDate: ManuDate,
        TexCat: $('#TexCat').val().trim().toUpperCase(),
        TexQuotaQty: $('#TexQuotaQty').val().trim().toUpperCase(),
        TexQuotaUOM: $('#TexQuotaUOM').val().trim(),
        CerInvNo: $('#TxtCerInvoice').val().trim().toUpperCase(),
        CerInvDate: InvDate,
        OriginOfCer: $('#OriginDes1').val().trim().toUpperCase() + $('#OriginDes2').val().trim().toUpperCase() + $('#OriginDes3').val().trim().toUpperCase(),
        HSCodeCer: $('#TxtHSCodeCer').val().trim().toUpperCase(),
        PerContent: $('#TxtPerOrigin').val().trim().toUpperCase(),
        CertificateDescription: $('#TxtCerDes').val().trim().toUpperCase(),
        VehicleType: $('#VehicalTypeUom').val(),
        OptionalChrgeUOM: $('#OptionalChrgeUOM').val().trim(),
        EngineCapcity: $('#EngineCapacity').val().trim().toUpperCase(),
        Optioncahrge: $('#Optioncahrge').val().trim().toUpperCase(),
        OptionalSumtotal: $('#OptionalSumtotal').val().trim().toUpperCase(),
        OptionalSumExchage: $('#OptionalSumExchage').val().trim().toUpperCase(),
        EngineCapUOM: $('#EngineCapacityUom').val().trim(),
        orignaldatereg: OrginalDate,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: (data) => {
        ItemData = data.item
        CascData = data.casc
        $("#Loading").hide()
        alert(data.message)
        ItemLoad()
        ItemReset()
      }
    })
  }
  else {
    alert("PLEASE CHECK THE ALL MANDATORY ")
  }

}

function ItemReset() {
  $("#Item span").hide();
  $("#Item input").prop("checked", false);
  $('#Item :input[type="number"]').val("0.00");
  $('#Item :input[type="text"]').val("");
  $("#Item select").val("--Select--");
  $("#Item textarea").val("");
  ItemCascShowAll("#packing_details", ".PackingDetails");
  ItemCascShowAll("#itemCascID", ".OutItemCascHide");
  ItemCascShowAll("#shippingMarkCheck", ".ShippingMark");
  ItemCascShowAll("#lotIdCheck", ".OutLotId");
  $(".OutItemCascHide p").html("");
  $("#ItemNo").val(ItemData.length + 1);
  HsCodeFocusOut()
}

function CascSave() {
  var cascArray = [];
  var casc1 = document.getElementsByName("Casc1");
  var casc2 = document.getElementsByName("Casc2");
  var casc3 = document.getElementsByName("Casc3");
  var casc4 = document.getElementsByName("Casc4");
  var casc5 = document.getElementsByName("Casc5");

  if ($("#itemProductCode1").val() != "") {
    var row1 = 1;
    for (var i = 0; i < casc1.length; i += 3) {
      cascArray.push({
        ProductCode: $("#itemProductCode1").val(),
        Quantity: $("#product1CodeCopyInput").val(),
        ProductUOM: $("#product1CodeCopyUom").val(),
        RowNo: row1,
        CascCode1: casc1[i].value,
        CascCode2: casc1[i + 1].value,
        CascCode3: casc1[i + 2].value,
        CASCId: "Casc1",
        EndUserDes: $('#EndUserDes1').val().trim()
      });
      row1 += 1;
    }
  }

  if ($("#itemProductCode2").val() != "") {
    var row2 = 1;
    for (var i = 0; i < casc2.length; i += 3) {
      cascArray.push({
        ProductCode: $("#itemProductCode2").val(),
        Quantity: $("#product2CodeCopyInput").val(),
        ProductUOM: $("#product2CodeCopyUom").val(),
        RowNo: row2,
        CascCode1: casc2[i].value,
        CascCode2: casc2[i + 1].value,
        CascCode3: casc2[i + 2].value,
        CASCId: "Casc2",
        EndUserDes: $('#EndUserDes2').val().trim()
      });
      row2 += 1;
    }
  }

  if ($("#itemProductCode3").val() != "") {
    var row3 = 1;
    for (var i = 0; i < casc3.length; i += 3) {
      cascArray.push({
        ProductCode: $("#itemProductCode3").val(),
        Quantity: $("#product3CodeCopyInput").val(),
        ProductUOM: $("#product3CodeCopyUom").val(),
        RowNo: row3,
        CascCode1: casc3[i].value,
        CascCode2: casc3[i + 1].value,
        CascCode3: casc3[i + 2].value,
        CASCId: "Casc3",
        EndUserDes: $('#EndUserDes3').val().trim()
      });
      row3 += 1;
    }
  }

  if ($("#itemProductCode4").val() != "") {
    var row4 = 1;
    for (var i = 0; i < casc4.length; i += 3) {
      cascArray.push({
        ProductCode: $("#itemProductCode4").val(),
        Quantity: $("#product4CodeCopyInput").val(),
        ProductUOM: $("#product4CodeCopyUom").val(),
        RowNo: row4,
        CascCode1: casc4[i].value,
        CascCode2: casc4[i + 1].value,
        CascCode3: casc4[i + 2].value,
        CASCId: "Casc4",
        EndUserDes: $('#EndUserDes4').val().trim()
      });
      row4 += 1;
    }
  }

  if ($("#itemProductCode5").val() != "") {
    var row5 = 1;
    for (var i = 0; i < casc5.length; i += 3) {
      cascArray.push({
        ProductCode: $("#itemProductCode5").val(),
        Quantity: $("#product5CodeCopyInput").val(),
        ProductUOM: $("#product5CodeCopyUom").val(),
        RowNo: row5,
        CascCode1: casc5[i].value,
        CascCode2: casc5[i + 1].value,
        CascCode3: casc5[i + 2].value,
        CASCId: "Casc5",
        EndUserDes: $('#EndUserDes5').val().trim()
      });
      row5 += 1;
    }
  }
  return cascArray;
}

function ItemEdit(itemnumber) {
  ItemReset()
  ItemData.forEach((items) => {
    if (itemnumber == items.ItemNo) {
      $('#ItemNo').val(items.ItemNo)
      $('#ItemHsCode').val(items.HSCode)
      $('#ItmeDescription').val(items.Description)
      $('#ItemDgIndicator').val(items.DGIndicator)
      $('#ItemCooInput').val(items.Contry)
      $('#Brand').val(items.Brand)
      $('#Model').val(items.Model)
      $('#InHAWBOBL').html(`<option>${items.InHAWBOBL}</option>`)
      $('#OutHAWBOBL').html(`<option>${items.OutHAWBOBL}</option>`)
      $('#TxtTotalDutiableQuantity').val(items.DutiableQty)
      $('#TDQUOM').val(items.DutiableUOM)
      $('#txttotDutiableQty').val(items.TotalDutiableQty)
      $('#ddptotDutiableQty').val(items.TotalDutiableUOM)
      $('#TxtInvQty').val(items.InvoiceQuantity)
      $('#TxtHSQuantity').val(items.HSQty)
      $('#HSQTYUOM').val(items.HSUOM)
      $('#txtAlcoholPer').val(items.AlcoholPer)
      $('#DrpInvoiceNo').val(items.InvoiceNo)
      $('#itemCheckUnitPrice').val(items.ChkUnitPrice)
      $('#UnitPrice').val(items.UnitPrice)
      $('#DRPCurrency').val(items.UnitPriceCurrency)
      $('#TxtExchangeRate').val(items.ExchangeRate)
      $('#SumExchangeRate').val(items.SumExchangeRate)
      $('#TxtTotalLineAmount').val(items.TotalLineAmount)
      $('#TxtTotalLineCharges').val(items.InvoiceCharges)
      $('#TxtCIFFOB').val(items.CIFFOB)
      $('#TxtOPQty').val(items.OPQty)
      $('#OPUOM').val(items.OPUOM)
      $('#TxtIPQty').val(items.IPQty)
      $('#IPUOM').val(items.IPUOM)
      $('#TxtINPQty').val(items.InPqty)
      $('#TxtINPQtyUom').val(items.InPUOM)
      $('#TxtIMPQty').val(items.ImPQty)
      $('#ImPUOM').val(items.ImPUOM)
      $('#itemPreferntialCode').val(items.PreferentialCode)
      $('#TxtCurrentLot').val(items.CurrentLot)
      $('#TxtPreviousLot').val(items.PreviousLot)
      $('#DrpMaking').val(items.Making)
      $('#txtShippingMarks1').val(items.ShippingMarks1)
      $('#txtShippingMarks2').val(items.ShippingMarks2)
      $('#txtShippingMarks3').val(items.ShippingMarks3)
      $('#txtShippingMarks4').val(items.ShippingMarks4)
      $('#TxtCerItemQty').val(items.CerItemQty)
      $('#DrpCerItemUOM').val(items.CerItemUOM)
      $('#TxtCIFCer').val(items.CIFValOfCer)
      // ManufactureCostDate: ManuDate,
      $('#TexCat').val(items.TexCat)
      $('#TexQuotaQty').val(items.TexQuotaQty)
      $('#TexQuotaUOM').val(items.TexQuotaUOM)
      $('#TxtCerInvoice').val(items.CerInvNo)
      // CerInvDate: InvDate,
      // OriginOfCer: $('#OriginDes1').val().trim().toUpperCase() + $('#OriginDes2').val().trim().toUpperCase() + $('#OriginDes3').val().trim().toUpperCase(),
      $('#TxtHSCodeCer').val(items.HSCodeCer)
      $('#TxtPerOrigin').val(items.PerContent)
      $('#TxtCerDes').val(items.CertificateDescription)
      $('#VehicalTypeUom').val(items.VehicleType)
      $('#OptionalChrgeUOM').val(items.OptionalChrgeUOM)
      $('#EngineCapacity').val(items.EngineCapcity)
      $('#Optioncahrge').val(items.Optioncahrge)
      $('#OptionalSumtotal').val(items.OptionalSumtotal)
      $('#OptionalSumExchage').val(items.OptionalSumExchage)
      $('#EngineCapacityUom').val(items.EngineCapUOM)
      // orignaldatereg: OrginalDate,
      HsCodeFocusOut()
      ItemCooOut()
      if (items.OPQty > 0 || items.IPQty > 0 || items.InPqty > 0 || items.ImPQty > 0) {
        $('#packing_details').prop('checked', true)
        ItemCascShowAll('#packing_details', '.PackingDetails')
      }
      if (items.ShippingMarks1 != "" || items.ShippingMarks2 != "" || items.ShippingMarks3 != "" || items.ShippingMarks4 != "") {
        $('#shippingMarkCheck').prop('checked', true)
        ItemCascShowAll('#shippingMarkCheck', '.ShippingMark')
      }
      if (items.CurrentLot != "" || items.PreviousLot != "" || items.Making != '--Select--') {
        $('#lotIdCheck').prop('checked', true)
        ItemCascShowAll('#lotIdCheck', '.OutLotId')
      }
      var cascResult = CascData.filter((data) => data.ItemNo == itemnumber ? data : "")
      if (cascResult.length > 0) {
        $('#itemCascID').prop('checked', true)
        ItemCascShowAll('#itemCascID', '.OutItemCascHide')
        CascLoad(cascResult)
      }
    }
  })
}

function CascLoad(cascResult) {
  let cascTable1 = ""
  let cascTable2 = ""
  let cascTable3 = ""
  let cascTable4 = ""
  let cascTable5 = ""
  cascResult.forEach((datas) => {
    if (datas.CASCId == 'Casc1') {
      $('#itemProductCode1').val(datas.ProductCode)
      $('#product1CodeCopyInput').val(datas.Quantity)
      $('#product1CodeCopyUom').val(datas.ProductUOM)
      $('#EndUserDes1').val(datas.EndUserDes)
      cascTable1 += `
        <tr>
          <td><input type="text" class="inputStyle" name="Casc1" value = "${datas.CascCode1}"></td>
          <td><input type="text" class="inputStyle" name="Casc1" value = "${datas.CascCode2}"></td>
          <td><input type="text" class="inputStyle" name="Casc1" value = "${datas.CascCode3}"></td>
          <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCasc(this)"></i></td>
        </tr>
      `
    }
    if (datas.CASCId == 'Casc2') {
      $('#itemProductCode2').val(datas.ProductCode)
      $('#product2CodeCopyInput').val(datas.Quantity)
      $('#product2CodeCopyUom').val(datas.ProductUOM)
      $('#EndUserDes2').val(datas.EndUserDes)
      cascTable2 += `
        <tr>
          <td><input type="text" class="inputStyle" name="Casc2" value = "${datas.CascCode1}"></td>
          <td><input type="text" class="inputStyle" name="Casc2" value = "${datas.CascCode2}"></td>
          <td><input type="text" class="inputStyle" name="Casc2" value = "${datas.CascCode3}"></td>
          <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCasc(this)"></i></td>
        </tr>
      `
    }
    if (datas.CASCId == 'Casc3') {
      $("#ProductCode3").prop("checked", true)
      ItemCascShow('#ProductCode3', '.OutCasc3')
      $('#itemProductCode3').val(datas.ProductCode)
      $('#product3CodeCopyInput').val(datas.Quantity)
      $('#product3CodeCopyUom').val(datas.ProductUOM)
      $('#EndUserDes3').val(datas.EndUserDes)
      cascTable3 += `
        <tr>
          <td><input type="text" class="inputStyle" name="Casc3" value = "${datas.CascCode1}"></td>
          <td><input type="text" class="inputStyle" name="Casc3" value = "${datas.CascCode2}"></td>
          <td><input type="text" class="inputStyle" name="Casc3" value = "${datas.CascCode3}"></td>
          <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCasc(this)"></i></td>
        </tr>
      `
    }
    if (datas.CASCId == 'Casc4') {
      $("#ProductCode4").prop("checked", true)
      ItemCascShow('#ProductCode4', '.OutCasc4')
      $('#itemProductCode4').val(datas.ProductCode)
      $('#product4CodeCopyInput').val(datas.Quantity)
      $('#product4CodeCopyUom').val(datas.ProductUOM)
      $('#EndUserDes4').val(datas.EndUserDes)
      cascTable4 += `
        <tr>
          <td><input type="text" class="inputStyle" name="Casc4" value = "${datas.CascCode1}"></td>
          <td><input type="text" class="inputStyle" name="Casc4" value = "${datas.CascCode2}"></td>
          <td><input type="text" class="inputStyle" name="Casc4" value = "${datas.CascCode3}"></td>
          <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCasc(this)"></i></td>
        </tr>
      `
    }
    if (datas.CASCId == 'Casc5') {
      $("#ProductCode5").prop("checked", true)
      ItemCascShow('#ProductCode5', '.OutCasc5')
      $('#itemProductCode5').val(datas.ProductCode)
      $('#product5CodeCopyInput').val(datas.Quantity)
      $('#product5CodeCopyUom').val(datas.ProductUOM)
      $('#EndUserDes5').val(datas.EndUserDes)
      cascTable5 += `
        <tr>
          <td><input type="text" class="inputStyle" name="Casc5" value = "${datas.CascCode1}"></td>
          <td><input type="text" class="inputStyle" name="Casc5" value = "${datas.CascCode2}"></td>
          <td><input type="text" class="inputStyle" name="Casc5" value = "${datas.CascCode3}"></td>
          <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCasc(this)"></i></td>
        </tr>
      `
    }
  })
  if (cascTable1 != "") {
    $("#OutItemCascTable1 tbody").html(cascTable1)
  }
  if (cascTable2 != "") {
    $("#OutItemCascTable2 tbody").html(cascTable2)
  }
  if (cascTable3 != "") {
    $("#OutItemCascTable3 tbody").html(cascTable3)
  }
  if (cascTable4 != "") {
    $("#OutItemCascTable4 tbody").html(cascTable4)
  }
  if (cascTable5 != "") {
    $("#OutItemCascTable5 tbody").html(cascTable5)
  }
}
function DeleteItem() {
  let arr = []
  document.getElementsByName("ItemDeleteCheckbox").forEach((e) => e.checked ? arr.push(e.value) : null)
  if (arr.length > 0) {
    $.ajax({
      url: "/OutItemDelete/",
      type: "POST",
      data: {
        Ids: JSON.stringify(arr),
        PermitId: $('#PermitId').val().toUpperCase(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: () => console.log("succes")
    })
  }
}

function DefrentprintingClick() {
  if ($('#Defrentprinting').prop("checked")) {
    $('#Defrentprinting').val("True")
  }
  else {
    $('#Defrentprinting').val("False")
  }
}

function CnbClick() {
  if ($('#OutCnb').prop("checked")) {
    $('#OutCnb').val("True")
  }
  else {
    $('#OutCnb').val("False")
  }
}

function AllDataSave() {
  let Check = true;
  let InvoiceCheck = ""
  if (InvoiceData.length === 0) {
    Check = false;
  }
  if (Check) {
    OutfinalSave()
  }

}
function OutfinalSave() {
  const url = "/outSaveSubmit/"
  try {
    $.ajax({
      url: url,
      type: "POST",
      data: {
        Refid: $('#Refid').val(),
        JobId: $('#JobId').val(),
        MSGId: $('#MSGId').val(),
        PermitId: $('#PermitId').val().toUpperCase(),
        TradeNetMailboxID: $('#MailBoxId').val(),
        MessageType: $('#MessageType').val(),
        DeclarationType: $('#DeclarationType').val(),
        PreviousPermit: $('#PreviousPermitNo').val(),
        CargoPackType: $('#CargoPackType').val(),
        InwardTransportMode: $('#OutInwardTransportMode').val(),
        OutwardTransportMode: $('#OutOutwardTransportMode').val(),
        BGIndicator: $('#BgIndicator').val(),
        SupplyIndicator: $('#SupplyIndicator').val(),
        ReferenceDocuments: $('#ReferenceDocuments').val(),
        License: $('#licence1').val() + "," + $('#licence2').val() + "," + $('#licence3').val() + "," + $('#licence4').val() + "," + $('#licence5').val(),
        COType: $('#CoType').val(),
        Entryyear: "",//$('#Entryyear').val(),//dont save
        GSPDonorCountry: "",//$('#GSPDonorCountry').val(),//dont save
        CerDetailtype1: $('#CertificateType1').val(),
        CerDetailCopies1: $('#CerDetailCopies1').val(),
        CerDetailtype2: $('#CertificateType2').val(),
        CerDetailCopies2: $('#CerDetailCopies2').val(),
        PerCommon: "",//$('#PerCommon').val(),//dont save
        CurrencyCode: $('#CurrencyCode').val(),
        AddCerDtl: $('#AddCerDtl1').val() + "-" + $('#AddCerDtl2').val() + "-" + $('#AddCerDtl3').val() + "-" + $('#AddCerDtl4').val() + "-" + $('#AddCerDtl5').val(),
        TransDtl: $('#TransDtl1').val() + "-" + $('#TransDtl2').val() + "-" + $('#TransDtl3').val() + "-" + $('#TransDtl4').val() + "-" + $('#TransDtl5').val(),
        Recipient: $('#Recipient1').val() + "-" + $('#Recipient2').val() + "-" + $('#Recipient3').val(),
        DeclarantCompanyCode: $('#DeclarantCompanyCode').val(),
        ExporterCompanyCode: $('#ExporterCode').val().trim().toUpperCase(),
        Inwardcarriercode: $('#InwardCode').val().trim().toUpperCase(),//
        OutwardCarrierAgentCode: $('#OutwardCode').val().trim().toUpperCase(),
        FreightForwarderCode: $('#FrieghtCode').val().trim().toUpperCase(),
        ImporterCompanyCode: $('#ImporterCode').val().trim().toUpperCase(),
        InwardCarrierAgentCode: $('#InwardCode').val().trim().toUpperCase(),
        CONSIGNEECode: $('#ConsigneCode').val().trim().toUpperCase(),
        EndUserCode: $('#EndConsigneCode').val().trim().toUpperCase(),
        Manufacturer: $('#ManuFactureCode').val().trim().toUpperCase(),
        ArrivalDate: $('#ArrivalDate').val(),
        ArrivalTime: $('#ArrivalTime').val(),
        LoadingPortCode: $('#LoadingPortCode').val().trim().toUpperCase(),
        VoyageNumber: $('#VoyageNumber').val().trim().toUpperCase(),
        VesselName: $('#VesselName').val().trim().toUpperCase(),
        OceanBillofLadingNo: $('#OceanBillofLadingNo').val(),
        ConveyanceRefNo: $('#ConveyanceRefNo').val().trim().toUpperCase(),
        TransportId: $('#TransportId').val().trim().toUpperCase(),
        FlightNO: $('#FlightNO').val().trim().toUpperCase(),
        AircraftRegNo: $('#AircraftRegNo').val().trim().toUpperCase(),
        MasterAirwayBill: $('#MasterAirwayBill').val(),//
        ReleaseLocation: $('#ReleaseLocaName').val(),
        RecepitLocation: $('#ReciptLocationCode').val(),
        StorageLocation: $('#StorageCode').val(),
        BlanketStartDate: $('#BlanketStartDate').val(),
        DepartureDate: $('#DepartureDate').val(),
        DepartureTime: $('#DepartureTime').val(),
        DischargePort: $('#DischargePort').val().trim().toUpperCase(),
        FinalDestinationCountry: $('#FinalDestinationCountry').val().trim().toUpperCase(),
        OutVoyageNumber: $('#OutVoyageNumber').val().trim().toUpperCase(),
        OutVesselName: $('#OutVesselName').val().trim().toUpperCase(),
        OutOceanBillofLadingNo: $('#OutOceanBillofLadingNo').val().trim().toUpperCase(),
        VesselType: $('#VesselType').val(),
        VesselNetRegTon: $('#VesselNetRegTon').val(),
        VesselNationality: $('#VesselNationality').val(),
        TowingVesselID: $('#TowingVesselID').val().trim().toUpperCase(),
        TowingVesselName: $('#TowingVesselName').val(),
        NextPort: $('#NextPort').val().trim().toUpperCase(),
        LastPort: $('#LastPort').val().trim().toUpperCase(),
        OutConveyanceRefNo: $('#OutConveyanceRefNo').val(),
        OutTransportId: $('#OutTransportId').val(),
        OutFlightNO: $('#OutFlightNO').val(),
        OutAircraftRegNo: $('#OutAircraftRegNo').val(),
        OutMasterAirwayBill: $('#OutMasterAirwayBill').val(),//
        TotalOuterPack: $('#TotalOuterPack').val(),
        TotalOuterPackUOM: $('#TotalOuterPackUOM').val(),
        TotalGrossWeight: $('#TotalGrossWeight').val(),
        TotalGrossWeightUOM: $('#TotalGrossWeightUOM').val(),
        GrossReference: $('#GrossReference').val(),
        TradeRemarks: $('#TradeRemarks').val(),
        InternalRemarks: $('#InternalRemarks').val(),
        DeclareIndicator: $('#DeclareIndicator').val(),
        NumberOfItems: $('#NumberOfItems').val(),
        TotalCIFFOBValue: $('#TotalCIFFOBValue').val(),
        TotalGSTTaxAmt: "0.00",
        TotalExDutyAmt: "0.00",
        TotalCusDutyAmt: "0.00",
        TotalODutyAmt: "0.00",
        TotalAmtPay: "0.00",
        Status: "NEW",
        PermitNumber: "PermitNumber",
        prmtStatus: "prmtStatus",
        ResLoaName: $('#ReleaseLocText').val(),
        RepLocName: $('#RecepitLocName').val(),
        RecepitLocName: $('#RecepitLocName').val(),
        outHAWB: $('#Hbl').val(),
        INHAWB: $('#Hawb').val(),
        CertificateNumber: "",
        Defrentprinting: $('#Defrentprinting').val(),
        Cnb: $('#OutCnb').val(),
        DeclarningFor: $('#DeclaringFor').val(),
        MRDate: $('#MRDate').val(),
        MRTime: $('#MRTime').val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: ((response) => {
        console.log(response);
      })
    })
  }
  catch (err) {
    console.log("The Error is : ", err)
  }
}
