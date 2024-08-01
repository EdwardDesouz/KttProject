var InvoiceData = [];
var ItemData = [];
var InhouseItemCode = [];
var ItemHsCodeData = [];
var ItemCascData = [];
var InFile = [];
var ChkHsCode = [];
const NowDate = new Date();
const TOUCHTIME = NowDate.toISOString().slice(0, 19).replace("T", " ");

const InvoiceUrl = fetch('/InvoiceInpayment/' + $('#PermitID').val().toUpperCase() + "/")
var response = InvoiceUrl.then(function (res) {
  return res.json()
}, function (err) {
  return "error"
})
response.then(function (response) {
  InvoiceData = response.invoice
  InvoiceLoadData()
})

const ItemUrl = fetch('/ItemInpayment/' + $('#PermitID').val().toUpperCase() + "/")
var response = ItemUrl.then(function (res) {
  return res.json()
}, function (err) {
  return "error"
})
response.then(function (response) {
  ItemData = response.item
  ItemCascData = response.itemCasc;
  ItemLoadData()
})

$(document).ready(function () {
  $('#Loading').show();
  $('#Header span ').hide();
  ContainerRefresh();
  CpcLoadData()

  $('#declarationType').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '--Select--') {
      $(this).next().show();
    }
  });
  $('#CargoPackType').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '--Select--') {
      $(this).next().show();
    }
  });
  $('#inwardTranseportMode').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '--Select--') {
      $(this).next().show();
    }
  });
  $('#DeclaringFor').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '--Select--') {
      $(this).next().show();
    }
  });
  $('#CargoTotalOuterPack').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoOuterPack').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '--Select--') {
      $(this).next('span').show();
    }
  });
  $('#CargoTotalGrossweight').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoTotalGrossUOM').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '--Select--') {
      $(this).next().show();
    }
  });
  $('#releaseLocationInput').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#receiptLocationInput').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoLoadingPort1').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoArrivalDate').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoVoyageNumber').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoVesselName').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoObl').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoFlightNumber').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
  $('#CargoMawb').focusout(function () {
    $(this).next().hide();
    if ($(this).val() == '') {
      $(this).next().show();
    }
  });
});


function TabHead(ID) {
  $("#PartyTab").removeClass("HeadTabStyleChange")
  $("#CargoTab").removeClass("HeadTabStyleChange")
  $("#InvoiceTab").removeClass("HeadTabStyleChange")
  $("#ItemTab").removeClass("HeadTabStyleChange")
  $("#CpcTab").removeClass("HeadTabStyleChange")
  $("#SummaryTab").removeClass("HeadTabStyleChange")
  $("#RefundTab").removeClass("HeadTabStyleChange")
  $("#AmendTab").removeClass("HeadTabStyleChange")
  $("#CancelTab").removeClass("HeadTabStyleChange")
  $("#HeaderTab").removeClass("HeadTabStyleChange")
  $('#Header').hide();
  $('#Party').hide();
  $('#Cargo').hide();
  $('#Invoice').hide();
  $('#Item').hide();
  $('#Cpc').hide();
  $('#Summary').hide();
  $('#Refund').hide();
  $('#Amend').hide();
  $('#Cancel').hide();
  if (ID == 'HeaderTab') {
    $("#HeaderTab").addClass('HeadTabStyleChange')
    $('#Header').show();
    $('#declarationType').focus()
  }
  if (ID == 'PartyTab') {
    $("#PartyTab").addClass('HeadTabStyleChange')
    $('#Party').show();
    $('#ImporterCode').focus()
  }
  if (ID == 'CargoTab') {
    $("#CargoTab").addClass('HeadTabStyleChange')
    $('#Cargo').show()
    $('#CargoTotalOuterPack').focus()
  }
  if (ID == 'InvoiceTab') {
    $("#InvoiceTab").addClass('HeadTabStyleChange')
    $('#Invoice').show()
    $('#InvoiceSupplierCode').focus()
  }
  if (ID == 'ItemTab') {
    $("#ItemTab").addClass('HeadTabStyleChange')
    $('#Item').show()
    $('#ItemHsCode').focus()
  }
  if (ID == 'CpcTab') {
    $("#CpcTab").addClass('HeadTabStyleChange')
    $('#Cpc').show()
    $('#cpcNextBtn').focus()
  }
  if (ID == 'SummaryTab') {
    $("#SummaryTab").addClass('HeadTabStyleChange')
    $('#Summary').show();
    SummaryLoad();
    $('#summarypreviousbtn').focus()
  }
  if (ID == 'AmendTab') {
    $("#AmendTab").addClass('HeadTabStyleChange')
    $('#Amend').show()
  }
  if (ID == 'CancelTab') {
    $("#CancelTab").addClass('HeadTabStyleChange')
    $('#Cancel').show()
  }
  if (ID == 'RefundTab') {
    $("#RefundTab").addClass('HeadTabStyleChange')
    $('#Refund').show()
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

function CargoPackTypeChange() {
  var val = $('#CargoPackType').val()
  $('#InpaymentContainerShow').hide();
  if (val == '9: Containerized') {
    $('#InpaymentContainerShow').show();
  }
}

function CargoGrossEdit(Value, Uom) {
  if ("TNE" == Uom) {
    $('#CargoTotalGrossweight').val(Number(Value * 1000))
  }
  else {
    $('#CargoTotalGrossweight').val(Value)
  }
  CargoGross();
}

function InwardTrasnPortModeChange() {
  var Val = $("#inwardTranseportMode").val()
  $('#CargoMode').val(Val);
  $('#inwardCarrierAgentCruei').removeClass('HighLight')
  $('#inwardCarrierAgentName').removeClass('HighLight')
  $('.CargoInwardHide').hide();
  $('.NotRequired').show();
  $('.CargoInwardHide input').val("");
  $('#CargoHblLabel').html('HBL');
  $('#itemHwabHbl').html("HBL");
  if (Val == '1 : Sea') {
    $('.CrgoSeaShow').show();
    $('#inwardCarrierAgentName').addClass('HighLight')
    $('#inwardCarrierAgentCruei').addClass('HighLight')
  }
  else if (Val == '4 : Air') {
    $('.CargoAirShow').show();
    $('#CargoHblLabel').html('HAWB');
    $('#itemHwabHbl').html("HAWB");
    $('#inwardCarrierAgentName').addClass('HighLight')
    $('#inwardCarrierAgentCruei').addClass('HighLight')

  }
  else if (Val == 'N : Not Required' || Val == '--Select--') {
    $('.NotRequired').hide();
    $('.NotRequired input').val('');
  }
  else {
    $('.CargoRailShow').show();
  }
}

function CargoHawbOut(arg) {
 
  
  var Data = ($('#CargoHbl').val()).split(',');
  var Sel = `<option value='${Data[0]}' selected>${Data[0]}</option>`
  for (var i = 1; i < Data.length; i++) {
    Sel += `<option value='${Data[i]}'>${Data[i]}</option>`
  }
  $('#CargoHAWBSpan').hide();
}

// function ChangeFunction(){
//   $('#CargoHAWBSpan').hide();

//   if($('#FreightForwarderCode').val() !== "" && $('#CargoHbl').val() ==="" ){
//     $('#CargoHAWBSpan').show();
//   }else{
//     $('#CargoHAWBSpan').hide();
//   }

// }



function ReferenceDocument() {
  $('#OutReferenceShow').hide();
  if ($('#ReferenceDocuments').prop('checked')) {
    $('#OutReferenceShow').show();
    $('#ReferenceDocuments').val("True");
  }
  else {
    $('#ReferenceDocuments').val("False");
    $("#OutReferenceShow input").val('');
    $('#Loading').show();
    $.ajax({
      type: 'GET',
      url: '/DocumentDeletePermitId/',
      data: {
        PermitID: $('#PermitID').val().toUpperCase(),
      },
      success: function (response) {
        Infile = response.Infile
        $('#HeaderDocumentTableshow').hide();
        $('#Loading').hide();
      }
    })
  }
}

function HeaderRefernceOut() {
  if ($('#ReferenceDocuments').prop('checked')) {
    $('#licence1').attr('tabindex', 10);
  }
  else {
    $('#HeaderNext').attr('tabindex', 10);

  }
}
function OutItemAddCasc(Table, NAME) {
  var rowAdd = `<tr>
          <td><input type="text" class="inputStyle" name="${NAME}"></td>
          <td><input type="text" class="inputStyle" name="${NAME}"></td>
          <td><input type="text" class="inputStyle" name="${NAME}"></td>
          <td class="OutItemCascDeleteButton"><i class="material-icons" style="color:red">delete</i></td>
      </tr>`;
  $(`${Table} tbody`).append(rowAdd);
}

$(document).on("click", ".OutItemCascDeleteButton", function () {
  if ($(this).closest("tr").index() + 1 > 1) {
    $(this).closest("tr").remove();
  }
  else {
    $(this).closest("tr").find('input').val('');
  }
  $('.SchemeMaximum').hide();
  $('.CwcMaximum').hide();
  $('.AeoMaximum').hide();
});


function ItemCascShowAll(ID, CLASS) {
  if ($(ID).prop("checked")) {
    $(CLASS).show();
  }
  else {
    $(CLASS + ' :input[type="number"]').val("0.00");
    $(CLASS + ' :input[type="text"]').val("");
    $(CLASS + ' select').val("--Select--");
    $(CLASS + ' textarea').val("");
    if (CLASS == ".OutItemCascHide") {
      $(".OutItemCascHide table").find("tr:gt(1)").remove();
      $('.OutCasc3').hide();
      $('.OutCasc4').hide();
      $('.OutCasc5').hide();
      $('#ProductCode3').prop('checked', false);
      $('#ProductCode4').prop('checked', false);
      $('#ProductCode5').prop('checked', false);
    }
    if ('.OutCasc3' == CLASS) {
      $(".OutCasc3 table").find("tr:gt(1)").remove();
    }
    if ('.OutCasc4' == CLASS) {
      $(".OutCasc4 table").find("tr:gt(1)").remove();
    }
    if ('.OutCasc5' == CLASS) {
      $(".OutCasc5 table").find("tr:gt(1)").remove();
    }
    $(CLASS).hide();
  }
}

function CpcHideShow(ID, CLASS, Name) {
  if ($(ID).prop("checked")) {
    $(CLASS).show();
  } else {
    $(CLASS).hide();
    $(CLASS + ' input').val('');
    $(CLASS + " table").find("tr:gt(1)").remove();
  }
}

function CpcADD(Table, NAME, CLASS) {
  if ($(`${Table} tr`).length < 6) {
    var rowAdd = `<tr>
        <td><input type="text" class="inputStyle"  name = "${NAME}"></td>
            <td><input type="text" class="inputStyle" name = "${NAME}"></td>
            <td><input type="text" class="inputStyle" name = "${NAME}"></td>
            <td class="OutItemCascDeleteButton"><i class="material-icons" style="color:red">delete</i></td>
        </tr>`;
    $(`${Table} tbody`).append(rowAdd);
    $(CLASS).hide();
  }
  else {
    $(CLASS).show();
  }
  var TableValues = [];
  var Name = document.getElementsByName(NAME);
  for (var i = 0; i < Name.length; i = i + 3) {
    TableValues.push([Name[i].value, Name[i + 1].value, Name[i + 2].value]);
  }
}
function containerValidNum(select, value) {
  $(select).next("span").hide();
  var regex = /^[A-Za-z]{4}\d{7}$/;
  if (!regex.test(value)) {
    $(select).next("span").show();
  }
}
function ContainerValidSize(selector, value) {
  $(selector).next("span").hide();
  if (value == "--Select--" || value == "") {
    $(selector).next("span").show();
  }
}
function CargoGross() {
  $("#CargoTotalGrossWeightSpan").hide();
  var totalWeight = Number($('#CargoTotalGrossweight').val());
  var selectedWeight = $('#CargoTotalGrossUOM').val();
  if ($("#inwardTranseportMode").val() == '1 : Sea') {
    if ($("#CargoTotalGrossUOM").val() != "TNE") {
      $("#CargoTotalGrossWeightSpan").show();
    }
  }
  if ('TNE' == selectedWeight && totalWeight != null) {
    var total = totalWeight / 1000
    $('#CargoPermitGrossWeight').val(total);
  } else {
    $('#CargoPermitGrossWeight').val(totalWeight);
  }
}

/*----------------------------------------------------------------INVOICE FUNCTIONS----------------------------------------------------------------*/
 $(function () {
  // var test = $.datepicker.formatDate("dd/mm/yy", new Date());
  $("#CargoArrivalDate").datepicker({
    dateFormat: "dd/mm/yy"
  });
  $("#CargoBlanketDate").datepicker({
    dateFormat: "dd/mm/yy"
  });
  $("#InvoiceDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#OriginalRegistrationDate").datepicker({ dateFormat: "dd/mm/yy" });
  $("#SummaryMRD").datepicker({ dateFormat: "dd/mm/yy" });
  // $("#SummaryMRD").val(test);

  $('#InvoiceDate').keydown(function (event) {
    if (event.keyCode == 32) { // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#InvoiceDate").val(currentDate);
    }
  });
  $('#CargoArrivalDate').keydown(function (event) {
    if (event.keyCode == 32) { // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#CargoArrivalDate").val(currentDate);
    }
  });
  $('#CargoBlanketDate').keydown(function (event) {
    if (event.keyCode == 32) { // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#CargoBlanketDate").val(currentDate);
    }
  });
  $('#OriginalRegistrationDate').keydown(function (event) {
    if (event.keyCode == 32) { // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#OriginalRegistrationDate").val(currentDate);
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

// $(function () {
//   // Set default values for date fields
//   var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
//   $("#CargoArrivalDate").val(currentDate);
//   $("#CargoBlanketDate").val(currentDate);
//   $("#InvoiceDate").val(currentDate);
//   $("#OriginalRegistrationDate").val(currentDate);
//   $("#SummaryMRD").val(currentDate);

//   // Initialize datepickers
//   $("#CargoArrivalDate").datepicker({
//     dateFormat: "dd/mm/yy"
//   });
//   $("#CargoBlanketDate").datepicker({
//     dateFormat: "dd/mm/yy"
//   });
//   $("#InvoiceDate").datepicker({ dateFormat: "dd/mm/yy" });
//   $("#OriginalRegistrationDate").datepicker({ dateFormat: "dd/mm/yy" });
//   $("#SummaryMRD").datepicker({ dateFormat: "dd/mm/yy" });

//   // Handle spacebar keydown event for date fields
//   $('#InvoiceDate, #CargoArrivalDate, #CargoBlanketDate, #OriginalRegistrationDate, #SummaryMRD').keydown(function (event) {
//     if (event.keyCode == 32) { // spacebar keycode
//       event.preventDefault();
//       $(this).val(currentDate);
//     }
//   });
// });


function InvoiceDateFunction(Arg) {
  $('#InvoiceDateSpan').hide();
  let x = document.getElementById(Arg);

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
function TrimKeyUp(Val) {
  $("#" + Val).keyup(function (event) {
    if (event.keyCode != 32 && event.keyCode != 13) {
      let Value = $("#" + Val).val()
      $("#" + Val).val(Value.trim())
    }
  });
}
function InvoiceTermChange(val) {
  $('#InvoiceCalculationTable input').val("0.00")
  $('#InvoiceCalculationTable select').val("--Select--")
  $('#InvoiceGstCharge').val(9)
  $('#InvoiceFrightRow').show();
  $('#InvoiceInsurenceRow').show();
  if (val == 'CFR : Cost and Frieght ( also known as C & F )') {
    $('#InvoiceFrightRow').hide();
    $('#InsurenceCharges').val('1.00')
    $('#InsurenceCurrency').val('SGD')
    $('#InsurenceExRate').val('1.000000')
  }
  else if (val == 'CIF : Cost,Insurance and Frieght') {
    $('#InvoiceFrightRow').hide();
    $('#InvoiceInsurenceRow').hide();
  }
  else if (val == 'CNI : Cost and Insurance (also Known as C & I )') {
    $('#InvoiceInsurenceRow').hide();
  }
  else if (val == "EXW : Exw Works (also known as Ex-Factory)") {
    $('#InsurenceCharges').val('1.00')
    $('#InsurenceCurrency').val('SGD')
    $('#InsurenceExRate').val('1.000000')
  }
  else if (val == "FAS : Free Alongside Ship") {
    $('#InsurenceCharges').val('1.00')
    $('#InsurenceCurrency').val('SGD')
    $('#InsurenceExRate').val('1.000000')
  }
  else if (val == "FOB : Free On Board") {
    $('#InsurenceCharges').val('1.00')
    $('#InsurenceCurrency').val('SGD')
    $('#InsurenceExRate').val('1.000000')
  }
  InsurenceChargesFocusOut();
}

function CheckFunction(ID) {
  if ($('#' + ID).prop('checked')) {
    $('#' + ID).val("True");
    if ('itemUnBrand' == ID) {
      $('#itemBrandInput').val('UNBRANDED');
    }
  }
  else {
    $('#' + ID).val("False");
    if ('itemUnBrand' == ID) {
      $('#itemBrandInput').val('');
    }
  }
}

function InsurenceChargesFocusOut(){
  console.log('hello')
var InsurenceCharges =$('#InsurenceCharges').val()
console.log(InsurenceCharges)

if (InsurenceCharges === '0.00'){
  $('#InsurenceAmount').prop('disabled', false)
}else if (InsurenceCharges !== '0.00'){
  $('#InsurenceAmount').prop('disabled', true)
}else{
  $('#InsurenceAmount').prop('disabled', false)
}
}


function InvoiceSave() {
  $('#InvoiceImportCodeSpan').hide();
  $('#InvoiceNameSpan').hide();
  $('#InvoiceImportCrueiSpan').hide();
  $('#InvoiceImportNameSpan').hide();
  $('#InvoiceDateSpan').hide();
  $('#InvoiceNumberSpan').hide();
  $('#InvoiceCurrencySpan').hide();
  var Check = true;
  if ($('#InvoiceName').val() == "") {
    $('#InvoiceNameSpan').show();
    Check = false;
  }
  if ($('#InvoiceImportCruei').val() == "") {
    $('#InvoiceImportCrueiSpan').show();
    Check = false;
  }
  if ($('#InvoiceImportName').val() == "") {
    $('#InvoiceImportNameSpan').show();
    Check = false;
  }
  if ($('#InvoiceDate').val() == "") {
    $('#InvoiceDateSpan').show();
    Check = false;
  }
  if ($('#InvoiceNumber').val() == "") {
    $('#InvoiceNumberSpan').show();
    Check = false;
  }
  if ($('#InvoiceCurrency').val() == "--SELECT--" || $('#InvoiceCurrency').val() == "--Select--") {
    $('#InvoiceCurrencySpan').show();
    Check = false;
  }
  if ($('#InvoiceImportCode').val() != $('#ImporterCode').val()) {
    $('#InvoiceImportCodeSpan').show();
    Check = false;
  }
  $("#InvoiceSaveSpan").hide()
  if (Check) {
    $('#Loading').show();
    const originalDate = $("#InvoiceDate").val();
    const parts = originalDate.split("/");
    const newDate = `${parts[2]}/${parts[1]}/${parts[0]}`;
    $.ajax({
      type: 'POST',
      url: '/InvoiceSave/',
      data: {
        SNo: $('#InvoiceSerial').val(),
        InvoiceNo: $('#InvoiceNumber').val(),
        InvoiceDate: newDate,
        TermType: $('#InvoiceTermType').val(),
        AdValoremIndicator: $('#InvoiceAdVal').val(),
        PreDutyRateIndicator: $('#InvoicePreferential').val(),
        SupplierImporterRelationship: $('#InvoiceRelationShip').val(),
        SupplierCode: $('#InvoiceSupplierCode').val(),
        ImportPartyCode: $('#InvoiceImportCode').val(),
        TICurrency: $('#InvoiceCurrency').val(),
        TIExRate: $('#InvoiceExRate').val(),
        TIAmount: $('#InvoiceAmount').val(),
        TISAmount: $('#InvoiceSumAmount').val(),
        OTCCharge: $('#OtherCharges').val(),
        OTCCurrency: $('#OtherCurrency').val(),
        OTCExRate: $('#OtherExRate').val(),
        OTCAmount: $('#OtherAmount').val(),
        OTCSAmount: $('#OtherSumAmount').val(),
        FCCharge: $('#FrightCharges').val(),
        FCCurrency: $('#FrightCurrency').val(),
        FCExRate: $('#FrightExRate').val(),
        FCAmount: $('#FrightAmount').val(),
        FCSAmount: $('#FrightSumAmount').val(),
        ICCharge: $('#InsurenceCharges').val(),
        ICCurrency: $('#InsurenceCurrency').val(),
        ICExRate: $('#InsurenceExRate').val(),
        ICAmount: $('#InsurenceAmount').val(),
        ICSAmount: $('#InsurenceSumAmount').val(),
        CIFSUMAmount: $('#CostInsurenceFreightSum').val(),
        GSTPercentage: $('#InvoiceGstCharge').val(),
        GSTSUMAmount: $('#InvoiceGstSum').val(),
        MessageType: $('#MsgType').val(),
        PermitId: $('#PermitID').val().toUpperCase(),
        TouchUser: $('#USERNAME').val().toUpperCase(),
        TouchTime: TOUCHTIME,
        ChkOtherInv: $('#InvoiceInsurence').val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InvoiceData = response.Invoice;
        InvoiceLoadData();
        InvoiceReset();
        $('#Loading').hide();
        $('#InvoiceNextBtn').focus()
      }
    })
  }
  else {
    $("#InvoiceSaveSpan").show()
  }
}

function InvoiceLoadData() {
  $('#InvoiceSerial').val((Number(InvoiceData.length) + 1).toString().padStart(3, '0'));
  $('#summaryNoOfVoice').val(InvoiceData.length)
  var invoiceCurAmountARR = [];
  var summaryTotalInvoiceCIFValue = 0;
  var summaryINvoiceGst = 0;
  if (InvoiceData.length > 0) {
    var Tbody = ""
    var ItemInvoice = "<option selected>--Select--</option>";
    for (var invoiceData of InvoiceData) {
      Tbody += `
        <tr>
            <td><i class="fa-solid fa-trash-can" style="color: #ff0000;" onclick='InvoiceDelete(${invoiceData.SNo},"${invoiceData.PermitId}")' id='DeleteBtnInvoice'></i></td>
            <td><i class="fa-regular fa-pen-to-square" style="color: #ff0000;" onclick="InvoiceEdit(${invoiceData.id})"></i></td>
            <td>${invoiceData.SNo}</td><td>${invoiceData.InvoiceNo}</td><td>${invoiceData.InvoiceDate}</td><td>${invoiceData.TermType}</td><td>${invoiceData.TICurrency}</td><td>${invoiceData.TIAmount}</td><td>${invoiceData.CIFSUMAmount}</td><td>${invoiceData.GSTSUMAmount}</td>
        </tr>
        `;
      ItemInvoice += `<option value = '${invoiceData.InvoiceNo}'>${invoiceData.InvoiceNo}</option>`
      invoiceCurAmountARR.push([invoiceData.TICurrency, Number(invoiceData.TIAmount)]);
      summaryTotalInvoiceCIFValue += Number(invoiceData.CIFSUMAmount);
      summaryINvoiceGst += Number(invoiceData.GSTSUMAmount);
    }
    $('#InvoiceTable tbody').html(Tbody)
    summarySumOfInvoiceAmountFunction(invoiceCurAmountARR);
    $("#summaryTotalInvoiceCIFValue").val(summaryTotalInvoiceCIFValue);
    $("#summaryTotalInvoiceGst").val(summaryINvoiceGst);
    $('#ItemInvoiceNumber').html(ItemInvoice)
    if ($('#ShowEdit').val() == 'True') {
      $('#DeleteBtnInvoice').html(``)
    }
  }
  else {
    $('#InvoiceTable tbody').html("<tr><td colspan=10 style='text-align:center'>No Record</td></tr>")
  }

}

function InvoiceDelete(SNo, PermitId) {
  $('#Loading').show();
  $.ajax({
    url: '/InvoiceDelete/',
    type: 'GET',
    data: {
      PermitId: PermitId,
      SNo: SNo,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      InvoiceData = response.Invoice;
      InvoiceLoadData();
      $('#Loading').hide();
    }
  })
}

function InvoiceReset() {
  InvoiceTermChange('--Select--')
  $('#Invoice span').hide();
  $('#Invoice input').val('');
  $('#InvoiceCalculationTable input').val('0.00');
  $('#Invoice select').val('--Select--');
  $('#Invoice input').prop('checked', false);
  $('#InvoiceSerial').val((Number(InvoiceData.length) + 1).toString().padStart(3, '0'));
}

function InvoiceEdit(Arg) {
  InvoiceReset();
  for (var i of InvoiceData) {
    if (i.id == Arg) {
      let oldDate = i.InvoiceDate;
      let parts = oldDate.split('-')
      let newDate1 = `${parts[2]}/${parts[1]}/${parts[0]}`
      $('#InvoiceSerial').val((i.SNo).toString().padStart(3, '0'));
      $("#InvoiceDate").val(newDate1);
      $('#InvoiceNumber').val(i.InvoiceNo);
      $('#InvoiceTermType').val(i.TermType);
      InvoiceTermChange(i.TermType)
      $('#InvoiceAdVal').val(i.AdValoremIndicator);
      if ('True' == i.AdValoremIndicator) {
        $('#InvoiceAdVal').prop('checked', true);
      }
      if ('True' == i.PreDutyRateIndicator) {
        $('#InvoicePreferential').prop('checked', true);
      }
      $('#InvoicePreferential').val(i.PreDutyRateIndicator);
      if (i.SupplierImporterRelationship == "--Select--" || i.SupplierImporterRelationship == "--SELECT--") {
        $('#InvoiceRelationShip').val("--Select--");
      }
      else {
        $('#InvoiceRelationShip').val(i.SupplierImporterRelationship);
      }
      $('#InvoiceSupplierCode').val(i.SupplierCode);
      $('#InvoiceImportCode').val(i.ImportPartyCode);
      SupplyFocusOut();
      InvoiceImporterOut();
      $('#InvoiceCurrency').val(i.TICurrency);
      $('#InvoiceExRate').val(i.TIExRate);
      $('#InvoiceAmount').val(i.TIAmount);
      $('#InvoiceSumAmount').val(i.TISAmount);
      $('#OtherCharges').val(i.OTCCharge);
      $('#OtherCurrency').val(i.OTCCurrency);
      $('#OtherExRate').val(i.OTCExRate);
      $('#OtherAmount').val(i.OTCAmount);
      $('#OtherSumAmount').val(i.OTCSAmount);
      $('#FrightCharges').val(i.FCCharge);
      $('#FrightCurrency').val(i.FCCurrency);
      $('#FrightExRate').val(i.FCExRate);
      $('#FrightAmount').val(i.FCAmount);
      $('#FrightSumAmount').val(i.FCSAmount);
      $('#InsurenceCharges').val(i.ICCharge);
      $('#InsurenceCurrency').val(i.ICCurrency);
      $('#InsurenceExRate').val(i.ICExRate);
      $('#InsurenceAmount').val(i.ICAmount);
      $('#InsurenceSumAmount').val(i.ICSAmount);
      $('#CostInsurenceFreightSum').val(i.CIFSUMAmount);
      $('#InvoiceGstCharge').val(i.GSTPercentage);
      $('#InvoiceGstSum').val(i.GSTSUMAmount);
      $('#InvoiceInsurence').val(i.ChkOtherInv);
    }
  }
}

/*----------------------------------------------------------------ITEM FUNCTIONS----------------------------------------------------------------*/

function ItemHscodeFocusIn() {
  var itemHscode = []
  for (var i of InhouseItemCode) {
    itemHscode.push(`${i.InhouseCode}:${i.HSCode}`)
  }
  Autocomplete(itemHscode, '#itemItemCode')
}

function ItemHscodeFocusOut() {
  var itemcodeVal = $("#itemItemCode").val().trim().toUpperCase()
  if (itemcodeVal !== "") {
    for (var i of InhouseItemCode) {
      if ((i.InhouseCode).toUpperCase() == (itemcodeVal.split(":")[0]).toUpperCase()) {
        $("#itemItemCode").val(i.InhouseCode)
        $("#ItemHsCode").val(i.HSCode)
        $("#itmeDescription").val(i.Description)
        $("#itemBrandInput").val(i.Brand)
        $("#itemModel").val(i.Model)
        $("#itemDgIndicator").val(i.DgIndicator)
        $("#itemProductCode1").val(i.ProductCode)
        if (i.DGIndicator == "True") {
          $('#itemDgIndicator').prop('checked', true);
        } else {
          $('#itemDgIndicator').prop('checked', false);
        }
        if (i.Brand == "UNBRANDED") {
          $('#itemUnBrand').prop('checked', true);
        } else {
          $('#itemUnBrand').prop('checked', false);
        }
      }
    }
    HsOnFocusOut()
  }

}

function HsOnFocus() {
  TrimKeyUp('ItemHsCode')

  var hsCode = [];
  for (var i of ItemHsCodeData) {
    hsCode.push(`${i.HSCode}:${i.Description}`)
  }
  Autocomplete(hsCode, '#ItemHsCode')
}

function HsCustemmCheck(ArgUom, ID) {
  if (ArgUom == 0) {
    $(ID).val('--Select--')
  } else {
    $(ID).val(ArgUom)
  }
}

function HsOnFocusOut() {
  $('#hsControledId').hide();
  $('#VehicalTypeShow').hide();
  $('#EngineCapacityShow').hide();
  $('#OriginalShow').hide();
  $('#itemDutiableQtyNone').hide();
  $('#itemAlchoholNone').hide();
  $('#OptimalCharges').hide();
  $("#itmeDescription").val("");
  $('#itemDutiableQtyNone input').val("0.00");
  $('#itemDutiableQtyNone select').val("--Select--");
  $('#itemAlchoholNone input').val("0.00");
  $('#itemAlchoholNone select').val("--Select--");
  $('#itemExciseDutyInput1').val("0.00");
  $('#itemCustomsDutyInput1').val("0.00");
  $('#itemExciseDutyInput2').val("0.00");
  $('#itemCustomsDutyInput2').val("0.00");
  $('#VehicalTypeUom').val('--Select--');
  $('#EngineCapacity').val('0.00');
  $('#EngineCapacityUom').val('--Select--');
  $('#OriginalRegistrationDate').val('');
  $('#OptionalChrgeUOM').val('--Select--');
  $('#Optioncahrge').val('0.00');
  $('#OptionalSumtotal').val('0.00');
  $('#OptionalSumExchage').val('0.00');
  let code = ($('#ItemHsCode').val()).split(":")
  console.log("hscode:", code)
  if ($('#ItemHsCode').val() != "") {
    for (var i of ItemHsCodeData) {
      if (i.HSCode == code[0].trim()) {
        if(Number(i.Inpayment) == 1){
          console.log("Number(i.Inpayment)",Number(i.Inpayment))
          $('#hsControledId').show();
          console.log('itemCascIDprop1:',$('#itemCascID').prop('checked'))
          document.getElementById('itemCascID').checked = true;
          console.log('itemCascIDprop2:',$('#itemCascID').prop('checked'))
          ItemCascShowAll('#itemCascID','.OutItemCascHide')

        }
        $('#ItemHsCode').val(i.HSCode)
        let chh = true;
        InhouseItemCode.filter((ans) => {
          if ((ans.InhouseCode).toUpperCase() == $("#itemItemCode").val().trim().toUpperCase()) {
            if (ans.HSCode == i.HSCode) {
              $('#itmeDescription').val(ans.Description);
              chh = false;
            } else {
              $('#itemItemCode').val("");
            }
          }
        })

        if (chh) {
          $('#itmeDescription').val(i.Description);
        }
        $('#itemHsQuantity').val(i.UOM);
        $('#itemDutyIDDummy').val(i.DUTYTYPID);
        $('#kgmvisibleDummy').val(i.Kgmvisible);
        let dutyId = i.DUTYTYPID;
        let uom = i.UOM;
        let DutiableUom = i.DuitableUom;
        let ExUom = i.Excisedutyuom;
        let ExRate = i.Excisedutyrate;
        let CustUom = i.Customsdutyuom;
        let CustRate = i.Customsdutyrate;
        if (uom !== "LTR") {
          document.getElementById('packing_details').checked = false;
          ItemCascShowAll('#packing_details', '.PackingDetails');
        }
        if (dutyId == 62 || dutyId == 63) {
          if (dutyId == 62 && uom == "LTR") {
            $('#ItemDutiableUom').val(uom);
            $('#itemTotalDuitableUom').val(uom);
            $('#itemDutiableQtyNone').show();
            $('#itemAlchoholNone').show();
            document.getElementById('packing_details').checked = true;
            ItemCascShowAll('#packing_details', '.PackingDetails')
          } else if (dutyId == 63 && uom == "KGM" || dutyId == 62 && uom != "LTR") {
            $('#ItemDutiableUom').val(uom);
            $('#itemTotalDuitableUom').val(uom);
            $('#itemDutiableQtyNone').show();
          } else {
            $('#ItemDutiableUom').val(uom);
            $('#itemTotalDuitableUom').val(uom);
            $('#itemDutiableQtyNone').show();
            $('#itemAlchoholNone').show();
            document.getElementById('packing_details').checked = true;
            ItemCascShowAll('#packing_details', '.PackingDetails')
          }
          if (DutiableUom == 'A') {
            $('#ItemDutiableUom').val('--Select--');
          }
          HsCustemmCheck(ExUom, '#itemExciseDutyInput2')
          HsCustemmCheck(CustUom, '#itemCustomsDutyInput2')
          $('#itemExciseDutyInput1').val(ExRate);
          $('#itemCustomsDutyInput1').val(CustRate);
        } else if (dutyId == 64) {
          if (uom != 'LTR') {
            $('#itemDutiableQtyNone').show();
            $('#itemAlchoholNone').hide();
          } else {
            $('#itemDutiableQtyNone').show();
            $('#itemAlchoholNone').show();
            document.getElementById('packing_details').checked = true;
            ItemCascShowAll('#packing_details', '.PackingDetails')
          }
          if (DutiableUom == 'A') {
            $('#ItemDutiableUom').val('--Select--');
          }
          HsCustemmCheck(ExUom, '#itemExciseDutyInput2');
          HsCustemmCheck(CustUom, '#itemCustomsDutyInput2');
          $('#itemExciseDutyInput1').val(ExRate);
          $('#itemCustomsDutyInput1').val(CustRate);
        } else if (dutyId == 61) {
          if (dutyId == 61 && uom == 'LTR') {
            $('#ItemDutiableUom').val(uom);
            $('#itemTotalDuitableUom').val(uom);
            $('#itemDutiableQtyNone').show();
            $('#itemAlchoholNone').show();
            document.getElementById('packing_details').checked = true;
            ItemCascShowAll('#packing_details', '.PackingDetails')
            HsCustemmCheck(ExUom, '#itemExciseDutyInput2');
            HsCustemmCheck(CustUom, '#itemCustomsDutyInput2');
            $('#itemExciseDutyInput1').val(ExRate);
            $('#itemCustomsDutyInput1').val(CustRate);
          } else if (dutyId == 61 && uom == 'KGM') {
            $('#ItemDutiableUom').val(uom);
            $('#itemTotalDuitableUom').val(uom);
            $('#itemDutiableQtyNone').show();
            $('#itemAlchoholNone').hide();
            HsCustemmCheck(ExUom, '#itemExciseDutyInput2');
            HsCustemmCheck(CustUom, '#itemCustomsDutyInput2');
            $('#itemExciseDutyInput1').val(ExRate);
            $('#itemCustomsDutyInput1').val(CustRate);
          } else {
            $('#itemDutiableQtyNone').hide();
            $('#itemAlchoholNone').hide();
          }
        }
        if (code[0].startsWith('87')) {
          for (var i of ChkHsCode) {
            if (code[0] == i.HSCode) {
              $('#VehicalTypeShow').show();
              $('#EngineCapacityShow').show();
              $('#OriginalShow').show();
              $('#itemDutiableQtyNone').show();
              $('#OptimalCharges').show();
              HsCustemmCheck(ExUom, '#itemExciseDutyInput2');
              HsCustemmCheck(CustUom, '#itemCustomsDutyInput2');
              $('#itemExciseDutyInput1').val(ExRate);
              $('#itemCustomsDutyInput1').val(CustRate);
              $('#ItemDutiableUom').val(uom);
              $('#itemTotalDuitableUom').val(uom);
            }
          }
        }
      }
    }
  }
}


function OriginalRegistrationlDateFunction() {
  let x = document.getElementById("OriginalRegistrationDate");

  if (x.value.length != 0) {
    if (x.value.length == 8) {
      if (x.value[0] + x.value[1] <= 31 && x.value[2] + x.value[3] <= 12) {
        x.value =
          `${x.value[0] + x.value[1]}/${x.value[2] + x.value[3]}/${x.value[4] + x.value[5] + x.value[6] + x.value[7]}`
      } else {
        x.value = DateTimeCalculation();
      }
    } else {
      x.value = DateTimeCalculation();
    }
  }
}

function dutiableQtyFunction() {
  let opQty = $("#itemOuterPackQtyInput").val();
  let inQty = $("#itemInPackQuantityInput").val();
  let oinnerQty = $("#itemInnerPackQtyInput").val();
  let inmostQty = $("#itemInmostPackQtyInput").val();
  let dutiAb = $("#itemDuitableQty").val();
  //itemDutiCalculation(opQty, inQty, oinnerQty, inmostQty, dutiAb)
  duticalc(opQty, inQty, oinnerQty, inmostQty, dutiAb)
  itemAlchoholCalculationFunction()
}



function itemDutiCalculation(op, inp, inner, inmost, dutiab) {
  var pckqty = 1;
  let dutiAb1 = $("itemDuitableQty").val();
  var typeId = $('#itemDutyIDDummy').val();
  var kgmvisible = $('#kgmvisibleDummy').val();
  let exiceDutyRate = $('#itemExciseDutyInput1').val(); //T1
  let cifob = $('#iteminvoiceCIFFOB').val(); //T2
  let uom = $('#itemHsQuantity').val();
  let hsCode = $('#ItemHsCode').val();
  if (0 < op) {
    pckqty = op;
  }
  if (0 < inp) {
    pckqty = pckqty * inp;
  }
  if (0 < inner) {
    pckqty = pckqty * inner;
  }
  if (0 < inmost) {
    pckqty = inmost * pckqty;
  }
  if (dutiAb1 != "") {
    if (uom == "LTR") {
      $('#ItemTotalDutiableQtyInput').val((Number(pckqty) * Number(dutiab)).toFixed(2));
      $('#ItemHsQtyInput').val((Number(pckqty) * Number(dutiab)).toFixed(2));
    } else if (uom == "KGM" && kgmvisible == "MULTIPLE") {
      $('#ItemTotalDutiableQtyInput').val((Number(pckqty) * Number(dutiab)).toFixed(2));
      if (!hsCode.startsWith('87')) {
        $('#TxtSumExciseDuty').val((Number(pckqty) * Number(dutiab)) * exiceDutyRate);
      }
      let exciseinput3 = $('#TxtSumExciseDuty').val();
      if ($('#declarationType').val() != 'GST : GST (Including Duty Exemption)') {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = (exiceDutyRate * gstperval) + (exciseinput3 * gstperval)
        $('#TxtItemSumGST').val(T4.toFixed(2))
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      } else {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = Number(cifob) * Number(gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      }
    } else if (uom == "KGM" && kgmvisible == "DIVIDE") {
      $('#ItemTotalDutiableQtyInput').val((Number(pckqty) * Number(dutiab) / 1000).toFixed(2));
      if (!hsCode.startsWith('87')) {
        $('#TxtSumExciseDuty').val(((Number(pckqty) * Number(dutiab)) / 1000) *
          exiceDutyRate);
      }
      let T3 = $('#TxtSumExciseDuty').val();
      if ($('#declarationType').val() != 'GST : GST (Including Duty Exemption)') {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = (Number(cifob) * Number(gstperval)) + (Number(T4) * Number(gstperval));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      } else {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = Number(cifob) * Number(gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      }
    } else if (uom == "STK") {
      $('#ItemTotalDutiableQtyInput').val(pckqty.toFixed(2));
      $("#ItemHsQtyInput").val(((pckqty * dutiab) / 1000).toFixed(2));
      if (!hsCode.startsWith('87')) {
        $('#TxtSumExciseDuty').val(pckqty * exiceDutyRate);
      }
      let T3 = $('#TxtSumExciseDuty').val();
      if ($('#declarationType').val() != 'GST : GST (Including Duty Exemption)') {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = (cifob * gstperval) + (T3 * gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      } else {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = Number(cifob) * Number(gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      }
    } else if (uom == "KGM" && typeId == 62) {
      $('#ItemTotalDutiableQtyInput').val((Number(pckqty) * Number(dutiab)).toFixed(2))
      if (!hsCode.startsWith('87')) {
        $('#TxtSumExciseDuty').val((Number(pckqty) * Number(dutiab)) * (
          exiceDutyRate));
      }
      let T3 = $('#TxtSumExciseDuty').val();
      if ($('#declarationType').val() != 'GST : GST (Including Duty Exemption)') {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = (cifob * gstperval) + (T3 * gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      } else {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = Number(cifob) * Number(gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      }
    } else if (uom == "TNE" && typeId == 62) {
      $('#ItemTotalDutiableQtyInput').val((Number(pckqty) * Number(dutiab)).toFixed(2))
      if (!hsCode.startsWith('87')) {
        $('#TxtSumExciseDuty').val((Number(pckqty) * Number(dutiab)) * (
          exiceDutyRate));
      }
      let T3 = $('#TxtSumExciseDuty').val();
      if ($('#declarationType').val() != 'GST : GST (Including Duty Exemption)') {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = (cifob * gstperval) + (T3 * gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      } else {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = Number(cifob) * Number(gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      }
    } else if (uom == "KGM" && typeId == 61) {
      $('#ItemTotalDutiableQtyInput').val((Number(pckqty) * Number(dutiab)).toFixed(2))
      if (!hsCode.startsWith('87')) {
        $('#TxtSumExciseDuty').val(((Number(pckqty) * Number(dutiab)).toFixed(2)) * (
          exiceDutyRate));
      }
      let T3 = $('#TxtSumExciseDuty').val();
      if ($('#declarationType').val() != 'GST : GST (Including Duty Exemption)') {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = (cifob * gstperval) + (T3 * gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      } else {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = Number(cifob) * Number(gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      }
    } else if (uom == "DAL") {
      $('#ItemTotalDutiableQtyInput').val((Number(pckqty) * Number(dutiab)).toFixed(2))
      if (!hsCode.startsWith('87')) {
        $('#TxtSumExciseDuty').val((Number(pckqty) * Number(dutiab)) * (
          exiceDutyRate));
      }
      let T3 = $('#TxtSumExciseDuty').val();
      if ($('#declarationType').val() != 'GST : GST (Including Duty Exemption)') {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = (cifob * gstperval) + (T3 * gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      } else {
        let gstperval = Number($('#invoiceGSTInput1').val()) / 100;
        let T4 = Number(cifob) * Number(gstperval);
        $('#TxtItemSumGST').val(T4.toFixed(2));
        if (T4 >= 10000) {
          $('#marquee1').val("Total GST Amount Greater than 10000");
        } else {
          if ($('#marquee1').val() == "") {
            $('#marquee1').val("");
          }
        }
      }
    }
  }
}

function itemAlchoholCalculationFunction() {
  let T1 = Number($("#ItemTotalDutiableQtyInput").val())
  let T2 = Number($("#itemAlchoholPer").val())
  let T3 = Number($("#itemExciseDutyInput1").val())
  let T4 = Number($("#itemCustomsDutyInput1").val())
  let T6;
  let gstperval;
  if (T1 != "" && T2 != "" && T3 != "") {
    if (T2 > 0) {
      $("#TxtSumExciseDuty").val((T1 * T2 * (T3 / 100)).toFixed(2))
      $("#itemCustomsDutyInput3").val((T1 * T2 * (T4 / 100)).toFixed(2))
    }
  }
  T4 = Number($("#TxtSumExciseDuty").val())
  let T5 = Number($("#iteminvoiceCIFFOB").val())
  let T7 = Number($("#itemCustomsDutyInput3").val())
  if ($('#declarationType').val() != 'GST : GST (Including Duty Exemption)') {
    gstperval = Number($('#invoiceGSTInput1').val()) / 100;
    T6 = ((T4 * gstperval) + (T5 * gstperval) + (T7 * gstperval));
    $('#TxtItemSumGST').val(T6.toFixed(2))
    if (T6 >= 10000) {
      $('#marquee1').val("Total GST Amount greater than 10000");
    } else {
      $('#marquee1').val("")
    }
  } else {
    gstperval = Number($('#invoiceGSTInput1').val()) / 100;
    T6 = T5 * gstperval;
    $('#TxtItemSumGST').val(T6.toFixed(2))
    if (T6 >= 10000) {
      $('#marquee1').val("Total GST Amount greater than 10000");
    } else {
      $('#marquee1').val("")
    }
  }
}

function ItemDelHblHawb() {
  $("#Loading").show();
  $.ajax({
    url: "/inpaymentItemDelHblHawb/",
    success: function (response) {
      ItemData = response.Item;
      ItemLoadData();
      $("#Loading").hide();
    }
  });
}
// function itemInvoiceQuantityFunction() {
//   var itemqty = $("#itemInvoiceQuantity").val();
//   if (itemqty != '0.0000') {
//     var hsopt = $('#itemHsQuantity').val();
//     var total;
//     if (hsopt == 'TEN' || hsopt == 'TPR') {
//       total = itemqty / 10;
//     } else if (hsopt == 'KGM') {
//       total = Number(itemqty) * 1;
//     } else if (hsopt == 'CEN') {
//       total = itemqty / 100;
//     } else if (hsopt == 'MIL' || hsopt == 'TNE') {
//       total = itemqty / 1000;
//     } else if (hsopt == 'MTK') {
//       total = itemqty / 3.213;
//     } else if (hsopt == 'LTR') {
//       total = itemqty * 1;
//     } 
//     else {
//       total = itemqty;
//     }
//     if (hsopt == 'KGM' || hsopt == 'LTR' || hsopt == 'TNE') {
//       if (Number(itemqty) > Number($('#CargoTotalGrossweight').val())) {
//         alert('The Total Gross Weight is Less Than The Sum Of The Item Weight Please Check!!!')
//       }
//     }
//     if ($("#ItemHsQtyInput").val() == "0.00" || $("#ItemHsQtyInput").val() == "") {
//       $("#ItemHsQtyInput").val(total.toFixed(2));
//     }
//     if ($("#itemInvoiceQuantity").val() != "0.00" && $("#ItemHsQtyInput").val() != "") {
//       $("#ItemHsQtyInput").val(total.toFixed(2));
//     }
//   }
// }

function itemInvoiceQuantityFunction() {
  var itemqty = $("#itemInvoiceQuantity").val();
  if (itemqty != '0.0000') {
    var hsopt = $('#itemHsQuantity').val();
    var total;
    if (hsopt == 'TEN' || hsopt == 'TPR') {
      total = itemqty / 10;
    } else if (hsopt == 'CEN') {
      total = itemqty / 100;
    } else if (hsopt == 'MIL' || hsopt == 'TNE') {
      total = itemqty / 1000;
    } else if (hsopt == 'MTK') {
      total = itemqty * 3.213;
    } else if (hsopt == 'LTR' || hsopt == 'KGM') {
      total = itemqty * 1;
    } 
    else {
      total = itemqty;
    }
    if (hsopt == 'KGM' || hsopt == 'LTR' || hsopt == 'TNE') {
      if (Number(itemqty) > Number($('#CargoTotalGrossweight').val())) {
        alert('The Total Gross Weight is Less Than The Sum Of The Item Weight Please Check!!!')
      }
    }
    if ($("#ItemHsQtyInput").val() == "0.00" || $("#ItemHsQtyInput").val() == "") {
      $("#ItemHsQtyInput").val(total);
    }
    if ($("#itemInvoiceQuantity").val() != "0.00" && $("#ItemHsQtyInput").val() != "") {
      $("#ItemHsQtyInput").val(total);
    }
  }
}

function HsQuantityError() {
  $("#itemHsQuantityInputError").hide();
  if (
    $("#ItemHsQtyInput").val() == "" ||
    $("#ItemHsQtyInput").val() == "0.00"
  ) {
    $("#itemHsQuantityInputError").show();
  }
}

function invoiceNumberFunction() {
  var invoiceNumberval = document.getElementById("ItemInvoiceNumber").value;
  if (invoiceNumberval == "--SELECT--" || invoiceNumberval == "--Select--") {
    document.getElementById("itemInvoiceCurr").value = '--Select--';
    document.getElementById("iteminvoiceCurrInput").value = '0.00';
  } else {
    for (var i of InvoiceData) {
      if (invoiceNumberval == i.InvoiceNo) {
        $('#itemInvoiceCurr').val(i.TICurrency)
        $('#iteminvoiceCurrInput').val(i.TIExRate)
      }
    }
  }
}

function itemCheckUnitPriceFunction() {
  var check = document.getElementById("itemCheckUnitPrice");
  $('#UnitPriceIDShow').hide()
  if (check.checked) {
    check.value = 'True';
    $('#UnitPriceIDShow').show()
  } else {
    $('#UnitPrice').val("0.00")
    $('#SumExchangeRate').val("0.00")
    check.value = 'False';
  }
}

function invoiceTotalLineAmountFunction() {
  var itotalAmount = Number($("#iteminvoiceTotalLineAmount").val());
  var icurrinput = Number($("#iteminvoiceCurrInput").val());
  var invoiceNumberval = $("#ItemInvoiceNumber").val();
  var totalAmd = 0;
  var TotInvoiceAmd = 0;
  for (var i of InvoiceData) {
    if (invoiceNumberval == i.InvoiceNo) {
      totalAmd = Number(i.OTCSAmount) + Number(i.FCSAmount) + Number(i.ICSAmount)
      TotInvoiceAmd = Number(i.TISAmount)
    }
  }
  const InvoiceAmd = totalAmd / TotInvoiceAmd;
  const TotalLineAmd = icurrinput * itotalAmount;

  $('#iteminvoiceTotalInvoiceCharge').val((InvoiceAmd * TotalLineAmd).toFixed(2))
  var iTICharge = $('#iteminvoiceTotalInvoiceCharge').val()
  var total2 = (Number(icurrinput) * Number(itotalAmount)) + Number(iTICharge);
  document.getElementById("iteminvoiceCIFFOB").value = total2.toFixed(2);
  var gst1 = Number(document.getElementById("invoiceGSTInput1").value);
  var GIf = Number(document.getElementById("iteminvoiceCIFFOB").value);
  var ans = (gst1 * GIf) / 100;
  document.getElementById("TxtItemSumGST").value = ans.toFixed(2);
  itemAlchoholCalculationFunction();
}

function totalDutiableQtyFunction() {
  if ($("#ItemTotalDutiableQtyInput").val() == $("#itemDuitableQty").val()) {
  }
  else {
    let totDuit = Number($("#ItemTotalDutiableQtyInput").val())
    let typeId = $('#itemDutyIDDummy').val();
    if (totDuit != "") {
      if (!typeId.startsWith('87')) {
        $("#TxtSumExciseDuty").val(totDuit * Number($("#itemExciseDutyInput1").val()))
      }
    }
    itemAlchoholCalculationFunction();
  }
}

function ItemValiDation(VALID, SPANID) {
  $('#' + SPANID).hide();
  if ($('#' + VALID).val() == "" || $('#' + VALID).val() == "--SELECT--" || $('#' + VALID).val() == "0.00" || $('#' + VALID).val() == "--Select--") {
    $('#' + SPANID).show();
    return false;
  }
}

function ItemSave(NEW_ITEM) {
  var check = true;
  if (ItemValiDation('ItemHsCode', 'HsCodeSpan') === false) {
    check = false;
  }
  if (ItemValiDation('itmeDescription', 'itmeDescriptionSpan') === false) {
    check = false;
  }
  if (ItemValiDation('itemCOO1', 'itemCOO1Error') === false) {
    check = false;
  }
  if (ItemValiDation('itemBrandInput', 'itemBrandInputSpan') === false) {
    check = false;
  }
  if (ItemValiDation('ItemHsQtyInput', 'itemHsQuantityInputSpan') === false) {
    check = false;
  }
  if (ItemValiDation('itemHsQuantity', 'itemHsQuantitySpan') === false) {
    check = false;
  }
  if (ItemValiDation('itemInvoiceCurr', 'itemInvoiceCurrSpan') === false) {
    check = false;
  }
  if (ItemValiDation('iteminvoiceTotalLineAmount', 'iteminvoiceTotalLineAmountSpan') === false) {
    check = false;
  }
  if ($('#itemCascID').prop('checked')) {
    if ($("#itemProductCode1").val().trim() == "") {
      check = false;
      alert("Please Check The Item Casc")
    }
  }
  if (check) {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/ItemSaveUrl/',
      dataType: "json",
      data: {
        CascDatas: JSON.stringify(ItemCascSave()),
        ItemNo: $('#ITEMNUMBER').val(),
        PermitId: $('#PermitID').val().toUpperCase(),
        MessageType: $('#MsgType').val(),
        HSCode: $('#ItemHsCode').val(),
        Description: $('#itmeDescription').val(),
        DGIndicator: $('#itemDgIndicator').val(),
        Contry: $('#itemCOO1').val(),
        Brand: $('#itemBrandInput').val(),
        Model: $('#itemModel').val(),
        InHAWBOBL: $('#itemHawb').val(),
        DutiableQty: $('#itemDuitableQty').val(),
        DutiableUOM: $('#ItemDutiableUom').val(),
        TotalDutiableQty: $('#ItemTotalDutiableQtyInput').val(),
        TotalDutiableUOM: $('#itemTotalDuitableUom').val(),
        InvoiceQuantity: $('#itemInvoiceQuantity').val(),
        HSQty: $('#ItemHsQtyInput').val(),
        HSUOM: $('#itemHsQuantity').val(),
        AlcoholPer: $('#itemAlchoholPer').val(),
        InvoiceNo: $('#ItemInvoiceNumber').val(),
        ChkUnitPrice: $('#itemCheckUnitPrice').val(),
        UnitPrice: $('#UnitPrice').val(),
        UnitPriceCurrency: $('#itemInvoiceCurr').val(),
        ExchangeRate: $('#iteminvoiceCurrInput').val(),
        SumExchangeRate: $('#SumExchangeRate').val(),
        TotalLineAmount: $('#iteminvoiceTotalLineAmount').val(),
        InvoiceCharges: $('#iteminvoiceTotalInvoiceCharge').val(),
        CIFFOB: $('#iteminvoiceCIFFOB').val(),
        OPQty: $('#itemOuterPackQtyInput').val(),
        OPUOM: $('#itemOuterPackQtySelect').val(),
        IPQty: $('#itemInPackQuantityInput').val(),
        IPUOM: $('#itemInPackQuantitySelect').val(),
        InPqty: $('#itemInnerPackQtyInput').val(),
        InPUOM: $('#itemInnerPackQtySelect').val(),
        ImPQty: $('#itemInmostPackQtyInput').val(),
        ImPUOM: $('#itemInmostPackQtySelect').val(),
        PreferentialCode: $('#itemPreferntialCode').val(),
        GSTRate: $('#invoiceGSTInput1').val(),
        GSTUOM: $('#invoiceGSTInput2').val(),
        GSTAmount: $('#TxtItemSumGST').val(),
        ExciseDutyRate: $('#itemExciseDutyInput1').val(),
        ExciseDutyUOM: $('#itemExciseDutyInput2').val(),
        ExciseDutyAmount: $('#TxtSumExciseDuty').val(),
        CustomsDutyRate: $('#itemCustomsDutyInput1').val(),
        CustomsDutyUOM: $('#itemCustomsDutyInput2').val(),
        CustomsDutyAmount: $('#itemCustomsDutyInput3').val(),
        OtherTaxRate: $('#itemOtherTaxRate').val(),
        OtherTaxUOM: $('#itemOtherTaxUom').val(),
        OtherTaxAmount: $('#itemOtherTaxAmount').val(),
        CurrentLot: $('#CurrentLot').val(),
        PreviousLot: $('#PreviousLot').val(),
        LSPValue: $('#itemLastSellingPrice').val(),
        Making: $('#Making').val(),
        ShippingMarks1: $('#ShippingMarks1').val(),
        ShippingMarks2: $('#ShippingMarks2').val(),
        ShippingMarks3: $('#ShippingMarks3').val(),
        ShippingMarks4: $('#ShippingMarks4').val(),
        TouchUser: $('#USERNAME').val().toUpperCase(),
        TouchTime: TOUCHTIME,
        VehicleType: $('#VehicalTypeUom').val(),
        EngineCapcity: $('#EngineCapacity').val(),
        EngineCapUOM: $('#EngineCapacityUom').val(),
        orignaldatereg: $('#OriginalRegistrationDate').val(),
        OptionalChrgeUOM: $('#OptionalChrgeUOM').val(),
        Optioncahrge: $('#Optioncahrge').val(),
        OptionalSumtotal: $('#OptionalSumtotal').val(),
        OptionalSumExchage: $('#OptionalSumExchage').val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        ItemData = response.Item;
        ItemCascData = response.ItemCasc;
        ItemLoadData();
        if (NEW_ITEM == 'NewItem') {
          ItemReset();
        }
        else if (NEW_ITEM == 'NextItem') {
          $('#ITEMNUMBER').val($('#ItemNextItemID').val());
        }
        else if (NEW_ITEM == 'PreviousItem') {
          $('#ITEMNUMBER').val($('#ItemNextItemID').val());
        }
        $('#Loading').hide();
        $('#ItemHsCode').focus()
      }
    })
  }
}

function ItemCascSave() {
  var itemNUmber = $("#ITEMNUMBER").val();
  var UserName = $("#USERNAME").val().toUpperCase();
  var cascArray = [];
  var casc1 = document.getElementsByName("cascName1");
  var casc2 = document.getElementsByName("cascName2");
  var casc3 = document.getElementsByName("cascName3");
  var casc4 = document.getElementsByName("cascName4");
  var casc5 = document.getElementsByName("cascName5");

  if ($("#itemProductCode1").val() != "") {
    var row1 = 1;
    for (var i = 0; i < casc1.length; i += 3) {
      cascArray.push({
        "ItemNo": itemNUmber,
        "ProductCode": $("#itemProductCode1").val(),
        "Quantity": $("#product1CodeCopyInput").val(),
        "ProductUOM": $("#product1CodeCopyUom").val(),
        "RowNo": row1,
        "CascCode1": casc1[i].value,
        "CascCode2": casc1[i + 1].value,
        "CascCode3": casc1[i + 2].value,
        "PermitId": $("#PermitID").val().toUpperCase(),
        "MessageType": $("#MsgType").val(),
        "TouchUser": UserName,
        "TouchTime": TOUCHTIME,
        "CascId": "Casc1"
      });
      row1 += 1;
    }
  }

  if ($("#itemProductCode2").val() != "") {
    var row2 = 1;
    for (var i = 0; i < casc2.length; i += 3) {
      cascArray.push({
        "ItemNo": itemNUmber,
        "ProductCode": $("#itemProductCode2").val(),
        "Quantity": $("#product2CodeCopyInput").val(),
        "ProductUOM": $("#product2CodeCopyUom").val(),
        "RowNo": row2,
        "CascCode1": casc2[i].value,
        "CascCode2": casc2[i + 1].value,
        "CascCode3": casc2[i + 2].value,
        "PermitId": $("#PermitID").val().toUpperCase(),
        "MessageType": $("#MsgType").val(),
        "TouchUser": UserName,
        "TouchTime": TOUCHTIME,
        "CascId": "Casc2"
      });
      row2 += 1;
    }
  }

  if ($("#itemProductCode3").val() != "") {
    var row3 = 1;
    for (var i = 0; i < casc3.length; i += 3) {
      cascArray.push({
        "ItemNo": itemNUmber,
        "ProductCode": $("#itemProductCode3").val(),
        "Quantity": $("#product3CodeCopyInput").val(),
        "ProductUOM": $("#product3CodeCopyUom").val(),
        "RowNo": row3,
        "CascCode1": casc3[i].value,
        "CascCode2": casc3[i + 1].value,
        "CascCode3": casc3[i + 2].value,
        "PermitId": $("#PermitID").val().toUpperCase(),
        "MessageType": $("#MsgType").val(),
        "TouchUser": UserName,
        "TouchTime": TOUCHTIME,
        "CascId": "Casc3"
      });
      row3 += 1;
    }
  }

  if ($("#itemProductCode4").val() != "") {
    var row4 = 1;
    for (var i = 0; i < casc4.length; i += 3) {
      cascArray.push({
        "ItemNo": itemNUmber,
        "ProductCode": $("#itemProductCode4").val(),
        "Quantity": $("#product4CodeCopyInput").val(),
        "ProductUOM": $("#product4CodeCopyUom").val(),
        "RowNo": row4,
        "CascCode1": casc4[i].value,
        "CascCode2": casc4[i + 1].value,
        "CascCode3": casc4[i + 2].value,
        "PermitId": $("#PermitID").val().toUpperCase(),
        "MessageType": $("#MsgType").val(),
        "TouchUser": UserName,
        "TouchTime": TOUCHTIME,
        "CascId": "Casc4"
      });
      row4 += 1;
    }
  }

  if ($("#itemProductCode5").val() != "") {
    var row5 = 1;
    for (var i = 0; i < casc5.length; i += 3) {
      cascArray.push({
        "ItemNo": itemNUmber,
        "ProductCode": $("#itemProductCode5").val(),
        "Quantity": $("#product5CodeCopyInput").val(),
        "ProductUOM": $("#product5CodeCopyUom").val(),
        "RowNo": row5,
        "CascCode1": casc5[i].value,
        "CascCode2": casc5[i + 1].value,
        "CascCode3": casc5[i + 2].value,
        "PermitId": $("#PermitID").val().toUpperCase(),
        "MessageType": $("#MsgType").val(),
        "TouchUser": UserName,
        "TouchTime": TOUCHTIME,
        "CascId": "Casc5"
      });
      row5 += 1;
    }
  }
  return cascArray;
}

function CopyHsQuantity(INPUT, UOM) {
  $("#" + INPUT).val($('#ItemHsQtyInput').val())
  $("#" + UOM).val($('#itemHsQuantity').val())
}

function ItemLoadData() {
  var itemCurAmountARR = [];
  $('#ITEMNUMBER').val((ItemData.length) + 1);
  $('#summaryNoOfItems').val(ItemData.length);
  var summaryTotalGstValue = 0;
  var summaryExciseDuty = 0;
  var summaryTotalCIFFOBValue = 0;
  var summaryCustomsDuty = 0;
  var itemOtherTaxAmountSummary = 0;
  var Table = ``
  if (ItemData.length < 1) {
    $("#ItemTable tbody").html("<tr><td colspan = 14 style = 'text-align:center'>No Record</td></tr>")
  }
  else {

    for (var itemeData of ItemData) {

      var Color = ItemHsCodeData.filter((data) => {
        if (data.HSCode == itemeData.HSCode && data.Inpayment == '1') {
          return true
        }
      })

      if (Color.length != 0) {
        Color = "red"
      }
      else {
        Color = '#000'
      }
      itemCurAmountARR.push([
        itemeData.UnitPriceCurrency,
        Number(itemeData.TotalLineAmount),
      ]);
      Table += `
            <tr style="color:${Color}">
                <td><input type="checkbox" class="inputStyleCheckBox" value="${itemeData.ItemNo}" name="itemCheckDel"></td>
                <td><i class="fa-regular fa-pen-to-square" style="color: #ff0000;" onclick="ItemEdit(${itemeData.ItemNo})"></i></td>
                <td>${itemeData.ItemNo}</td>
                <td>${itemeData.HSCode}</td>
                <td>${itemeData.Description}</td>
                <td>${itemeData.Contry}</td>
                <td>${itemeData.InHAWBOBL}</td>
                <td>${itemeData.UnitPriceCurrency}</td>
                <td>${itemeData.CIFFOB}</td>
                <td>${itemeData.HSQty}</td>
                <td>${itemeData.HSUOM}</td>
                <td>${itemeData.GSTAmount}</td>
                <td>${itemeData.TotalLineAmount}</td>
            </tr>`;
      summaryTotalGstValue += Number(itemeData.GSTAmount);
      summaryExciseDuty += Number(itemeData.ExciseDutyAmount);
      summaryTotalCIFFOBValue += Number(itemeData.CIFFOB);
      summaryCustomsDuty += Number(itemeData.CustomsDutyAmount);
      itemOtherTaxAmountSummary += Number(itemeData.OtherTaxAmount);
    }
    $("#ItemTable tbody").html(Table);
    $("#summaryTotalGstValue").val(summaryTotalGstValue.toFixed(2));
    $("#summaryExciseDuty").val(summaryExciseDuty.toFixed(2));
    $("#summaryTotalCIFFOBValue").val(summaryTotalCIFFOBValue.toFixed(2));
    $("#summaryCustomsDuty").val(summaryCustomsDuty.toFixed(2));
    $("#itemOtherTaxAmountSummary").val(itemOtherTaxAmountSummary.toFixed(2));
    $("#summaryTotalPayable").val(summaryTotalGstValue.toFixed(2));
    $("#summaryTotalItemGst").val(summaryTotalGstValue.toFixed(2));

    if ($("#declarationType").val() == "DNG : Duty & GST") {
      let suTot = itemOtherTaxAmountSummary + summaryTotalGstValue + summaryExciseDuty + summaryCustomsDuty;
      $("#summaryTotalPayable").val(suTot.toFixed(2));
    }

    summarySumOfItemAmoutFunction(itemCurAmountARR);
  }
  if ($('#ShowEdit').val() == 'True') {
    $('input').prop('disabled', true);
  }
}

function ItemEdit(Arg) {
  for (var i of ItemData) {
    if (i.ItemNo == Arg) {
      $('#itemUnBrand').prop('checked', false);
      $('#itemDgIndicator').prop('checked', false);
      $("#UnitPriceIDShow").prop("checked", false);
      $("#shippingMarkCheck").prop("checked", false);
      $("#lotIdCheck").prop("checked", false);
      $("#packing_details").prop("checked", false);
      $('#ITEMNUMBER').val(Arg);
      $('#ItemNextItemID').val(Arg);
      $('#MsgType').val(i.MessageType);
      $('#ItemHsCode').val(i.HSCode);
      $('#itemDgIndicator').val(i.DGIndicator);
      if (i.DGIndicator == "True") {
        $('#itemDgIndicator').prop('checked', true);
      }
      $('#itemCOO1').val(i.Contry);
      $('#itemBrandInput').val(i.Brand);
      if (i.Brand == "UNBRANDED") {
        $('#itemUnBrand').prop('checked', true);
      }
      $('#itemModel').val(i.Model);
      if (i.InHAWBOBL != "") {
        $('#itemHawb').val(i.InHAWBOBL);
      } if (i.InHAWBOBL == "") {
        $('#itemHawb').val("");
      }
      $('#itemDuitableQty').val(i.DutiableQty);
      $('#ItemDutiableUom').val(i.DutiableUOM);
      $('#ItemTotalDutiableQtyInput').val(i.TotalDutiableQty);
      $('#itemTotalDuitableUom').val(i.TotalDutiableUOM);
      $('#itemInvoiceQuantity').val(i.InvoiceQuantity);
      $('#ItemHsQtyInput').val(i.HSQty);
      $('#itemHsQuantity').val(i.HSUOM);
      $('#itemAlchoholPer').val(i.AlcoholPer);
      $('#ItemInvoiceNumber').val(i.InvoiceNo);
      $('#itemCheckUnitPrice').val(i.ChkUnitPrice);
      $('#UnitPrice').val(i.UnitPrice);
      $('#itemInvoiceCurr').val(i.UnitPriceCurrency);
      $('#iteminvoiceCurrInput').val(i.ExchangeRate);
      $('#SumExchangeRate').val(i.SumExchangeRate);
      $('#iteminvoiceTotalLineAmount').val(i.TotalLineAmount);
      $('#iteminvoiceTotalInvoiceCharge').val(i.InvoiceCharges);
      $('#iteminvoiceCIFFOB').val(i.CIFFOB);
      $('#itemOuterPackQtyInput').val(i.OPQty);
      $('#itemOuterPackQtySelect').val(i.OPUOM);
      $('#itemInPackQuantityInput').val(i.IPQty);
      $('#itemInPackQuantitySelect').val(i.IPUOM);
      $('#itemInnerPackQtyInput').val(i.InPqty);
      $('#itemInnerPackQtySelect').val(i.InPUOM);
      $('#itemInmostPackQtyInput').val(i.ImPQty);
      $('#itemInmostPackQtySelect').val(i.ImPUOM);
      if ("--SELECT--" == i.PreferentialCode || i.PreferentialCode == "--Select--") {
        $('#itemPreferntialCode').val("--Select--");
      }
      else {
        $('#itemPreferntialCode').val(i.PreferentialCode);
      }

      //$('#invoiceGSTInput1').val(i.GSTRate);
      $('#invoiceGSTInput2').val(i.GSTUOM);
      $('#TxtItemSumGST').val(i.GSTAmount);
      $('#itemExciseDutyInput1').val(i.ExciseDutyRate);
      $('#itemExciseDutyInput2').val(i.ExciseDutyUOM);
      $('#TxtSumExciseDuty').val(i.ExciseDutyAmount);
      $('#itemCustomsDutyInput1').val(i.CustomsDutyRate);
      $('#itemCustomsDutyInput2').val(i.CustomsDutyUOM);
      $('#itemCustomsDutyInput3').val(i.CustomsDutyAmount);
      $('#itemOtherTaxRate').val(i.OtherTaxRate);
      if (i.OtherTaxUOM == "--Select--" || i.OtherTaxUOM == "--SELECT--") {
        $('#itemOtherTaxUom').val("--Select--");
      }
      else {
        $('#itemOtherTaxUom').val(i.OtherTaxUOM);
      }

      $('#itemOtherTaxAmount').val(i.OtherTaxAmount);
      $('#CurrentLot').val(i.CurrentLot);
      $('#PreviousLot').val(i.PreviousLot);
      $('#itemLastSellingPrice').val(i.LSPValue);
      $('#Making').val(i.Making);
      $('#ShippingMarks1').val(i.ShippingMarks1);
      $('#ShippingMarks2').val(i.ShippingMarks2);
      $('#ShippingMarks3').val(i.ShippingMarks3);
      $('#ShippingMarks4').val(i.ShippingMarks4);
      $('#VehicalTypeUom').val(i.VehicleType);
      $('#EngineCapacity').val(i.EngineCapcity);
      $('#EngineCapacityUom').val(i.EngineCapUOM);
      $('#OriginalRegistrationDate').val(i.orignaldatereg);
      $('#OptionalChrgeUOM').val(i.OptionalChrgeUOM);
      $('#Optioncahrge').val(i.Optioncahrge);
      $('#OptionalSumtotal').val(i.OptionalSumtotal);
      $('#OptionalSumExchage').val(i.OptionalSumExchage);
      if ($("#SumExchangeRate").val() == "0.0000" || $("#UnitPrice").val() == "0.0000") {
        $("#UnitPriceIDShow").prop("checked", true);
        itemCheckUnitPriceFunction();
      }
      if (i.ShippingMarks1 != "" || i.ShippingMarks2 != "" || i.ShippingMarks3 != "" || i.ShippingMarks4 != "") {
        $("#shippingMarkCheck").prop("checked", true);
        ItemCascShowAll('#shippingMarkCheck', '.ShippingMark')
      }
      if (i.CurrentLot != "" && i.PreviousLot != "" && (i.Making != "--SELECT--" || i.Making != "--Select--")) {
        $("#lotIdCheck").prop("checked", true);
        ItemCascShowAll('#lotIdCheck', '.OutLotId')
      }
      if (i.OPQty != "0") {
        $("#packing_details").prop("checked", true);
        ItemCascShowAll('#packing_details', '.PackingDetails')
      }

      HsOnFocusOut();
      invoiceNumberFunction();
      invoiceTotalLineAmountFunction();
      CountryFocusOut()
      dutiableQtyFunction();
      if (i.Description == "") {
        HsOnFocusOut()
      }
      else {
        $('#itmeDescription').val(i.Description);
      }
      ItemCascEdit(i.ItemNo);
      $("#ITEMNUMBER").focus();
      break;
     
    }
  }
}

var CascTable1 = '';
var CascTable2 = '';
var CascTable3 = '';
var CascTable4 = '';
var CascTable5 = '';
function CascEditUpdate(proCode, CopyInput, CopyUom, TableName, InputName, Data) {
  $(proCode).val(Data.ProductCode);
  $(CopyInput).val(Data.Quantity);
  $(CopyUom).val(Data.ProductUOM);
  var cascTab = `<tr>
              <td><input type="text" class="inputStyle" name="${InputName}" value = '${Data.CascCode1}' tabindex="22"></td>
              <td><input type="text" class="inputStyle" name="${InputName}" value = '${Data.CascCode2}' tabindex="23"></td>
              <td><input type="text" class="inputStyle" name="${InputName}" value = '${Data.CascCode3}' tabindex="24"></td>
              <td class="OutItemCascDeleteButton" onclick = "ItemCascDelete('${Data.id}','${Data.PermitId}')"><i class="material-icons" style="color:red">delete</i></td>
          </tr>`;
  if (InputName == "cascName1") {
    CascTable1 += cascTab
  }
  if (InputName == "cascName2") {
    CascTable2 += cascTab
  }
  if (InputName == "cascName3") {
    CascTable3 += cascTab
  }
  if (InputName == "cascName4") {
    CascTable4 += cascTab
  }
  if (InputName == "cascName5") {
    CascTable5 += cascTab
  }
}
function ItemCascDelete(ID, PermitID) {
  $('#Loading').show();
  $.ajax({
    url: '/CascDelete/',
    type: 'GET',
    data: {
      ID: ID,
      PermitID: PermitID
    },
    success: function (response) {
      ItemCascData = response.ItemCasc;
      $('#Loading').hide();
    }
  })
}
function ItemDelete() {

  if ($('#ItemHeadCheck').prop('checked')) {
    $('#Loading').show();
    $.ajax({
      url: '/ItemAllDelte/',
      type: 'GET',
      data: {
        PermitId: $('#PermitID').val().toUpperCase(),
      },
      success: function (response) {
        ItemData = response.Item;
        ItemCascData = response.ItemCasc;
        ItemLoadData();
        $('#Loading').hide();
        $('#ItemHeadCheck').prop("checked", false)
      }
    })
  }
  else {
    var CheckArray = [];
    var CheckBoxName = document.getElementsByName('itemCheckDel');
    for (var i of CheckBoxName) {
      if (i.checked) {
        CheckArray.push(i.value);
      }
    }
    if (CheckArray != "") {
      $('#Loading').show();
      $.ajax({
        url: '/ItemDelete/',
        type: 'GET',
        data: {
          PermitId: $('#PermitID').val().toUpperCase(),
          ItemNo: JSON.stringify(CheckArray)
        },
        success: function (response) {
          ItemData = response.Item;
          ItemCascData = response.ItemCasc;
          ItemLoadData();
          ItemReset();
          $('#Loading').hide();
          $('#ItemHeadCheck').prop("checked", false)
        }
      })
    }
  }
}
function ItemCascEdit(Arg) {
  // $('#itemCascID').prop('checked', false); we need to check when its false or true not when you click the edit all button
  $("#ProductCode3").prop("checked", false);
  $("#ProductCode4").prop("checked", false);
  $("#ProductCode5").prop("checked", false);
  for (var i of ItemCascData) {
    if (i.ItemNo == Arg) {
      $('#itemCascID').prop('checked', true);
      if (i.CASCId == 'Casc1' || i.CascId == 'Casc1') {
        CascEditUpdate('#itemProductCode1', '#product1CodeCopyInput', '#product1CodeCopyUom', "ItemCascTable1", 'cascName1', i)
        $("#ItemCascTable1 tbody").html(CascTable1);
      }
      if (i.CASCId == 'Casc2') {
        CascEditUpdate('#itemProductCode2', '#product2CodeCopyInput', '#product2CodeCopyUom', "ItemCascTable2", 'cascName2', i)
        $("#ItemCascTable2 tbody").html(CascTable2);
      }
      if (i.CASCId == 'Casc3') {
        $("#ProductCode3").prop("checked", true);
        ItemCascShowAll('#ProductCode3', '.OutCasc3');
        CascEditUpdate('#itemProductCode3', '#product3CodeCopyInput', '#product3CodeCopyUom', "ItemCascTable3", 'cascName3', i)
        $("#ItemCascTable3 tbody").html(CascTable3);
      }
      if (i.CASCId == 'Casc4') {
        $("#ProductCode4").prop("checked", true);
        ItemCascShowAll('#ProductCode4', '.OutCasc4');
        CascEditUpdate('#itemProductCode4', '#product4CodeCopyInput', '#product4CodeCopyUom', "ItemCascTable4", 'cascName4', i)
        $("#ItemCascTable4 tbody").html(CascTable4);
      }
      if (i.CASCId == 'Casc5') {
        $("#ProductCode5").prop("checked", true);
        ItemCascShowAll('#ProductCode5', '.OutCasc5');
        CascEditUpdate('#itemProductCode5', '#product5CodeCopyInput', '#product5CodeCopyUom', "ItemCascTable5", 'cascName5', i)
        $("#ItemCascTable5 tbody").html(CascTable5);
      }
    }
  }
  ItemCascShowAll('#itemCascID', '.OutItemCascHide');
  CascTable1 = "";
  CascTable2 = "";
  CascTable3 = "";
  CascTable4 = "";
  CascTable5 = "";
}

function ItemReset() {
  $('#Item input').prop('checked', false);
  $('#Item :input[type="number"]').val("0.00");
  $('#Item :input[type="text"]').val("");
  $('#Item select').val("--Select--");
  $('#Item textarea').val("");
  ItemCascShowAll('#packing_details', '.PackingDetails')
  ItemCascShowAll('#itemCascID', '.OutItemCascHide')
  ItemCascShowAll('#shippingMarkCheck', '.ShippingMark')
  ItemCascShowAll('#lotIdCheck', '.OutLotId')
  $('#ITEMNUMBER').val(Number($('#summaryNoOfItems').val()) + 1);
  $('#invoiceGSTInput2').val('PER');
  $('#invoiceGSTInput1').val(8);
  $(".OutItemCascHide p").html("")
  CargoHawbOut();
  $("#hsControledId").hide();
}

function ItemDelAllCheckBox() {
  if ($('#ItemHeadCheck').prop('checked')) {
    $('#ItemTable input').prop('checked', true);
  }
  else {
    $('#ItemTable input').prop('checked', false);
  }
}

function ItemUploadData() {
  var fileInput = document.getElementById("InpaymentFile");
  if (fileInput.value != "") {
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append("file", file);
    formData.append("PermitId", $('#PermitID').val().toUpperCase());
    formData.append("MsgType", $('#MsgType').val());
    formData.append("UserName", $('#USERNAME').val().toUpperCase());
    formData.append("TouchTime", TOUCHTIME);
    formData.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/ItemExcelUpload/',
      dataType: "json",
      processData: false,
      contentType: false,
      data: formData,
      mimeType: "multipart/form-data",
      success: function (response) {
        ItemData = response.Item;
        ItemCascData = response.ItemCasc;
        alert(response.message);
        ItemLoadData();
        $('#Loading').hide();
      },
      error: function (response) {
        $('#Loading').hide();
      }
    })
  }
}

function ItemEditAll() {
  // $('#editAllitemBtn').prop('disabled', true)
  $('#Loading').show();
  setTimeout(ItemEditAll1, 1000);
}

// async function ItemEditAll1() {
//   $('#Loading').show();
//   var ItemAllData = [];
//   for (var item of ItemData) {
//     console.log("Item:", item);
//     ItemEdit(item.ItemNo)
//     let echeck = false;
//     console.log($('#itemCascID').prop('checked'))
//     if ($('#itemCascID').prop('checked')) {
//       if ($('#itemProductCode1').val() != "") {
//         echeck = true
//       }
//       else {
//         echeck = false
//       }
//     }
//     if (echeck) {
//       ItemAllData.push({
//         ItemNo: $('#ITEMNUMBER').val(),
//         PermitId: $('#PermitID').val().toUpperCase(),
//         MessageType: $('#MsgType').val(),
//         HSCode: $('#ItemHsCode').val(),
//         Description: $('#itmeDescription').val(),
//         DGIndicator: $('#itemDgIndicator').val(),
//         Contry: $('#itemCOO1').val(),
//         Brand: $('#itemBrandInput').val(),
//         Model: $('#itemModel').val(),
//         InHAWBOBL: $('#itemHawb').val(),
//         DutiableQty: $('#itemDuitableQty').val(),
//         DutiableUOM: $('#ItemDutiableUom').val(),
//         TotalDutiableQty: $('#ItemTotalDutiableQtyInput').val(),
//         TotalDutiableUOM: $('#itemTotalDuitableUom').val(),
//         InvoiceQuantity: $('#itemInvoiceQuantity').val(),
//         HSQty: $('#ItemHsQtyInput').val(),
//         HSUOM: $('#itemHsQuantity').val(),
//         AlcoholPer: $('#itemAlchoholPer').val(),
//         InvoiceNo: $('#ItemInvoiceNumber').val(),
//         ChkUnitPrice: $('#itemCheckUnitPrice').val(),
//         UnitPrice: $('#UnitPrice').val(),
//         UnitPriceCurrency: $('#itemInvoiceCurr').val(),
//         ExchangeRate: $('#iteminvoiceCurrInput').val(),
//         SumExchangeRate: $('#SumExchangeRate').val(),
//         TotalLineAmount: $('#iteminvoiceTotalLineAmount').val(),
//         InvoiceCharges: $('#iteminvoiceTotalInvoiceCharge').val(),
//         CIFFOB: $('#iteminvoiceCIFFOB').val(),
//         OPQty: $('#itemOuterPackQtyInput').val(),
//         OPUOM: $('#itemOuterPackQtySelect').val(),
//         IPQty: $('#itemInPackQuantityInput').val(),
//         IPUOM: $('#itemInPackQuantitySelect').val(),
//         InPqty: $('#itemInnerPackQtyInput').val(),
//         InPUOM: $('#itemInnerPackQtySelect').val(),
//         ImPQty: $('#itemInmostPackQtyInput').val(),
//         ImPUOM: $('#itemInmostPackQtySelect').val(),
//         PreferentialCode: $('#itemPreferntialCode').val(),
//         GSTRate: $('#invoiceGSTInput1').val(),
//         GSTUOM: $('#invoiceGSTInput2').val(),
//         GSTAmount: $('#TxtItemSumGST').val(),
//         ExciseDutyRate: $('#itemExciseDutyInput1').val(),
//         ExciseDutyUOM: $('#itemExciseDutyInput2').val(),
//         ExciseDutyAmount: $('#TxtSumExciseDuty').val(),
//         CustomsDutyRate: $('#itemCustomsDutyInput1').val(),
//         CustomsDutyUOM: $('#itemCustomsDutyInput2').val(),
//         CustomsDutyAmount: $('#itemCustomsDutyInput3').val(),
//         OtherTaxRate: $('#itemOtherTaxRate').val(),
//         OtherTaxUOM: $('#itemOtherTaxUom').val(),
//         OtherTaxAmount: $('#itemOtherTaxAmount').val(),
//         CurrentLot: $('#CurrentLot').val(),
//         PreviousLot: $('#PreviousLot').val(),
//         LSPValue: $('#itemLastSellingPrice').val(),
//         Making: $('#Making').val(),
//         ShippingMarks1: $('#ShippingMarks1').val(),
//         ShippingMarks2: $('#ShippingMarks2').val(),
//         ShippingMarks3: $('#ShippingMarks3').val(),
//         ShippingMarks4: $('#ShippingMarks4').val(),
//         TouchUser: $('#USERNAME').val().toUpperCase(),
//         TouchTime: TOUCHTIME,
//         VehicleType: $('#VehicalTypeUom').val(),
//         EngineCapcity: $('#EngineCapacity').val(),
//         EngineCapUOM: $('#EngineCapacityUom').val(),
//         orignaldatereg: $('#OriginalRegistrationDate').val(),
//         OptionalChrgeUOM: $('#OptionalChrgeUOM').val(),
//         Optioncahrge: $('#Optioncahrge').val(),
//         OptionalSumtotal: $('#OptionalSumtotal').val(),
//         OptionalSumExchage: $('#OptionalSumExchage').val(),
//       })
//     }
//     ItemReset();
//   }
//   $('#Loading').show();
//   $.ajax({
//     type: 'POST',
//     url: '/AllItemUpdate/',
//     data: {
//       'Item': JSON.stringify(ItemAllData),
//       'PermitId': $('#PermitID').val().toUpperCase(),
//       'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
//     },
//     success: function (response) {
//       ItemData = response.Item;
//       ItemCascData = response.ItemCasc;
//       alert(response.message)
//       ItemLoadData();
//       $('#Loading').hide();
//     }
//   })
// }
async function ItemEditAll1() {
  $('#Loading').show();
  var ItemAllData = [];
  for (var item of ItemData) {
    console.log("Item:", item);
    ItemEdit(item.ItemNo)
    let echeck = true;
    // console.log($('#itemCascID').prop('checked'))
    if ($('#itemCascID').prop('checked')) {
      if ($('#itemProductCode1').val() == ""){
        echeck = false;      
      }     
    }
    if (echeck) {
      console.log('echeck:', echeck);
      console.log('ItemNo:', $('#ITEMNUMBER').val());
      ItemAllData.push({
        ItemNo: $('#ITEMNUMBER').val(),
        PermitId: $('#PermitID').val().toUpperCase(),
        MessageType: $('#MsgType').val(),
        HSCode: $('#ItemHsCode').val(),
        Description: $('#itmeDescription').val(),
        DGIndicator: $('#itemDgIndicator').val(),
        Contry: $('#itemCOO1').val(),
        Brand: $('#itemBrandInput').val(),
        Model: $('#itemModel').val(),
        InHAWBOBL: $('#itemHawb').val(),
        DutiableQty: $('#itemDuitableQty').val(),
        DutiableUOM: $('#ItemDutiableUom').val(),
        TotalDutiableQty: $('#ItemTotalDutiableQtyInput').val(),
        TotalDutiableUOM: $('#itemTotalDuitableUom').val(),
        InvoiceQuantity: $('#itemInvoiceQuantity').val(),
        HSQty: $('#ItemHsQtyInput').val(),
        HSUOM: $('#itemHsQuantity').val(),
        AlcoholPer: $('#itemAlchoholPer').val(),
        InvoiceNo: $('#ItemInvoiceNumber').val(),
        ChkUnitPrice: $('#itemCheckUnitPrice').val(),
        UnitPrice: $('#UnitPrice').val(),
        UnitPriceCurrency: $('#itemInvoiceCurr').val(),
        ExchangeRate: $('#iteminvoiceCurrInput').val(),
        SumExchangeRate: $('#SumExchangeRate').val(),
        TotalLineAmount: $('#iteminvoiceTotalLineAmount').val(),
        InvoiceCharges: $('#iteminvoiceTotalInvoiceCharge').val(),
        CIFFOB: $('#iteminvoiceCIFFOB').val(),
        OPQty: $('#itemOuterPackQtyInput').val(),
        OPUOM: $('#itemOuterPackQtySelect').val(),
        IPQty: $('#itemInPackQuantityInput').val(),
        IPUOM: $('#itemInPackQuantitySelect').val(),
        InPqty: $('#itemInnerPackQtyInput').val(),
        InPUOM: $('#itemInnerPackQtySelect').val(),
        ImPQty: $('#itemInmostPackQtyInput').val(),
        ImPUOM: $('#itemInmostPackQtySelect').val(),
        PreferentialCode: $('#itemPreferntialCode').val(),
        GSTRate: $('#invoiceGSTInput1').val(),
        GSTUOM: $('#invoiceGSTInput2').val(),
        GSTAmount: $('#TxtItemSumGST').val(),
        ExciseDutyRate: $('#itemExciseDutyInput1').val(),
        ExciseDutyUOM: $('#itemExciseDutyInput2').val(),
        ExciseDutyAmount: $('#TxtSumExciseDuty').val(),
        CustomsDutyRate: $('#itemCustomsDutyInput1').val(),
        CustomsDutyUOM: $('#itemCustomsDutyInput2').val(),
        CustomsDutyAmount: $('#itemCustomsDutyInput3').val(),
        OtherTaxRate: $('#itemOtherTaxRate').val(),
        OtherTaxUOM: $('#itemOtherTaxUom').val(),
        OtherTaxAmount: $('#itemOtherTaxAmount').val(),
        CurrentLot: $('#CurrentLot').val(),
        PreviousLot: $('#PreviousLot').val(),
        LSPValue: $('#itemLastSellingPrice').val(),
        Making: $('#Making').val(),
        ShippingMarks1: $('#ShippingMarks1').val(),
        ShippingMarks2: $('#ShippingMarks2').val(),
        ShippingMarks3: $('#ShippingMarks3').val(),
        ShippingMarks4: $('#ShippingMarks4').val(),
        TouchUser: $('#USERNAME').val().toUpperCase(),
        TouchTime: TOUCHTIME,
        VehicleType: $('#VehicalTypeUom').val(),
        EngineCapcity: $('#EngineCapacity').val(),
        EngineCapUOM: $('#EngineCapacityUom').val(),
        orignaldatereg: $('#OriginalRegistrationDate').val(),
        OptionalChrgeUOM: $('#OptionalChrgeUOM').val(),
        Optioncahrge: $('#Optioncahrge').val(),
        OptionalSumtotal: $('#OptionalSumtotal').val(),
        OptionalSumExchage: $('#OptionalSumExchage').val(),
      })
    }
    ItemReset();
  }
  $('#Loading').show();
  $.ajax({
    type: 'POST',
    url: '/AllItemUpdate/',
    data: {
      'Item': JSON.stringify(ItemAllData),
      'PermitId': $('#PermitID').val().toUpperCase(),
      'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      ItemData = response.Item;
      ItemCascData = response.ItemCasc;
      alert(response.message)
      ItemLoadData();
      $('#Loading').hide();
    }
  })
}

function ItemConsolidate() {
  $('#Loading').show();
  try {
    $.ajax({
      url: "/InpaymentConsolidate/",
      type: "POST",
      data: {
        PermitId: $("#PermitID").val().toUpperCase(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        ItemData = response.Item;
        ItemCascData = response.ItemCasc;
        ItemLoadData();
        $('#Loading').hide();
      },
      error: function (response) {
        $('#Loading').hide();
        // $('#editAllitemBtn').prop('disabled',true)
      },
    });
  }
  catch {
    alert("Somthig error")
  }

}


function NextItem() {
  if ($('#ItemNextItemID').val() != "") {
    ItemSave('NextItem');
    var ItemNum = Number($('#ItemNextItemID').val()) + 1;
    ItemEdit(ItemNum);
  }

}

function PreviousItem() {
  if ($('#ItemNextItemID').val() != "") {
    ItemSave('PreviousItem');
    var ItemNum = Number($('#ItemNextItemID').val()) - 1;
    ItemEdit(ItemNum);
  }
}

function summaryPreviousFunction() {
  var Val = $('#PreviousPermitNo').val();
  $('#summaryTradeRemarks').val("PREVIOUS PERMIT NO : " + Val);
}

function summaryEXRateFunction() {
  let trade = document.getElementById("summaryTradeRemarks");
  let arr1 = [];
  let arr2 = [];
  for (let i = 0; i < InvoiceData.length; i++) {
    if (0 == i) {
      arr1.push(InvoiceData[i].TICurrency);
      arr2.push([InvoiceData[i].TICurrency, InvoiceData[i].TIExRate])
    } else {
      if (arr1.includes(InvoiceData[i].TICurrency)) {
        var sase = 0;
      } else {
        arr1.push(InvoiceData[i].TICurrency);
        arr2.push([InvoiceData[i].TICurrency, InvoiceData[i].TIExRate])
      }
    }
  }
  for (let j = 0; j < arr2.length; j++) {
    trade.value = trade.value + " CURRENCY : " + arr2[j][0] + " , EXCHANGE RATE : " + arr2[
      j][1] + "\n";
  }
}
function summaryConfigBtnFunction() {
  let trade = document.getElementById("summaryTradeRemarks");
  let remark = document.getElementById("summaryFormatRemark").value;
  let sp = trade.value.replaceAll("\n", remark);
  document.getElementById("summaryTradeRemarks").value = sp;
}

function summarySumOfItemAmoutFunction(itemCurAmountARR) {
  document.getElementById("summarySumOfItemAmout").innerHTML = "";
  let a = itemCurAmountARR;
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
    x.setAttribute("name", 'summarySumOfItemAmout');
    x.setAttribute("value", `${c[y][0]} : ${c[y][1].toFixed(2)}`);
    document.getElementById('summarySumOfItemAmout').appendChild(x);
    $('#summarySumOfItemValue').val(c[y][1].toFixed(2))
  }
}

function summarySumOfInvoiceAmountFunction(invoiceCurAmountARR) {
  document.getElementById("summarySumOfInvoiceAmount").innerHTML = "";
  let a = invoiceCurAmountARR;
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
    x.setAttribute("name", 'summarySumOfInvoiceAmount');
    document.getElementById('summarySumOfInvoiceAmount').appendChild(x);
  }
  let artst = c.toString()
  document.getElementById('summaryInvoiceAmount').innerHTML = artst.replaceAll(",", " ");
}

function SummaryLoad() {
  var importer = $('#ImporterCruei').val() + "-" + $('#ImporterName').val();
  var NoOfPacking = $('#CargoTotalOuterPack').val() + " " + $('#CargoOuterPack').val();
  var Gross = $('#CargoTotalGrossweight').val() + " " + $('#CargoTotalGrossUOM').val();
  let MawbValue = $('#CargoMawb').val().trim().toUpperCase();
  let OblValue = $('#CargoObl').val().trim().toUpperCase();
  let InMAWB = MawbValue !== "" ? MawbValue : OblValue;

  $('#SummaryImporter').html(importer);
  $('#SummarymawbObl').html(InMAWB);
  $('#Summarynoofpacking').html(NoOfPacking);
  $('#SummaryHawbHbl').html($('#CargoHbl').val());
  $('#SummaryGrossWeight').html(Gross);
  $('#SummaryTotalGst').html($("#summaryTotalGstValue").val());
  $('#SummaryTotalIncoiseGSt').html($("#summaryTotalGstValue").val());

  var SInvoice = (document.getElementsByName('summarySumOfInvoiceAmount')[0].value).split('.');
  var SItem = (document.getElementsByName('summarySumOfItemAmout')[0].value).split('.');
  if ((Number(SInvoice[0]) === Number(SItem[0])) || Number($('#summaryTotalInvoiceCIFValue').val()) === Number($('#summaryTotalCIFFOBValue').val())) {
    $('#SUmmaryEqualNot').hide();
  }
  else {
    $('#SUmmaryEqualNot').show();
  }
}

function HeaderDocumentAttch() {
  var FileName = 'HeadAttach'
  var MeesageID = $("#MSGID").val();
  var PermitId = $("#PermitID").val().toUpperCase();
  var UserName = $("#USERNAME").val().toUpperCase();
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
  formData.append("DocumentType", $('#HeaddocumentType').val());
  formData.append("InPaymentId", MeesageID);
  formData.append("FilePath", "D:\\Users\\Public\\QXMF004\\NewDocument");
  formData.append("Size", size + " KB");
  formData.append("PermitId", PermitId);
  formData.append("UserName", UserName);
  formData.append("Type", 'NEW');
  formData.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
  var csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
  });
  $('#Loading').show();
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/HeaderDocumentSave/",
    processData: false,
    contentType: false,
    mimeType: "multipart/form-data",
    data: formData,
    success: function (response) {
      InFile = response.Infile;
      DocumentLoadFunction();
      $('#Loading').hide();
    },
    error: function (response) {
      $('#Loading').hide();
    }
  });
}

function DocumentLoadFunction() {

  var check = false;
  var Tab = ''
  for (var i of InFile) {
    if (i.Type == 'NEW') {
      check = true;
      Tab += `<tr>
      <td class = "DocumentDelClass"> <i class="material-icons" style="color:red;font-size : 12px" value = "${i.Id}" onclick = 'DocumentDelete("${i.Id}")' >delete</i></td>
      <td>${i.DocumentType}</td>
      <td><a href = '/headAttachDownload/${i.Id}/' style="text-decoration:none">${i.Name}</a></td>
      <td>${i.Size}</td>
  </tr>`
    }
  }
  if (check) {
    $('#HeaderDocumentTableshow').show();
    $('#HeaderAttachTable tbody').html(Tab);
    $("#ReferenceDocuments").prop('checked', true);
    $('#OutReferenceShow').show();
  }

}

function DocumentDelete(Val) {
  $('#Loading').show();
  $.ajax({
    url: '/DocumentDelete/',
    type: 'GET',
    data: {
      ID: Val,
      PermitID: $('#PermitID').val().toUpperCase(),
    },
    success: function (response) {
      Infile = response.Infile
      $('#Loading').hide();
    }
  })
}
$(document).on("click", ".DocumentDelClass", function () {
  $(this).closest("tr").remove();
  var rowCount = $("#HeaderAttachTable tr").length;
  if (rowCount <= 1) {
    $('#HeaderDocumentTableshow').hide();
  }
});

function CpcSaveFunction() {
  var cpcArray = [];
  var AeoName = document.getElementsByName("AeoName");
  var CwcName = document.getElementsByName("CwcName");
  var schemeName = document.getElementsByName("SchemeName");
  var UserName = $('#USERNAME').val().toUpperCase();

  if ($("#Aeo").prop("checked")) {
    var row1 = 1;
    for (var i = 0; i < AeoName.length; i += 3) {
      cpcArray.push({
        "PermitId": $('#PermitID').val().toUpperCase(),
        "MessageType": $("#MsgType").val(),
        "RowNo": row1,
        "CpcType": "AEO",
        "ProcessingCode1": AeoName[i].value,
        "ProcessingCode2": AeoName[i + 1].value,
        "ProcessingCode3": AeoName[i + 2].value,
        "TouchUser": UserName,
        "TouchTime": TOUCHTIME,
      });
      row1 += 1;
    }
  }

  if ($("#Cwc").prop("checked")) {
    var row2 = 1;
    for (var i = 0; i < CwcName.length; i += 3) {
      cpcArray.push({
        "PermitId": $('#PermitID').val().toUpperCase(),
        "MessageType": $("#MsgType").val(),
        "RowNo": row2,
        "CpcType": "CWC",
        "ProcessingCode1": CwcName[i].value,
        "ProcessingCode2": CwcName[i + 1].value,
        "ProcessingCode3": CwcName[i + 2].value,
        "TouchUser": UserName,
        "TouchTime": TOUCHTIME,
      });
      row2 += 1;
    }
  }

  if ($("#Scheme").prop("checked")) {
    var row3 = 1;
    for (var i = 0; i < schemeName.length; i += 3) {
      cpcArray.push({
        "PermitId": $('#PermitID').val().toUpperCase(),
        "MessageType": $("#MsgType").val(),
        "RowNo": row3,
        "CpcType": "SCHEME",
        "ProcessingCode1": schemeName[i].value,
        "ProcessingCode2": schemeName[i + 1].value,
        "ProcessingCode3": schemeName[i + 2].value,
        "TouchUser": UserName,
        "TouchTime": TOUCHTIME,
      });
      row3 += 1;
    }
  }
  var jsonData = JSON.stringify(cpcArray);
  return jsonData;
}

function FinalSubmit() {
  $('#FinalSuccess').hide();
  $('#Header span ').hide();
  $('#FinalPopUpHeader tbody ').html('');
  $('#FinalPopUpParty tbody ').html('');
  $('#FinalPopUpCargo tbody').html('');
  $('#FinalPopUpInvoice tbody').html('');
  $('#FinalPopUpItem tbody').html('');
  $('#FinalPopUpSummary tbody').html('');
  $('#FinalPopUpRefund tbody').html('');

  var Chcek = true;

  /*----------------------------------------------------------------HEADER PAGE VALIDATION----------------------------------------------------------------*/
  var Declaration = $('#declarationType').val();
  var CargoPack = $('#CargoPackType').val();
  var Inward = $('#inwardTranseportMode').val();
  var DeclaringFor = $('#DeclaringFor').val();

  if (Declaration == "--Select--") {
    Chcek = false;
    $('#FinalPopUpHeader tbody').append("<tr><td class= 'PopUptd'>Header => CHECK THE DECLARATION TYPE</td></tr>");
    $('#declarationTypeSpan').show();
  }
  if (CargoPack == "--Select--") {
    Chcek = false;
    $('#FinalPopUpHeader tbody').append("<tr><td class= 'PopUptd'>Header => CHECK THE CARGO PACK TYPE</td></tr>");
    $('#CargoPackTypeSpan').show();

  }
  if (Declaration != "BKT : Blanket") {
    if (Inward == "--Select--") {
      Chcek = false;
      $('#FinalPopUpHeader tbody').append("<tr><td class= 'PopUptd'>Header => CHECK THE INWARDTRANSPORT MODE</td></tr>");
      $('#inwardTranseportModeSpan').show();
    }
  }
  if (DeclaringFor == "--Select--") {
    Chcek = false;
    $('#FinalPopUpHeader tbody').append("<tr><td class= 'PopUptd'>Header => CHECK THE  DECLARING FOR</td></tr>");
    $('#DeclaringForSpan').show();
  }

  /*----------------------------------------------------------------PARTY PAGE VALIDATION----------------------------------------------------------------*/

  if ($('#ImporterCruei').val() == "") {
    $('#FinalPopUpParty tbody').append("<tr><td class= 'PopUptd'> Party => CHECK THE  IMPORTER CRUEI</td></tr>");
    $('#ImporterCrueiError').show();
    Chcek = false;
  }
  if ($('#ImporterName').val() == "") {
    $('#FinalPopUpParty tbody').append("<tr><td class= 'PopUptd'> Party => CHECK THE  IMPORTER NAME</td></tr>");
    $('#importerNameError').show();
    Chcek = false;
  }
  if (Inward == '1 : Sea' || Inward == '4 : Air') {
    if ($('#inwardCarrierAgentCruei').val() == "") {
      $('#FinalPopUpParty tbody').append("<tr><td class= 'PopUptd'> Party => CHECK THE  INWARD CRUEI</td></tr>");
      $('#inwardCarrierAgentCrueiError').show();
      Chcek = false;
    }
    if ($('#inwardCarrierAgentName').val() == "") {
      $('#FinalPopUpParty tbody').append("<tr><td class= 'PopUptd'> Party => CHECK THE  INWARD CRUEI</td></tr>");
      $('#inwardCarrierAgentNameError').show();
      Chcek = false;
    }
  }

  /*----------------------------------------------------------------CARGO PAGE VALIDATION----------------------------------------------------------------*/
  $('#CargoTotalOuterPackSpan').hide();
  $('#CargoOuterPackSpan').hide();
  $('#CargoTotalGrossweightSpanInput').hide();
  $('#CargoTotalGrossUOMSpan').hide();
  $('#releaseLocationInputSpan').hide();
  $('#receiptLocationInputSpan').hide();
  $('#CargoLoadingPort1Span').hide();
  $('#CargoArrivalDateSpan').hide();
  $('#CargoVoyageNumberSpan').hide();

  if ($('#CargoTotalOuterPack').val() == "" || $('#CargoOuterPack').val() == "--Select--") {
    $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  TOTAL OUTER PACK</td></tr>");
    Chcek = false;
    if ($('#CargoTotalOuterPack').val() == "") {
      $('#CargoTotalOuterPackSpan').show();
    }
    if ($('#CargoOuterPack').val() == "--Select--") {
      $('#CargoOuterPackSpan').show();
    }

  }

  if ($('#CargoTotalGrossweight').val() == "" || $('#CargoTotalGrossUOM').val() == "--Select--") {
    $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  TOTAL GROSS WEIGHT</td></tr>");
    Chcek = false;
    if ($('#CargoTotalGrossweight').val() == "") {
      $('#CargoTotalGrossweightSpanInput').show();
    }
    if ($('#CargoTotalGrossUOM').val() == "--Select--") {
      $('#CargoTotalGrossUOMSpan').show();
    }
  }

  if ($('#releaseLocationInput').val() == "") {
    $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  RELEASE LOCATION</td></tr>");
    Chcek = false;
    $('#releaseLocationInputSpan').show();
  }

  if ($('#receiptLocationInput').val() == "") {
    $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  RECEIPT LOCATION</td></tr>");
    Chcek = false;
    $('#receiptLocationInputSpan').show();
  }

  if (Inward != "N : Not Required") {
    if ($('#CargoLoadingPort1').val() == "") {
      $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  LOADING PORT</td></tr>");
      Chcek = false;
      $('#CargoLoadingPort1Span').show();
    }
    if ($('#CargoArrivalDate').val() == "") {
      $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  ARRIVAL DATE </td></tr>");
      Chcek = false;
      $('#CargoArrivalDateSpan').show();
    }
  }



  if (Inward == '1 : Sea') {
    if ($('#CargoVoyageNumber').val() == "") {
      $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  VOYAGE NUMBER </td></tr>");
      Chcek = false;
      $('#CargoVoyageNumberSpan').show();
    }
    if ($('#CargoVesselName').val() == "") {
      $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  VESSEL NAME  </td></tr>");
      Chcek = false;
      $('#CargoVesselNameSpan').show();
    }
    if ($('#CargoObl').val() == "") {
      $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  OBL</td></tr>");
      Chcek = false;
      $('#CargoOblSpan').show();
    }
  }

  if (Inward == '4 : Air') {
    if ($('#CargoFlightNumber').val() == "") {
      $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE  FLIGHT NUMBER  </td></tr>");
      Chcek = false;
      $('#CargoFlightNumberSpan').show();
    }
    if ($('#CargoMawb').val() == "") {
      $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE MAWB </td></tr>");
      Chcek = false;
      $('#CargoMawbSpan').show();
    }
  }

  if ('9: Containerized' == CargoPack) {
    if (!(Number($("#ContainerLength").val()) > 0)) {
      Chcek = false;
      $('#FinalPopUpCargo tbody').append("<tr><td class= 'PopUptd'> Cargo => CHECK THE CONTAINER </td></tr>");
    }
  }

  /*----------------------------------------------------------------INVOICE PAGE VALIDATION----------------------------------------------------------------*/

  if (Number($('#summaryNoOfVoice').val()) < 1) {
    Chcek = false;
    $('#FinalPopUpInvoice tbody').append("<tr><td class= 'PopUptd'> Invoice => PLEASE ADD THE INVOICE</td></tr>");
  }

  if (Number($('#summaryNoOfItems').val()) < 1) {
    Chcek = false;
    $('#FinalPopUpItem tbody').append("<tr><td class= 'PopUptd'> Item => PLEASE ADD THE ITEM</td></tr>");
  }

  if (!($('#FinalCheckBox').prop('checked'))) {
    Chcek = false;
    $('#FinalPopUpSummary tbody').append("<tr><td class= 'PopUptd'> SUMMARY =>PLEASE CHOOSE DECLARATION INDICATOR</td></tr>");
  }

  if ($('#SummaryMRD').val() == "") {
    Chcek = false;
    $('#FinalPopUpSummary tbody').append("<tr><td class= 'PopUptd'> SUMMARY =>PLEASE ADD MRD</td></tr>");
  }
  if ($('#SummaryTIME').val() == "") {
    Chcek = false;
    $('#FinalPopUpSummary tbody').append("<tr><td class= 'PopUptd'> SUMMARY =>PLEASE ADD SUMMARY TIME</td></tr>");
  }

  /*----------------------------------------------------------------REFUND ----------------------------------------------------*/

  if ($('#RefundUpdateIndicator').val() != '') {
    if ($("#TypeOfRefundId").val() == "--Select--") {
      Chcek = false;
      $("#RefundTypeError").show();
      $('#FinalPopUpRefund tbody').append("<tr><td class= 'PopUptd'> REFUND =>PLEASE ADD TYPE FOR REFUND</td></tr>");
    }
    if ($("#ResonForRefundID").val() == "--Select--") {
      $("#RefundReasonError").show();
      Chcek = false;
      $('#FinalPopUpRefund tbody').append("<tr><td class= 'PopUptd'> REFUND =>PLEASE ADD REASON FOR REFUND</td></tr>");
    }
    if ($("#RefundDescription").val() == "") {
      $("#RefundDescriptionError").show();
      Chcek = false;
      $('#FinalPopUpRefund tbody').append("<tr><td class= 'PopUptd'> REFUND =>PLEASE ADD DESCRIPTION FOR REFUND</td></tr>");
    }
  }

  if (Chcek) {
    $('#FinalPopup').hide();
    FinalSave()
    //$('#FinalError').hide();
    //$('#FinalSuccess').show();
  }
  else {
    $('#FinalError').show();
    $('#FinalPopup').show();
  }
}

function FinalSave() {

  if ($("#CargoArrivalDate").val() != "") {
    var ArrivalDate = ($("#CargoArrivalDate").val()).split("/");
    ArrivalDate = `${ArrivalDate[2]}/${ArrivalDate[1]}/${ArrivalDate[0]}`;
  }
  else {
    var ArrivalDate = '1900-01-01'
  }

  var SummaryDate = ($("#SummaryMRD").val()).split("/");
  SummaryDate = `${SummaryDate[2]}/${SummaryDate[1]}/${SummaryDate[0]}`;

  var BlanketStartDate;
  if ($("#CargoBlanketDate").val() != "") {
    BlanketStartDate = ($("#CargoBlanketDate").val()).split("/");
    BlanketStartDate = `${BlanketStartDate[2]}/${BlanketStartDate[1]}/${BlanketStartDate[0]}`;
  }
  else {
    BlanketStartDate = '1900-01-01'
  }

  var Licence = $("#licence1").val() + "," + $("#licence2").val() + "," + $("#licence3").val() + "," + $("#licence4").val() + "," + $("#licence5").val();
  var Recipient = $("#Recipient1").val() + "-" + $("#Recipient2").val() + "-" + $("#Recipient3").val();


  var RefundData = [];
  var sno = 1;
  var reci = document.getElementsByName("RefundCalculation");
  for (var i = 0; i < reci.length; i = i + 6) {
    RefundData.push([sno, reci[i].value, reci[i + 1].value, reci[i + 2].value,
      reci[i + 3].value, reci[i + 4].value, reci[i + 5].value
    ]);
    sno += 1;
  }
  var RefundDatas = JSON.stringify(RefundData);
  var PermitStatus = "NEW";
  var PermitNumber = $('#PermitNumberId').val();
  if (PermitNumber == "None" || PermitNumber == "" || PermitNumber == "NONE") {
    PermitNumber = "";
  }
  if ($("#RefundUpdateIndicator").val() == "RFD") {
    PermitStatus = "RFD";
    PermitNumber = $('#RefundPermitNumber').val();
  }
  if ($("#CancelUpdateIndicator").val() == "CNL") {
    PermitStatus = "CNL";
    PermitNumber = $('#CancelPermitNumber').val();
  }
  if ($("#AmendUpdateIndicator").val() == "AME") {
    PermitStatus = "AME";
    PermitNumber = $('#AmendPermitNumber').val();
  }
  $('#Loading').show();
  $.ajax({
    type: 'POST',
    url: '/InpaymentSave/',
    data: {
      Cpc: CpcSaveFunction(),
      Refid: $('#REFID').val(),
      JobId: $('#JOBID').val(),
      MSGId: $('#MSGID').val(),
      PermitId: $('#PermitID').val().toUpperCase(),
      TradeNetMailboxID: $('#MailBoxId').val(),
      MessageType: $('#MsgType').val(),
      DeclarationType: $('#declarationType').val(),
      PreviousPermit: $('#PreviousPermitNo').val(),
      CargoPackType: $('#CargoPackType').val(),
      InwardTransportMode: $('#inwardTranseportMode').val(),
      BGIndicator: $('#BgIndicator').val(),
      SupplyIndicator: $('#SupplyIndicator').val(),
      ReferenceDocuments: $('#ReferenceDocuments').val(),
      License: Licence,
      Recipient: Recipient,
      DeclarantCompanyCode: $('#declarationCompanyCode').val(),
      ImporterCompanyCode: $('#ImporterCode').val(),
      InwardCarrierAgentCode: $('#inwardCarrierAgentCode').val(),
      FreightForwarderCode: $('#FreightForwarderCode').val(),
      ClaimantPartyCode: $('#claimantPartyCode').val(),
      HBL: $('#CargoHbl').val(),
      ArrivalDate: ArrivalDate,
      LoadingPortCode: $('#CargoLoadingPort1').val(),
      VoyageNumber: $('#CargoVoyageNumber').val(),
      VesselName: $('#CargoVesselName').val(),
      OceanBillofLadingNo: $('#CargoObl').val(),
      ConveyanceRefNo: $('#CargoConveyanceNo').val(),
      TransportId: $('#CargoTransportId').val(),
      FlightNO: $('#CargoFlightNumber').val(),
      AircraftRegNo: $('#CargoAirCraftNo').val(),
      MasterAirwayBill: $('#CargoMawb').val(),
      ReleaseLocation: $('#releaseLocationInput').val(),
      ReleaseLocName: $('#releaseLocationText').val(),
      RecepitLocation: $('#receiptLocationInput').val(),
      TotalOuterPack: $('#CargoTotalOuterPack').val(),
      TotalOuterPackUOM: $('#CargoOuterPack').val(),
      TotalGrossWeight: $('#CargoPermitGrossWeight').val(),
      TotalGrossWeightUOM: $('#CargoTotalGrossUOM').val(),
      GrossReference: $('#SummaryCrossReference').val(),
      BlanketStartDate: BlanketStartDate,
      TradeRemarks: $('#summaryTradeRemarks').val(),
      InternalRemarks: $('#summaryInternalRemarks').val(),
      CustomerRemarks: "",
      DeclareIndicator: $('#FinalCheckBox').val(),
      NumberOfItems: $('#summaryNoOfItems').val(),
      TotalCIFFOBValue: $('#summaryTotalCIFFOBValue').val(),
      TotalGSTTaxAmt: $('#summaryTotalGstValue').val(),
      TotalExDutyAmt: $('#summaryExciseDuty').val(),
      TotalCusDutyAmt: $('#summaryCustomsDuty').val(),
      TotalODutyAmt: $('#itemOtherTaxAmountSummary').val(),
      TotalAmtPay: $('#summaryTotalPayable').val(),
      Status: "NEW",
      TouchUser: $('#USERNAME').val().toUpperCase(),
      TouchTime: TOUCHTIME,
      PermitNumber: PermitNumber,
      prmtStatus: PermitStatus,
      RecepitLocName: $('#receiptLocationText').val(),
      Cnb: $('#CNB').val(),
      DeclarningFor: $('#DeclaringFor').val(),
      MRDate: SummaryDate,
      MRTime: $('#SummaryTIME').val(),
      /*----------------------------------------Refund Datas---------------------------------*/
      RefundDatas: RefundDatas,
      PermitNo: $("#RefundPermitNumber").val(),
      UpdateIndicator: $("#RefundUpdateIndicator").val(),
      ReplacementPermitno: $("#RefundReplacement").val(),
      TypeOfRefund: $("#TypeOfRefundId").val(),
      ResonForRefund: $("#ResonForRefundID").val(),
      DescriptionOfReason: $("#RefundDescription").val(),
      DeclarationIndigator: $("#FinalCheckBox").val(),
      AdditionalInfo: $("#RefundRecipient1").val() + "-" + $("#RefundRecipient2").val() + "-" + $("#RefundRecipient3").val(),
      TotalGstAmt: $("#RefundTotalGst").val(),
      TotalExciseAmt: $("#RefundTotalExcise").val(),
      TxtCusdutyAmt: $("#RefundTotalCustoms").val(),
      TxtOtherAmt: $("#RefundTotalOther").val(),
      /*------------------------------------------Cancel Datas-------------------------------*/
      CancelPermitNo: $("#CancelPermitNumber").val(),
      CancelUpdateIndicator: $("#CancelUpdateIndicator").val(),
      CancelReplacementPermitno: $("#CancelPermitNumberReplacement").val(),
      ResonForCancel: $("#ResonForCancel").val(),
      CancelDescriptionOfReason: $("#DescriptionOfReason").val(),
      CancelDeclarationIndigator: $('#FinalCheckBox').val(),
      CancelType: $("#CancelationType").val(),
      /*-----------------------------------------Amend Datas --------------------------------*/
      AmendPermitNo: $("#AmendPermitNumber").val(),
      AmendMentCount: $("#AmendCount").val(),
      AmendUpdateIndicator: $("#AmendUpdateIndicator").val(),
      AmendReplacementPermitno: $("#AmendPermitNumberReplacement").val(),
      AmendDescriptionOfReason: $("#AmendDescription").val(),
      AmendPermitExtension: $("#AmendPermitValidity").val(),
      AmendExtendImportPeriod: $("#AmendExtendPeriod").val(),
      AmendDeclarationIndigator: $("#AmendCheckBoxTik").val(),
      AmendType: $("#AmendType").val(),

      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function () {
      window.location.assign("/InpaymentList/");
      $('#Loading').hide();
    }
  })

}


/*----------------------------------------------------------------REFUND----------------------------------------------------------------*/
function addRefund() {
  var retable = `<tr>
        <td><input type="text" class="inputStyle" name="RefundCalculation" ></td>
        <td><input type="text" class="inputStyle" name="RefundCalculation" ></td>
        <td><input type="text" class="inputStyle" name="RefundCalculation" value="0.00"></td>
        <td><input type="text" class="inputStyle" name="RefundCalculation" value="0.00"></td>
        <td><input type="text" class="inputStyle" name="RefundCalculation" value="0.00"></td>
        <td><input type="text" class="inputStyle" name="RefundCalculation" value="0.00"></td>
        <td style = width:4%><i class="material-icons refundDelBtn" style="color:red" onclick ="refundDelBtnFunction()">delete</i></td>
    </tr>`
  $('#RefundTABLE tbody').append(retable)
}

function RefundDeclareIndicatorFunction() {
  var check = document.getElementById('RefundDeclareIndicator')
  if (check.checked) {
    check.value = 'True';
  } else {
    check.value = 'False';
  }
}
function refundchangefunction(val) {
  $("#RefundTypeError").hide();
  var reci = document.getElementsByName("RefundCalculation");
  for (var i = 0; i < reci.length; i = i + 6) {
    $("#RefundTABLE").find("tr:gt(1)").remove();
    reci[i].value = "";
    reci[i + 1].value = "";
    reci[i + 2].value = "0.00";
    reci[i + 3].value = "0.00";
    reci[i + 4].value = "0.00";
    reci[i + 5].value = "0.00";

  }
  $("#RefundTotalGst").val("0.00")
  $("#RefundTotalExcise").val("0.00")
  $("#RefundTotalCustoms").val("0.00")
  $("#RefundTotalOther").val("0.00")
  $("#itemRefundId").hide();
  $("#refundSummaryId").hide();
  if (val == "PRS:Partial refund (specific)") {
    $("#itemRefundId").show();
    $("#refundSummaryId").show();
    $("#refundPrg").show();
  } else if (val == "FRF:Full refund") {
    $("#refundSummaryId").show();
    $("#refundPrg").show();
  } else if (val == "PRG:Partial refund (general)") {
    $("#refundSummaryId").show();
    $("#refundPrg").hide();
  }
}

function refundDelBtnFunction() {
  $('#RefundTABLE').on('click', '.refundDelBtn', function () {
    $(this).closest('tr').remove();
  })
}

function RefundDocumentAttch() {
  var FileName = 'RefundAttach'
  var MeesageID = $("#MSGID").val();
  var PermitId = $("#PermitID").val().toUpperCase();
  var UserName = $("#USERNAME").val().toUpperCase();
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
  formData.append("DocumentType", $('#RefundDocumentType').val());
  formData.append("InPaymentId", MeesageID);
  formData.append("FilePath", "/Users/hightech/Desktop/Yosuva_KttProject/");
  formData.append("Size", size + " KB");
  formData.append("PermitId", PermitId);
  formData.append("UserName", UserName);
  formData.append("Type", 'RFD');
  formData.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
  var csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
  });
  $('#Loading').show();
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/HeaderDocumentSave/",
    processData: false,
    contentType: false,
    mimeType: "multipart/form-data",
    data: formData,
    success: function (response) {
      InFile = response.Infile;
      RefundDocumentLoadFunction();
      $('#Loading').hide();
    },
  });
}

function RefundDocumentLoadFunction() {

  var check = false;
  var Tab = ''
  for (var i of InFile) {
    if (i.Type == "RFD") {
      check = true;
      Tab += `<tr>
            <td class = "DocumentDelClass"> <i class="material-icons" style="color:red;font-size : 12px" value = "${i.id}" onclick = 'DocumentDelete("${i.id}")' >delete</i></td>
            <td>${i.DocumentType}</td>
            <td>${i.Name}</td>
            <td>${i.Size}</td>
        </tr>`
    }
  }
  if (check) {
    $('#RefundAttachTable tbody').html(Tab);
    $('#RefundDocumentTableshow').show();
  }
}

function CancelDocumentAttch() {
  var FileName = 'CancelAttach'
  var MeesageID = $("#MSGID").val();
  var PermitId = $("#PermitID").val().toUpperCase();
  var UserName = $("#USERNAME").val().toUpperCase();
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
  formData.append("DocumentType", $('#CanceldocumentType').val());
  formData.append("InPaymentId", MeesageID);
  formData.append("FilePath", "/Users/hightech/Desktop/Yosuva_KttProject/");
  formData.append("Size", size + " KB");
  formData.append("PermitId", PermitId);
  formData.append("UserName", UserName);
  formData.append("Type", 'CNL');
  formData.append("csrfmiddlewaretoken", $("[name=csrfmiddlewaretoken]").val());
  var csrftoken = $("[name=csrfmiddlewaretoken]").val();
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
  });
  $('#Loading').show();
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/HeaderDocumentSave/",
    processData: false,
    contentType: false,
    mimeType: "multipart/form-data",
    data: formData,
    success: function (response) {
      InFile = response.Infile;
      CancelDocumentLoadFunction();
      $('#Loading').hide();
    },
  });
}

function CancelDocumentLoadFunction() {
  var check = false;
  var Tab = ''
  for (var i of InFile) {
    if (i.Type == "CNL") {
      check = true;
      Tab += `<tr>
            <td class = "DocumentDelClass"> <i class="material-icons" style="color:red;font-size : 12px" value = "${i.id}" onclick = 'DocumentDelete("${i.id}")' >delete</i></td>
            <td>${i.DocumentType}</td>
            <td>${i.Name}</td>
            <td>${i.Size}</td>
        </tr>`
    }
  }
  if (check) {
    $('#CancelAttachTable tbody').html(Tab);
    $('#CancelDocumentTableshow').show();
  }
}

function AmendPermitExtension() {
  var check = document.getElementById('AmendPermitValidity')
  if (check.checked) {
    check.value = 'True';
  } else {
    check.value = 'False';
  }
}


function Recalculate() {
  if ($('#GstAutoCompute').prop('checked')) {
    $('#TxtItemSumGST').prop('disabled', false)
  }
  else {
    $('#TxtItemSumGST').prop('disabled', true)
  }
}


var ImporterData = [];
var InwardData = [];
var FrieghtData = [];
var ClaimantData = [];
var SupplyData = [];
var InhouseData = [];

$(document).ready(function () {
  $('#Loading').show();
  $.ajax({
    type: "GET",
    url: '/PartyLoadDatas/',
    success: function (response) {
      ImporterData = response.Importer;
      InwardData = response.Inward;
      FrieghtData = response.Frieght;
      ClaimantData = response.Claimant;
      SupplyData = response.Supply;
      InhouseData = response.Inhouse;
      ImportFocusOutFunction('#ImporterCode');
      InwardFocusOut();
      FrightFocusOut();
      ClaimentFocusOut();

      InFile = response.Infile;
      if (InFile.length >= 1) {
        DocumentLoadFunction();
      }
      $('#Loading').hide();
    }
  })
})


function ImporterFocusIN(arg) {
  TrimKeyUp('ImporterCode')
  TrimKeyUp('InvoiceImportCode')
  //$('#Loading').show();
  var myValues = [];
  for (var i of ImporterData) {
    myValues.push(i.Code + ":" + i.Name)
  }
  //$('#Loading').hide();
  Autocomplete(myValues, arg)
}

function ImportFocusOutFunction(arg) {
  $('#ImporterCrueiError').hide();
  $('#importerNameError').hide();
  if ($(arg).val() == "") {
    $('.ImporterEmpty input').val("")
  }
  else {
    for (var i of ImporterData) {
      if (i.Code == $(arg).val()) {
        $('#ImporterCode').val(i.Code)
        $('#ImporterCruei').val(i.CRUEI);
        $('#ImporterName').val(i.Name);
        $('#ImporterName1').val(i.Name1);
        $('#InvoiceImportCode').val(i.Code);
        $('#InvoiceImportCruei').val(i.CRUEI);
        $('#InvoiceImportName').val(i.Name);
        $('#InvoiceImportName1').val(i.Name1);
        $('#inwardCarrierAgentCode').focus();
      }
    }
  }
}

// $(document).ready(function() {

//   $('input').keydown(function(e) {
//     if (e.shiftKey && e.keyCode == 9) {  // Shift+Tab key combination
//       e.preventDefault(); // Prevent the default behavior of Shift+Tab
//       var focusedTabIndex = parseInt($(':focus').attr('tabindex'));
//       var newTabIndex = focusedTabIndex === 1 ? 2 : 1;
//       $('[tabindex="' + newTabIndex + '"]').focus();
//     }
//   });
// });
function ImporterSave() {
  $("#ImportCodeSpan").hide();
  if ($('#ImporterCode').val() == "") {
    $("#ImportCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CargoSave/',
      data: {
        ModelName: 'ImporterModel',
        code: ($("#ImporterCode").val()).trim(),
        cruei: ($("#ImporterCruei").val()).trim(),
        name: ($("#ImporterName").val()).trim(),
        name1: ($("#ImporterName1").val()).trim(),
        TouchUser: $("#USERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        ImporterData = response.Importer;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

function InvoiceImporterSave() {
  $("#InImporterCodeSpan").hide();
  if ($('#InvoiceImportCode').val() == "") {
    $("#InImporterCodeSpan").show();
  }
  else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CargoSave/',
      data: {
        ModelName: 'ImporterModel',
        code: ($("#InvoiceImportCode").val()).trim(),
        cruei: ($("#InvoiceImportCruei").val()).trim(),
        name: ($("#InvoiceImportName").val()).trim(),
        name1: ($("#InvoiceImportName1").val()).trim(),
        TouchUser: $("#USERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        ImporterData = response.Importer;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

function InvoiceImporterOut() {
  $('#InvoiceImportCodeSpan').hide();
  if ($('#InvoiceImportCode').val() == "") {
    $('.InvoiceImporterEmpty input').val("")
  }
  else {
    for (var i of ImporterData) {
      if (i.Code == $('#InvoiceImportCode').val()) {
        if ($('#ImporterCode').val() != $('#InvoiceImportCode').val()) {
          $('#InvoiceImportCodeSpan').show();
        }
        $('#InvoiceImportCode').val(i.Code);
        $('#InvoiceImportCruei').val(i.CRUEI);
        $('#InvoiceImportName').val(i.Name);
        $('#InvoiceImportName1').val(i.Name1);
        $("#InvoiceDate").focus()
        backspaceEvent('InvoiceImportCode', 'InvoiceName1')
      }
    }
  }
}

function ItemCascOut() {
  if ($('#itemCascID').prop('checked')) {
    $('#itemProductCode1').focus()
  }
  backspaceEvent('itemCascID', 'packing_details')
}

function ImporterSearch(Data) {
  $('#ImporterPopUp').show()
  var tag = ""
  for (var i of ImporterData) {
    if (Data == "Party") {
      tag += `<tr onclick="ImporterSelectRow(this)" style="cursor: pointer;">`
    }
    else if (Data == "Invoice") {
      tag += `<tr onclick="InvoiceImporterSelectRow(this)" style="cursor: pointer;">`
    }
    tag += `
          <td>${i.Code}</td>
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.CRUEI}</td>
        </tr>
    `
  }
  $('#ImporterPopUp').html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>IMPORTER</h1>
                  <input type="text" id="ImporterImgSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#ImporterTable').DataTable().search($('#ImporterImgSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "ImporterTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#ImporterPopUp').hide()">CLOSE</button>
              </div>
          </div>
          `)
  $("#ImporterTable").DataTable({
    "pageLength": 5,
    "ordering": false,
    "dom": 'rtip',
    "autoWidth": false,
  })
}
function InvoiceImporterSelectRow(arg) {
  let currentRow = $(arg).closest("tr");
  let col1 = currentRow.find("td:eq(0)").text();
  let col2 = currentRow.find("td:eq(1)").text();
  let col3 = currentRow.find("td:eq(2)").text();
  let col4 = currentRow.find("td:eq(3)").text();

  $('#InvoiceImportCode').val(col1);
  $('#InvoiceImportName').val(col2);
  $('#InvoiceImportName1').val(col3);
  $('#InvoiceImportCruei').val(col4);
  $('#ImporterPopUp').hide();
  InvoiceImporterOut()
}
function ImporterSelectRow(arg) {

  let currentRow = $(arg).closest("tr");
  let col1 = currentRow.find("td:eq(0)").text();
  let col2 = currentRow.find("td:eq(1)").text();
  let col3 = currentRow.find("td:eq(2)").text();
  let col4 = currentRow.find("td:eq(3)").text();

  $('#ImporterCode').val(col1)
  $('#ImporterName').val(col2);
  $('#ImporterName1').val(col3);
  $('#ImporterCruei').val(col4);
  $('#InvoiceImportCode').val(col1);
  $('#InvoiceImportName').val(col2);
  $('#InvoiceImportName1').val(col3);
  $('#InvoiceImportCruei').val(col4);
  $('#ImporterPopUp').hide();
}

function InwardFocusIN() {
  TrimKeyUp('inwardCarrierAgentCode')
  var myValues = [];
  $('#Loading').show();
  for (var i of InwardData) {
    myValues.push(i.Code + ":" + i.Name)
  }
  $('#Loading').hide();
  Autocomplete(myValues, "#inwardCarrierAgentCode")
}

function InwardFocusOut() {
  $('#inwardCarrierAgentCrueiError').hide();
  $('#inwardCarrierAgentNameError').hide();
  if ($('#inwardCarrierAgentCode').val() == "") {
    $('.InwardEmpty input').val("");
  }
  else {
    for (var i of InwardData) {
      if (i.Code == $("#inwardCarrierAgentCode").val()) {
        $('#inwardCarrierAgentCode').val(i.Code)
        $('#inwardCarrierAgentCruei').val(i.CRUEI);
        $('#inwardCarrierAgentName').val(i.Name);
        $('#inwardCarrierAgentName1').val(i.Name1);
        $("#FreightForwarderCode").focus()
        backspaceEvent('inwardCarrierAgentCode', 'ImporterName1')
      }
    }
  }
}

function itemProductCodeonblur() {
  backspaceEvent('itemProductCode1', 'packing_details')
}

function product1CodeCopyUomOnblur() {
  $('[name="cascName1"]:first').focus();
  backspaceEvent('product1CodeCopyUom', 'product1CodeCopyInput')
}

function backspaceEvent(Id, PreviousID) {
  $('#' + Id).keydown(function (event) {
    if (event.shiftKey && event.key === 'Tab') {
      $("#" + PreviousID).focus()
    }
  });
}

function InwardCarrierSave() {
  $("#InwardCodeSpan").hide();
  if ($('#inwardCarrierAgentCode').val() == "") {
    $("#InwardCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CargoSave/',
      data: {
        ModelName: 'InawrdModel',
        code: ($("#inwardCarrierAgentCode").val()).trim(),
        cruei: ($("#inwardCarrierAgentCruei").val()).trim(),
        name: ($("#inwardCarrierAgentName").val()).trim(),
        name1: ($("#inwardCarrierAgentName1").val()).trim(),
        TouchUser: $("#USERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        InwardData = response.Inward;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

function InwardSearch() {
  $('#InwardPopup').show()
  var tag = ""
  for (var i of InwardData) {
    tag += `
      <tr onclick="InwardSelectRow(this)" style="cursor: pointer;">
          <td>${i.Code}</td>
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.CRUEI}</td>
        </tr>
    `
  }
  $('#InwardPopup').html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>INWARD</h1>
                  <input type="text" id="InwardImgSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InwardTable').DataTable().search($('#InwardImgSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InwardTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InwardPopup').hide()">CLOSE</button>
              </div>
          </div>
          `)
  $("#InwardTable").DataTable({
    "pageLength": 5,
    "ordering": false,
    "dom": 'rtip',
    "autoWidth": false,
  })
}

function InwardSelectRow(arg) {
  let SelectRow = $(arg).closest("tr")

  let col1 = SelectRow.find("td:eq(0)").text();
  let col2 = SelectRow.find("td:eq(1)").text();
  let col3 = SelectRow.find("td:eq(2)").text();
  let col4 = SelectRow.find("td:eq(3)").text();

  $('#inwardCarrierAgentCode').val(col1)
  $('#inwardCarrierAgentName').val(col2);
  $('#inwardCarrierAgentName1').val(col3);
  $('#inwardCarrierAgentCruei').val(col4);
  $('#InwardPopup').hide()
}

function FrightFrwdFocusIN() {
  TrimKeyUp('FreightForwarderCode')
  var myValues = [];
  for (var i of FrieghtData) {
    myValues.push(i.Code + ":" + i.Name)
  }
  Autocomplete(myValues, "#FreightForwarderCode")
}

function FrightFocusOut() {
  
  if ($('#FreightForwarderCode').val() == "") {
    $('.FrieghtEmpty input').val('')
    $("#CargoHAWBSpan").hide()
  }  else {
    for (var i of FrieghtData) {
      if (i.Code == $("#FreightForwarderCode").val()) {
        $("#CargoHAWBSpan").show()
        $('#FreightForwarderCode').val(i.Code)
        $('#FreightForwarderCruei').val(i.CRUEI);
        $('#FreightForwarderName').val(i.Name);
        $('#FreightForwarderName1').val(i.Name1);
        $('#PartyNextBtn').focus()
        backspaceEvent('FreightForwarderCode', 'inwardCarrierAgentName1')
      }
    }
  
  }
}

function FreightSearch() {
  $('#FreightPopUp').show()
  var tag = ""
  for (var i of FrieghtData) {
    tag += `
      <tr onclick="FreightSelectRow(this)" style="cursor: pointer;">
          <td>${i.Code}</td>
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.CRUEI}</td>
        </tr>
    `
  }
  $('#FreightPopUp').html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>FREIGHT FORWARDER</h1>
                  <input type="text" id="FreightImgSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#FreightTable').DataTable().search($('#FreightImgSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "FreightTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#FreightPopUp').hide()">CLOSE</button>
              </div>
          </div>
          `)
  $("#FreightTable").DataTable({
    "pageLength": 5,
    "ordering": false,
    "dom": 'rtip',
    "autoWidth": false,
  })
}

function FreightSelectRow(arg) {
  let SelectRow = $(arg).closest("tr")

  let col1 = SelectRow.find("td:eq(0)").text();
  let col2 = SelectRow.find("td:eq(1)").text();
  let col3 = SelectRow.find("td:eq(2)").text();
  let col4 = SelectRow.find("td:eq(3)").text();

  $('#FreightForwarderCode').val(col1)
  $('#FreightForwarderName').val(col2);
  $('#FreightForwarderName1').val(col3);
  $('#FreightForwarderCruei').val(col4);
  $('#FreightPopUp').hide()

}

function FrightSave() {
  $("#FrightCodeSpan").hide();
  if ($('#FreightForwarderCode').val() == "") {
    $("#FrightCodeSpan").show();
  } else {

    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CargoSave/',
      data: {
        ModelName: 'FreightModel',
        code: ($("#FreightForwarderCode").val()).trim(),
        cruei: ($("#FreightForwarderCruei").val()).trim(),
        name: ($("#FreightForwarderName").val()).trim(),
        name1: ($("#FreightForwarderName1").val()).trim(),
        TouchUser: $("#USERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        FrieghtData = response.Frieght;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}

function ClaimentFocusIN() {
  TrimKeyUp('claimantPartyCode')
  var myValues = [];
  for (var i of ClaimantData) {
    myValues.push(i.ClaimantCode + ":" + i.Name)
  }
  Autocomplete(myValues, "#claimantPartyCode")
}

function ClaimentFocusOut() {
  if ($('#claimantPartyCode').val() == "") {
    $('#claimantPartyId input').val('')
  }
  else {
    for (var i of ClaimantData) {
      if (i.ClaimantCode == $("#claimantPartyCode").val()) {
        $('#claimantPartyCode').val(i.ClaimantCode)
        $('#claimantPartyCruie').val(i.CRUEI);
        $('#claimantPartyName').val(i.Name);
        $('#claimantPartyName1').val(i.Name1);
        $('#claimantPartyID1').val(i.ClaimantName);
        $('#claimantPartyName2').val(i.ClaimantName1);
      }
    }
  }
}

function ClaimentSearch() {
  $('#ClaimentPopUp').show()
  var tag = ""
  for (var i of ClaimantData) {
    tag += `
      <tr onclick="ClaimantSelectRow('${i.ClaimantCode}')" style="cursor: pointer;">
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.CRUEI}</td>
          <td>${i.ClaimantName}</td>
          <td>${i.ClaimantName1}</td>
        </tr>
    `
  }
  $('#ClaimentPopUp').html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>CLAIMANT PARTY</h1>
                  <input type="text" id="ClaimantImgSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#ClaimantTable').DataTable().search($('#ClaimantImgSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "ClaimantTable">
                      <thead>
                          <th>NAME</th>
                          <th>NAME 1</th>
                          <th>CR UEI</th>
                          <th>CLAIMANT NAME</th>
                          <th>CLAIMANT ID</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#ClaimentPopUp').hide()">CLOSE</button>
              </div>
          </div>
          `)
  $("#ClaimantTable").DataTable({
    "pageLength": 5,
    "ordering": false,
    "dom": 'rtip',
    "autoWidth": false,
  })
}
function ClaimantSelectRow(val) {
  for (var Im of ClaimantData) {
    if (Im.ClaimantCode == val) {
      $("#claimantPartyCode").val(Im.ClaimantCode);
      $("#claimantPartyCruie").val(Im.CRUEI);
      $("#claimantPartyName").val(Im.Name);
      $("#claimantPartyName1").val(Im.Name1);
      $("#claimantPartyID1").val(Im.ClaimantName);
      $("#claimantPartyName2").val(Im.ClaimantName1);
      $("#ClaimantPopUp").hide();
      $('#ClaimentPopUp').hide();
    }
  }

}
function ClaimentSave() {
  $("#ClaimantCodeSpan").hide();
  if ($('#claimantPartyCode').val() == "") {
    $("#ClaimantCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CargoSave/',
      data: {
        ModelName: 'ClaimantModel',
        ClaimantCode: ($("#claimantPartyCode").val()).trim(),
        cruei: ($("#claimantPartyCruie").val()).trim(),
        name: ($("#claimantPartyName").val()).trim(),
        name1: ($("#claimantPartyName1").val()).trim(),
        ClaimantName: ($("#claimantPartyID1").val()).trim(),
        ClaimantName1: ($("#claimantPartyName2").val()).trim(),
        TouchUser: $("#USERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        ClaimantData = response.Claimant;
        alert(response.Result);
        $('#Loading').hide();
      }
    })

  }
}
function SupplyFocusIN() {
  TrimKeyUp('InvoiceSupplierCode')
  var myValues = [];
  for (var i of SupplyData) {
    myValues.push(i.Code + ":" + i.Name)
  }
  Autocomplete(myValues, "#InvoiceSupplierCode")
}
function SupplyFocusOut() {
  $('.InvoiceSupplierEmpty span').hide();
  if ($('#InvoiceSupplierCode').val() == "") {
    $('.InvoiceSupplierEmpty input').val('')
  }
  else {
    for (var i of SupplyData) {
      if (i.Code == $("#InvoiceSupplierCode").val()) {
        $('#InvoiceSupplierCode').val(i.Code)
        $('#InvoiceCruei').val(i.CRUEI);
        $('#InvoiceName').val(i.Name);
        $('#InvoiceName1').val(i.Name1);
        $('#InvoiceImportCode').focus()
        // backspaceEvent('FreightForwarderCode','inwardCarrierAgentName1')
      }
    }
  }
}
function SupplySearch() {
  $('#SupplierPopUp').show()
  var tag = ""
  for (var i of SupplyData) {
    tag += `
      <tr onclick="SupplySelectRow(this)" style="cursor: pointer;">
          <td>${i.Code}</td>
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.CRUEI}</td>
        </tr>
    `
  }
  $('#SupplierPopUp').html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>SUPPLIER / MANUFACTURER </h1>
                  <input type="text" id="SUPPLIERImgSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#SupplierTable').DataTable().search($('#SUPPLIERImgSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "SupplierTable">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Cruei</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#SupplierPopUp').hide()">CLOSE</button>
              </div>
          </div>
          `)
  $("#SupplierTable").DataTable({
    "pageLength": 5,
    "ordering": false,
    "dom": 'rtip',
    "autoWidth": false,
  })
}
function SupplySelectRow(arg) {

  let SelectRow = $(arg).closest("tr")

  let col1 = SelectRow.find("td:eq(0)").text();
  let col2 = SelectRow.find("td:eq(1)").text();
  let col3 = SelectRow.find("td:eq(2)").text();
  let col4 = SelectRow.find("td:eq(3)").text();

  $("#InvoiceSupplierCode").val(col1);
  $("#InvoiceName").val(col2);
  $("#InvoiceName1").val(col3);
  $("#InvoiceCruei").val(col4);
  $("#SupplierPopUp").hide();
}
function SupplierSave() {
  $("#SupplierCodeSpan").hide();
  if ($('#InvoiceSupplierCode').val() == "") {
    $("#SupplierCodeSpan").show();
  } else {
    $('#Loading').show();
    $.ajax({
      type: "POST",
      url: '/CargoSave/',
      data: {
        ModelName: 'SupplierModel',
        code: $("#InvoiceSupplierCode").val(),
        cruei: $("#InvoiceCruei").val(),
        name: $("#InvoiceName").val(),
        name1: $("#InvoiceName1").val(),
        TouchUser: $("#USERNAME").val().toUpperCase(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
      },
      success: function (response) {
        SupplyData = response.Supply;
        alert(response.Result);
        $('#Loading').hide();
      }
    })
  }
}
function ItemCascSearch(Code, Uom) {
  $('#Loading').show();
  $.ajax({
    url: "/Inpayment/CascProductCodes/?search=" + $("#ItemHsCode").val(),
    type: "GET",
    success: function (response) {
      $('#ItemCascPopUp').show()
      $('#Loading').hide();
      var tag = ""
      for (var i of response) {
        tag += `
      <tr onclick="ProductSelectRow(this,'${Code}','${Uom}')" style="cursor: pointer;">
          <td>${i.CASCCode}</td>
          <td>${i.Description}</td>
          <td>${i.UOM}</td>
        </tr>
    `
      }
      $('#ItemCascPopUp').html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>PRODUCT CODE</h1>
                  <input type="text" id="PRODUCTImgSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#ItemProductTab1').DataTable().search($('#PRODUCTImgSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "ItemProductTab1">
                      <thead>
                          <th>CASCCODE</th>
                          <th>DESCRIPTION</th>
                          <th>UOM</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#ItemCascPopUp').hide()">CLOSE</button>
              </div>
          </div>
          `)
      $("#ItemProductTab1").DataTable({
        "pageLength": 5,
        "ordering": false,
        "dom": 'rtip',
        "autoWidth": false,
      })

    }
  })
}
function ProductSelectRow(val, Code, Uom) {
  var currentRow = $(val).closest("tr");
  var col1 = currentRow.find("td:eq(0)").text();
  var col2 = currentRow.find("td:eq(1)").text();
  var col3 = currentRow.find("td:eq(2)").text();
  $("#" + Code).val(col1)
  $("#" + Uom).val(col3)
  $('#ItemCascPopUp').hide()
}

function ProductFocusIn1(ID, Desc, Uom) {
  $.ajax({
    url: "/Inpayment/CascProductCodes/?search=" + $("#ItemHsCode").val(),
    type: "GET",
    success: function (response) {
      $('#Loading').show();
      let store = []
      for (var i of response) {
        store.push(`${i.CASCCode}:${i.Description}`)
      }
      Autocomplete(store, ID)
      $('#Loading').hide();
      $(ID).focusout(function () {
        if ($(ID).val() == "") {
          $(Desc).html("")
          $(Uom).val("--Select--")
        }
        else {
          for (var i of response) {
            if (i.CASCCode == $(ID).val()) {
              $(Desc).html(i.Description)
              $(Uom).val(i.UOM)
            }
          }
        }
      });
    }
  })
}

function CpcLoadData() {
  $('#Loading').show();
  $.ajax({
    url: "/CpcLoad/",
    success: function (response) {
      $('.SchemeClass').hide()
      $('.AeoClass').hide()
      $('.CwcClass').hide()
      if ((response.CpAeo).length > 0) {
        var AeoTable = ''
        for (var i of response.CpAeo) {
          aeo = true;
          $("#Aeo").prop("checked", true);
          AeoTable += `<tr>
              <td><input type="text" class="inputStyle" name="AeoName" value = "${i.ProcessingCode1}"></td>
              <td><input type="text" class="inputStyle" name="AeoName" value = "${i.ProcessingCode2}"></td>
              <td><input type="text" class="inputStyle" name="AeoName" value = "${i.ProcessingCode3}"></td>
              <td class="OutItemCascDeleteButton"><i class="material-icons" style="color:red">delete</i></td>
            </tr>`
        }
        $('.AeoClass').show()
        $('#AeoTable tbody').html(AeoTable)
      }
      if ((response.CpCwc).length > 0) {
        var CwcTable = ''
        for (var i of response.CpCwc) {
          $("#Cwc").prop("checked", true);
          CwcTable += `<tr>
            <td><input type="text" class="inputStyle" name="CwcName" value = "${i.ProcessingCode1}"></td>
            <td><input type="text" class="inputStyle" name="CwcName" value = "${i.ProcessingCode2}"></td>
            <td><input type="text" class="inputStyle" name="CwcName" value = "${i.ProcessingCode3}"></td>
            <td class="OutItemCascDeleteButton"><i class="material-icons" style="color:red">delete</i></td>
          </tr>`
        }
        $('.CwcClass').show()
        $('#CwcTable tbody').html(CwcTable)
      }
      if ((response.CpScheme).length > 0) {
        var SchemeTable = ''
        for (var i of response.CpScheme) {
          $("#Scheme").prop("checked", true);
          SchemeTable += `<tr>
            <td><input type="text" class="inputStyle" name="SchemeName" value = "${i.ProcessingCode1}"></td>
            <td><input type="text" class="inputStyle" name="SchemeName" value = "${i.ProcessingCode2}"></td>
            <td><input type="text" class="inputStyle" name="SchemeName" value = "${i.ProcessingCode3}"></td>
            <td class="OutItemCascDeleteButton"><i class="material-icons" style="color:red">delete</i></td>
          </tr>`
        }
        $('.SchemeClass').show()
        $('#SchemeTable tbody').html(SchemeTable)
      }

      $('#Loading').hide();
    }
  })
}

function MrtTimeOut(Val) {
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

var HsCode = [];
var ChkHsCode = [];
$(document).ready(function () {
  $.ajax({
    url: "/InPaymentItemLoad/",
    data: {
      PermitId: $("#PermitID").val().toUpperCase(),
    },
    success: function (response) {
      console.log("Item Page Loaded ...!");
      InhouseItemCode = response.inhouseItemCode;
      ItemHsCodeData = response.hsCode;
      ChkHsCode = response.chkHsCode;
      console.log(ItemHsCodeData)
      ItemLoadData()
    },
  });
});

function duticalc(op, ip, inp, imp, totduti) {
  let pckqty = 1;
  let HsVal = $("#ItemHsCode").val();
  let typeidval = 0;
  let kgmvis;
  for (var Hs of HsCode) {
    if (Hs.HSCode == HsVal) {
      kgmvis = Hs.Kgmvisible;
      typeidval = Hs.DUTYTYPID;
      console.log("tupeidval:",typeidval)
    }
  }
  if (op > 0) {
    pckqty = op;
  }
  if (ip > 0) {
    pckqty = pckqty * ip;
  }
  if (inp > 0) {
    pckqty = pckqty * inp;
  }
  if (imp > 0) {
    pckqty = pckqty * imp;
  }
  if ($("#ItemTotalDutiableQtyInput").val() != "") {
    let T1 = Number($("#itemExciseDutyInput1").val());
    let T2 = Number($("#iteminvoiceCIFFOB").val());
    let T3;
    let T4;
    let gstperval = Number($("#invoiceGSTInput1").val()) / 100;
    let TDQUOM = $("#ItemDutiableUom").val();
    if (TDQUOM == "LTR") {
      $("#ItemTotalDutiableQtyInput").val((pckqty * totduti).toFixed(2));
      $("#ItemHsQtyInput").val((pckqty * totduti).toFixed(2));
    } else if (TDQUOM == "KGM" && kgmvis == "MULTIPLE") {
      $("#ItemTotalDutiableQtyInput").val((pckqty * totduti).toFixed(2));
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(pckqty * totduti * T1);
      }

      T3 = Number($("#iteminvoiceCIFFOB").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "KGM" && kgmvis == "DIVIDE") {
      $("#ItemTotalDutiableQtyInput").val(((pckqty * totduti) / 1000).toFixed(2));
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(((pckqty * totduti) / 1000) * T1);
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "STK") {
      $("#ItemTotalDutiableQtyInput").val(pckqty.toFixed(2));
      $("#ItemHsQtyInput").val(((pckqty * totduti) / 1000).toFixed(2));
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val((pckqty * T1).toFixed(2));
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "KGM" && typeidval == 62) {
      $("#ItemTotalDutiableQtyInput").val((pckqty * totduti).toFixed(2));
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val((pckqty * totduti * T1).toFixed(2));
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "TNE" && typeidval == 62) {
      $("#ItemTotalDutiableQtyInput").val((pckqty * totduti).toFixed(2));
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val((pckqty * totduti * T1).toFixed(2));
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "KGM" && typeidval == 61) {
      $("#ItemTotalDutiableQtyInput").val((pckqty * totduti).toFixed(2));
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val((pckqty * totduti * T1).toFixed(2));
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "DAL") {
      $("#ItemTotalDutiableQtyInput").val((pckqty * totduti).toFixed(2));
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val((pckqty * totduti * T1).toFixed(2));
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    }
  }
}

function itemPreferntialCodeOut() {
  let Pref = $("#itemPreferntialCode").val()
  if (Pref == "PRF : if goods are imported under preferential duty rates") {
    $("#itemCustomsDutyInput1").val("0.00")
    $("#itemCustomsDutyInput2").val("--Select--")
    $("#itemCustomsDutyInput3").val("0.00")
  }
  dutiableQtyFunction()
}


//Invoive calculation 
//  onkeyup="InvoiceCalculation()" onblur="InvoiceCalculation()"

// document.getElementById('InvoiceAmount').addEventListener('input', function () {
//   const InvoiceExRate = Number($('#InvoiceExRate').val())
//   const InvoiceAmount = Number($('#InvoiceAmount').val())
//   const total = InvoiceExRate * InvoiceAmount
//   $('#InvoiceSumAmount').val(total.toFixed(2))
//   TotalCalculation()
// })

// document.getElementById('OtherCharges').addEventListener('input', function () {
//   const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//   const OtherCharges = Number($('#OtherCharges').val())

//   if (OtherCharges > 0) {
//     $('#OtherCurrency').val('--Select--')
//     $('#OtherExRate').val('0.00')
//     $('#OtherAmount').val('0.00')
//   }

//   const total = (InvoiceSumAmount * OtherCharges) / 100
//   $('#OtherSumAmount').val(total.toFixed(2))

//   TotalCalculation()
// })

// document.getElementById('OtherAmount').addEventListener('input', function () {

//   const ExRate = Number($('#OtherExRate').val())
//   const Amount = Number($('#OtherAmount').val())

//   const total = ExRate * Amount
//   $('#OtherSumAmount').val(total.toFixed(2))
//   TotalCalculation()
// })

// document.getElementById('FrightAmount').addEventListener('input', function () {

//   const ExRate = Number($('#FrightExRate').val())
//   const Amount = Number($('#FrightAmount').val())

//   const total = ExRate * Amount
//   $('#FrightSumAmount').val(total.toFixed(2))
//   TotalCalculation()
// })

// document.getElementById('FrightCharges').addEventListener('input', function () {

//   const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//   const Charges = Number($('#FrightCharges').val())

//   if (Charges > 0) {
//     $('#FrightCurrency').val('--Select--')
//     $('#FrightExRate').val('0.00')
//     $('#FrightAmount').val('0.00')
//   }

//   const total = (InvoiceSumAmount * Charges) / 100
//   $('#FrightSumAmount').val(total.toFixed(2))

//   TotalCalculation()
// })

// document.getElementById('InsurenceAmount').addEventListener('input', function () {

//   const ExRate = Number($('#InsurenceExRate').val())
//   const Amount = Number($('#InsurenceAmount').val())

//   const total = ExRate * Amount
//   $('#InsurenceSumAmount').val(total.toFixed(2))
//   TotalCalculation()
// })



// document.getElementById('InsurenceCharges').addEventListener('input', function () {
//   Insurance()
// })
// function Insurance() {
//   const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//   const OtherSumAmount = Number($('#OtherSumAmount').val())
//   const FrightSumAmount = Number($('#FrightSumAmount').val())
//   const InsurenceCharges = Number($('#InsurenceCharges').val())
//   const total = InvoiceSumAmount + OtherSumAmount + FrightSumAmount
//   const result = total * (InsurenceCharges / 100)
 
  
//   $('#InsurenceSumAmount').val(result.toFixed(2))
//   console.log($('#InsurenceSumAmount').val())

// }

// function TotalCalculation() {
//   const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//   const OtherSumAmount = Number($('#OtherSumAmount').val())
//   const FrightSumAmount = Number($('#FrightSumAmount').val())

//   if ($('#InsurenceAmount').val() < 1) {
//     Insurance()
//     console.log('hello1')
//   }

//   const InsurenceSumAmount = Number($('#InsurenceSumAmount').val())
//   const total = InvoiceSumAmount + OtherSumAmount + FrightSumAmount + InsurenceSumAmount
//   $('#CostInsurenceFreightSum').val(total.toFixed(2))
//   const gst = total * (Number($('#InvoiceGstCharge').val()) / 100)
//   $('#InvoiceGstSum').val(gst.toFixed(2))
// }


// today try
// $(document).ready(function() {
//   // Event listener for Invoice Amount input
//   document.getElementById('InvoiceAmount').addEventListener('input', function () {
//     const InvoiceExRate = Number($('#InvoiceExRate').val())
//     const InvoiceAmount = Number($('#InvoiceAmount').val())
//     const total = InvoiceExRate * InvoiceAmount
//     $('#InvoiceSumAmount').val(total.toFixed(2))
//     TotalCalculation()
//   })

//   // Event listener for Other Charges input
//   document.getElementById('OtherCharges').addEventListener('input', function () {
//     const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//     const OtherCharges = Number($('#OtherCharges').val())

//     if (OtherCharges > 0) {
//       $('#OtherCurrency').val('--Select--')
//       $('#OtherExRate').val('0.00')
//       $('#OtherAmount').val('0.00')
//     }

//     const total = (InvoiceSumAmount * OtherCharges) / 100
//     $('#OtherSumAmount').val(total.toFixed(2))

//     TotalCalculation()
//   })

//   // Event listener for Other Amount input
//   document.getElementById('OtherAmount').addEventListener('input', function () {
//     const ExRate = Number($('#OtherExRate').val())
//     const Amount = Number($('#OtherAmount').val())

//     const total = ExRate * Amount
//     $('#OtherSumAmount').val(total.toFixed(2))
//     TotalCalculation()
//   })

//   // Event listener for Freight Amount input
//   document.getElementById('FrightAmount').addEventListener('input', function () {
//     const ExRate = Number($('#FrightExRate').val())
//     const Amount = Number($('#FrightAmount').val())

//     const total = ExRate * Amount
//     $('#FrightSumAmount').val(total.toFixed(2))
//     TotalCalculation()
//   })

//   // Event listener for Freight Charges input
//   document.getElementById('FrightCharges').addEventListener('input', function () {
//     const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//     const Charges = Number($('#FrightCharges').val())

//     if (Charges > 0) {
//       $('#FrightCurrency').val('--Select--')
//       $('#FrightExRate').val('0.00')
//       $('#FrightAmount').val('0.00')
//     }

//     const total = (InvoiceSumAmount * Charges) / 100
//     $('#FrightSumAmount').val(total.toFixed(2))

//     TotalCalculation()
//   })

//   // Event listener for Insurance Amount input
//   document.getElementById('InsurenceAmount').addEventListener('input', function () {
//     const ExRate = Number($('#InsurenceExRate').val())
//     const Amount = Number($('#InsurenceAmount').val())

//     const total = ExRate * Amount
//     $('#InsurenceSumAmount').val(total.toFixed(2))
//     TotalCalculation()
//   })

//   // Event listener for Insurance Charges input
//   document.getElementById('InsurenceCharges').addEventListener('input', function () {
//     Insurance()
//   })

//   // Function to calculate Insurance
//   function Insurance() {
//     const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//     const OtherSumAmount = Number($('#OtherSumAmount').val())
//     const FrightSumAmount = Number($('#FrightSumAmount').val())
//     const InsurenceCharges = Number($('#InsurenceCharges').val())
//     const total = InvoiceSumAmount + OtherSumAmount + FrightSumAmount
//     const result = total * (InsurenceCharges / 100)

//     $('#InsurenceSumAmount').val(result.toFixed(2))
//   }

//   // Function to calculate total
//   function TotalCalculation() {
//     const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//     const OtherSumAmount = Number($('#OtherSumAmount').val())
//     const FrightSumAmount = Number($('#FrightSumAmount').val())

//     if ($('#InsurenceAmount').val() < 1) {
//       Insurance()
//       console.log('hello1')
//     }

//     const InsurenceSumAmount = Number($('#InsurenceSumAmount').val())
//     const total = InvoiceSumAmount + OtherSumAmount + FrightSumAmount + InsurenceSumAmount
//     $('#CostInsurenceFreightSum').val(total.toFixed(2))
//     const gst = total * (Number($('#InvoiceGstCharge').val()) / 100)
//     $('#InvoiceGstSum').val(gst.toFixed(2))
//   }
// })



//------------------------------------------------------------------------------------------------------------------------------//

$(document).ready(function() {
  // Event listener for Invoice Amount input
  document.getElementById('InvoiceAmount').addEventListener('input', function () {
    const InvoiceExRate = Number($('#InvoiceExRate').val())
    const InvoiceAmount = Number($('#InvoiceAmount').val())
    const total = InvoiceExRate * InvoiceAmount
    $('#InvoiceSumAmount').val(total.toFixed(2))

    const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
    const OtherSumAmount = Number($('#OtherSumAmount').val())
    const FrightSumAmount = Number($('#FrightSumAmount').val())
    const InsurenceCharges = Number($('#InsurenceCharges').val())
    const totalinsurance = InvoiceSumAmount + OtherSumAmount + FrightSumAmount
    const result = totalinsurance * (InsurenceCharges / 100)

    $('#InsurenceAmount').val(result.toFixed(2))
    $('#InsurenceSumAmount').val(result.toFixed(2))
    TotalCalculation()
  
  })

  //Event listener for Other Charges input
  document.getElementById('OtherCharges').addEventListener('input', function () {
    const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
    const OtherCharges = Number($('#OtherCharges').val())

    if (OtherCharges > 0) {
      $('#OtherCurrency').val('--Select--')
      $('#OtherExRate').val('0.00')
      $('#OtherAmount').val('0.00')
    }

    const total = (InvoiceSumAmount * OtherCharges) / 100
    $('#OtherSumAmount').val(total.toFixed(2))
    TotalCalculation()

   
  })

  // Event listener for Other Amount input
  document.getElementById('OtherAmount').addEventListener('input', function () {
    const ExRate = Number($('#OtherExRate').val())
    const Amount = Number($('#OtherAmount').val())

    const total = ExRate * Amount
    $('#OtherSumAmount').val(total.toFixed(2))
    TotalCalculation()
    
  })

//   // Event listener for Freight Amount input
  document.getElementById('FrightAmount').addEventListener('input', function () {
    const ExRate = Number($('#FrightExRate').val())
    const Amount = Number($('#FrightAmount').val())

    const total = ExRate * Amount
    $('#FrightSumAmount').val(total.toFixed(2))

    const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
    const FrightSumAmount = Number($('#FrightSumAmount').val())
    const InsurenceCharges = Number($('#InsurenceCharges').val())
    const totalinsurance = InvoiceSumAmount  + FrightSumAmount
    const result = totalinsurance * (InsurenceCharges / 100)

    $('#InsurenceAmount').val(result.toFixed(2))
    $('#InsurenceSumAmount').val(result.toFixed(2))
    TotalCalculation()
   
  })

  // Event listener for Freight Charges input
  document.getElementById('FrightCharges').addEventListener('input', function () {
    const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
    const Charges = Number($('#FrightCharges').val())

    if (Charges > 0) {
      $('#FrightCurrency').val('--Select--')
      $('#FrightExRate').val('0.00')
      $('#FrightAmount').val('0.00')
    }

    const total = (InvoiceSumAmount * Charges) / 100
    $('#FrightSumAmount').val(total.toFixed(2))

    TotalCalculation()

   
  })

//   // Event listener for Insurance Amount input
  // document.getElementById('InsurenceAmount').addEventListener('input', function () {
  //   const ExRate = Number($('#InsurenceExRate').val())
  //   const Amount = Number($('#InsurenceAmount').val())

  //   const total = ExRate * Amount
  //   $('#InsurenceSumAmount').val(total.toFixed(2))
   
  // })

  // // Event listener for Insurance Charges input
  document.getElementById('InsurenceCharges').addEventListener('input', function () {
   
  })

//   // Function to calculate Insurance
//   function Insurance() {
//     const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
//     const OtherSumAmount = Number($('#OtherSumAmount').val())
//     const FrightSumAmount = Number($('#FrightSumAmount').val())
//     const InsurenceCharges = Number($('#InsurenceCharges').val())
//     const total = InvoiceSumAmount + OtherSumAmount + FrightSumAmount
//     const result = total * (InsurenceCharges / 100)

//     $('#InsurenceSumAmount').val(result.toFixed(2))
//   }

//   // Function to calculate total
  function TotalCalculation() {
    const InvoiceSumAmount = Number($('#InvoiceSumAmount').val())
    const OtherSumAmount = Number($('#OtherSumAmount').val())
    const FrightSumAmount = Number($('#FrightSumAmount').val())

    if ($('#InsurenceAmount').val() < 1) {
      // Insurance()
      console.log('hello1')
    }

    const InsurenceSumAmount = Number($('#InsurenceSumAmount').val())
    const total = InvoiceSumAmount + OtherSumAmount + FrightSumAmount + InsurenceSumAmount
    $('#CostInsurenceFreightSum').val(total.toFixed(2))
    const gst = total * (Number($('#InvoiceGstCharge').val()) / 100)
    $('#InvoiceGstSum').val(gst.toFixed(2))
  }
})

//------------------------------------------------------------------------------------------------------------------------------------


function CopyImporter() {
  const ImporterCode = $('#ImporterCode').val().trim()
  if (ImporterCode === '') {
    alert("EMPTY IMPORTER CODE CHECK THE IMPORTER")
  }
  $('#InvoiceImportCode').val(ImporterCode);
  InvoiceImporterOut()
}