const NowDate = new Date();
const TOUCHTIME = NowDate.toISOString().slice(0, 19).replace("T", " ");
window.onload = function () {
  document.getElementById('declarationType').focus();
};

$(document).ready(function () {
  $("#INNONPAYMENT").css("background-color", "white");
  $("#INNONPAYMENT a").css("color", "green");
  $("#INPAYMENT").css("background-color", "rgb(25, 135, 84)");
  $("#INPAYMENT a").css("color", "white");
  $('#declarationType').focus();
});

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
  if (ID == "InvoiceTab") {
    $("#InvoiceTab").addClass("HeadTabStyleChange");
    $("#Invoice").show();
    $('#SupplierCodeInNon').focus();
  }
  if (ID == "ItemTab") {
    $("#ItemTab").addClass("HeadTabStyleChange");
    $("#Item").show();
    $('#ItemHsCodeInNon').focus()
  }
  if (ID == "CpcTab") {
    $("#CpcTab").addClass("HeadTabStyleChange");
    $("#Cpc").show();
    $('#cpcNextBtn').focus()
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
  if (ID == "CancelTab") {
    $("#CancelTab").addClass("HeadTabStyleChange");
    $("#Cancel").show();
  }
  if (ID == "RefundTab") {
    $("#RefundTab").addClass("HeadTabStyleChange");
    $("#Refund").show();
  }
}

function DeclarationChange() {
  let Dname = $("#declarationType").val().trim();
  $("#ItemOutHawbHblShow").hide();

  $("#claimantPartyCode").css("background", "#fff");
  $("#claimantPartyCruie").css("background", "#fff");
  $("#claimantPartyID1").css("background", "#fff");

  $("#ExporterCruei").css("background", "#fff");
  $("#ExporterName").css("background", "#fff");

  $("#InwardCruei").css("background", "#fff");
  $("#InwardName").css("background", "#fff");

  //$("#ConsigneeCountryCode").css("background", "#fff");

  $("#cargoStartDateVisible").hide();
  $("#LoadingPortVisible").show();

  $("#ExhibitionVisible").hide();
  $("#ExhibitionVisible input").val("");
  $("#cargoStartDateVisible").hide();
  $("#cargoEndDateVisible").hide();

  $("#InwardVisible").show();
  $("#OutwardVisible").hide();

  $("#InwardVisible select").val("--Select--");
  $("#OutwardVisible select").val("--Select--");

  $("#claimantPartyVisible").hide();
  $("#claimantPartyVisible input").val("");

  $("#ConsigneVisible").show();

  $("#ExporterVisible").hide();
  $("#ExporterVisible input").val("");

  $("#PartyOutwardVisible").hide();
  $("#PartyOutwardVisible input").val("");

  $("#InwardModeVisible").hide();
  $("#InwardModeVisible input").val("");

  $("#CargoStorageVisible").show();

  if (
    Dname == "BKT : BLANKET [INCLUDING BLANKET GST RELIEF (& DUTY EXEMPTION)]"
  ) {
    $("#LoadingPortVisible").hide();
    $("#LoadingPortVisible input").val("");
    $("#LoadingPortVisible textarea").val("");

    $("#cargoStartDateVisible").show();
    $("#CargoInHawbVisibile").hide();
    $("#CargoInHawbVisibile input").val("");
    $("#ExhibitionVisible").show();

    $("#InwardVisible").hide();

    $("#ConsigneVisible").hide();
    $("#ConsigneVisible input").val("");
    $("#claimantPartyVisible").show();
  } else if (Dname == "DES : DESTRUCTION") {
    $("#CargoInHawbVisibile").show();
  } else if (Dname == "APS : APPROVED PREMISES/SCHEMES") {
    $("#InwardCruei").css("background", "#d7f8dd");
    $("#InwardName").css("background", "#d7f8dd");

  } else if (Dname.trim() == "TCI : TEMPORARY EXPORT / RE-IMPORTED GOODS") {
    $("#OutwardVisible").hide();
  } else if (
    Dname == "TCE : TEMPORARY IMPORT FOR EXHIBITION/AUCTIONS WITHOUT SALES" ||
    Dname == "TCO : TEMPORARY IMPORT FOR OTHER PURPOSES" ||
    Dname == "TCR : TEMPORARY IMPORT FOR REPAIRS" ||
    Dname == "TCS : TEMPORARY IMPORT FOR EXHIBITION/AUCTIONS WITH SALES"
  ) {
    $("#ConsigneVisible").hide();
    $("#ConsigneVisible input").val("");
    $("#InwardModeVisible").show();
    $("#ExhibitionVisible").show();
    $("#cargoStartDateVisible").show();
    $("#cargoEndDateVisible").show();
  } else if (Dname == "REX : FOR RE-EXPORT") {
    $("#ItemOutHawbHblShow").show();
    $("#OutwardVisible").show();
    $("#ExporterVisible").show();
    $("#PartyOutwardVisible").show();
    $("#InwardModeVisible").show();
    $("#CargoInHawbVisibile").show();

    $("#ExporterCruei").css("background", "#d7f8dd");
    $("#ExporterName").css("background", "#d7f8dd");

    $("#InwardCruei").css("background", "#fff");
    $("#InwardName").css("background", "#fff");

    $("#ConsigneeCountryCode").css("background", "#d7f8dd");

  }
  else if (Dname == "SFZ : STORAGE IN FTZ") {
    $("#ItemOutHawbHblShow").show();
    $("#OutwardVisible").show();
    $("#PartyOutwardVisible").show();

    $("#InwardModeVisible").show();
  }
  else {
    $("#ConsigneVisible").hide();
    $("#CargoInHawbVisibile").show();
    if (Dname == "GTR : GST RELIEF (& DUTY EXEMPTION)") {
      $("#claimantPartyVisible ").show();
      $("#claimantPartyCode").css("background", "#d7f8dd");
      $("#claimantPartyCruie").css("background", "#d7f8dd");
      $("#claimantPartyID1").css("background", "#d7f8dd");

      $("#InwardCruei").css("background", "#d7f8dd");
      $("#InwardName").css("background", "#d7f8dd");

      $("#InwardModeVisible").show();
    } else if (Dname == "TCR : TEMPORARY IMPORT FOR REPAIRS") {
      $("#InwardCruei").css("background", "#d7f8dd");
      $("#InwardName").css("background", "#d7f8dd");

      $("#ExhibitionVisible").show();

      $("#cargoStartDateVisible").show();
      $("#cargoEndDateVisible").show();
    } else if (Dname == "SHO : SHUT-OUT") {
      $("#InwardModeVisible").show();
      $("#CargoStorageVisible").hide();
    } else {
      $("#ConsigneVisible").show();
    }
  }
}

function CargoPackChange() {
  var Cargo = $("#CargoPackType").val();

  if (Cargo == "9: Containerized") {
    $("#InpaymentContainerShow").show();
  } else {
    $("#InpaymentContainerShow").hide();
    $("#InpaymentContainerShow input").val("");
    $.ajax({
      url: "/ContainerInNon/",
      type: "POST",
      data: {
        Method: "ALLDELETE",
        PermitId: $("#PermitIDInNon").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        ContainerLoad(response.ContainerValue);
      },
    });
  }
}

function InwardChange() {
  var Inward = $("#inwardTranseportMode").val();

  $("#InwardModeInsert").val(Inward);
  var Insert = $("#InwardModeInsert").val();

  if( Insert == "--Select--"){
    $("#InNonLoadingPortInput").val("");
    $("#InNonLoadingPortText").val("");
    $("#CargoInHawb").val("");
    $("#ArrivalDate").val("");
  };

  $("#CargoInwardDetails").show();
  $("#InwardModeVisible").show();


  $("#CargoInHawbVisibile label").html("IN HAWB/HBL");
  $("#itemHwabHbl").html("IN HAWB/HBL");

  $("#VoyageNumberVisible").hide();
  $("#VesselNameVisible").hide();
  $("#OblVisible").hide();
  $("#VoyageNumberVisible input").val("");
  $("#VesselNameVisible input").val("");
  $("#OblVisible input").val("");

  $("#InwardConvetanceNoVisible input").val("");
  $("#InwardTransportIdVisible input").val("");
  $("#InwardConvetanceNoVisible").hide();
  $("#InwardTransportIdVisible").hide();

  $("#FlightNumberVisible").hide();
  $("#AirCraftRegNoVisible").hide();
  $("#CargoMawbVisible").hide();
  $("#FlightNumberVisible input").val("");
  $("#AirCraftRegNoVisible input").val("");
  $("#CargoMawbVisible input").val("");

  if (Inward == "1 : Sea") {
    $("#VoyageNumberVisible").show();
    $("#CargoInHawbVisibile label").html("HBL");
    $("#itemHwabHbl").html("IN HBL");
    $("#VesselNameVisible").show();
    $("#OblVisible").show();
    $("#InNonLoadingPortInput").val("");
    $("#InNonLoadingPortText").val("");
    $("#CargoInHawb").val("");
    $("#ArrivalDate").val("");

  } else if (
    Inward == "2 : Rail" ||
    Inward == "3 : Road" ||
    Inward == "5 : Mail" ||
    Inward == "7 : Pipeline" ||
    Inward == "6 : Multi-model(Not in use)"
  ) {
    $("#CargoInHawbVisibile label").html("HBL");
    $("#itemHwabHbl").html("IN HBL");
    $("#InwardConvetanceNoVisible").show();
    $("#InwardTransportIdVisible").show();
    $("#InNonLoadingPortInput").val("");
    $("#InNonLoadingPortText").val("");
    $("#CargoInHawb").val("");
    $("#ArrivalDate").val("");
  } else if (Inward == "N : Not Required") {
    $("#CargoInwardDetails").hide();
    $("#CargoInwardDetails input").val("");
  } else if (Inward == "4 : Air") {
    $("#CargoInHawbVisibile label").html("HAWB");
    $("#itemHwabHbl").html("IN HAWB");
    $("#FlightNumberVisible").show();
    $("#AirCraftRegNoVisible").show();
    $("#CargoMawbVisible").show();
    $("#InNonLoadingPortInput").val("");
    $("#InNonLoadingPortText").val("");
    $("#CargoInHawb").val("");
    $("#ArrivalDate").val("");
  }

}

function OutwardChange() {
  var Outward = $("#OutwardTranseportMode").val();
  $("#InNonOutMode").val(Outward);

  if( Outward == "--Select--"){
    $("#InNonDisachargeInput").val("");
    $("#InNonDisachargeText").val("");
    $("#InNonFinalDestinationSelect").val("--Select--");
    $("#DepartureDate").val("");
    $("#InNonOutHblHawbInput").val("");
    $("#InNonOutConveyanceInput").val("");
    $("#InNonOutTranseportIdInput").val("");
  };
 
  
  if (Outward != "--Select--") {
    $("#InNonOutMode").val(Outward);

    $("#ExhibitionVisible").show();
    $("#ExhibitionVisible1").hide();

    $("#OutwardVisibile").show();
    $("#OutWardModeVisible").show();
    $("#OutwardDischargePort").show();
    $("#FinalDestinationCountryVisible").show();
    $("#DepartureDateDiv").show();
    $("#SeaStoreVisible").show();

    $("#InNonOutVoyageDiv").hide();
    $("#InNonOutVesselNameDiv").hide();
    $("#InNonOutOblDiv").hide();
    $("#InNonOutHblHawbDiv").hide();
    $("#InNonOutHblHawbLabel").html("HAWB/HBL");
    $("#ItemOutHawbHblShow").show();
    $("#ItemOutHawb").html("HAWB/HBL");
    $("#InNonVesselTypeDiv").hide();
    $("#InNonVesselNetRegisterDiv").hide();
    $("#InNonVesselNationalityDiv").hide();
    $("#InNonTowingVesselIdDiv").hide();
    $("#InNonTowingVesselNameDiv").hide();
    $("#InNonNextPortDiv").hide();
    $("#InNonLastPortDiv").hide();

    $("#InNonOutConveyanceDiv").hide();
    $("#InNonOutTranseportIdDiv").hide();

    $("#InNonOutFlightNumberDiv").hide();
    $("#InNonOutAirCraftDiv").hide();
    $("#InNonOutMawbDiv").hide();

    $("#InNonOutVoyageDiv input").val("");
    $("#InNonOutVesselNameDiv input").val("");
    $("#InNonOutOblDiv input").val("");
    $("#InNonOutHblHawbDiv input").val("");
    $("#InNonVesselTypeDiv select").val("--Select--");
    $("#InNonVesselNetRegisterDiv input").val("");
    $("#InNonVesselNationalityDiv input").val("");
    $("#InNonTowingVesselIdDiv input").val("");
    $("#InNonTowingVesselNameDiv input").val("");
    $("#InNonNextPortDiv input").val("");
    $("#InNonLastPortDiv input").val("");

    $("#InNonOutConveyanceDiv input").val("");
    $("#InNonOutTranseportIdDiv input").val("");

    $("#InNonOutFlightNumberDiv input").val("");
    $("#InNonOutAirCraftDiv input").val("");
    $("#InNonOutMawbDiv input").val("");

    if (Outward == "1 : Sea") {
      $("#InNonOutVoyageDiv").show();
      $("#InNonOutVesselNameDiv").show();
      $("#InNonOutOblDiv").show();
      $("#InNonOutHblHawbDiv").show();
      $("#InNonOutHblHawbLabel").html("HBL");
      $("#ItemOutHawb").html("OUT HBL");
      $("#InNonVesselTypeDiv").show();
      $("#InNonVesselNetRegisterDiv").show();
      $("#InNonVesselNationalityDiv").show();
      $("#InNonTowingVesselIdDiv").show();
      $("#InNonTowingVesselNameDiv").show();
      $("#InNonNextPortDiv").show();
      $("#InNonLastPortDiv").show();
      $("#InNonDisachargeInput").val("");
      $("#InNonDisachargeText").val("");
      $("#InNonFinalDestinationSelect").val("--Select--");
      $("#DepartureDate").val("");
      $("#InNonOutHblHawbInput").val("");
      $("#InNonOutConveyanceInput").val("");
      $("#InNonOutTranseportIdInput").val("");


    } else if (
      Outward == "2 : Rail" ||
      Outward == "3 : Road" ||
      Outward == "5 : Mail" ||
      Outward == "7 : Pipeline" ||
      Outward == "6 : Multi-model(Not in use)"
    ) {
      $("#InNonOutHblHawbDiv").show();
      $("#InNonOutHblHawbLabel").html("HBL");
      $("#ItemOutHawb").html("OUT HBL");
      $("#InNonOutConveyanceDiv").show();
      $("#InNonOutTranseportIdDiv").show();
      $("#InNonDisachargeInput").val("");
      $("#InNonDisachargeText").val("");
      $("#InNonFinalDestinationSelect").val("--Select--");
      $("#DepartureDate").val("");
      $("#InNonOutHblHawbInput").val("");
      $("#InNonOutConveyanceInput").val("");
      $("#InNonOutTranseportIdInput").val("");
    } else if (Outward == "4 : Air") {

      $("#FlightNO").css("background", "#fff");
      $("#MasterAirwayBill").css("background", "#fff");

      $("#InNonOutHblHawbDiv").show();
      $("#InNonOutHblHawbLabel").html("HAWB");
      $("#ItemOutHawb").html("OUT HAWB");
      $("#InNonOutFlightNumberDiv").show();
      $("#InNonOutAirCraftDiv").show();
      $("#InNonOutMawbDiv").show();
      $("#InNonDisachargeInput").val("");
      $("#InNonDisachargeText").val("");
      $("#InNonFinalDestinationSelect").val("--Select--");
      $("#DepartureDate").val("");
      $("#InNonOutHblHawbInput").val("");
      $("#InNonOutConveyanceInput").val("");
      $("#InNonOutTranseportIdInput").val("");
    } else if (Outward == "N : Not Required") {
      $("#ExhibitionVisible").hide();

      $("#OutwardVisibile").hide();
      $("#OutwardVisibile input").val("");
      $("#OutwardVisibile select").val("--Select--");
    }
  }
  // CargoResetInNon()
}

function ReferenceDocument() {
  if ($("#ReferenceDocuments").prop("checked")) {
    $("#ReferenceShow").show();
    $("#ReferenceDocuments").val("True");
  } else {
    $("#ReferenceDocuments").val("False");
    $("#ReferenceShow").hide();
    $("#ReferenceShow input").val("");
    $("#ReferenceShow select").val("--Select--");
    $.ajax({
      url: "/AttachInNon/",
      data: {
        Method: "ALLDELETE",
        PermitId: $("#PermitIDInNon").val(),
      },
      success: function (response) {
        AttachData = response.attachFile;
        AttachLoad(AttachData);
      },
    });
  }
}

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


function HeaderResetInNon(){

    $("#declarationType").val("--Select--");
    $("#PreviousPermitNo").val("");
    $("#CargoPackType").val("--Select--");
    $("#inwardTranseportMode").val("--Select--");
    $("#OutwardTranseportMode").val("--Select--");
    $("#DeclaringFor").val("--Select--");
    $("#BgIndicator").val("--Select--");
    $("#OverRideExchangeRate").prop('checked',false);
    $("#SupplyIndicator").prop('checked',false);
    $("#ReferenceDocuments").prop('checked',false);
    $("#Recipient1").val("");
    $("#Recipient2").val("");
    $("#Recipient3").val("");
    $("#License1").val("");
    $("#License2").val("");
    $("#License3").val("");
    $("#License4").val("");
    $("#License5").val("");
 
    ReferenceDocument()

}
/*-----------------------------------Party AutoComplete-----------------------------------------*/

var InNonImporter = [];
var InNonExporter = [];
var InNonInward = [];
var InNonOutWard = [];
var InNonFright = [];
var InNonConsign = [];
var InNonClaimant = [];
var InvoiceData = [];
var ItemData = [];
var CascData = [];
var CpcData = [];
$(document).ready(function () {
  $("#Loading").show();
  $.ajax({
    url: "/InNonPartyLoad/",
    data: {
      PermitId: $("#PermitIDInNon").val(),
    },
    success: function (response) {
      console.log("Party Page Loades...!");
      InNonImporter = response.Importer;
      InNonExporter = response.Exporter;
      InNonInward = response.Inward;
      InNonOutWard = response.Outward;
      InNonFright = response.fright;
      InNonConsign = response.consign;
      InNonClaimant = response.Claimant;
      InvoiceData = response.invoice;
      ItemData = response.item;
      CascData = response.casc;
      CpcData = response.Cpc;
      InvoiceLoadInNon();
      ItemLoad();
      $("#Loading").hide();
      InNonImporterOut();
      InNonExporterOut();
      InwardFocusOut();
      OutWardFocusOut();
      ConsigneFocusOut();
      FrightFocusOut();
      InNonClaimentFocusOut();
      CpcDataLoad();
      $("#declarationType").focus()
    },
  });
});

function InNonImporterIn() {
  var myValues = [];
  for (var i of InNonImporter) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#InNonImporterCode");
}

function InNonImporterOut() {
  let Value = $("#InNonImporterCode").val().trim();
  if (Value == "") {
    $(".ImporterEmpty input").val("");
  } else {
    for (var i of InNonImporter) {
      if (i.Code == Value) {
        $("#InNonImporterCruei").val(i.CRUEI);
        $("#InNonImporterName").val(i.Name);
        $("#InNonImporterName1").val(i.Name1);
        InNonInvoiceImporterOut(Value);
        var nextIndex = parseInt($('#InNonImporterCode').attr('tabindex')) + 4;
        $('[tabindex="' + nextIndex + '"]').focus();
      }
    }
  }
}

function InNonExporterIn() {
  var myValues = [];
  for (var i of InNonExporter) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#ExporterCode");
}
function backspaceEvent(Id) {
  $('#' + Id).keydown(function (event) {
    if (event.shiftKey && event.key === 'Tab') {
      var nextIndex = parseInt($('#' + Id).attr('tabindex')) - 1;
      $('[tabindex="' + nextIndex + '"]').focus();
    }
  });
}
function InNonExporterOut() {
  let Value = $("#ExporterCode").val().trim();
  if (Value == "") {
    $("#ExporterVisible input").val("");
  } else {
    for (var i of InNonExporter) {
      if (i.Code == Value) {
        $("#ExporterCruei").val(i.CRUEI);
        $("#ExporterName").val(i.Name);
        $("#ExporterName1").val(i.Name1);
        var nextIndex = parseInt($('#ExporterCode').attr('tabindex')) + 4;
        $('[tabindex="' + nextIndex + '"]').focus();
        backspaceEvent('ExporterCode')
      }
    }
  }
}

function InwardFocusIn() {
  var myValues = [];
  for (var i of InNonInward) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#InwardCode");
}

function InwardFocusOut() {
  let Value = $("#InwardCode").val().trim();
  if (Value == "") {
    $(".InwardEmpty input").val("");
  } else {
    for (var i of InNonInward) {
      if (i.Code.trim() == Value) {
        $("#InwardCruei").val(i.CRUEI);
        $("#InwardName").val(i.Name);
        $("#InwardName1").val(i.Name1);
        var nextIndex = parseInt($('#InwardCode').attr('tabindex')) + 4;
        $('[tabindex="' + nextIndex + '"]').focus();
        backspaceEvent('InwardCode')
      }
    }
  }
}

function OutWardFocusIn() {
  var myValues = [];
  for (var i of InNonOutWard) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#OutWardCarreirCode");
}

function OutWardFocusOut() {
  let Value = $("#OutWardCarreirCode").val().trim();
  if (Value == "") {
    $(".OutwardEmpty input").val("");
  } else {
    for (var i of InNonOutWard) {
      if (i.Code == Value) {
        $("#OutWardCarreirCRUEI").val(i.CRUEI);
        $("#OutWardCarreirName").val(i.Name);
        $("#OutWardCarreirName1").val(i.Name1);
        var nextIndex = parseInt($('#OutWardCarreirCode').attr('tabindex')) + 4;
        $('[tabindex="' + nextIndex + '"]').focus();
        backspaceEvent('OutWardCarreirCode')
      }
    }
  }
}

function FrightFrwdFocusIN() {
  var myValues = [];
  for (var i of InNonFright) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#FreightForwarderCode");
}

function FrightFocusOut() {
  let Value = $("#FreightForwarderCode").val().trim();
  if (Value == "") {
    $(".FrieghtEmpty input").val("");
  } else {
    for (var i of InNonFright) {
      if (i.Code == Value) {
        $("#FreightForwarderCruei").val(i.CRUEI);
        $("#FreightForwarderName").val(i.Name);
        $("#FreightForwarderName1").val(i.Name1);
        var nextIndex = parseInt($('#FreightForwarderCode').attr('tabindex')) + 4;
        $('[tabindex="' + nextIndex + '"]').focus();
        backspaceEvent('FreightForwarderCode')
      }
    }
  }
}

function ConsigneFocusIN() {
  var myValues = [];
  for (var i of InNonConsign) {
    myValues.push(i.ConsigneeCode + ":" + i.ConsigneeName);
  }
  Autocomplete1(myValues, "#ConsignCode");
}

function ConsigneFocusOut() {
  let Value = $("#ConsignCode").val().trim();
  if (Value == "") {
    $("#ConsigneVisible input").val("");
  } else {
    for (var i of InNonConsign) {
      if (i.ConsigneeCode == Value) {
        $("#ConsignName").val(i.ConsigneeName);
        $("#ConsignName1").val(i.ConsigneeName1);
        $("#ConsignCruei").val(i.ConsigneeCRUEI);
        $("#ConsignAddress").val(i.ConsigneeAddress);
        $("#ConsignAddress1").val(i.ConsigneeAddress1);
        $("#ConsignCity").val(i.ConsigneeCity);
        $("#ConsignSubCode").val(i.ConsigneeSub);
        $("#ConsignSubDivision").val(i.ConsigneeSubDivi);
        $("#ConsignPostal").val(i.ConsigneePostal);
        $("#ConsignCountryCode").val(i.ConsigneeCountry);
        var nextIndex = parseInt($('#ConsignCode').attr('tabindex')) + 4;
        $('[tabindex="' + nextIndex + '"]').focus();
        backspaceEvent('ConsignCode')
        break;
      }
    }
  }
}

function InNonClaimentFocusIN() {
  var myValues = [];
  for (var i of InNonClaimant) {
    myValues.push(i.Name + ":" + i.Name1);
  }
  Autocomplete1(myValues, "#ClaimantName");
}

function InNonClaimentFocusOut() {
  let Value = $("#ClaimantName").val().trim();
  if (Value == "") {
    $("#claimantPartyVisible input").val("");
  } else {
    for (var i of InNonClaimant) {
      if (i.Name == Value) {
        $("#ClaimantCruei").val(i.CRUEI);
        $("#Claimant_Name1").val(i.Name1);
        $("#Claimant_Name2").val(i.Name2);
        $("#ClaimantName1").val(i.ClaimantName);
        $("#ClaimantName2").val(i.ClaimantName1);
        var nextIndex = parseInt($('#ClaimantName').attr('tabindex')) + 4;
        $('[tabindex="' + nextIndex + '"]').focus();
        backspaceEvent('ClaimantName')
        break;
      }
    }
  }
}
/*-----------------------------------Party Searching-----------------------------------------*/

function InNonImporeterSearch(Model, Head, Code, Cruei, Name, Name1) {
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Model) {
    tag += `
      <tr onclick="InNonImporeterSearchSelectRow(this,'${Code}','${Cruei}','${Name}','${Name1}')" style="cursor: pointer;">
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

function InNonConsigneImg() {
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of InNonConsign) {
    tag += `
      <tr onclick="InNonConsigneImgSelectRow(this)" style="cursor: pointer;">
          <td>${i.ConsigneeCode}</td>
          <td>${i.ConsigneeName}</td>
          <td>${i.ConsigneeName1}</td>
          <td>${i.ConsigneeAddress}</td>
          <td>${i.ConsigneeCity}</td>
          <td>${i.ConsigneeCountry}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>CONSIGNEE</h1>
                  <input type="text" id="InNonConsigneSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonConsignee').DataTable().search($('#InNonConsigneSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonConsignee">
                      <thead>
                          <th>Code</th>
                          <th>Name</th>
                          <th>Name1</th>
                          <th>Address</th>
                          <th>City</th>
                          <th>Country</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonConsignee").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}

function InNonConsigneImgSelectRow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  $("#ConsignCode").val(col1);
  ConsigneFocusOut();

  $("#InNonImporterSerchId").hide();
}

function InNonClaimantImg() {
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of InNonClaimant) {
    tag += `
      <tr onclick="InNonClaimantImgSelectrow(this)" style="cursor: pointer;">
          <td>${i.Name}</td>
          <td>${i.Name1}</td>
          <td>${i.Name2}</td>
          <td>${i.CRUEI}</td>
          <td>${i.ClaimantName}</td>
          <td>${i.ClaimantName1}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>CLAIMANT PARTY</h1>
                  <input type="text" id="InNonConsigneSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonConsignee').DataTable().search($('#InNonConsigneSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonConsignee">
                      <thead>
                          <th>NAME</th>
                          <th>NAME 1</th>
                          <th>NAME 2</th>
                          <th>CR UEI</th>
                          <th>CLAIMANT NAME</th>
                          <th>CLAIMANT ID</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonConsignee").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}

function InNonClaimantImgSelectrow(Arg) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  $("#ClaimantName").val(col1);
  InNonClaimentFocusOut(col1);
  $("#InNonImporterSerchId").hide();
}
/*-----------------------------------Party Inserting Datas-----------------------------------------*/

function InNonImporterSave() {
  $("#InNonImporterCodeSpan").hide();
  $("#InNonImporterCrueiSpan").hide();
  $("#InNonImporterNameSpan").hide();
  let code = $("#InNonImporterCode").val();
  let cruei = $("#InNonImporterCruei").val();
  let name = $("#InNonImporterName").val();
  let name1 = $("#InNonImporterName1").val();
  let check = true;
  if (code == "") {
    check = false;
    $("#InNonImporterCodeSpan").show();
  }
  if (cruei == "") {
    check = false;
    $("#InNonImporterCrueiSpan").show();
  }
  if (name == "") {
    check = false;
    $("#InNonImporterNameSpan").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonPartyLoad/",
      type: "POST",
      data: {
        MODEL: "IMPORTER",
        Code: code.trim(),
        CRUEI: cruei.trim(),
        Name: name.trim(),
        Name1: name1.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InNonImporter = response.Importer;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function InNonExporterSave() {
  $("#ExporterCodeSpan").hide();
  $("#ExporterCrueiSpan").hide();
  $("#ExporterNameSpan").hide();
  let code = $("#ExporterCode").val();
  let cruei = $("#ExporterCruei").val();
  let name = $("#ExporterName").val();
  let name1 = $("#ExporterName1").val();
  let check = true;
  if (code == "") {
    check = false;
    $("#ExporterCodeSpan").show();
  }
  if (cruei == "") {
    check = false;
    $("#ExporterCrueiSpan").show();
  }
  if (name == "") {
    check = false;
    $("#ExporterNameSpan").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonPartyLoad/",
      type: "POST",
      data: {
        MODEL: "EXPORTER",
        Code: code.trim(),
        CRUEI: cruei.trim(),
        Name: name.trim(),
        Name1: name1.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InNonExporter = response.Exporter;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function InNonInwardSave() {
  $("#InNonInwardCodeSpan").hide();
  $("#InNonInwardCrueiSpan").hide();
  $("#InNonInwardNameSpan").hide();
  let code = $("#InwardCode").val();
  let cruei = $("#InwardCruei").val();
  let name = $("#InwardName").val();
  let name1 = $("#InwardName1").val();
  let check = true;
  if (code == "") {
    check = false;
    $("#InNonInwardCodeSpan").show();
  }
  if (cruei == "") {
    check = false;
    $("#InNonInwardCrueiSpan").show();
  }
  if (name == "") {
    check = false;
    $("#InNonInwardNameSpan").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonPartyLoad/",
      type: "POST",
      data: {
        MODEL: "INWARD",
        Code: code.trim(),
        CRUEI: cruei.trim(),
        Name: name.trim(),
        Name1: name1.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InNonFright = response.fright;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function InNonOutwardSave() {
  $("#OutWardCarreirCodeSpan").hide();
  $("#OutWardCarreirCRUEISpan").hide();
  $("#OutWardCarreirNameSpan").hide();
  let code = $("#OutWardCarreirCode").val();
  let cruei = $("#OutWardCarreirCRUEI").val();
  let name = $("#OutWardCarreirName").val();
  let name1 = $("#OutWardCarreirName1").val();
  let check = true;
  if (code == "") {
    check = false;
    $("#OutWardCarreirCodeSpan").show();
  }
  if (cruei == "") {
    check = false;
    $("#OutWardCarreirCRUEISpan").show();
  }
  if (name == "") {
    check = false;
    $("#OutWardCarreirNameSpan").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonPartyLoad/",
      type: "POST",
      data: {
        MODEL: "OUTWARD",
        Code: code.trim(),
        CRUEI: cruei.trim(),
        Name: name.trim(),
        Name1: name1.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InNonOutWard = response.Outward;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function InNonFrightSave() {
  $("#FrightCodeSpan").hide();
  $("#FreightForwarderCrueiSpan").hide();
  $("#FreightForwarderNameSpan").hide();
  let code = $("#FreightForwarderCode").val();
  let cruei = $("#FreightForwarderCruei").val();
  let name = $("#FreightForwarderName").val();
  let name1 = $("#FreightForwarderName1").val();
  let check = true;
  if (code == "") {
    check = false;
    $("#FrightCodeSpan").show();
  }
  if (cruei == "") {
    check = false;
    $("#FreightForwarderCrueiSpan").show();
  }
  if (name == "") {
    check = false;
    $("#FreightForwarderNameSpan").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonPartyLoad/",
      type: "POST",
      data: {
        MODEL: "FRIGHT",
        Code: code.trim(),
        CRUEI: cruei.trim(),
        Name: name.trim(),
        Name1: name1.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InNonFright = response.fright;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function ConsigneSave() {
  $("#ConsignCodeSpan").hide();
  $("#ConsignCrueiSpan").hide();
  $("#ConsignNameSpan").hide();
  let code = $("#ConsignCode").val();
  let cruei = $("#ConsignCruei").val();
  let name = $("#ConsignName").val();
  let name1 = $("#ConsignName1").val();
  let address = $("#ConsignAddress").val();
  let address1 = $("#ConsignAddress1").val();
  let city = $("#ConsignCity").val();
  let subcode = $("#ConsignSubCode").val();
  let subdivision = $("#ConsignSubDivision").val();
  let postal = $("#ConsignPostal").val();
  let countryCode = $("#ConsignCountryCode").val();
  let check = true;
  if (code == "") {
    check = false;
    $("#ConsignCodeSpan").show();
  }
  if (cruei == "") {
    check = false;
    $("#ConsignCrueiSpan").show();
  }
  if (name == "") {
    check = false;
    $("#ConsignNameSpan").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonPartyLoad/",
      type: "POST",
      data: {
        MODEL: "CONSIGNE",
        ConsigneeCode: code.trim(),
        ConsigneeName: name.trim(),
        ConsigneeName1: name1.trim(),
        ConsigneeCRUEI: cruei.trim(),
        ConsigneeAddress: address.trim(),
        ConsigneeAddress1: address1.trim(),
        ConsigneeCity: city.trim(),
        ConsigneeSub: subcode.trim(),
        ConsigneeSubDivi: subdivision.trim(),
        ConsigneePostal: postal.trim(),
        ConsigneeCountry: countryCode.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InNonConsign = response.consign;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function InNonClaimantSave() {
  $("#ClaimantNameSpan").hide();
  $("#ClaimantCrueiSpan").hide();
  $("#Claimant_Name1Span").hide();
  let name = $("#ClaimantName").val();
  let cruei = $("#ClaimantCruei").val();
  let name1 = $("#Claimant_Name1").val();
  let name2 = $("#Claimant_Name2").val();
  let claimantName1 = $("#ClaimantName1").val();
  let claimantName2 = $("#ClaimantName2").val();
  let check = true;
  if (name == "") {
    check = false;
    $("#ClaimantNameSpan").show();
  }
  if (cruei == "") {
    check = false;
    $("#ClaimantCrueiSpan").show();
  }
  if (name1 == "") {
    check = false;
    $("#Claimant_Name1Span").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonPartyLoad/",
      type: "POST",
      data: {
        MODEL: "CLAIMANT",
        Name: name.trim(),
        Name1: name1.trim(),
        Name2: name2.trim(),
        CRUEI: cruei.trim(),
        ClaimantName: claimantName1.trim(),
        ClaimantName1: claimantName2.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InNonClaimant = response.Claimant;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function PartyresetInNon() {
  $("#InNonImporterCode").val("");
  $("#InNonImporterCruei").val("");
  $("#InNonImporterName").val("");
  $("#InNonImporterName1").val("");
  $("#ExporterCode").val("");
  $("#ExporterCruei").val("");
  $("#ExporterName").val("");
  $("#ExporterName1").val("");
  $("#InwardCode").val("");
  $("#InwardCruei").val("");
  $("#InwardName").val("");
  $("#InwardName1").val("");
  $("#OutWardCarreirCode").val("");
  $("#OutWardCarreirCRUEI").val("");
  $("#OutWardCarreirName").val("");
  $("#OutWardCarreirName1").val("");
  $("#FreightForwarderCode").val("");
  $("#FreightForwarderCruei").val("");
  $("#FreightForwarderName").val("");
  $("#FreightForwarderName1").val("");
  $("#ConsignCode").val("");
  $("#ConsignCruei").val("");
  $("#ConsignName").val("");
  $("#ConsignName1").val("");
  $("#ConsignAddress").val("");
  $("#ConsignAddress1").val("");
  $("#ConsignCity").val("");
  $("#ConsignSubCode").val("");
  $("#ConsignSubDivision").val("");
  $("#ConsignPostal").val("");
  $("#ConsignCountryCode").val("");
  $("#ClaimantName").val("");
  $("#ClaimantCruei").val("");
  $("#Claimant_Name1").val("");
  $("#Claimant_Name2").val("");
  $("#ClaimantName2").val("");


}
/*-----------------------------------CARGO PAGE-----------------------------------------*/

var TotalOuterPack;
var ReleaseLocation;
var ReceiptLocation;
var StorageLocation;
var LoadingPort;
var Country = [];
var InNonVessel;
var NextPort;
var LastPort;
$(document).ready(function () {
  $.ajax({
    url: "/InNonCargoPage/",
    success: function (response) {
      console.log("Cargo Page Loaded ...!");
      TotalOuterPack = response.TotOuterPack;
      ReleaseLocation = response.releaseLoc;
      ReceiptLocation = response.reciptLoc;
      StorageLocation = response.storageLoc;
      LoadingPort = response.loadingPort;
      Country = response.country;
      InNonVessel = response.vessel;
      NextPort = response.loadingPort;
      LastPort = response.loadingPort;
      InNonTotOuterPackDropFunction(response.TotOuterPack);
      InNonFinalDestinationCountry(response.country);
      InNonOutVesselFunction(response.vessel);
      InNonLoadingPortFocusout();
      InNonStorageFocusOut();
      InNonLoadingNextPortFocusOut($("#InNonNextPortInput").val())
      InNonLoadingLastPortFocusOut($("#InNonLastPortInput").val())
      InNonDisachargePortFocusOut($("#InNonDisachargeInput").val())
      TotalOutUom()
      $("#declarationType").focus()
    },
  });
});

function InNonTotOuterPackDropFunction(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option value=${i.Name}>${i.Name}</option>`;
  }
  $("#InNonTotOuterPackDrop").html(drop);
  $("#ItemDutiableUom").html(drop);
  $("#ItemTotalDutiableQtyUom").html(drop);
  $("#ItemHsQtyUom").html(drop);
  $("#itemOtherTaxUom").html(drop);
  $("#itemOuterPackQtySelect").html(drop);
  $("#itemInPackQuantitySelect").html(drop);
  $("#itemInnerPackQtySelect").html(drop);
  $("#itemInmostPackQtySelect").html(drop);
  $("#product1CodeCopyUom").html(drop);
  $("#product2CodeCopyUom").html(drop);
  $("#product3CodeCopyUom").html(drop);
  $("#product4CodeCopyUom").html(drop);
  $("#product5CodeCopyUom").html(drop);
  TotalOutUom();
}

function InNonReleaseFocusIn() {
  var myValues = [];
  for (var i of ReleaseLocation) {
    myValues.push(i.locationCode + ":" + `${i.description}`);
  }
  Autocomplete1(myValues, "#InNonReleaseInput");
}

function InNonReleaseFocusOut(val) {
  if (val == "") {
    $("#InNonReleaseText").val("");
  } else {
    for (var i of ReleaseLocation) {
      if (val.trim().toUpperCase() == (i.locationCode).trim().toUpperCase()) {
        let Desc = (i.description).replaceAll("\n", "")
        $("#InNonReleaseText").val(`${Desc}`);
      }
    }
  }
}

function InNonReleaseSearchImg(Head, Table, Input, Text) { 
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Table) {
    tag += `
      <tr onclick="ReleaseImgSelectRow(this,'${Input}','${Text}')" style="cursor: pointer;">
          <td>${i.code}</td>
          <td>${i.locationCode}</td>
          <td>${i.description}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>${Head}</h1>
                  <input type="text" id="InNonReleaseSearch" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#InNonRelease').DataTable().search($('#InNonReleaseSearch').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "InNonRelease">
                      <thead>
                          <th>code</th>
                          <th>locationCode</th>
                          <th>description</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#InNonRelease").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}

function ReleaseImgSelectRow(Arg, Input, Text) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(1)").text();
  let col2 = SelectRow.find("td:eq(2)").text();
  $("#" + Input).val(col1);
  $("#" + Text).val(col2);

  $("#InNonImporterSerchId").hide();
}

function InNonReciptFocusIn() {
  var myValues = [];
  for (var i of ReceiptLocation) {
    myValues.push(i.locationCode + ":" + i.description);
  }
  Autocomplete1(myValues, "#InNonReciptInput");
}

function InNonReciptFocusOut(val) {
  if (val == "") {
    $("#InNonReciptInputText").val("");
  } else {
    for (var i of ReceiptLocation) {
      if (val.trim().toUpperCase() == (i.locationCode).trim().toUpperCase()) {
        $("#InNonReciptInputText").val(i.description);
      }
    }
  }
}

function InNonStorageFocusIn() {
  var myValues = [];
  for (var i of StorageLocation) {
    myValues.push(i.StorageCode + ":" + i.description);
  }
  Autocomplete1(myValues, "#InNonStorageInput");
}

function InNonStorageFocusOut() {
  let val = $("#InNonStorageInput").val().trim();
  if (val == "") {
    $("#InNonStorageInputText").val("");
  } else {
    for (var i of StorageLocation) {
      if (val.trim().toUpperCase() == (i.StorageCode).trim().toUpperCase()) {
        $("#InNonStorageInputText").val(i.description);
      }
    }
  }
}

function InNonLoadingPortFocusIn() {
  var myValues = [];
  for (var i of LoadingPort) {
    myValues.push(i.PortCode + ":" + i.PortName);
  }
  Autocomplete1(myValues, "#InNonLoadingPortInput");
}

function InNonLoadingPortFocusout() {
  let val = $("#InNonLoadingPortInput").val().trim().toUpperCase();
  if (val == "") {
    $("#InNonLoadingPortText").val("");
  } else {
    for (var i of LoadingPort) {
      if (val == (i.PortCode).trim().toUpperCase()) {
        $("#InNonLoadingPortText").val(i.PortName);
      }
    }
  }
}

function InNonLoadingSearchImg(Head, Table, Input, Text) {
  $("#InNonImporterSerchId").show();
  var tag = "";
  for (var i of Table) {
    tag += `
      <tr onclick="InNonLoadingSearchSelectRow(this,'${Input}','${Text}')" style="cursor: pointer;">
          <td>${i.PortCode}</td>
          <td>${i.PortName}</td>
          <td>${i.Country}</td>
        </tr>
    `;
  }
  $("#InNonImporterSerchId").html(`
        <div class="SearchPopUp">
              <div class="centerPopUp">
                  <h1>${Head}</h1>
                  <input type="text" id="LoadingSearchInputImgInNon" class="inputStyle" placeholder="Search Here By Code  " style="width: 30%;margin-top: 10px;" onkeyup="$('#LoadingSearchTable').DataTable().search($('#LoadingSearchInputImgInNon').val()).draw();">
                  <table style="margin-top: 20px;width: 100%;" id = "LoadingSearchTable">
                      <thead>
                          <th>PortCode</th>
                          <th>PortName</th>
                          <th>Country</th>
                      </thead>
                      <tbody>${tag}</tbody>
                  </table>
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
  $("#LoadingSearchTable").DataTable({
    pageLength: 5,
    ordering: false,
    dom: "rtip",
    autoWidth: false,
  });
}

function InNonLoadingSearchSelectRow(Arg, Input, Text) {
  let SelectRow = $(Arg).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  let col2 = SelectRow.find("td:eq(1)").text();
  $("#" + Input).val(col1);
  $("#" + Text).val(col2);

  $("#InNonImporterSerchId").hide();
}

function InNonDisachargePortFocusIn() {
  var myValues = [];
  for (var i of LoadingPort) {
    myValues.push(i.PortCode + ":" + i.PortName);
  }
  Autocomplete1(myValues, "#InNonDisachargeInput");
}

function InNonDisachargePortFocusOut(val) {
  if (val == "") {
    $("#InNonDisachargeText").val("");
  } else {
    for (var i of LoadingPort) {
      if (val.trim().toUpperCase() == (i.PortCode).trim().toUpperCase()) {
        $("#InNonDisachargeText").val(i.PortName);
      }
    }
  }
}

function InNonFinalDestinationCountry(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option value="${i.CountryCode}:${i.Description}">${i.CountryCode}:${i.Description}</option>`;
  }
  $("#InNonFinalDestinationSelect").html(drop);
  $("#InNonVesselNationalityDrop").html(drop);
}

function InNonOutVesselFunction(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option value="${i.Name}">${i.Name}</option>`;
  }
  $("#InNonVesselTypeDrop").html(drop);
}

function InNonLoadingNextPortFocusIn() {
  var myValues = [];
  for (var i of NextPort) {
    myValues.push(i.PortCode + ":" + i.PortName);
  }
  Autocomplete1(myValues, "#InNonNextPortInput");
}

function InNonLoadingNextPortFocusOut(val) {
  if (val == "") {
    $("#InNonNextPortText").val("");
  } else {
    for (var i of NextPort) {
      if (val.trim().toUpperCase() == (i.PortCode).trim().toUpperCase()) {
        $("#InNonNextPortText").val(i.PortName);
      }
    }
  }
}

function InNonLoadingLastPortFocusIn() {
  var myValues = [];
  for (var i of LastPort) {
    myValues.push(i.PortCode + ":" + i.PortName);
  }
  Autocomplete1(myValues, "#InNonLastPortInput");
}

function InNonLoadingLastPortFocusOut(val) {
  if (val == "") {
    $("#InNonLastPortText").val("");
  } else {
    for (var i of LastPort) {
      if (val.trim().toUpperCase() == (i.PortCode).trim().toUpperCase()) {
        $("#InNonLastPortText").val(i.PortName);
      }
    }
  }
}

function InNonSeaStoreClick() {
  if ($("#InNonSeaStoreId").prop("checked")) {
    $("#InNonSeaStoreId").val("True");
    $("#OutwardDischargePort").hide();
    $("#FinalDestinationCountryVisible").hide();
    $("#OutwardDischargePort input").val("");
    $("#FinalDestinationCountryVisible select").val("--Select--");
  } else {
    $("#InNonSeaStoreId").val("False");
    $("#OutwardDischargePort").show();
    $("#FinalDestinationCountryVisible").show();
  }
}

function CargoInHawbOut() {
  var Val = $("#CargoInHawb").val()
  var Val1= $("#MasterAirwayBill").val()

  let ht = "";
  for (var i of Val.split(",")) {
    ht += `<option>${i}</option>`;
  }
  $("#itemHawb").html(ht);
  $("#SummaryInHawbHbl").html("<p>" + Val + "</p>");
  $("#SummaryInMawbObl").html("<p>" + Val1 + "</p>");
  $("#Summarynoofpacking").html("<p>" + $("#InNonTotOuterPackInput").val() + " " + $("#InNonTotOuterPackDrop").val() + "</p>");
  $("#SummaryGrossWeight").html("<p>" + $("#CargoPermitGrossWeight").val() + " " + $("#InNonTotalGrossWeightDrop").val() + "</p>");
}

function CargoOutHawbOut() {
  let ht = "";
  var Val = $("#InNonOutHblHawbInput").val()
  for (var i of Val.split(",")) {
    ht += `<option>${i}</option>`;
  }
  $("#ItemOutHawbDrop").html(ht);
  $("#SummaryOutMawbObl").html("<p>" + Val + "</p>");
  $("#SummaryOutHawbHbl").html("<p>" + $("#OutOceanBillofLadingNo").val() + "</p>");
}

function CargoGross() {
  $("#InNonTotalGrossWeightInputSpan1").hide();
  var totalWeight = Number($("#InNonTotalGrossWeightInput").val());
  var selectedWeight = $("#InNonTotalGrossWeightDrop").val();
  if ($("#inwardTranseportMode").val() == "1 : Sea") {
    if ($("#InNonTotalGrossWeightDrop").val() != "TNE") {
      $("#InNonTotalGrossWeightInputSpan1").show();
    }
  }
  if ("TNE" == selectedWeight && totalWeight != null) {
    var total = totalWeight / 1000;
    $("#CargoPermitGrossWeight").val(total);
  } else {
    $("#CargoPermitGrossWeight").val(totalWeight);
  }
  CargoInHawbOut()
}

function CargoGrossEdit(Value, Uom) {
  if ("TNE" == Uom) {
    $("#InNonTotalGrossWeightInput").val(Number(Value * 1000));
  } else {
    $("#InNonTotalGrossWeightInput").val(Value);
  }
  CargoGross();
}


  function CargoResetInNon(){
    $("#InNonTotOuterPackInput").val("");
    $("#InNonTotOuterPackDrop").val("--Select--");
    $("#InNonTotalGrossWeightInput").val("");
    $("#InNonTotalGrossWeightDrop").val("--Select--");
    $("#CargoPermitGrossWeight").val("");
    $("#InNonReleaseInput").val("");
    $("#InNonReleaseText").val("");
    $("#InNonReciptInput").val("");
    $("#InNonReciptInputText").val("");
    $("#InNonStorageInput").val("");
    $("#InNonStorageInputText").val("");
    $("#InNonLoadingPortInput").val("");
    $("#InNonLoadingPortText").val("");
    $("#CargoInHawb").val("");
    $("#CargoInHawbOut").val("");
    $("#ArrivalDate").val("");
    $("#FlightNO").val("");
    $("#AircraftRegNo").val("");
    $("#MasterAirwayBill").val("");
    $("#VoyageNumber").val("");
    $("#VesselName").val("");
    $("#OceanBillofLadingNo").val("");
    $("#ConveyanceRefNo").val("");
    $("#TransportId").val("");
    $("#ExhibitionSDate").val("");
    $("#ExhibitionEDate").val("");
    $("#BlanketStartDate").val("");
    $("#InNonDisachargeInput").val("");
    $("#InNonDisachargeText").val("");
    $("#InNonFinalDestinationSelect").val("--Select--");
    $("#DepartureDate").val("");
    $("#InNonSeaStoreId").prop('checked',false);
    $("#InNonOutFlightNumberInput").val("");
    $("#InNonOutAirCraftInput").val("");
    $("#InNonOutMawbInput").val("");
    $("#OutVoyageNumber").val("");
    $("#InNonOutVesselNameInput").val("");
    $("#OutOceanBillofLadingNo").val("");
    $("#InNonOutHblHawbInput").val("");
    $("#InNonOutConveyanceInput").val("");
    $("#InNonVesselTypeDrop").val("--Select--");
    $("#InNonVesselNetRegisterInput").val("");
    $("#InNonVesselNationalityDrop").val("--Select--");
    $("#InNonTowingVesselIdInput").val("");
    $("#InNonTowingVesselNameInput").val("");
    $("#InNonNextPortInput").val("");
    $("#InNonNextPortText").val("");
    $("#InNonLastPortInput").val("");
    $("#InNonLastPortText").val("");
    var row = $(".SaveContainer").closest("tr");
    row.find("input:eq(2)").val(""); 
    row.find("input:eq(3)").val(""); 
    row.find("input:eq(4)").val(""); 
    row.find("select:eq(0)").val("--Select--");

  
  



  }

/*-----------------------------------INVOICE PAGE -----------------------------------------*/

var SupplyInNon;
var TermType;
var Currency;
var Vehical;
var Engine;
var Preferntial;
var Making;
$(document).ready(function () {
  $.ajax({
    url: "/InNonInvoiceLoad/",
    success: function (response) {
      console.log("Invoice Page Loading...!");
      SupplyInNon = response.supply;
      TermType = response.termType;
      Currency = response.currency;
      Vehical = response.vehical;
      Engine = response.engine;
      Preferntial = response.preferntial;
      Making = response.making;
      TermTypeLoad(TermType);
      InvoiceCurrencyLoad(Currency);
      VehicalLoad(Vehical);
      EngineLoad(Engine);
      PreferntialLoad(Preferntial);
      ItemMakingLoad(Making);
      $("#declarationType").focus()
    },
  });
});

function InNonSupplierIn() {
  var myValues = [];
  for (var i of SupplyInNon) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#SupplierCodeInNon");
}

function InNonSupplierOut(Value) {
  if (Value == "") {
    $(".InvoiceSupplierEmpty input").val("");
  } else {
    for (var i of SupplyInNon) {
      if (i.Code == Value) {
        $("#SupplierCrueiInNon").val(i.CRUEI);
        $("#SupplierNameInNon").val(i.Name);
        $("#SupplierName1InNon").val(i.Name1);
      }
    }
  }
}

function InNonInvoiceImporterIn() {
  var myValues = [];
  for (var i of InNonImporter) {
    myValues.push(i.Code + ":" + i.Name);
  }
  Autocomplete1(myValues, "#InvoiceImporterCodeInNon");
}

function InNonInvoiceImporterOut(Value) {
  if (Value == $("#InNonImporterCode").val()) {
    $("#InvoiceImporterCodeInNonSpan1").hide();
  } else {
    $("#InvoiceImporterCodeInNonSpan1").show();
  }
  if (Value == "") {
    $(".InvoiceImporterEmpty input").val("");
  } else {
    for (var i of InNonImporter) {
      if (i.Code == Value) {
        $("#InvoiceImporterCodeInNon").val(i.Code);
        $("#InvoiceImporterCrueiInNon").val(i.CRUEI);
        $("#InvoiceImporterNameInNon").val(i.Name);
        $("#InvoiceImporterName1InNon").val(i.Name1);
      }
    }
  }
}

function TermTypeLoad(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option>${i.Name}</option>`;
  }
  $("#InvoiceTermTypeInNon").html(drop);
}

function InvoiceCurrencyLoad(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option value=${i.Currency}>${i.Currency}</option>`;
  }
  $("#InvoiceCurrencyInNon").html(drop);
  $("#OtherCurrencyInNon").html(drop);
  $("#FrightCurrencyInNon").html(drop);
  $("#InsurenceCurrencyInNon").html(drop);
  $("#ItemInvoiceCurrencyDrop").html(drop);
  $("#OptionalChrgeUOM").html(drop);
}

function InvoiceTermChangeInNon(val) {
  $("#InvoiceCalculationTable input").val("0.00");
  $("#InvoiceCalculationTable select").val("--Select--");
  $("#InvoiceGstChargeInNon").val("9");
  $("#InvoiceTableInvoiceRowInNon").show();
  $("#InvoiceOtherInNon").show();
  $("#InvoiceFrightRowInNon").show();
  $("#InvoiceInsurenceRowInNon").show();
  $("#InvoiceCostInsFrightInNon").show();
  $("#InvoiceGstRowInNon").show();
  if (val == "CFR : Cost and Frieght ( also known as C & F )") {
    $("#InvoiceFrightRowInNon").hide();
    $("#InsurenceChargeInNon").val("1.00");
    $("#InsurenceCurrencyInNon").val("SGD");
    InvoiceCurrencyChange("SGD", "InsurenceExRateInNon");
  } else if (val == "CIF : Cost,Insurance and Frieght") {
    $("#InvoiceFrightRowInNon").hide();
    $("#InvoiceInsurenceRowInNon").hide();
  } else if (val == "EXW : Exw Works (also known as Ex-Factory)") {
    $("#InsurenceChargeInNon").val("1.00");
    $("#InsurenceCurrencyInNon").val("SGD");
    InvoiceCurrencyChange("SGD", "InsurenceExRateInNon");
  } else if (val == "CNI : Cost and Insurance (also Known as C & I )") {
    $("#InvoiceInsurenceRowInNon").hide();
  } else if (val == "FAS : Free Alongside Ship") {
    $("#InsurenceChargeInNon").val("1.00");
    $("#InsurenceCurrencyInNon").val("SGD");
    InvoiceCurrencyChange("SGD", "InsurenceExRateInNon");
  } else if (val == "FOB : Free On Board") {
    $("#InsurenceChargeInNon").val("1.00");
    $("#InsurenceCurrencyInNon").val("SGD");
    InvoiceCurrencyChange("SGD", "InsurenceExRateInNon");
  } else {
  }
}

function InvoiceCurrencyChange(Val, ID) {
  $("#" + ID).val("0.00");
  for (var i of Currency) {
    if (Val == i.Currency) {
      $("#" + ID).val(i.CurrencyRate);
      break;
    }
  }
  if (ID == "InvoiceExRateInNon") {
    InvoiceValueAmountCalculation();
  }
  if (ID == "OtherExRateInNon") {
    OtherChargesInNonCalculation();
  }
  if (ID == "FrightExRateInNon") {
    FrighChargeInNonCalculation();
  }
  if (ID == "InsurenceExRateInNon") {
    InsurenceChargeInNonCalculation();
  }
}

function InvoiceValueAmountCalculation() {
  let InvAmount = Number($("#InvoiceAmountInNon").val());
  let CurrencyVal = Number($("#InvoiceExRateInNon").val());
  if (InvAmount != "") {
    $("#InvoiceSumAmountInNon").val((InvAmount * CurrencyVal).toFixed(2));
  } else {
    $("#InvoiceSumAmountInNon").val("0.00");
  }
  TotalInvoiceCalculation();
}

function TotalInvoiceCalculation() {
  let InvSumAmount = Number($("#InvoiceSumAmountInNon").val());
  let OtherSumAmount = Number($("#OtherSumAmountInNon").val());
  let FrieghtSumAmount = Number($("#FrightSumAmountInNon").val());
  let InsurenceSumAmount = Number($("#InsurenceSumAmountInNon").val());

  $("#CostInsurenceFreightSumInNon").val(
    (
      InvSumAmount +
      OtherSumAmount +
      FrieghtSumAmount +
      InsurenceSumAmount
    ).toFixed(2)
  );

  let Tot = $("#CostInsurenceFreightSumInNon").val();
  let GstPer = $("#InvoiceGstChargeInNon").val();

  let Result = ((Tot * GstPer) / 100).toFixed(2);
  $("#InvoiceGstSumInNon").val(Number(Result).toFixed(2));
}

function OtherChargesInNonCalculation() {
  let OtherCharge = $("#OtherChargesInNon").val();
  let OtherCurrency = $("#OtherCurrencyInNon").val();
  let InvoiceTot = $("#InvoiceSumAmountInNon").val();
  let OtherExRate = $("#OtherExRateInNon").val();

  if (OtherCharge != "" && parseInt(OtherCharge) > 0) {
    if (OtherCurrency != "--Select--") {
      $("#OtherSumAmountInNon").val(((InvoiceTot * OtherCharge) / 100).toFixed(2)
      );
      let OtherSum = $("#OtherSumAmountInNon").val();
      $("#OtherAmountInNon").val((OtherSum / OtherExRate).toFixed(4));
    }
    else {
      $("#OtherSumAmountInNon").val(((InvoiceTot * OtherCharge) / 100).toFixed(2));
    }
  }
  // else if (OtherCharge == "0.00" ){
  //   $("#OtherSumAmountInNon").val("0.00");
  //   $("#OtherAmountInNon").val("0.00");
  // }
  TotalInvoiceCalculation();
  SumOfInsurence();
}

function OtherAmountInNonCalculation() {
  let OtherAmount = $("#OtherAmountInNon").val();
  let OtherExRate = $("#OtherExRateInNon").val();
  if (OtherAmount != "") {
    $("#OtherSumAmountInNon").val((OtherAmount * OtherExRate).toFixed(2));
  } else {
    $("#OtherSumAmountInNon").val("0.00");
  }
  SumOfInsurence();
  let InvoiceSumAmount = Number($("#InvoiceSumAmountInNon").val());
  let OtherSumAmount = Number($("#OtherSumAmountInNon").val());

  $("#CostInsurenceFreightSumInNon").val(
    (InvoiceSumAmount + OtherSumAmount).toFixed(2)
  );

  let GstAmd = Number($("#CostInsurenceFreightSumInNon").val());
  let GstPer = Number($("#InvoiceGstChargeInNon").val());
  $("#InvoiceGstSumInNon").val(((GstAmd * GstPer) / 100).toFixed(2));
}

function SumOfInsurence() {
  let InvSumAmount = Number($("#InvoiceSumAmountInNon").val());
  let FrightSumAmount = Number($("#FrightSumAmountInNon").val());
  let InsurenceCharge = Number($("#InsurenceChargeInNon").val());
  let InsurenceExrate = Number($("#InsurenceExRateInNon").val());

  let Tot = InvSumAmount + FrightSumAmount;

  if (InsurenceCharge > 0) {
    $("#InsurenceSumAmountInNon").val(((InsurenceCharge * Tot) / 100).toFixed(2));
    $("#InsurenceAmountInNon").val(((InsurenceCharge * Tot) / 100).toFixed(2));
    console.log("InsurenceAmountInNon:",$("#InsurenceAmountInNon").val())
  }
}

function FrighChargeInNonCalculation() {
  let FrighCharge = Number($("#FrighChargeInNon").val());
  let FrightCurrency = $("#FrightCurrencyInNon").val();
  let InvSumAmount = Number($("#InvoiceSumAmountInNon").val());
  let FrightExRate = Number($("#FrightExRateInNon").val());

  if (FrighCharge != "") {
    if (FrightCurrency != "--Select--") {
      let tot = (InvSumAmount * FrighCharge) / 100;
      $("#FrightSumAmountInNon").val(tot.toFixed(2));
      $("#FrightAmountInNon").val((tot / FrightExRate).toFixed(4));
    } else {
      let tot = (InvSumAmount * FrighCharge) / 100;
      $("#FrightSumAmountInNon").val(tot.toFixed(2));
    }
  } else {
    $("#FrighChargeInNon").val("0.00");
  }
  SumOfInsurence();
  if (Number($("#InsurenceExRateInNon").val()) > 0) {
    $("#InsurenceAmountInNon").val(
      Number($("#InsurenceSumAmountInNon").val() / $("#InsurenceExRateInNon").val()).toFixed(2)
    );
  } else {
    $("#InsurenceAmountInNon").val("0.00");
  }
  TotalInvoiceCalculation();
}

function FrightAmountInNonCalculation() {
  let FrightExRate = Number($("#FrightExRateInNon").val());
  let FrightAmount = Number($("#FrightAmountInNon").val());

  if ($("#FrightAmountInNon").val() != "") {
    $("#FrightSumAmountInNon").val((FrightExRate * FrightAmount).toFixed(2));
  } else {
    $("#FrightSumAmountInNon").val("0.00");
  }
  SumOfInsurence();
  let InvSumAmount = Number($("#InvoiceSumAmountInNon").val());
  let InsurenceSumAmount = Number($("#InsurenceSumAmountInNon").val());
  let FrightSumAmount = Number($("#FrightSumAmountInNon").val());

  $("#CostInsurenceFreightSumInNon").val(
    (InvSumAmount + InsurenceSumAmount + FrightSumAmount).toFixed(2)
  );

  let Gst = $("#CostInsurenceFreightSumInNon").val();
  let GstPer = $("#InvoiceGstChargeInNon").val();
  $("#InvoiceGstSumInNon").val(((Gst * GstPer) / 100).toFixed(2));

  let Inv = Number($("#InvoiceSumAmountInNon").val());
  let OTC = Number($("#OtherSumAmountInNon").val());
  let FC = Number($("#FrightSumAmountInNon").val());

  if ($("#InsurenceChargeInNon").val() > 0) {
    let INSC = (Inv + FC) / 100;
    $("#InsurenceAmountInNon").val(Number(INSC).toFixed(2));
  }
  TotalInvoiceCalculation();
}

function InsurenceChargeInNonCalculation() {
  if (
    $("#InsurenceChargeInNon").val() != "" &&
    $("#InsurenceChargeInNon").val() != "0.00" &&
    $("#InvoiceSumAmountInNon").val() != ""
  ) {
    let InvoiceSumAmount = Number($("#InvoiceSumAmountInNon").val());
    let InsurenceCharge = Number($("#InsurenceChargeInNon").val());

    if (InsurenceCharge > 0) {
      let Tis = (InvoiceSumAmount * InsurenceCharge) / 100;
      $("#InsurenceAmountInNon").val(Tis.toFixed(2));
      let tot = InvoiceSumAmount + Number($("#FrightSumAmountInNon").val());
      $("#InsurenceSumAmountInNon").val(Number(((tot * InsurenceCharge) / 100)).toFixed(2));
    }
  } else {
    $("#InsurenceSumAmountInNon").val("0.00");
  }
  SumOfInsurence();
  TotalInvoiceCalculation();
}

function InsurenceAmountInNonCalculation() {
  let InsurenceAmount = Number($("#InsurenceAmountInNon").val());
  let InsurenceExRate = Number($("#InsurenceExRateInNon").val());
  if (InsurenceExRate != "") {
    $("#InsurenceSumAmountInNon").val(Number((InsurenceExRate * InsurenceAmount)).toFixed(2));
  } else {
    $("#InsurenceSumAmountInNon").val("0.00");
  }
  SumOfInsurence();
  TotalInvoiceCalculation();

  if ($("#InsurenceCurrencyInNon").val() != "SGD") {
    InsurenceAmount = Number($("#InsurenceAmountInNon").val());
    InsurenceExRate = Number($("#InsurenceExRateInNon").val());
    let val1 = "0.00";
    if (InsurenceExRate > 0) {
      val1 = InsurenceAmount / InsurenceExRate;
    }
    $("#InsurenceAmountInNon").val(Number(val1).toFixed(2));
  }
}

function DateTimeCalculation() {
  let today = new Date();
  let day = today.getDate().toString().padStart(2, "0");
  let month = (today.getMonth() + 1).toString().padStart(2, "0");
  let year = today.getFullYear().toString();
  let formattedDate = `${day}/${month}/${year}`;
  return formattedDate;
}

$(function () {
  $("#InvoiceDateInNon").datepicker({ dateFormat: "dd/mm/yy" });

  $("#OriginalRegistrationDate").datepicker({ dateFormat: "dd/mm/yy" });

  $("#SummaryMRD").datepicker({ dateFormat: "dd/mm/yy" });

  $("#ArrivalDate").datepicker({ dateFormat: "dd/mm/yy" });

  $("#ExhibitionSDate").datepicker({ dateFormat: "dd/mm/yy" });

  $("#ExhibitionEDate").datepicker({ dateFormat: "dd/mm/yy" });

  $("#BlanketStartDate").datepicker({ dateFormat: "dd/mm/yy" });

  $("#DepartureDate").datepicker({ dateFormat: "dd/mm/yy" });

  $("#InvoiceDateInNon").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#InvoiceDateInNon").val(currentDate);
    }
  });

  $("#OriginalRegistrationDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#OriginalRegistrationDate").val(currentDate);
    }
  });

  $("#SummaryMRD").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#SummaryMRD").val(currentDate);
    }
  });

  $("#ArrivalDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#ArrivalDate").val(currentDate);
    }
  });

  $("#ExhibitionSDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#ExhibitionSDate").val(currentDate);
    }
  });

  $("#ExhibitionEDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#ExhibitionEDate").val(currentDate);
    }
  });

  $("#BlanketStartDate").keydown(function (event) {
    if (event.keyCode == 32) {
      // spacebar keycode
      event.preventDefault();
      var currentDate = $.datepicker.formatDate("dd/mm/yy", new Date());
      $("#BlanketStartDate").val(currentDate);
    }
  });

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

/*-----------------------------------INVOICE SAVE PAGE -----------------------------------------*/

function InNonSupplierSave() {
  $("#SupplierCodeInNonSpan").hide();
  $("#SupplierCrueiInNonSpan").hide();
  $("#SupplierNameInNonSpan").hide();
  let code = $("#SupplierCodeInNon").val();
  let cruei = $("#SupplierCrueiInNon").val();
  let name = $("#SupplierNameInNon").val();
  let name1 = $("#SupplierName1InNon").val();
  let check = true;
  if (code == "") {
    check = false;
    $("#SupplierCodeInNonSpan").show();
  }
  if (cruei == "") {
    check = false;
    $("#SupplierCrueiInNonSpan").show();
  }
  if (name == "") {
    check = false;
    $("#SupplierNameInNonSpan").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonInvoiceLoad/",
      type: "POST",
      data: {
        MODEL: "SUPPLIER",
        Code: code.trim(),
        CRUEI: cruei.trim(),
        Name: name.trim(),
        Name1: name1.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        SupplyInNon = response.supply;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function InNonInvoiceImporterSave() {
  $("#InvoiceImporterCodeInNonSpan2").hide();
  $("#InvoiceImporterCrueiInNonSpan").hide();
  $("#InvoiceImporterNameInNonSpan").hide();
  let code = $("#InvoiceImporterCodeInNon").val();
  let cruei = $("#InvoiceImporterCrueiInNon").val();
  let name = $("#InvoiceImporterNameInNon").val();
  let name1 = $("#InvoiceImporterName1InNon").val();
  let check = true;
  if (code == "") {
    check = false;
    $("#InvoiceImporterCodeInNonSpan2").show();
  }
  if (cruei == "") {
    check = false;
    $("#InvoiceImporterCrueiInNonSpan").show();
  }
  if (name == "") {
    check = false;
    $("#InvoiceImporterNameInNonSpan").show();
  }

  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonPartyLoad/",
      type: "POST",
      data: {
        MODEL: "IMPORTER",
        Code: code.trim(),
        CRUEI: cruei.trim(),
        Name: name.trim(),
        Name1: name1.trim(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        InNonImporter = response.Importer;
        alert(response.Result);
        $("#Loading").hide();
      },
    });
  }
}

function InvoiceResetInNon() {
  $("#Invoice span").hide();
  $("#Invoice input").val("");
  $("#Invoice select").val("--Select--");
  InvoiceTermChangeInNon("--Select--");
  $("#InvoiceCalculationTable input").val("0.00");
  $("#InvoiceGstChargeInNon").val("9");
  $("#Invoice input").prop("checked", false);
  $("#InvoiceAdValInNon").val("False");
  $("#InvoicePreferentialInNon").val("False");
  $("#InvoiceSerialInNon").val((Number(InvoiceData.length) + 1).toString().padStart(3, "0")
  );
  InNonInvoiceImporterOut($("#InNonImporterCode").val());
}

function InvoiceSaveInNon() {
  $("#Invoice span").hide();
  var check = true;

  if ($("#InvoiceImporterCodeInNon").val() != $("#InNonImporterCode").val()) {
    check = false;
    $("#InvoiceImporterCodeInNonSpan1").show();
  }

  if ($("#InvoiceImporterCrueiInNon").val() == "") {
    check = false;
    $("#InvoiceImporterCrueiInNonSpan").show();
  }

  if ($("#InvoiceImporterNameInNon").val() == "") {
    check = false;
    $("#InvoiceImporterNameInNonSpan").show();
  }

  if ($("#InvoiceDateInNon").val() == "") {
    check = false;
    $("#InvoiceDateInNonSpan").show();
  }

  if ($("#InvoiceNumber").val() == "") {
    check = false;
    $("#InvoiceNumberSpan").show();
  }

  if ($("#InvoiceCurrencyInNon").val() == "--Select--") {
    check = false;
    $("#InvoiceCurrencyInNonSpan").show();
  }
  if (check) {
    $("#Loading").show();
    var InvoiceDate = $("#InvoiceDateInNon").val().split("/");
    InvoiceDate = `${InvoiceDate[2]}/${InvoiceDate[1]}/${InvoiceDate[0]}`;

    $.ajax({
      url: "/InNonInvoiceLoad/",
      type: "POST",
      data: {
        MODEL: "INVOICE",
        SNo: $("#InvoiceSerialInNon").val(),
        InvoiceNo: $("#InvoiceNumber").val(),
        InvoiceDate: InvoiceDate,
        TermType: $("#InvoiceTermTypeInNon").val(),
        AdValoremIndicator: $("#InvoiceAdValInNon").val(),
        PreDutyRateIndicator: $("#InvoicePreferentialInNon").val(),
        SupplierImporterRelationship: $("#InvoiceRelationShip").val(),
        SupplierCode: $("#SupplierCodeInNon").val(),
        ImportPartyCode: $("#InvoiceImporterCodeInNon").val(),
        TICurrency: $("#InvoiceCurrencyInNon").val(),
        TIExRate: $("#InvoiceExRateInNon").val(),
        TIAmount: $("#InvoiceAmountInNon").val(),
        TISAmount: $("#InvoiceSumAmountInNon").val(),
        OTCCharge: $("#OtherChargesInNon").val(),
        OTCCurrency: $("#OtherCurrencyInNon").val(),
        OTCExRate: $("#OtherExRateInNon").val(),
        OTCAmount: $("#OtherAmountInNon").val(),
        OTCSAmount: $("#OtherSumAmountInNon").val(),
        FCCharge: $("#FrighChargeInNon").val(),
        FCCurrency: $("#FrightCurrencyInNon").val(),
        FCExRate: $("#FrightExRateInNon").val(),
        FCAmount: $("#FrightAmountInNon").val(),
        FCSAmount: $("#FrightSumAmountInNon").val(),
        ICCharge: $("#InsurenceChargeInNon").val(),
        ICCurrency: $("#InsurenceCurrencyInNon").val(),
        ICExRate: $("#InsurenceExRateInNon").val(),
        ICAmount: $("#InsurenceAmountInNon").val(),
        ICSAmount: $("#InsurenceSumAmountInNon").val(),
        CIFSUMAmount: $("#CostInsurenceFreightSumInNon").val(),
        GSTPercentage: $("#InvoiceGstChargeInNon").val(),
        GSTSUMAmount: $("#InvoiceGstSumInNon").val(),
        MessageType: $("#MsgType").val(),
        PermitId: $("#PermitIDInNon").val(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        $("#Loading").hide();
        InvoiceResetInNon();
        InvoiceData = response.invoice;
        InvoiceLoadInNon();
        alert(response.Result);
        $('[tabindex="24"]').focus();
      },
    });
  }
}

function formatDate(inputDate) {
  const [year, month, day] = inputDate.split("-");
  const formattedDate = `${day}/${month}/${year}`;
  return formattedDate;
}

function InvoiceLoadInNon() {
  let InvoiceCurrAmd = [];
  let CifSum = 0;
  let InvoiceGst= 0;
  $("#InvoiceSerialInNon").val((Number(InvoiceData.length) + 1).toString().padStart(3, "0")
  );
  $("#summaryNoOfVoice").val(
    Number(InvoiceData.length).toString().padStart(3)
  );
  let ItemNumberDrop = "<option selected>--Select--</option>";
  if (InvoiceData.length > 0) {
    let Tab = "";
    for (var i of InvoiceData) {
      Tab += ` 
        <tr>
          <td><i class="fa-solid fa-trash" style="color: #ff0000;" onclick = "InvoiceDeleteInNon('${i.SNo
        }')"></i></td>
          <td><i class="fa-regular fa-pen-to-square" style="color: #ff0000;" onclick = "InvoiceEditInNon('${i.SNo
        }')"></i></td>
          <td>${Number(i.SNo).toString().padStart(3, "0")}</td> 
          <td>${i.InvoiceNo}</td>
          <td>${formatDate(i.InvoiceDate)}</td>
          <td>${i.TermType}</td>
          <td>${i.TICurrency}</td>
          <td>${i.TIAmount}</td>
          <td>${i.CIFSUMAmount}</td>
          <td>${i.GSTSUMAmount}</td>
      </tr>
      `;
      InvoiceCurrAmd.push([i.TICurrency, Number(i.TIAmount)]);
      CifSum += Number(i.CIFSUMAmount);
      InvoiceGst += Number(i.GSTSUMAmount)
      ItemNumberDrop += `<option>${i.InvoiceNo}</option>`;
      
     
    }
    $("#summaryTotalInvoiceCIFValue").val(CifSum);
    $("#InvoiceTableInNon tbody").html(Tab);
    $("#SummaryTotalIncoiseGSt").html(InvoiceGst);
    console.log("SummaryTotalIncoiseGSt:",$("#SummaryTotalIncoiseGSt").val())

   
    SummaryInvoiceSumofInvoiceAmount(InvoiceCurrAmd)
  } else {
    $("#summaryTotalInvoiceCIFValue").val("0.00");
    $("#SummaryTotalIncoiseGSt").val("");
    $("#InvoiceTableInNon tbody").html(
      "<tr> <td colspan=10 style='text-align:center'>No Record</td></tr>"
    );
  }
  $("#ItemInvoiceNumberInNon").html(ItemNumberDrop);


  var SInvoice = (document.getElementsByName('summarySumOfInvoiceAmount')[0].value).split('.');
  var SItem = (document.getElementsByName('summarySumOfItemAmout')[0].value).split('.');
  if ((SInvoice[0] == SItem[0]) || $('#summaryTotalInvoiceCIFValue').val() == $('#summaryTotalCIFFOBValue').val()) {
    $('#SUmmaryEqualNot').hide();
  }
  else {
    $('#SUmmaryEqualNot').show();
  }
  
}

function CopyImporterInvoice() {
  $('#InvoiceImporterCodeInNon').val($('#InNonImporterCode').val())
  InNonInvoiceImporterOut($('#InNonImporterCode').val())
}
function InvoiceEditInNon(SNO) {
  for (var Inv of InvoiceData) {
    if (Inv.SNo == SNO) {
      InvoiceResetInNon();
      $("#InvoiceSerialInNon").val(Number(Inv.SNo).toString().padStart(3, "0"));
      $("#InvoiceNumber").val(Inv.InvoiceNo);
      $("#InvoiceTermTypeInNon").val(Inv.TermType);
      InvoiceTermChangeInNon(Inv.TermType);
      $("#InvoiceAdValInNon").val(Inv.AdValoremIndicator);
      if (
        Inv.AdValoremIndicator == "True" ||
        Inv.AdValoremIndicator == "true"
      ) {
        $("#InvoiceAdValInNon").prop("checked", true);
      }
      $("#InvoicePreferentialInNon").val(Inv.PreDutyRateIndicator);
      if (
        Inv.PreDutyRateIndicator == "True" ||
        Inv.PreDutyRateIndicator == "true"
      ) {
        $("#InvoicePreferentialInNon").prop("checked", true);
      }
      $("#InvoiceRelationShip").val(Inv.SupplierImporterRelationship);
      $("#SupplierCodeInNon").val(Inv.SupplierCode);
      InNonSupplierOut(Inv.SupplierCode);
      $("#InvoiceImporterCodeInNon").val(Inv.ImportPartyCode);
      InNonInvoiceImporterOut(Inv.ImportPartyCode);
      $("#InvoiceCurrencyInNon").val(Inv.TICurrency);
      $("#InvoiceExRateInNon").val(Inv.TIExRate);
      $("#InvoiceAmountInNon").val(Inv.TIAmount);
      $("#InvoiceSumAmountInNon").val(Inv.TISAmount);
      $("#OtherChargesInNon").val(Inv.OTCCharge);
      $("#OtherCurrencyInNon").val(Inv.OTCCurrency);
      $("#OtherExRateInNon").val(Inv.OTCExRate);
      $("#OtherAmountInNon").val(Inv.OTCAmount);
      $("#OtherSumAmountInNon").val(Inv.OTCSAmount);
      $("#FrighChargeInNon").val(Inv.FCCharge);
      $("#FrightCurrencyInNon").val(Inv.FCCurrency);
      $("#FrightExRateInNon").val(Inv.FCExRate);
      $("#FrightAmountInNon").val(Inv.FCAmount);
      $("#FrightSumAmountInNon").val(Inv.FCSAmount);
      $("#InsurenceChargeInNon").val(Inv.ICCharge);
      $("#InsurenceCurrencyInNon").val(Inv.ICCurrency);
      $("#InsurenceExRateInNon").val(Inv.ICExRate);
      $("#InsurenceAmountInNon").val(Inv.ICAmount);
      $("#InsurenceSumAmountInNon").val(Inv.ICSAmount);
      $("#CostInsurenceFreightSumInNon").val(Inv.CIFSUMAmount);
      $("#InvoiceGstChargeInNon").val(Inv.GSTPercentage);
      $("#InvoiceGstSumInNon").val(Inv.GSTSUMAmount);
      $("#InvoiceDateInNon").val(formatDate(Inv.InvoiceDate));
      break;
    }
  }
}

function InvoiceDeleteInNon(SNO) {
  $("#Loading").show();
  $.ajax({
    url: "/InNonInvoiceLoad/",
    type: "POST",
    data: {
      MODEL: "DELETE",
      SNo: SNO,
      PermitId: $("#PermitIDInNon").val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      $("#Loading").hide();
      InvoiceData = response.invoice;
      InvoiceLoadInNon();
    },
  });
}

/*--------------------------------------ITEM PAGE LOAD-----------------------------------------*/
var InhouseItemCode = [];
var HsCode = [];
var ChkHsCode = [];
var HsCodeLoading = [];
$(document).ready(function () {
  $.ajax({
    url: "/InNonItemLoad/",
    data: {
      PermitId: $("#PermitIDInNon").val(),
    },
    success: function (response) {
      console.log("Item Page Loaded ...!");
      InhouseItemCode = response.inhouseItemCode;
      HsCode = response.hsCode;
      ChkHsCode = response.chkHsCode;
      ItemLoad()
      console.log(HsCode)
      for (var i of HsCode) {
        HsCodeLoading.push(i.HSCode + ":" + i.Description);
      }
      $('#HsCodeLoadingId').hide()
      document.getElementById('ItemHsCodeInNon').addEventListener('input', function () {
        Autocomplete1(HsCodeLoading, "#ItemHsCodeInNon");
      })
    },
  });
});

function ItemMakingLoad(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option>${i.Name}</option>`;
  }
  $("#Making").html(drop);
}

function ItemItemCodeInNonIn() {
  var myValues = [];
  for (var i of InhouseItemCode) {
    myValues.push(i.InhouseCode + ":" + i.HSCode);
  }
  Autocomplete1(myValues, "#ItemItemCodeInNon");
}

function ItemItemCodeInNonOut(val) {
  if (val == "") {
    $("#ItemHsCodeInNon").val("");
    $("#ItemDescriptionInNon").val("");
  } else {
    for (var i of InhouseItemCode) {
      if (val == i.InhouseCode) {
        $("#ItemHsCodeInNon").val(i.HSCode);
        $("#ItemDescriptionInNon").val(i.Description);
        //$("#ItemHsCodeInNon").val(i.HSCode)
      }
    }
  }
}

function ItemHscodeFocusIn() {
  // Autocomplete1(HsCodeLoading, "#ItemHsCodeInNon");
}

// document.getElementById('ItemHsCodeInNon').addEventListener('input', function () {
//   Autocomplete1(HsCodeLoading, "#ItemHsCodeInNon");

// })

function ItemInNonDelHblHawb() {
  $("#Loading").show();
  $.ajax({
    url: "/InNonDelHblHawb/" + $("#PermitIDInNon").val() + "/",
    success: function (response) {
      ItemResetInNon();
      ItemData = response.item;
      ItemLoad();
      $("#Loading").hide();
    }
  })
}
function ItemHscodeFocusOut() {
  let HsVal = $('#ItemHsCodeInNon').val().trim()
  $("#ControlledItemInNon").hide();
  if (HsVal != "") {
    if (HsVal.startsWith("87")) {
      for (var chk of ChkHsCode) {
        if (chk.HSCode == HsVal) {
          $("#VehicalTypeShow").show();
          $("#EngineCapacityShow").show();
          $("#OriginalShow").show();
          $("#OptimalCharges").show();
        }
      }
    } else {
      $("#VehicalTypeShow").hide();
      $("#VehicalTypeShow select").val("--Select--");
      $("#EngineCapacityShow").hide();
      $("#OriginalShow").hide();
      $("#EngineCapacityShow input").val("0.00");
      $("#EngineCapacityShow select").val("--Select--");
      $("#OriginalShow").val("");
      $("#OptimalCharges").hide();
      $("#OptimalCharges select").val("--Select--");
      $("#OptimalCharges input").val("0.00");
    }
    let typeid = 0; 
    for (var Hs of HsCode) {
      if (Hs.HSCode == HsVal) {
        let UOm = Hs.UOM;
        typeid = Hs.DUTYTYPID;
        if ($("#ItemDescriptionInNon").val() == "" || $('#ItemItemCodeInNon') != "") {
          $("#ItemDescriptionInNon").val(Hs.Description);
        }
        $("#ItemHsQtyUom").val(UOm);
        let uom = Hs.DuitableUom;
        let exuom = Hs.Excisedutyuom;
        let exrate = Hs.Excisedutyrate;
        let crate = Hs.Customsdutyrate;
        let cuom = Hs.Customsdutyuom;
        if (Hs.InnonPayment == "1") {
          // $('#packing_details').prop('checked', true)
          $('#itemCascID').prop('checked', true)
          // ItemCascShowAll('#packing_details', '.PackingDetails')
          ItemCascShowAll('#itemCascID', '.OutItemCascHide')
          if (Hs.HSCode == "85165000") {
            $("#ControlledItemInNon").hide();
          } else {
            if ("" == "CNB") {
              //Hs.ImpControll
              $("#ControlledItemInNon").show();
              $("#ControlledItemInNon").html("CNB CONTROLLED ITEM");
            } else {
              $("#ControlledItemInNon").show();
              $("#ControlledItemInNon").html("CONTROLLED ITEM");
            }
          }
        }
        else {
          $('#packing_details').prop('checked', false)
          $('#itemCascID').prop('checked', false)
          ItemCascShowAll('#packing_details', '.PackingDetails')
          ItemCascShowAll('#itemCascID', '.OutItemCascHide')
        }
        if (exuom == "0") {
          exuom = "--Select--";
        }
        if (cuom == "0") {
          cuom = "--Select--";
        }
        if (typeid == 62 || typeid == 63) {
          if (
            (typeid == 62 && UOm == "LTR") ||
            (typeid == 62 && UOm != "LTR")
          ) {
            $("#itemDutiableQtyNone").show();
            $("#itemAlchoholNone").hide();
          } else {
            $("#itemDutiableQtyNone").show();
            $("#itemAlchoholNone").show();
          }
          $("#TxtExciseDutyRate").val(exrate);
          $("#TxtExciseDutyUOM").val(exuom);
          $("#TxtCustomsDutyRate").val(crate);
          $("#TxtCustomsDutyUOM").val(cuom);
          if (uom == "A") {
            $("#ItemDutiableUom").val("--Select--");
            $("#ItemTotalDutiableQtyUom").val("--Select--");
          } else {
            $("#ItemDutiableUom").val(uom);
            $("#ItemTotalDutiableQtyUom").val(uom);
          }
        } else if (typeid == 64) {
          if (UOm != "LTR") {
            $("#itemDutiableQtyNone").show();
            $("#itemAlchoholNone").hide();
          } else {
            $("#itemDutiableQtyNone").show();
            $("#itemAlchoholNone").show();
          }
          $("#TxtExciseDutyRate").val(exrate);
          $("#TxtExciseDutyUOM").val(exuom);
          $("#TxtCustomsDutyRate").val(crate);
          $("#TxtCustomsDutyUOM").val(cuom);
          if (uom == "A") {
            $("#ItemDutiableUom").val("--Select--");
            $("#ItemTotalDutiableQtyUom").val("--Select--");
          } else {
            $("#ItemDutiableUom").val(uom);
            $("#ItemTotalDutiableQtyUom").val(uom);
          }
        } else if (
          (typeid == 61 || typeid == 67) &&
          (UOm == "LTR" || UOm == "KGM")
        ) {
          $("#itemDutiableQtyNone").show();
          $("#itemAlchoholNone").show();
          $("#TxtExciseDutyRate").val(exrate);
          $("#TxtExciseDutyUOM").val(exuom);
          $("#TxtCustomsDutyRate").val(crate);
          $("#TxtCustomsDutyUOM").val(cuom);
          if (uom == "A") {
            $("#ItemDutiableUom").val("--Select--");
            $("#ItemTotalDutiableQtyUom").val("--Select--");
          } else {
            $("#ItemDutiableUom").val(uom);
            $("#ItemTotalDutiableQtyUom").val(uom);
          }
        } else {
          $("#itemDutiableQtyNone").hide();
          $("#itemAlchoholNone").hide();
          $("#TxtExciseDutyRate").val(exrate);
          $("#TxtCustomsDutyRate").val(crate);
          $("#ItemTotalDutiableQtyInput").val("0.00");
          $("#ItemDutiableUom").val("--Select--");
          $("#itemAlchoholPer").val("0.00");
        }
        if (
          HsVal == "24031100" ||
          HsVal == "24039930" ||
          HsVal == "24039940" ||
          HsVal == "24039950" ||
          HsVal == "24039990" ||
          HsVal == "33021020"
        ) {
          $("#itemAlchoholNone").hide();
          $("#itemAlchoholPer").val("0.00");
        }
      }
    }
  } else {
    $("#ItemDescriptionInNon").val("");
  }
}


function ItemCodeSave(){
  console.log('hello')
  $('#Loading').show();
  $("#ItemItemCodeInNonSpan").hide()
  $("#ItemHsCodeInNonSpan").hide()
  $("#ItemDescriptionInNonSpan").hide()
  if (($('#ItemHsCodeInNon').val() != "") && ($('#ItemDescriptionInNon').val() != "") && ($("#ItemItemCodeInNon").val()!="")){
    console.log('hai')
    $.ajax({
      type: "POST",
      url: "/ItemCodeSave/",
      data: {
          ModelName: 'InNonhouseItemCodeModel',
          InhouseCode: $("#ItemItemCodeInNon").val(),
          Hscode: $("#ItemHsCodeInNon").val(),
          Description: $("#ItemDescriptionInNon").val(),
          Brand: $("#itemBrandInput").val(),
          Model: $("#itemModel").val(),
          DgIndicator: $("#itemDgIndicator").val(),
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
  if ($('#ItemHsCodeInNon').val() == "") {
      $("#ItemHsCodeInNonSpan").show()
  }
  if ($('#ItemDescriptionInNon').val() == "") {
      $("#ItemDescriptionInNonSpan").show()
  }
  if ($('#ItemItemCodeInNon').val() == "") {
      $("#ItemItemCodeInNonSpan").show()
  }
}
}

// function ItemCodeSave() {
//   $('#Loading').show();
//   $("#ItemItemCodeInNonSpan").hide()
//   $("#ItemHsCodeInNonSpan").hide()
//   $("#ItemDescriptionInNonSpan").hide()
//   if (($('#ItemHsCodeInNon').val() != "") && ($('#ItemDescriptionInNon').val() != "") && ($("#ItemItemCodeInNon").val() != "")) {
//       $.ajax({
//           type: "POST",
//           url: "/InNonPartyLoad/",
//           data: {
//               ModelName: 'InNonhouseItemCodeModel',
//               InhouseCode: $("#ItemItemCodeInNon").val(),
//               Hscode: $("#ItemHsCodeInNon").val(),
//               Description: $("#ItemDescriptionInNon").val(),
//               Brand: $("#itemBrandInput").val(),
//               Model: $("#itemModel").val(),
//               DgIndicator: $("#itemDgIndicator").val(),
//               TouchUser: $("#INONUSERNAME").val().toUpperCase(),
//               TouchTime: TOUCHTIME,
//               csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
//           },
//           success: function (data) {
//             if (data.Result) {
//                 alert(data.Result);
//                 console.log("ans:", data.Result);
//             }
//             if (data.ItemCodeSave) {
//                 console.log("ItemCodeSave values:", data.ItemCodeSave);
//                 // Process item data as needed
//             }
//             $('#Loading').hide();
//         },
//         error: function (xhr, status, error) {
//             console.log('An error occurred during the request:', error);
//             $('#Loading').hide();
//         }
        
//       });
//   } else {
//       if ($('#ItemHsCodeInNon').val() == "") {
//           $("#ItemHsCodeInNonSpan").show()
//       }
//       if ($('#ItemDescriptionInNon').val() == "") {
//           $("#ItemDescriptionInNonSpan").show()
//       }
//       if ($('#ItemItemCodeInNon').val() == "") {
//           $("#ItemItemCodeInNonSpan").show()
//       }
//   }
// }



function ItemCooIn() {
  var myValues = [];
  for (var i of Country) {
    myValues.push(i.CountryCode + ":" + i.Description);
  }
  Autocomplete1(myValues, "#ItemCooInput");
}

function ItemCooOut(Val) {
  for (var i of Country) {
    if ((i.CountryCode).trim().toUpperCase() == Val.trim().toUpperCase()) {
      $("#ItemCooInputText").val(i.Description);
      break;
    }
  }
}

function VehicalLoad(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option>${i.Name}</option>`;
  }
  $("#VehicalTypeUom").html(drop);
}

function EngineLoad(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option>${i.Name}</option>`;
  }
  $("#EngineCapacityUom").html(drop);
}

function duticalc(op, ip, inp, imp, totduti) {
  let pckqty = 1;
  let HsVal = $("#ItemHsCodeInNon").val();
  let typeidval = 0;
  let kgmvis;
  for (var Hs of HsCode) {
    if (Hs.HSCode == HsVal) {
      kgmvis = Hs.Kgmvisible;
      typeidval = Hs.DUTYTYPID;
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
    let T1 = Number($("#TxtExciseDutyRate").val());
    let T2 = Number($("#iteminvoiceCIFFOB").val());
    let T3;
    let T4;
    let gstperval = Number($("#ItemGSTRate").val()) / 100;
    let TDQUOM = $("#ItemDutiableUom").val();
    if (TDQUOM == "LTR") {
      $("#ItemTotalDutiableQtyInput").val(pckqty * totduti);
      $("#ItemHsQtyInput").val(pckqty * totduti);
    } else if (TDQUOM == "KGM" && kgmvis == "MULTIPLE") {
      $("#ItemTotalDutiableQtyInput").val(pckqty * totduti);
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(pckqty * totduti * T1);
      }

      T3 = Number($("#iteminvoiceCIFFOB").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "KGM" && kgmvis == "DIVIDE") {
      $("#ItemTotalDutiableQtyInput").val((pckqty * totduti) / 1000);
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(((pckqty * totduti) / 1000) * T1);
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "STK") {
      $("#ItemTotalDutiableQtyInput").val(pckqty);
      $("#ItemHsQtyInput").val((pckqty * totduti) / 1000);
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(pckqty * T1);
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "KGM" && typeidval == 62) {
      $("#ItemTotalDutiableQtyInput").val(pckqty * totduti);
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(pckqty * totduti * T1);
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "TNE" && typeidval == 62) {
      $("#ItemTotalDutiableQtyInput").val(pckqty * totduti);
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(pckqty * totduti * T1);
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "KGM" && typeidval == 61) {
      $("#ItemTotalDutiableQtyInput").val(pckqty * totduti);
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(pckqty * totduti * T1);
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    } else if (TDQUOM == "DAL") {
      $("#ItemTotalDutiableQtyInput").val(pckqty * totduti);
      if (!HsVal.startsWith("87")) {
        $("#TxtSumExciseDuty").val(pckqty * totduti * T1);
      }
      T3 = Number($("#TxtSumExciseDuty").val());
      T4 = T2 * gstperval + T3 * gstperval;
      $("#TxtItemSumGST").val(T4.toFixed(2));
    }
  }
}

function txtAlcoholPer_TextChanged() {
  if ($("#itemAlchoholPer").val() != "") {
    let T1 = Number($("#ItemTotalDutiableQtyInput").val());
    let T2 = Number($("#itemAlchoholPer").val());
    let T3 = Number($("#TxtExciseDutyRate").val());
    let T4 = Number($("#TxtCustomsDutyRate").val());
    let gstperval;
    let T6;

    if (T2 > 0) {
      $("#TxtSumExciseDuty").val((T1 * T2 * (T3 / 100)).toFixed(2));
      $("#TxtSumCustomsDuty").val((T1 * T2 * (T4 / 100)).toFixed(2));
    }

    gstperval = Number($("#ItemGSTRate").val()) / 100;
    T4 = Number($("#TxtSumExciseDuty").val());
    T5 = Number($("#iteminvoiceCIFFOB").val());
    T7 = Number($("#TxtSumCustomsDuty").val());
    if ($("#declarationType").val() == "GTR : GST RELIEF (& DUTY EXEMPTION)") {
      T6 = T5 * gstperval;
    } else {
      T6 = T4 * gstperval + T5 * gstperval + T7 * gstperval;
    }
    $("#TxtItemSumGST").val(T6.toFixed(2));
  }
}

function itemDuitableQtyOnChange() {
  let T1 = Number($("#itemOuterPackQtyInput").val());
  let T2 = Number($("#itemInPackQuantityInput").val());
  let T3 = Number($("#itemInnerPackQtyInput").val());
  let T4 = Number($("#itemInmostPackQtyInput").val());
  let T5 = Number($("#itemDuitableQty").val());
  duticalc(T1, T2, T3, T4, T5);
  txtAlcoholPer_TextChanged();
}

function ItemCascShowAll(ID, CLASS) {
  if ($(ID).prop("checked")) {
    $(CLASS).show();
    $(ID).val("True");
  } else {
    $(ID).val("False");
    $(CLASS + ' :input[type="number"]').val("0.00");
    $(CLASS + ' :input[type="text"]').val("");
    $(CLASS + " select").val("--Select--");
    $(CLASS + " textarea").val("");
    if (CLASS == ".OutItemCascHide") {
      $(".OutItemCascHide table").find("tr:gt(1)").remove();
      $(".OutCasc3").hide();
      $(".OutCasc4").hide();
      $(".OutCasc5").hide();
      $("#ProductCode3").prop("checked", false);
      $("#ProductCode4").prop("checked", false);
      $("#ProductCode5").prop("checked", false);
    }
    if (".OutCasc3" == CLASS) {
      $(".OutCasc3 table").find("tr:gt(1)").remove();
    }
    if (".OutCasc4" == CLASS) {
      $(".OutCasc4 table").find("tr:gt(1)").remove();
    }
    if (".OutCasc5" == CLASS) {
      $(".OutCasc5 table").find("tr:gt(1)").remove();
    }
    $(CLASS).hide();
  }
}

function ItemTotalDutiableOnchange() {
  if ($("#ItemTotalDutiableQtyInput").val() != "") {
    if (!$("#ItemHsCodeInNon").val().startsWith("87")) {
      $("#TxtSumExciseDuty").val(
        Number($("#ItemTotalDutiableQtyInput").val()) *
        Number($("#TxtExciseDutyRate").val())
      );
    }
  } else {
    $("#TxtSumExciseDuty").val("0.00");
  }
  txtAlcoholPer_TextChanged();
}

function itemInvoiceQuantityFunction() {
  var itemqty = $("#itemInvoiceQuantity").val();
  if (itemqty != "0.0000") {
    var hsopt = $("#ItemHsQtyUom").val();
    var total;
    if (hsopt == "TEN" || hsopt == "TPR") {
      total = itemqty / 10;
    } else if (hsopt == "CEN") {
      total = itemqty / 100;
    } else if (hsopt == "MIL" || hsopt == "TNE") {
      total = itemqty / 1000;
    } else if (hsopt == "MTK") {
      total = itemqty * 3.213;
    } else if (hsopt == "LTR") {
      total = itemqty * 1;
    } else {
      total = itemqty;
    }
    if (hsopt == "KGM" || hsopt == "LTR" || hsopt == "TNE") {
      if (Number(itemqty) > Number($("#InNonTotalGrossWeightInput").val())) {
        alert(
          "The Total Gross Weight is Less Than The Sum Of The Item Weight Please Check!!!"
        );
      }
    }
    if (
      $("#ItemHsQtyInput").val() == "0.00" ||
      $("#ItemHsQtyInput").val() == ""
    ) {
      $("#ItemHsQtyInput").val(total);
    }
    if (
      $("#itemInvoiceQuantity").val() != "0.00" &&
      $("#ItemHsQtyInput").val() != ""
    ) {
      $("#ItemHsQtyInput").val(total);
    }
  }
}

function itemCheckUnitPriceFunction() {
  var check = document.getElementById("itemCheckUnitPrice");
  $("#UnitPriceIDShow").hide();
  if (check.checked) {
    check.value = "True";
    $("#UnitPriceIDShow").show();
  } else {
    $("#UnitPrice").val("0.00");
    $("#SumExchangeRate").val("0.00");
    check.value = "False";
  }
}

function PreferntialLoad(Val) {
  let drop = "<option selected>--Select--</option>";
  for (var i of Val) {
    drop += `<option>${i.Name}</option>`;
  }
  $("#itemPreferntialCode").html(drop);
}
function itemPreferntialCodeOut() {
  let Pref = $("#itemPreferntialCode").val()
  if (Pref == "PRF : if goods are imported under preferential duty rates") {
    $("#TxtCustomsDutyRate").val("0.00")
    $("#TxtCustomsDutyUOM").val("--Select--")
    $("#TxtSumCustomsDuty").val("0.00")
  }
  dutiableQtyFunction()
}

function OutItemAddCasc(Table, NAME) {
  var rowAdd = `<tr>
          <td><input type="text" class="inputStyle" name="${NAME}"></td>
          <td><input type="text" class="inputStyle" name="${NAME}"></td>
          <td><input type="text" class="inputStyle" name="${NAME}"></td>
          <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCascTable(this)" ></i></td>
      </tr>`;
  $(`${Table} tbody`).append(rowAdd);
}

// function CopyHsQuantity(INPUT, UOM) {
//   $("#" + INPUT).val($("#ItemHsQtyInput").val());
//   $("#" + UOM).val($("#ItemHsQtyUom").val());
// }

function CopyHsQuantity(INPUT) {
  $("#" + INPUT).val($("#ItemHsQtyInput").val());
  
}


function DeleteCascTable(TAB) {
  var deletedIndex = $(TAB).closest("tr").index();
  var row = $(TAB).closest("tr");
  if (deletedIndex !== 0) {
    $(TAB).closest("tr").remove();
  } else if (deletedIndex === 0) {
    row.find("input:eq(0)").val("");
    row.find("input:eq(1)").val("");
    row.find("input:eq(2)").val("");
  }
}

function ItemInvoiceNumberChange(Val) {
  if (Val == "--Select--" || Val == "--Select--") {
    $("#ItemInvoiceCurrencyDrop").val("--Select--");
    $("#ItemInvoiceCurrencyInput").val("0.00");
  } else {
    for (var inv of InvoiceData) {
      if (Val == inv.InvoiceNo) {
        $("#ItemInvoiceCurrencyDrop").val(inv.TICurrency);
        $("#ItemInvoiceCurrencyInput").val(inv.TIExRate);
      }
    }
  }
}

function TotalLineAmountCalculation() {
  let InvoiceCharge = "";
  let OtherChnage = "";
  let Insurancecharge = "";
  let FrightCharge = "";
  let TxtTotalLineAmount = Number($("#iteminvoiceTotalLineAmount").val());

  for (var Inv of InvoiceData) {
    if (Inv.InvoiceNo == $("#ItemInvoiceNumberInNon").val()) {
      InvoiceCharge = Inv.TISAmount;
      OtherChnage = Inv.OTCSAmount;
      Insurancecharge = Inv.ICSAmount;
      FrightCharge = Inv.FCSAmount;
    }
  }
  if (InvoiceData.length > 0 && TxtTotalLineAmount != "") {
    let T1 = Number(InvoiceCharge);
    let T2 = Number(OtherChnage);
    let T3 = Number(Insurancecharge);
    let T4 = Number(FrightCharge);
    let A1 = Number($("#iteminvoiceTotalLineAmount").val());
    let A2 = Number($("#ItemInvoiceCurrencyInput").val());

    let T5 = (T2 + T3 + T4) / T1;
    $("#iteminvoiceTotalInvoiceCharge").val((A2 * A1 * T5).toFixed(2));

    let gstper = Number($("#ItemGSTRate").val());
    T1 = Number($("#iteminvoiceTotalLineAmount").val());
    T2 = Number($("#ItemInvoiceCurrencyInput").val());
    T3 = Number($("#iteminvoiceTotalInvoiceCharge").val());

    $("#iteminvoiceCIFFOB").val((T1 * T2 + T3).toFixed(2));
    T4 = Number($("#iteminvoiceCIFFOB").val());
    $("#TxtItemSumGST").val(((T4 * gstper) / 100).toFixed(2));
  }

  let cif;
  let exrate;
  let sumex;
  let itemgst;
  let summerygst;
  let optional;
  let gstperval;

  cif = Number($("#iteminvoiceCIFFOB").val());
  exrate = Number($("#iteminvoiceCIFFOB").val());
  sumex = 0;
  if (!$("#ItemHsCodeInNon").val().startsWith("87")) {
    sumex = Number($("#TxtSumExciseDuty").val());
  } else if (!$("#ItemHsCodeInNon").val().startsWith("87")) {
    sumex = (cif * (exrate / 100)).toFixed(2);
  }
  itemgst = Number($("#TxtItemSumGST").val());
  if ($("#OptionalSumExchage").val() == "") {
    $("#OptionalSumExchage").val("0.00");
  }
  optional = Number($("#OptionalSumExchage").val());
  if (!$("#ItemHsCodeInNon").val().startsWith("87")) {
    $("#TxtSumExciseDuty").val(sumex);
  }
  gstperval = Number($("#ItemGSTRate").val()) / 100;
  summerygst = sumex * gstperval + cif * gstperval + optional * gstperval;
  $("#TxtItemSumGST").val(summerygst.toFixed(2));
}

function itemLastSellingPriceOut() {
  if ($("#itemLastSellingPrice") != "") {
    let T4 = Number($("#TxtOtherTaxableCharge").val());
    let T5 = Number($("#txtlsp").val());
    let T6 = Number($("#TxtSumCustomsDuty").val());
    let T7 = Number($("#TxtSumExciseDuty").val());
    T6 = T4 * 0.07 + T5 * 0.07 + T7 * 0.07 + T6 * 0.07;
    $("#TxtItemSumGST").val(T6.toFixed(2));
  }
}

function ItemResetInNon() {
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
  $("#ItemGSTUOM").val("PER");
  $("#ItemGSTRate").val(9);
  $(".OutItemCascHide p").html("");
  CargoInHawbOut($("#CargoInHawb").val());
  CargoOutHawbOut($("#InNonOutHblHawbInput").val());
  $("#ITEMNUMBER").val(ItemData.length + 1);
}

// function product1CodeCopyUomChange(){
//   console.log('hello')
//   var output=$("#ItemHsQtyInput").val()
//   console.log('output:',output)
//   if ($("#ItemHsQtyUom").val() === $("#product1CodeCopyUom").val()){
//      $("#product1CodeCopyInput").val(output)
//   }
// }

function ItemCascSave() {
  var itemNUmber = $("#ITEMNUMBER").val();
  var UserName = $("#INONUSERNAME").val();
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
        ItemNo: itemNUmber,
        ProductCode: $("#itemProductCode1").val(),
        Quantity: $("#product1CodeCopyInput").val(),
        ProductUOM: $("#product1CodeCopyUom").val(),
        RowNo: row1,
        CascCode1: casc1[i].value,
        CascCode2: casc1[i + 1].value,
        CascCode3: casc1[i + 2].value,
        PermitId: $("#PermitIDInNon").val(),
        MessageType: $("#MsgType").val(),
        TouchUser: UserName,
        TouchTime: TOUCHTIME,
        CASCId: "Casc1",
      });
      row1 += 1;
    }
  }

  if ($("#itemProductCode2").val() != "") {
    var row2 = 1;
    for (var i = 0; i < casc2.length; i += 3) {
      cascArray.push({
        ItemNo: itemNUmber,
        ProductCode: $("#itemProductCode2").val(),
        Quantity: $("#product2CodeCopyInput").val(),
        ProductUOM: $("#product2CodeCopyUom").val(),
        RowNo: row2,
        CascCode1: casc2[i].value,
        CascCode2: casc2[i + 1].value,
        CascCode3: casc2[i + 2].value,
        PermitId: $("#PermitIDInNon").val(),
        MessageType: $("#MsgType").val(),
        TouchUser: UserName,
        TouchTime: TOUCHTIME,
        CASCId: "Casc2",
      });
      row2 += 1;
    }
  }

  if ($("#itemProductCode3").val() != "") {
    var row3 = 1;
    for (var i = 0; i < casc3.length; i += 3) {
      cascArray.push({
        ItemNo: itemNUmber,
        ProductCode: $("#itemProductCode3").val(),
        Quantity: $("#product3CodeCopyInput").val(),
        ProductUOM: $("#product3CodeCopyUom").val(),
        RowNo: row3,
        CascCode1: casc3[i].value,
        CascCode2: casc3[i + 1].value,
        CascCode3: casc3[i + 2].value,
        PermitId: $("#PermitIDInNon").val(),
        MessageType: $("#MsgType").val(),
        TouchUser: UserName,
        TouchTime: TOUCHTIME,
        CASCId: "Casc3",
      });
      row3 += 1;
    }
  }

  if ($("#itemProductCode4").val() != "") {
    var row4 = 1;
    for (var i = 0; i < casc4.length; i += 3) {
      cascArray.push({
        ItemNo: itemNUmber,
        ProductCode: $("#itemProductCode4").val(),
        Quantity: $("#product4CodeCopyInput").val(),
        ProductUOM: $("#product4CodeCopyUom").val(),
        RowNo: row4,
        CascCode1: casc4[i].value,
        CascCode2: casc4[i + 1].value,
        CascCode3: casc4[i + 2].value,
        PermitId: $("#PermitIDInNon").val(),
        MessageType: $("#MsgType").val(),
        TouchUser: UserName,
        TouchTime: TOUCHTIME,
        CASCId: "Casc4",
      });
      row4 += 1;
    }
  }

  if ($("#itemProductCode5").val() != "") {
    var row5 = 1;
    for (var i = 0; i < casc5.length; i += 3) {
      cascArray.push({
        ItemNo: itemNUmber,
        ProductCode: $("#itemProductCode5").val(),
        Quantity: $("#product5CodeCopyInput").val(),
        ProductUOM: $("#product5CodeCopyUom").val(),
        RowNo: row5,
        CascCode1: casc5[i].value,
        CascCode2: casc5[i + 1].value,
        CascCode3: casc5[i + 2].value,
        PermitId: $("#PermitIDInNon").val(),
        MessageType: $("#MsgType").val(),
        TouchUser: UserName,
        TouchTime: TOUCHTIME,
        CASCId: "Casc5",
      });
      row5 += 1;
    }
  }
  return cascArray;
}

function ItemSaveInNon(MoveVal) {
  $("#Item span").hide();
  var Check = true;
  if ($("#ItemHsCodeInNon").val() == "") {
    Check = false;
    $("#ItemHsCodeInNonSpan").show();
  }

  if ($("#ItemDescriptionInNon").val() == "") {
    Check = false;
    $("#ItemDescriptionInNonSpan").show();
  }

  if ($("#declarationType").val() == "SFZ : STORAGE IN FTZ") {
    if ($("#ItemCooInput").val() == "IL") {
      alert("PLEASE CHECK COO");
      Check = false;
    }
  }

  if ($("#ItemCooInput").val() == "") {
    Check = false;
    $("#ItemCooInputSpan").show();
  }

  if (
    $("#ItemHsQtyUom").val() == "--Select--" ||
    $("#ItemHsQtyUom").val() == "-"
  ) {
    Check = false;
    $("#ItemHsQtyUomSpan").show();
  }

  if ($("#itemCascID").prop("checked")) {
    if ($("#itemProductCode1").val() == "") {
      Check = false;
      $("#itemProductCode1Span").show();
    }
  }

  var Orginregdate;
  if ($("#OriginalRegistrationDate").val() == "") {
    Orginregdate = "01/01/1900";
  } else {
    Orginregdate = $("#OriginalRegistrationDate").val().split("/");
    Orginregdate = `${Orginregdate[2]}/${Orginregdate[1]}/${Orginregdate[0]}`;
  }
  let ItemNumberEdit = $("#ITEMNUMBER").val()

  if (Check) {
    $("#Loading").show();
    $.ajax({
      url: "/InNonItemLoad/",
      type: "POST",
      data: {
        CascDatas: JSON.stringify(ItemCascSave()),
        ItemNo: $("#ITEMNUMBER").val().trim(),
        PermitId: $("#PermitIDInNon").val().trim(),
        MessageType: $("#MsgType").val().trim(),
        HSCode: $("#ItemHsCodeInNon").val().trim(),
        Description: $("#ItemDescriptionInNon").val().trim().toUpperCase(),
        DGIndicator: $("#itemDgIndicator").val().trim(),
        Contry: $("#ItemCooInput").val().trim(),
        Brand: $("#itemBrandInput").val().trim(),
        Model: $("#itemModel").val().trim(),
        Vehicletype: $("#VehicalTypeUom").val(),
        Enginecapacity: $("#EngineCapacity").val().trim(),
        Engineuom: $("#EngineCapacityUom").val(),
        Orginregdate: Orginregdate,
        InHAWBOBL: $("#itemHawb").val(),
        OutHAWBOBL: $("#ItemOutHawbDrop").val(),
        DutiableQty: $("#itemDuitableQty").val(),
        DutiableUOM: $("#ItemDutiableUom").val(),
        TotalDutiableQty: $("#ItemTotalDutiableQtyInput").val().trim(),
        TotalDutiableUOM: $("#ItemTotalDutiableQtyUom").val(),
        InvoiceQuantity: $("#itemInvoiceQuantity").val().trim(),
        HSQty: $("#ItemHsQtyInput").val().trim(),
        HSUOM: $("#ItemHsQtyUom").val(),
        AlcoholPer: $("#itemAlchoholPer").val(),
        InvoiceNo: $("#ItemInvoiceNumberInNon").val(),
        ChkUnitPrice: $("#itemCheckUnitPrice").val().trim(),
        UnitPrice: $("#UnitPrice").val().trim(),
        UnitPriceCurrency: $("#ItemInvoiceCurrencyDrop").val().trim(),
        ExchangeRate: $("#ItemInvoiceCurrencyInput").val().trim(),
        SumExchangeRate: $("#SumExchangeRate").val().trim(),
        TotalLineAmount: $("#iteminvoiceTotalLineAmount").val().trim(),
        InvoiceCharges: $("#iteminvoiceTotalInvoiceCharge").val().trim(),
        CIFFOB: $("#iteminvoiceCIFFOB").val().trim(),
        OPQty: $("#itemOuterPackQtyInput").val().trim(),
        OPUOM: $("#itemOuterPackQtySelect").val().trim(),
        IPQty: $("#itemInPackQuantityInput").val().trim(),
        IPUOM: $("#itemInPackQuantitySelect").val().trim(),
        InPqty: $("#itemInnerPackQtyInput").val().trim(),
        InPUOM: $("#itemInnerPackQtySelect").val().trim(),
        ImPQty: $("#itemInmostPackQtyInput").val().trim(),
        ImPUOM: $("#itemInmostPackQtySelect").val().trim(),
        PreferentialCode: $("#itemPreferntialCode").val().trim(),
        GSTRate: $("#ItemGSTRate").val().trim(),
        GSTUOM: $("#ItemGSTUOM").val().trim(),
        GSTAmount: $("#TxtItemSumGST").val().trim(),
        ExciseDutyRate: $("#TxtExciseDutyRate").val().trim(),
        ExciseDutyUOM: $("#TxtExciseDutyUOM").val().trim(),
        ExciseDutyAmount: $("#TxtSumExciseDuty").val().trim(),
        CustomsDutyRate: $("#TxtCustomsDutyRate").val().trim(),
        CustomsDutyUOM: $("#TxtCustomsDutyUOM").val().trim(),
        CustomsDutyAmount: $("#TxtSumCustomsDuty").val().trim(),
        OtherTaxRate: $("#itemOtherTaxRate").val().trim(),
        OtherTaxUOM: $("#itemOtherTaxUom").val().trim(),
        OtherTaxAmount: $("#itemOtherTaxAmount").val().trim(),
        CurrentLot: $("#CurrentLot").val().trim(),
        PreviousLot: $("#PreviousLot").val().trim(),
        LSPValue: $("#itemLastSellingPrice").val().trim(),
        Making: $("#Making").val(),
        ShippingMarks1: $("#ShippingMarks1").val().trim(),
        ShippingMarks2: $("#ShippingMarks2").val().trim(),
        ShippingMarks3: $("#ShippingMarks3").val().trim(),
        ShippingMarks4: $("#ShippingMarks4").val().trim(),
        TouchUser: $("#INONUSERNAME").val().trim(),
        TouchTime: TOUCHTIME,
        OptionalChrgeUOM: $("#OptionalChrgeUOM").val().trim(),
        Optioncahrge: $("#Optioncahrge").val().trim(),
        OptionalSumtotal: $("#OptionalSumtotal").val().trim(),
        OptionalSumExchage: $("#OptionalSumExchage").val().trim(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        ItemResetInNon();
        ItemData = response.item;
        CascData = response.casc;
        alert(response.Result);
        ItemLoad();
        $("#Loading").hide();
        let EditValue = 1;
        if (MoveVal == "NEXTMOVE") {
          EditValue = Number(ItemNumberEdit) + 1
        }
        else if (MoveVal == "PREVIOUSMOVE") {
          EditValue = Number(ItemNumberEdit) - 1
        }

        if (MoveVal != "NEWMOVE") {
          if (ItemData.length >= 1 && ItemData.length <= ItemData.length) {
            ItemEditInNon(EditValue)
          }
        }
        $('#ItemHsCodeInNon').focus()
      },
    });
  } else {
    alert("PLEASE FILL THE ALL Mandatory FIELD");
  }
}

function ItemLoad() {
  let TotalLineAmd = 0;
  let GstAmd = 0;
  let Cifob = 0;
  let ExciseDutyAmd = 0;
  let CustomsDutyAmd = 0;
  let OtherTaxAmd = 0;

  let ItemCurrAmd = [];

  $("#ITEMNUMBER").val(ItemData.length + 1);
  $("#summaryNoOfItems").val(Number(ItemData.length).toString().padStart(3));
  if (ItemData.length > 0) {
    var Tab = "";
    for (var Itm of ItemData) {
      var Color = HsCode.filter((data) => {
        if (data.HSCode == Itm.HSCode && data.InnonPayment == '1') {
          return true
        }
      })

      if (Color.length != 0) {
        Color = "red"
      }
      else {
        Color = '#000'
      }
      Tab += `
          <tr style="color:${Color}">
            <td><input type="checkbox" name = "itemCheckDel" value = "${Itm.ItemNo}" ></td>
            <td><i class="fa-regular fa-pen-to-square" style="color: #ff0000;" onclick = "ItemEditInNon('${Itm.ItemNo}')" ></i></td>
            <td>${Itm.ItemNo}</td>
            <td>${Itm.HSCode}</td>
            <td>${Itm.Description}</td>
            <td>${Itm.Contry}</td>
            <td>${Itm.InHAWBOBL}</td>
            <td>${Itm.OutHAWBOBL}</td>
            <td>${Itm.UnitPriceCurrency}</td>
            <td>${Itm.CIFFOB}</td>
            <td>${Itm.HSQty}</td>
            <td>${Itm.HSUOM}</td>
            <td>${Itm.GSTAmount}</td>
            <td>${Itm.TotalLineAmount}</td>
        </tr>
        `;


      ItemCurrAmd.push([Itm.UnitPriceCurrency, Number(Itm.TotalLineAmount)]);
      TotalLineAmd += Number(Itm.TotalLineAmount);
      GstAmd += Number(Itm.GSTAmount);
      Cifob += Number(Itm.CIFFOB);
      ExciseDutyAmd += Number(Itm.ExciseDutyAmount);
      CustomsDutyAmd += Number(Itm.CustomsDutyAmount);
      OtherTaxAmd += Number(Itm.OtherTaxAmount);
    }
    $("#summarySumOfItemValue").val(TotalLineAmd.toFixed(2));
    $("#summaryTotalCIFFOBValue").val(Cifob.toFixed(2));
    $("#summaryTotalGstValue").val(GstAmd.toFixed(2));
    $("#summaryCustomsDuty").val(CustomsDutyAmd.toFixed(2));
    $("#itemOtherTaxAmountSummary").val(OtherTaxAmd.toFixed(2));
    $("#summaryTotalPayable").val(GstAmd.toFixed(2));
    $("#ItemTable tbody").html(Tab);
    SummarySumofItemAmd(ItemCurrAmd)

    if ($("#declarationType").val() == "DNG : Duty & GST") {
      let suTot = OtherTaxAmd + GstAmd + ExciseDutyAmd + CustomsDutyAmd;
      $("#summaryTotalPayable").val(suTot.toFixed(2));
    }
  } else {
    $("#ItemTable tbody").html(
      ` <tr><td colspan=14 style='text-align:center'>No Record</td></tr>`
    );
    $("#summarySumOfItemValue").val("0.00");
    $("#summaryTotalCIFFOBValue").val("0.00");
    $("#summaryTotalGstValue").val("0.00");
    $("#summaryCustomsDuty").val("0.00");
    $("#itemOtherTaxAmountSummary").val("0.00");
    $("#summaryTotalPayable").val("0.00");
  }

  var SInvoice = (document.getElementsByName('summarySumOfInvoiceAmount')[0].value).split('.');
  var SItem = (document.getElementsByName('summarySumOfItemAmout')[0].value).split('.');
  if ((SInvoice[0] == SItem[0]) || $('#summaryTotalInvoiceCIFValue').val() == $('#summaryTotalCIFFOBValue').val()) {
    $('#SUmmaryEqualNot').hide();
  }
  else {
    $('#SUmmaryEqualNot').show();
  }
}

function ItemEditInNon(ItemNumber) {
   ItemResetInNon();
  for (var Itm of ItemData) {
    if (Itm.ItemNo == ItemNumber) {
      $("#ITEMNUMBER").val(Itm.ItemNo);
      $("#ItemNextItemID").val(Itm.ItemNo)
      $("#PermitIDInNon").val(Itm.PermitId);
      $("#MsgType").val(Itm.MessageType);
      $("#ItemHsCodeInNon").val(Itm.HSCode);
      $("#itemDgIndicator").val(Itm.DGIndicator);
      if (Itm.Brand == "true" || Itm.Brand == "True") {
        $("#itemDgIndicator").prop("checked", true);
      }
      else {
        $("#itemDgIndicator").prop("checked", false);
      }
      $("#ItemCooInput").val(Itm.Contry);
      $("#itemBrandInput").val(Itm.Brand);
      if (Itm.Brand === "UNBRANDED") {
        $("#itemUnBrand").prop("checked", true);
      } else {
        $("#itemUnBrand").prop("checked", false);
      }
      $("#itemModel").val(Itm.Model);
      $("#VehicalTypeUom").val(Itm.Vehicletype);
      $("#EngineCapacity").val(Itm.Enginecapacity);
      $("#EngineCapacityUom").val(Itm.Engineuom);
      // $("#itemHawb").val(Itm.InHAWBOBL);
      // $("#ItemOutHawbDrop").val(Itm.OutHAWBOBL);
      $("#itemDuitableQty").val(Itm.DutiableQty);
      $("#ItemDutiableUom").val(Itm.DutiableUOM);
      $("#ItemTotalDutiableQtyInput").val(Itm.TotalDutiableQty);
      $("#ItemTotalDutiableQtyUom").val(Itm.TotalDutiableUOM);
      $("#itemInvoiceQuantity").val(Itm.InvoiceQuantity);
      $("#ItemHsQtyInput").val(Itm.HSQty);
      $("#ItemHsQtyUom").val(Itm.HSUOM);
      $("#itemAlchoholPer").val(Itm.AlcoholPer);
      $("#ItemInvoiceNumberInNon").val(Itm.InvoiceNo);
      $("#itemCheckUnitPrice").val(Itm.ChkUnitPrice);
      $("#UnitPrice").val(Itm.UnitPrice);
      $("#ItemInvoiceCurrencyDrop").val(Itm.UnitPriceCurrency);
      $("#ItemInvoiceCurrencyInput").val(Itm.ExchangeRate);
      $("#SumExchangeRate").val(Itm.SumExchangeRate);
      $("#iteminvoiceTotalLineAmount").val(Itm.TotalLineAmount);
      $("#iteminvoiceTotalInvoiceCharge").val(Itm.InvoiceCharges);
      $("#iteminvoiceCIFFOB").val(Itm.CIFFOB);
      $("#itemOuterPackQtyInput").val(Itm.OPQty);
      $("#itemOuterPackQtySelect").val(Itm.OPUOM);
      $("#itemInPackQuantityInput").val(Itm.IPQty);
      $("#itemInPackQuantitySelect").val(Itm.IPUOM);
      $("#itemInnerPackQtyInput").val(Itm.InPqty);
      $("#itemInnerPackQtySelect").val(Itm.InPUOM);
      $("#itemInmostPackQtyInput").val(Itm.ImPQty);
      $("#itemInmostPackQtySelect").val(Itm.ImPUOM);
      $("#itemPreferntialCode").val(Itm.PreferentialCode);
      //$("#ItemGSTRate").val(Itm.GSTRate);
      $("#ItemGSTUOM").val(Itm.GSTUOM);
      $("#TxtItemSumGST").val(Itm.GSTAmount);
      $("#TxtExciseDutyRate").val(Itm.ExciseDutyRate);
      $("#TxtExciseDutyUOM").val(Itm.ExciseDutyUOM);
      $("#TxtSumExciseDuty").val(Itm.ExciseDutyAmount);
      $("#TxtCustomsDutyRate").val(Itm.CustomsDutyRate);
      $("#TxtCustomsDutyUOM").val(Itm.CustomsDutyUOM);
      $("#TxtSumCustomsDuty").val(Itm.CustomsDutyAmount);
      $("#itemOtherTaxRate").val(Itm.OtherTaxRate);
      $("#itemOtherTaxUom").val(Itm.OtherTaxUOM);
      $("#itemOtherTaxAmount").val(Itm.OtherTaxAmount);
      $("#CurrentLot").val(Itm.CurrentLot);
      $("#PreviousLot").val(Itm.PreviousLot);
      $("#itemLastSellingPrice").val(Itm.LSPValue);
      $("#Making").val(Itm.Making);
      $("#ShippingMarks1").val(Itm.ShippingMarks1);
      $("#ShippingMarks2").val(Itm.ShippingMarks2);
      $("#ShippingMarks3").val(Itm.ShippingMarks3);
      $("#ShippingMarks4").val(Itm.ShippingMarks4);
      $("#OptionalChrgeUOM").val(Itm.OptionalChrgeUOM);
      $("#Optioncahrge").val(Itm.Optioncahrge);
      $("#OptionalSumtotal").val(Itm.OptionalSumtotal);
      $("#OptionalSumExchage").val(Itm.OptionalSumExchage);
      if (
        Itm.OPQty != "0" ||
        Itm.IPQty != "0" ||
        Itm.InPqty != "0" ||
        Itm.ImPQty != "0"
      ) {
        $("#packing_details").prop("checked", true);
        ItemCascShowAll("#packing_details", ".PackingDetails");
        
      }
      if (
        Itm.ShippingMarks1 != "" ||
        Itm.ShippingMarks2 != "" ||
        Itm.ShippingMarks3 != "" ||
        Itm.ShippingMarks4 != ""
      ) {
        $("#shippingMarkCheck").prop("checked", true);
        ItemCascShowAll("#shippingMarkCheck", ".ShippingMark");
      }
      if (
        Itm.CurrentLot != "" ||
        Itm.PreviousLot != "" ||
        Itm.Making != "--Select--"
      ) {
        $("#lotIdCheck").prop("checked", true);
        ItemCascShowAll("#lotIdCheck", ".OutLotId");
      }

      ItemHscodeFocusOut();
      ItemCooOut(Itm.Contry);
      itemDuitableQtyOnChange();
      ItemTotalDutiableOnchange();
      itemInvoiceQuantityFunction();
      txtAlcoholPer_TextChanged();
      OptionalChrgeUOMOut(Itm.OptionalChrgeUOM);
      ItemInvoiceNumberChange(Itm.InvoiceNo);
      TotalLineAmountCalculation();
      if (Itm.Description == "") {
        ItemHscodeFocusOut();
      }
      else {
        $("#ItemDescriptionInNon").val(Itm.Description);
      }
      ItemCascEdit(Itm.ItemNo);
      $("#ItemDescriptionInNon").focus();
    }
  }
}

function ProductFocusIn1(ID, Desc, Uom) {
  $.ajax({
    url: "/Inpayment/CascProductCodes/?search=" + $("#ItemHsCodeInNon").val(),
    type: "GET",
    success: function (response) {
      $("#Loading").show();
      let store = [];
      for (var i of response) {
        store.push(`${i.CASCCode}:${i.Description}`);
      }
      Autocomplete1(store, ID);
      $("#Loading").hide();
      $(ID).focusout(function () {
        if ($(ID).val() == "") {
          $(Desc).html("");
          $(Uom).val("--Select--");
        } else {
          for (var i of response) {
            if (i.CASCCode == $(ID).val()) {
              $(Desc).html(i.Description);
              $(Uom).val(i.UOM);
            }
          }
        }
      });
    },
  });
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

function CooSelectRow(Tag) {
  let SelectRow = $(Tag).closest("tr");
  let col1 = SelectRow.find("td:eq(0)").text();
  let col2 = SelectRow.find("td:eq(1)").text();
  $("#ItemCooInput").val(col1);
  $("#ItemCooInputText").val(col2);
  $("#InNonImporterSerchId").hide();
}

function ItemCascSearch(Code, Desc, Uom) {
  $("#Loading").show();
  $.ajax({
    url: "/Inpayment/CascProductCodes/?search=" + $("#ItemHsCodeInNon").val(),
    type: "GET",
    success: function (response) {
      $("#InNonImporterSerchId").show();
      $("#Loading").hide();
      var tag = "";
      for (var i of response) {
        tag += `
      <tr onclick="ProductSelectRow(this,'${Code}','${Desc}','${Uom}')" style="cursor: pointer;">
          <td>${i.CASCCode}</td>
          <td>${i.Description}</td>
          <td>${i.UOM}</td>
        </tr>
    `;
      } 
      $("#InNonImporterSerchId").html(`
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
                  <button type="button" class="ButtonClick" style="margin-top: 30px;margin-left: 40%;" onclick="$('#InNonImporterSerchId').hide()">CLOSE</button>
              </div>
          </div>
          `);
      $("#ItemProductTab1").DataTable({
        pageLength: 5,
        ordering: false,
        dom: "rtip",
        autoWidth: false,
        
      });
      
    },
   
  });
  
}

// function ProductSelectRow(val, Code, Desc, Uom) {
//   var currentRow = $(val).closest("tr");
//   var col1 = currentRow.find("td:eq(0)").text();
//   var col2 = currentRow.find("td:eq(1)").text();
//   var col3 = currentRow.find("td:eq(2)").text();
//   $("#" + Code).val(col1);
//   $("#" + Desc).html(col2);
//   $("#" + Uom).val(col3);
//   $("#InNonImporterSerchId").hide();
//   var output = $("#ItemHsQtyInput").val();
//   if ($("#ItemHsQtyUom").val() === $("#product1CodeCopyUom").val()){
//     $("#product1CodeCopyInput").val(output);
//   }else if($("#ItemHsQtyUom").val() !== $("#product1CodeCopyUom").val()){
//     $("#product1CodeCopyInput").val("");
//   }
// }

function ProductSelectRow(val, Code, Desc, Uom, productCodeCopyUom, productCodeCopyInput) {
  var currentRow = $(val).closest("tr");
  var col1 = currentRow.find("td:eq(0)").text();
  var col2 = currentRow.find("td:eq(1)").text();
  var col3 = currentRow.find("td:eq(2)").text();
  $("#" + Code).val(col1);
  $("#" + Desc).html(col2);
  $("#" + Uom).val(col3);
  $("#InNonImporterSerchId").hide();
  var output = $("#ItemHsQtyInput").val();
  var products = [
    { copyUom: $("#product1CodeCopyUom").val(), copyInput: $("#product1CodeCopyInput") },
    { copyUom: $("#product2CodeCopyUom").val(), copyInput: $("#product2CodeCopyInput") }, 
  ];  
  products.forEach(function(product) {
    if ($("#ItemHsQtyUom").val() === product.copyUom) {
      product.copyInput.val(output);
    } else {
      product.copyInput.val("0.00");
    }
  });
}



function product1CodeCopyUomChange(){
  if($("#ItemHsQtyUom").val() !== $("#product1CodeCopyUom").val()){
    $("#product1CodeCopyInput").val("");
  }
  ProductSelectRow()
}


function product2CodeCopyUomChange(){
  if($("#ItemHsQtyUom").val() !== $("#product2CodeCopyUom").val()){
    $("#product2CodeCopyInput").val("");
  }
  ProductSelectRow()
}


function ProductFocusOut(Val, ID) {
  if (Val == "") {
    $("#" + ID).html("");
  }
}

function ItemCascEdit(Arg) {
  $("#itemCascID").prop("checked", false);
  $("#ProductCode3").prop("checked", false);
  $("#ProductCode4").prop("checked", false);
  $("#ProductCode5").prop("checked", false);
  for (var i of CascData) {
    if (i.ItemNo == Arg) {
      $("#itemCascID").prop("checked", true);
      if (i.CASCId == "Casc1") {
        CascEditUpdate(
          "#itemProductCode1",
          "#product1CodeCopyInput",
          "#product1CodeCopyUom",
          "ItemCascTable1",
          "cascName1",
          i
        );
        $("#ItemCascTable1 tbody").html(CascTable1);
      }
      if (i.CASCId == "Casc2") {
        CascEditUpdate(
          "#itemProductCode2",
          "#product2CodeCopyInput",
          "#product2CodeCopyUom",
          "ItemCascTable2",
          "cascName2",
          i
        );
        $("#ItemCascTable2 tbody").html(CascTable2);
      }
      if (i.CASCId == "Casc3") {
        $("#ProductCode3").prop("checked", true);
        ItemCascShowAll("#ProductCode3", ".OutCasc3");
        CascEditUpdate(
          "#itemProductCode3",
          "#product3CodeCopyInput",
          "#product3CodeCopyUom",
          "ItemCascTable3",
          "cascName3",
          i
        );
        $("#ItemCascTable3 tbody").html(CascTable3);
      }
      if (i.CASCId == "Casc4") {
        $("#ProductCode4").prop("checked", true);
        ItemCascShowAll("#ProductCode4", ".OutCasc4");
        CascEditUpdate(
          "#itemProductCode4",
          "#product4CodeCopyInput",
          "#product4CodeCopyUom",
          "ItemCascTable4",
          "cascName4",
          i
        );
        $("#ItemCascTable4 tbody").html(CascTable4);
      }
      if (i.CASCId == "Casc5") {
        $("#ProductCode5").prop("checked", true);
        ItemCascShowAll("#ProductCode5", ".OutCasc5");
        CascEditUpdate(
          "#itemProductCode5",
          "#product5CodeCopyInput",
          "#product5CodeCopyUom",
          "ItemCascTable5",
          "cascName5",
          i
        );
        $("#ItemCascTable5 tbody").html(CascTable5);
      }
    }
  }
  ItemCascShowAll("#itemCascID", ".OutItemCascHide");
  CascTable1 = "";
  CascTable2 = "";
  CascTable3 = "";
  CascTable4 = "";
  CascTable5 = "";
}

var CascTable1 = "";
var CascTable2 = "";
var CascTable3 = "";
var CascTable4 = "";
var CascTable5 = "";

function CascEditUpdate(
  proCode,
  CopyInput,
  CopyUom,
  TableName,
  InputName,
  Data
) {
  $(proCode).val(Data.ProductCode);
  $(CopyInput).val(Data.Quantity);
  $(CopyUom).val(Data.ProductUOM);
  var cascTab = `<tr>
              <td><input type="text" class="inputStyle" name="${InputName}" value = ${Data.CascCode1}></td>
              <td><input type="text" class="inputStyle" name="${InputName}" value = ${Data.CascCode2}></td>
              <td><input type="text" class="inputStyle" name="${InputName}" value = ${Data.CascCode3}></td>
              <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCascTable(this)" ></i></td>
          </tr>`;
  if (InputName == "cascName1") {
    CascTable1 += cascTab;
  }
  if (InputName == "cascName2") {
    CascTable2 += cascTab;
  }
  if (InputName == "cascName3") {
    CascTable3 += cascTab;
  }
  if (InputName == "cascName4") {
    CascTable4 += cascTab;
  }
  if (InputName == "cascName5") {
    CascTable5 += cascTab;
  }
}

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
      url: "/ItemInNonExcelUpload/",
      dataType: "json",
      processData: false,
      contentType: false,
      data: formData,
      mimeType: "multipart/form-data",
      success: function (response) {
        ItemData = response.item;
        CascData = response.casc;
        ItemLoad();
        $("#Loading").hide();
      },
      error: function (response) {
        $("#Loading").hide();
      },
    });
  }
}

// function ItemEditAllInNon() {
//   console.log('hello')
//   $('#EditAllItemBtn').prop('disabled', true)
//   $("#Loading").show();
//   var ItemAllDataInNon = [];
//   for (var item of ItemData) {
//     ItemEditInNon(item.ItemNo);
//     var Echeck = true;
//     if ($('#itemCascID').prop('checked')) {
//       if ($('#itemProductCode1').val() == "") {
//         Echeck = false;
//       }
//     }
//     if (Echeck) {
//       ItemAllDataInNon.push({
//         ItemNo: $("#ITEMNUMBER").val().trim(),
//         PermitId: $("#PermitIDInNon").val().trim(),
//         MessageType: $("#MsgType").val().trim(),
//         HSCode: $("#ItemHsCodeInNon").val().trim(),
//         Description: $("#ItemDescriptionInNon").val().trim(),
//         DGIndicator: $("#itemDgIndicator").val().trim(),
//         Contry: $("#ItemCooInput").val().trim(),
//         Brand: $("#itemBrandInput").val().trim(),
//         Model: $("#itemModel").val().trim(),
//         Vehicletype: $("#VehicalTypeUom").val(),
//         Enginecapacity: $("#EngineCapacity").val().trim(),
//         Engineuom: $("#EngineCapacityUom").val(),
//         Orginregdate: $("#OriginalRegistrationDate").val(),
//         InHAWBOBL: $("#itemHawb").val(),
//         OutHAWBOBL: $("#ItemOutHawbDrop").val(),
//         DutiableQty: $("#itemDuitableQty").val(),
//         DutiableUOM: $("#ItemDutiableUom").val(),
//         TotalDutiableQty: $("#ItemTotalDutiableQtyInput").val().trim(),
//         TotalDutiableUOM: $("#ItemTotalDutiableQtyUom").val(),
//         InvoiceQuantity: $("#itemInvoiceQuantity").val().trim(),
//         HSQty: $("#ItemHsQtyInput").val().trim(),
//         HSUOM: $("#ItemHsQtyUom").val(),
//         AlcoholPer: $("#itemAlchoholPer").val(),
//         InvoiceNo: $("#ItemInvoiceNumberInNon").val(),
//         ChkUnitPrice: $("#itemCheckUnitPrice").val().trim(),
//         UnitPrice: $("#UnitPrice").val().trim(),
//         UnitPriceCurrency: $("#ItemInvoiceCurrencyDrop").val().trim(),
//         ExchangeRate: $("#ItemInvoiceCurrencyInput").val().trim(),
//         SumExchangeRate: $("#SumExchangeRate").val().trim(),
//         TotalLineAmount: $("#iteminvoiceTotalLineAmount").val().trim(),
//         InvoiceCharges: $("#iteminvoiceTotalInvoiceCharge").val().trim(),
//         CIFFOB: $("#iteminvoiceCIFFOB").val().trim(),
//         OPQty: $("#itemOuterPackQtyInput").val().trim(),
//         OPUOM: $("#itemOuterPackQtySelect").val().trim(),
//         IPQty: $("#itemInPackQuantityInput").val().trim(),
//         IPUOM: $("#itemInPackQuantitySelect").val().trim(),
//         InPqty: $("#itemInnerPackQtyInput").val().trim(),
//         InPUOM: $("#itemInnerPackQtySelect").val().trim(),
//         ImPQty: $("#itemInmostPackQtyInput").val().trim(),
//         ImPUOM: $("#itemInmostPackQtySelect").val().trim(),
//         PreferentialCode: $("#itemPreferntialCode").val().trim(),
//         GSTRate: $("#ItemGSTRate").val().trim(),
//         GSTUOM: $("#ItemGSTUOM").val().trim(),
//         GSTAmount: $("#TxtItemSumGST").val().trim(),
//         ExciseDutyRate: $("#TxtExciseDutyRate").val().trim(),
//         ExciseDutyUOM: $("#TxtExciseDutyUOM").val().trim(),
//         ExciseDutyAmount: $("#TxtSumExciseDuty").val().trim(),
//         CustomsDutyRate: $("#TxtCustomsDutyRate").val().trim(),
//         CustomsDutyUOM: $("#TxtCustomsDutyUOM").val().trim(),
//         CustomsDutyAmount: $("#TxtSumCustomsDuty").val().trim(),
//         OtherTaxRate: $("#itemOtherTaxRate").val().trim(),
//         OtherTaxUOM: $("#itemOtherTaxUom").val().trim(),
//         OtherTaxAmount: $("#itemOtherTaxAmount").val().trim(),
//         CurrentLot: $("#CurrentLot").val().trim(),
//         PreviousLot: $("#PreviousLot").val().trim(),
//         LSPValue: $("#itemLastSellingPrice").val().trim(),
//         Making: $("#Making").val(),
//         ShippingMarks1: $("#ShippingMarks1").val().trim(),
//         ShippingMarks2: $("#ShippingMarks2").val().trim(),
//         ShippingMarks3: $("#ShippingMarks3").val().trim(),
//         ShippingMarks4: $("#ShippingMarks4").val().trim(),
//         TouchUser: $("#INONUSERNAME").val().trim(),
//         TouchTime: TOUCHTIME,
//         OptionalChrgeUOM: $("#OptionalChrgeUOM").val().trim(),
//         Optioncahrge: $("#Optioncahrge").val().trim(),
//         OptionalSumtotal: $("#OptionalSumtotal").val().trim(),
//         OptionalSumExchage: $("#OptionalSumExchage").val().trim(),
//       });
//     }
//     ItemResetInNon();
//   }
//   $("#Loading").show();
//   $.ajax({
//     type: "POST",
//     url: "/AllItemUpdateInNon/",
//     data: {
//       Item: JSON.stringify(ItemAllDataInNon),
//       PermitId: $("#PermitIDInNon").val(),
//       csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
//     },
//     success: function (response) {
//       ItemData = response.item;
//       ItemLoad();
//       $("#Loading").hide();
//     },
//   });
// }


// function ItemEditAllInNon() {
//   console.log('hello');
//   $('#EditAllItemBtn').prop('disabled', true);
//   $("#Loading").show();
//   var ItemAllDataInNon = [];
//   for (var item of ItemData) {
//     ItemEditInNon(item.ItemNo);
//     var Echeck = true;
//     if ($('#itemCascID').prop('checked')) {
//       if ($('#itemProductCode1').val() == "") {
//         Echeck = false;
//       }
//     }
//     if (Echeck) {
//       ItemAllDataInNon.push({
//         ItemNo: $("#ITEMNUMBER").val().trim(),
//         PermitId: $("#PermitIDInNon").val().trim(),
//         MessageType: $("#MsgType").val().trim(),
//         HSCode: $("#ItemHsCodeInNon").val().trim(),
//         Description: $("#ItemDescriptionInNon").val().trim(),
//         DGIndicator: $("#itemDgIndicator").val().trim(),
//         Contry: $("#ItemCooInput").val().trim(),
//         Brand: $("#itemBrandInput").val().trim(),
//         Model: $("#itemModel").val().trim(),
//         Vehicletype: $("#VehicalTypeUom").val(),
//         Enginecapacity: $("#EngineCapacity").val().trim(),
//         Engineuom: $("#EngineCapacityUom").val(),
//         Orginregdate: $("#OriginalRegistrationDate").val(),
//         InHAWBOBL: $("#itemHawb").val(),
//         OutHAWBOBL: $("#ItemOutHawbDrop").val(),
//         DutiableQty: $("#itemDuitableQty").val(),
//         DutiableUOM: $("#ItemDutiableUom").val(),
//         TotalDutiableQty: $("#ItemTotalDutiableQtyInput").val().trim(),
//         TotalDutiableUOM: $("#ItemTotalDutiableQtyUom").val(),
//         InvoiceQuantity: $("#itemInvoiceQuantity").val().trim(),
//         HSQty: $("#ItemHsQtyInput").val().trim(),
//         HSUOM: $("#ItemHsQtyUom").val(),
//         AlcoholPer: $("#itemAlchoholPer").val(),
//         InvoiceNo: $("#ItemInvoiceNumberInNon").val(),
//         ChkUnitPrice: $("#itemCheckUnitPrice").val().trim(),
//         UnitPrice: $("#UnitPrice").val().trim(),
//         UnitPriceCurrency: $("#ItemInvoiceCurrencyDrop").val().trim(),
//         ExchangeRate: $("#ItemInvoiceCurrencyInput").val().trim(),
//         SumExchangeRate: $("#SumExchangeRate").val().trim(),
//         TotalLineAmount: $("#iteminvoiceTotalLineAmount").val().trim(),
//         InvoiceCharges: $("#iteminvoiceTotalInvoiceCharge").val().trim(),
//         CIFFOB: $("#iteminvoiceCIFFOB").val().trim(),
//         OPQty: $("#itemOuterPackQtyInput").val().trim(),
//         OPUOM: $("#itemOuterPackQtySelect").val().trim(),
//         IPQty: $("#itemInPackQuantityInput").val().trim(),
//         IPUOM: $("#itemInPackQuantitySelect").val().trim(),
//         InPqty: $("#itemInnerPackQtyInput").val().trim(),
//         InPUOM: $("#itemInnerPackQtySelect").val().trim(),
//         ImPQty: $("#itemInmostPackQtyInput").val().trim(),
//         ImPUOM: $("#itemInmostPackQtySelect").val().trim(),
//         PreferentialCode: $("#itemPreferntialCode").val().trim(),
//         GSTRate: $("#ItemGSTRate").val().trim(),
//         GSTUOM: $("#ItemGSTUOM").val().trim(),
//         GSTAmount: $("#TxtItemSumGST").val().trim(),
//         ExciseDutyRate: $("#TxtExciseDutyRate").val().trim(),
//         ExciseDutyUOM: $("#TxtExciseDutyUOM").val().trim(),
//         ExciseDutyAmount: $("#TxtSumExciseDuty").val().trim(),
//         CustomsDutyRate: $("#TxtCustomsDutyRate").val().trim(),
//         CustomsDutyUOM: $("#TxtCustomsDutyUOM").val().trim(),
//         CustomsDutyAmount: $("#TxtSumCustomsDuty").val().trim(),
//         OtherTaxRate: $("#itemOtherTaxRate").val().trim(),
//         OtherTaxUOM: $("#itemOtherTaxUom").val().trim(),
//         OtherTaxAmount: $("#itemOtherTaxAmount").val().trim(),
//         CurrentLot: $("#CurrentLot").val().trim(),
//         PreviousLot: $("#PreviousLot").val().trim(),
//         LSPValue: $("#itemLastSellingPrice").val().trim(),
//         Making: $("#Making").val(),
//         ShippingMarks1: $("#ShippingMarks1").val().trim(),
//         ShippingMarks2: $("#ShippingMarks2").val().trim(),
//         ShippingMarks3: $("#ShippingMarks3").val().trim(),
//         ShippingMarks4: $("#ShippingMarks4").val().trim(),
//         TouchUser: $("#INONUSERNAME").val().trim(),
//         TouchTime: TOUCHTIME,
//         OptionalChrgeUOM: $("#OptionalChrgeUOM").val().trim(),
//         Optioncahrge: $("#Optioncahrge").val().trim(),
//         OptionalSumtotal: $("#OptionalSumtotal").val().trim(),
//         OptionalSumExchage: $("#OptionalSumExchage").val().trim(),
//       });
//     }
//     ItemResetInNon();
//   }
  
//   $("#Loading").show();
//   $.ajax({
//     type: "POST",
//     url: "/AllItemUpdateInNon/",
//     data: {
//       Item: JSON.stringify(ItemAllDataInNon),
//       PermitId: $("#PermitIDInNon").val(),
//       csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
//     },
//     success: function (response) {
//       ItemData = response.item;
//       ItemLoad();
//       $("#Loading").hide();
//       $('#EditAllItemBtn').prop('disabled', false); // Re-enable the button after AJAX call
//     },
//     error: function (xhr, status, error) {
//       console.error(xhr.responseText);
//       console.log("error");
//       $('#EditAllItemBtn').prop('disabled', false); // Re-enable the button in case of an error
//     }
//   });
// }

function ItemEditAllInNon() {
  console.log('hello');
  $('#EditAllItemBtn').prop('disabled', true);
  $("#Loading").show();
  var ItemAllDataInNon = [];
  var selectedItemHawb = $("#itemHawb").val(); 
  console.log('selectedItemHawb:',selectedItemHawb)
  var selectedItemOutHawbDrop = $("#ItemOutHawbDrop").val(); 
  console.log('selectedItemOutHawbDrop:',selectedItemOutHawbDrop)

  for (var item of ItemData) {
      ItemEditInNon(item.ItemNo);
      var Echeck = true;
      if ($('#itemCascID').prop('checked')) {
          if ($('#itemProductCode1').val() == "") {
              Echeck = false;
          }
      }
      if (Echeck) {
          ItemAllDataInNon.push({
              ItemNo: $("#ITEMNUMBER").val().trim(),
              PermitId: $("#PermitIDInNon").val().trim(),
              MessageType: $("#MsgType").val().trim(),
              HSCode: $("#ItemHsCodeInNon").val().trim(),
              Description: $("#ItemDescriptionInNon").val().trim(),
              DGIndicator: $("#itemDgIndicator").val().trim(),
              Contry: $("#ItemCooInput").val().trim(),
              Brand: $("#itemBrandInput").val().trim(),
              Model: $("#itemModel").val().trim(),
              Vehicletype: $("#VehicalTypeUom").val(),
              Enginecapacity: $("#EngineCapacity").val().trim(),
              Engineuom: $("#EngineCapacityUom").val(),
              Orginregdate: $("#OriginalRegistrationDate").val(),
              InHAWBOBL: selectedItemHawb,
              OutHAWBOBL: selectedItemOutHawbDrop,
              DutiableQty: $("#itemDuitableQty").val(),
              DutiableUOM: $("#ItemDutiableUom").val(),
              TotalDutiableQty: $("#ItemTotalDutiableQtyInput").val().trim(),
              TotalDutiableUOM: $("#ItemTotalDutiableQtyUom").val(),
              InvoiceQuantity: $("#itemInvoiceQuantity").val().trim(),
              HSQty: $("#ItemHsQtyInput").val().trim(),
              HSUOM: $("#ItemHsQtyUom").val(),
              AlcoholPer: $("#itemAlchoholPer").val(),
              InvoiceNo: $("#ItemInvoiceNumberInNon").val(),
              ChkUnitPrice: $("#itemCheckUnitPrice").val().trim(),
              UnitPrice: $("#UnitPrice").val().trim(),
              UnitPriceCurrency: $("#ItemInvoiceCurrencyDrop").val().trim(),
              ExchangeRate: $("#ItemInvoiceCurrencyInput").val().trim(),
              SumExchangeRate: $("#SumExchangeRate").val().trim(),
              TotalLineAmount: $("#iteminvoiceTotalLineAmount").val().trim(),
              InvoiceCharges: $("#iteminvoiceTotalInvoiceCharge").val().trim(),
              CIFFOB: $("#iteminvoiceCIFFOB").val().trim(),
              OPQty: $("#itemOuterPackQtyInput").val().trim(),
              OPUOM: $("#itemOuterPackQtySelect").val().trim(),
              IPQty: $("#itemInPackQuantityInput").val().trim(),
              IPUOM: $("#itemInPackQuantitySelect").val().trim(),
              InPqty: $("#itemInnerPackQtyInput").val().trim(),
              InPUOM: $("#itemInnerPackQtySelect").val().trim(),
              ImPQty: $("#itemInmostPackQtyInput").val().trim(),
              ImPUOM: $("#itemInmostPackQtySelect").val().trim(),
              PreferentialCode: $("#itemPreferntialCode").val().trim(),
              GSTRate: $("#ItemGSTRate").val().trim(),
              GSTUOM: $("#ItemGSTUOM").val().trim(),
              GSTAmount: $("#TxtItemSumGST").val().trim(),
              ExciseDutyRate: $("#TxtExciseDutyRate").val().trim(),
              ExciseDutyUOM: $("#TxtExciseDutyUOM").val().trim(),
              ExciseDutyAmount: $("#TxtSumExciseDuty").val().trim(),
              CustomsDutyRate: $("#TxtCustomsDutyRate").val().trim(),
              CustomsDutyUOM: $("#TxtCustomsDutyUOM").val().trim(),
              CustomsDutyAmount: $("#TxtSumCustomsDuty").val().trim(),
              OtherTaxRate: $("#itemOtherTaxRate").val().trim(),
              OtherTaxUOM: $("#itemOtherTaxUom").val().trim(),
              OtherTaxAmount: $("#itemOtherTaxAmount").val().trim(),
              CurrentLot: $("#CurrentLot").val().trim(),
              PreviousLot: $("#PreviousLot").val().trim(),
              LSPValue: $("#itemLastSellingPrice").val().trim(),
              Making: $("#Making").val(),
              ShippingMarks1: $("#ShippingMarks1").val().trim(),
              ShippingMarks2: $("#ShippingMarks2").val().trim(),
              ShippingMarks3: $("#ShippingMarks3").val().trim(),
              ShippingMarks4: $("#ShippingMarks4").val().trim(),
              TouchUser: $("#INONUSERNAME").val().trim(),
              TouchTime: TOUCHTIME,
              OptionalChrgeUOM: $("#OptionalChrgeUOM").val().trim(),
              Optioncahrge: $("#Optioncahrge").val().trim(),
              OptionalSumtotal: $("#OptionalSumtotal").val().trim(),
              OptionalSumExchage: $("#OptionalSumExchage").val().trim(),
          });
      }
      ItemResetInNon();
  }
  $("#itemHawb").val(selectedItemHawb);
  $("#ItemOutHawbDrop").val(selectedItemOutHawbDrop);

  $("#Loading").show();
  $.ajax({
      type: "POST",
      url: "/AllItemUpdateInNon/",
      data: {
          Item: JSON.stringify(ItemAllDataInNon),
          PermitId: $("#PermitIDInNon").val(),

          SelectedItemHawb: selectedItemHawb,
          SelectedItemOutHawbDrop: selectedItemOutHawbDrop,
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function(response) {
          ItemData = response.item;
          ItemLoad();
          $("#Loading").hide();
          $('#EditAllItemBtn').prop('disabled', false); 
      },
      error: function(xhr, status, error) {
          console.error(xhr.responseText);
          console.log("error");
          $('#EditAllItemBtn').prop('disabled', false); 
      }
  });
}



function OptionalChrgeUOMOut(Val) {
  if (Val == "--Select--" || Val == "--SELECT--") {
    $("#ItemInvoiceCurrencyDrop").val("--Select--");
    $("#ItemInvoiceCurrencyInput").val("0.00");
  } else {
    for (var inv of Currency) {
      if (Val == inv.Currency) {
        $("#Optioncahrge").val(inv.CurrencyRate);
      }
    }
  }
}

function ItemConsolidateInNon() {
  $("#Loading").show();
  $.ajax({
    url: "/ConsolidateInNon/",
    type: "POST",
    data: {
      PermitId: $("#PermitIDInNon").val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      ItemData = response.item;
      CascData = response.casc;
      ItemLoad();
      alert("Consolidate SuccesFully ...!");
      $("#Loading").hide();
    },
    error: function (response) {
      $("#Loading").hide();
    },
  });
}

function ItemDeleteInNon() {
  var CheckArray = [];
  var CheckBoxName = document.getElementsByName("itemCheckDel");
  for (var i of CheckBoxName) {
    if (i.checked) {
      CheckArray.push(i.value);
    }
  }
  if (CheckArray != "") {
    $("#Loading").show();
    $.ajax({
      url: "/AllItemUpdateInNon/",
      type: "GET",
      data: {
        PermitId: $("#PermitIDInNon").val(),
        ItemNo: JSON.stringify(CheckArray),
      },
      success: function (response) {
        ItemData = response.item;
        CascData = response.casc;
        ItemLoad();
        $("#Loading").hide();
        $('#ItemHeadCheck').prop('checked', false)
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

/*------------------------------------------CPC----------------------------------------------------*/

function CpcHideShow(ID, CLASS, Name) {
  if ($(ID).prop("checked")) {
    $(CLASS).show();
  } else {
    $(CLASS).hide();
    $(CLASS + " input").val("");
    $(CLASS + " table")
      .find("tr:gt(1)")
      .remove();
  }
}

function CpcADD(Table, NAME, CLASS) {
  if ($(`${Table} tr`).length < 6) {
    var rowAdd = `<tr>
        <td><input type="text" class="inputStyle"  name = "${NAME}"></td>
            <td><input type="text" class="inputStyle" name = "${NAME}"></td>
            <td><input type="text" class="inputStyle" name = "${NAME}"></td>
            <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCascTable(this)"></i></td>
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

/*------------------------------------------CONTAINER INFO--------------------------------------------*/
var ContainerData = [];
$(document).ready(function () {
  $.ajax({
    url: "/ContainerInNon/",
    data: {
      PermitId: $("#PermitIDInNon").val(),
    },
    success: function (response) {
      $("#declarationType").focus()
      console.log("Container Page Loaded ...!");
      ContainerData = response.ContainerValue;
      ContainerLoad(response.ContainerValue);
      if (ContainerData.length > 0) {
        $("#InpaymentContainerShow").show();
      }
      $("#declarationType").focus()
    },
  });
});

$(document).on("click", ".SaveContainer", function () {
  var row = $(this).closest("tr");
  var Sno = row.find("input:eq(1)").val();
  var ContainerNumber = row.find("input:eq(2)").val();
  var Weight = row.find("input:eq(3)").val();
  var Seal = row.find("input:eq(4)").val();
  var Size = row.find("select:eq(0)").val();
  var check = true;

  row.find("input:eq(2)").next("span").hide();
  row.find("input:eq(3)").next("span").hide();
  row.find("input:eq(4)").next("span").hide();
  row.find("select:eq(0)").next("span").hide();

  var regex = /^[A-Za-z]{4}\d{7}$/;
  if (!regex.test(ContainerNumber)) {
    check = false;
    row.find("input:eq(2)").next("span").show();
  }
  if (Size == "--Select--") {
    check = false;
    row.find("select:eq(0)").next("span").show();
  }
  if (Weight == "") {
    check = false;
    row.find("input:eq(3)").next("span").show();
  }
  if (Seal == "") {
    check = false;
    row.find("input:eq(4)").next("span").show();
  }
  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/ContainerInNon/",
      type: "POST",
      data: {
        Method: "SAVE",
        PermitId: $("#PermitIDInNon").val(),
        RowNo: Sno,
        ContainerNo: ContainerNumber,
        size: Size,
        weight: Weight,
        SealNo: Seal,
        MessageType: $("#MsgType").val(),
        TouchUser: $("#INONUSERNAME").val(),
        TouchTime: TOUCHTIME,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        $("#Loading").hide();
        alert(response.Result);
        ContainerData = response.ContainerValue;
        ContainerLoad(response.ContainerValue);
      },
    });
    CargoResetInNon();
  }
 
});

$(document).on("click", ".containerDeleteBtn", function () {
  var deletedIndex = $(this).closest("tr").index();

  var row = $(this).closest("tr");
  var Sno = row.find("input:eq(1)").val();

  var ContainerNumber = row.find("input:eq(2)").val();
  var Weight = row.find("input:eq(3)").val();
  var Seal = row.find("input:eq(4)").val();
  var Size = row.find("select:eq(0)").val();

  var check = true;

  var regex = /^[A-Za-z]{4}\d{7}$/;
  if (!regex.test(ContainerNumber)) {
    check = false;
    row.find("input:eq(2)").next("span").show();
  }
  if (Size == "--Select--") {
    check = false;
    row.find("select:eq(0)").next("span").show();
  }
  if (Weight == "") {
    check = false;
    row.find("input:eq(3)").next("span").show();
  }
  if (Seal == "") {
    check = false;
    row.find("input:eq(4)").next("span").show();
  }
  if (check) {
    $("#Loading").show();
    $.ajax({
      url: "/ContainerInNon/",
      type: "POST",
      data: {
        Method: "DELETE",
        PermitId: $("#PermitIDInNon").val(),
        SNo: Sno,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        $("#Loading").hide();
        alert(response.Result);
        ContainerData = response.ContainerValue;
        ContainerLoad(response.ContainerValue);
        if (deletedIndex === 0) {
          row.find("input:eq(1)").val("1");
          row.find("input:eq(2)").val("");
          row.find("input:eq(3)").val("");
          row.find("input:eq(4)").val("");
          row.find("select:eq(0)").val("--Select--");
        }
      },
    });
  } else {
    if (deletedIndex !== 0) {
      $(this).closest("tr").remove();
    } else if (deletedIndex === 0) {
    }
  }
});

function InputLenth(input1) {
  var value = input1.value;
  if (value.length > 3) {
    input1.value = value.slice(0, 3);
  }
}

function DeleteContainerBtn() {
  var checkedValues = [];
  $(".ContainerCheckBox:checked").each(function () {
    checkedValues.push($(this).val());
  });
  if (checkedValues.length > 0) {
    $("#Loading").show();
    $.ajax({
      url: "/ContainerInNon/",
      type: "POST",
      data: {
        Method: "CHECKDELETE",
        IDS: JSON.stringify(checkedValues),
        PermitId: $("#PermitIDInNon").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        $("#Loading").hide();
        alert(response.Result);
        ContainerLoad(response.ContainerValue);
      },
    });
  }
}

$(document).on("click", ".ContainerEdit", function () {
  var row = $(this).closest("tr");

  row.find("input:eq(2)").prop("disabled", false);
  row.find("input:eq(3)").prop("disabled", false);
  row.find("input:eq(4)").prop("disabled", false);
  row.find("select:eq(0)").prop("disabled", false);
  row.find("button:eq(0)").prop("disabled", false);
});

function ContainerAllCheckBox(input) {
  if ($(input).prop("checked")) {
    $(".ContainerCheckBox").prop("checked", true);
  } else {
    $(".ContainerCheckBox").prop("checked", false);
  }
}

function AllCheckContainerTable(check) {
  if (!$(check).prop("checked")) {
    $("#ContainercheckBoxThead").prop("checked", false);
  }
}

/*------------------------------------------ATTACH DOCUMENT--------------------------------------------*/
var AttachData;
$(document).ready(function () {
  $.ajax({
    url: "/AttachInNon/",
    data: {
      Method: "LOAD",
      PermitId: $("#PermitIDInNon").val(),
      Type: "NEW",
    },
    success: function (response) {
      console.log("Attach Page Loaded ...!");
      AttachData = response.attachFile;
      AttachLoad(AttachData);
      $("#declarationType").focus()
    },
  });
});

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
    formData.append("FilePath", "/Users/Public/IMG/");
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
      url: "/AttachInNon/",
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

function AttachLoad(Val) {
  let Ans = "";
  for (let At of Val) {
    Ans += `
    <tr>
      <td><i class="fa-solid fa-trash-can" style="color: #ff0000;" onclick = "DeleteAttach('${At.Id}')"></i></td>
      <td>${At.DocumentType}</td>
      <td><a href = '/AttachDownloadInNon/${At.Id}/' style="text-decoration:none">${At.Name}</a></td>
      <td>${At.Size}</td>
    </tr>`;
  }
  if (Val.length > 0) {
    $("#ReferenceDocuments").prop("checked", true);
    $("#ReferenceShow").show();
    $("#HeaderDocumentTableshow").show();
    $("#HeaderAttachTable tbody").html(Ans);
  } else {
    $("#HeaderDocumentTableshow").hide();
  }
}

function DeleteAttach(Arg) {
  $.ajax({
    url: "/AttachInNon/",
    data: {
      Method: "DELETE",
      Data: Arg,
      PermitId: $("#PermitIDInNon").val(),
      Type: "NEW"
    },
    success: function (response) {
      AttachData = response.attachFile;
      AttachLoad(AttachData);
    },
  });
}

/*------------------------------------------SUMMARY----------------------------------------------------*/

function SummaryLoadInNon() {
  $("#summaryNoOfVoice").val("0.00");
  $("#summaryNoOfItems").val("0.00");

  if (InvoiceData.length > 0) {
    $("#summaryNoOfVoice").val(InvoiceData.length);
  }
  if (ItemData.length > 0) {
    $("#summaryNoOfItems").val(ItemData.length);
  }

  var CifSum = 0;
  InvoiceData.forEach((element) => {
    CifSum += Number(element.CIFSUMAmount);
    console.log("CifSum:",CifSum)
  });

  $("#summaryTotalInvoiceCIFValue").val("0.00");
  if (CifSum != 0) {
    $("#summaryTotalInvoiceCIFValue").val(CifSum);
  }
  var InvoiceGst = 0;
  InvoiceData.forEach((element) => {
    InvoiceGst += Number(element.GSTSUMAmount);
    console.log("InvoiceGst:",InvoiceGst)
  });

  $("#SummaryTotalIncoiseGSt").val("");
  if (InvoiceGst != 0) {
    $("#SummaryTotalIncoiseGSt").val(InvoiceGst);
  }

  ItemData.forEach((element) => {
    TotalLineAmd += Number(element.TotalLineAmount);
    GstAmd += Number(element.GSTAmount);
    Cifob += Number(element.CIFFOB);
    ExciseDutyAmd += Number(element.ExciseDutyAmount);
    CustomsDutyAmd += Number(element.CustomsDutyAmount);
    OtherTaxAmd += Number(element.OtherTaxAmount);
  });

  $("#summarySumOfItemValue").val("0.00");
  if (TotalLineAmd != 0) {
    $("#summarySumOfItemValue").val(TotalLineAmd.toFixed(2));
  }

  $("#summaryTotalCIFFOBValue").val("0.00");
  if (Cifob != 0) {
    $("#summaryTotalCIFFOBValue").val(Cifob.toFixed(2));
  }

  $("#summaryExciseDuty").val("0.00");
  if (ExciseDutyAmd != 0) {
    $("#summaryExciseDuty").val(CifSum.toFixed(2));
  }

  $("#summaryTotalGstValue").val("0.00");
  if (GstAmd != 0) {
    $("#summaryTotalGstValue").val(GstAmd.toFixed);
  }

  $("#summaryCustomsDuty").val("0.00");
  if (CustomsDutyAmd != 0) {
    $("#summaryCustomsDuty").val(CustomsDutyAmd.toFixed);
  }

  $("#itemOtherTaxAmountSummary").val("0.00");
  if (OtherTaxAmd != 0) {
    $("#itemOtherTaxAmountSummary").val(OtherTaxAmd.toFixed);
  }
}

function summaryPreviousFunction() {
  var Val = $("#PreviousPermitNo").val();
  $("#summaryTradeRemarks").val("PREVIOUS PERMIT NO : " + Val);
}

function summaryEXRateFunction() {
  let trade = document.getElementById("summaryTradeRemarks");
  let arr1 = [];
  let arr2 = [];
  for (let i = 0; i < InvoiceData.length; i++) {
    if (0 == i) {
      arr1.push(InvoiceData[i].TICurrency);
      arr2.push([InvoiceData[i].TICurrency, InvoiceData[i].TIExRate]);
    } else {
      if (arr1.includes(InvoiceData[i].TICurrency)) {
        var sase = 0;
      } else {
        arr1.push(InvoiceData[i].TICurrency);
        arr2.push([InvoiceData[i].TICurrency, InvoiceData[i].TIExRate]);
      }
    }
  }
  for (let j = 0; j < arr2.length; j++) {
    trade.value = trade.value + " CURRENCY : " + arr2[j][0] + " , EXCHANGE RATE : " + arr2[j][1] + "\n";
  }
}

function summaryConfigBtnFunction() {
  let trade = document.getElementById("summaryTradeRemarks");
  let remark = document.getElementById("summaryFormatRemark").value;
  let sp = trade.value.replaceAll("\n", remark);
  document.getElementById("summaryTradeRemarks").value = sp;
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


function SavePermit() {
  $("span").hide();
  let Header = true;
  let Cargo = true;
  let Party = true;
  let CheckCont = true;
  let Summary = true;

  if ($("#declarationType").val() == "--Select--") {
    Header = false;
    $("#declarationTypeSpan").show();
  }

  if ($("#CargoPackType").val() == "--Select--") {
    Header = false;
    $("#CargoPackTypeSpan").show();
  }

  if ($("#CargoPackType").val() == "--Select--") {
    Header = false;
    $("#CargoPackTypeSpan").show();
  }

  if ($("#AccountId").val() == "KAIZEN") {
    if ($("#DeclaringFor").val() == "--Select--") {
      Header = false;
      $("#DeclaringForSpan").show();
    }
  }

  if ($("#InNonTotOuterPackInput").val() == "") {
    Cargo = false;
    $("#InNonTotOuterPackInputSpan").show();
  }

  if ($("#InNonTotOuterPackDrop").val() == "--Select--") {
    Cargo = false;
    $("#InNonTotOuterPackDropSpan").show();
  }

  if ($("#InNonTotalGrossWeightInput").val() == "") {
    Cargo = false;
    $("#InNonTotalGrossWeightInputSpan").show();
  }

  if ($("#InNonTotalGrossWeightDrop").val() == "--Select--") {
    Cargo = false;
    $("#InNonTotalGrossWeightDropSpan").show();
  }

  if ($("#FreightForwarderCode").val() != "") {
    if ($("#CargoInHawb").val() == "") {
      Cargo = false;
      $("#CargoInHawbSpan").show();
    }
  }

  if ($("#InNonImporterCruei").val() == "") {
    Party = false;
    $("#InNonImporterCrueiSpan").show();
  }

  if ($("#declarationType").val() == "REX : FOR RE-EXPORT") {
    if ($("#ExporterCode").val() == "") {
      Party = false;
      $("#ExporterCodeSpan").show();
    }

    if ($("#ExporterCruei").val() == "") {
      Party = false;
      $("#ExporterCrueiSpan").show();
    }

    if ($("#ExporterName").val() == "") {
      Party = false;
      $("#ExporterNameSpan").show();
    }

    if ($("#ConsignCode").val() == "") {
      Party = false;
      $("#ConsignCodeSpan").show();
    }

    if ($("#ConsignCruei").val() == "") {
      Party = false;
      $("#ConsignCrueiSpan").show();
    }

    if ($("#ConsignName").val() == "") {
      Party = false;
      $("#ConsignNameSpan").show();
    }

    if ($("#ConsignAddress").val() == "") {
      Party = false;
      $("#ConsignAddressSpan").show();
    }

    if ($("#ConsignCountryCode").val() == "") {
      Party = false;
      $("#ConsignCountryCodeSpan").show();
    }

    if ($("#DepartureDate").val() == "") {
      Cargo = false;
      $("#DepartureDateSpan").show();
    }
  }

  if ($("#InNonReleaseInput").val() == "") {
    Cargo = false;
    $("#InNonReleaseInputSpan").show();
  }

  if ($("#InNonReciptInput").val() == "") {
    Cargo = false;
    $("#InNonReciptInputSpan").show();
  }

  if (
    $("#declarationType").val() == "APS : APPROVED PREMISES/SCHEMES" ||
    $("#declarationType").val() == "DES : DESTRUCTION" ||
    $("#declarationType").val() == "GTR : GST RELIEF (& DUTY EXEMPTION)" ||
    $("#declarationType").val() == "SFZ : STORAGE IN FTZ" ||
    $("#declarationType").val() == "SHO : SHUT-OUT" ||
    $("#declarationType").val() ==
    "TCE : TEMPORARY IMPORT FOR EXHIBITION/AUCTIONS WITHOUT SALES" ||
    $("#declarationType").val() ==
    "TCI : TEMPORARY EXPORT / RE-IMPORTED GOODS" ||
    $("#declarationType").val() == "TCO : TEMPORARY IMPORT FOR OTHER PURPOSE" ||
    $("#declarationType").val() == "TCR : TEMPORARY IMPORT FOR REPAIRS" ||
    $("#declarationType").val() ==
    "TCS : TEMPORARY IMPORT FOR EXHIBITION/AUCTIONS WITH SALES"
  ) {
    if ($("#inwardTranseportMode").val() == "--Select--") {
      Header = false;
      $("#inwardTranseportModeSpan").show();
    }
  } else {
    if (
      $("#declarationType").val() !=
      "BKT : BLANKET [INCLUDING BLANKET GST RELIEF (& DUTY EXEMPTION)]"
    ) {
      if ($("#InwardModeInsert").val() != "N : Not Required") {
        if ($("#ArrivalDate").val() == "") {
          Cargo = false;
          $("#ArrivalDateSpan").show();
        }
      }
    }
  }

  if (
    $("#declarationType").val() ==
    "TCE : TEMPORARY IMPORT FOR EXHIBITION/AUCTIONS WITHOUT SALES" ||
    $("#declarationType").val() ==
    "TCE : TEMPORARY IMPORT FOR EXHIBITION/AUCTIONS WITHOUT SALES" ||
    $("#declarationType").val() == "TCO : TEMPORARY IMPORT FOR OTHER PURPOSE" ||
    $("#declarationType").val() == "TCR : TEMPORARY IMPORT FOR REPAIRS" ||
    $("#declarationType").val() ==
    "TCS : TEMPORARY IMPORT FOR EXHIBITION/AUCTIONS WITH SALES"
  ) {
    if ($("#ExhibitionSDate").val() == "") {
      Cargo = false;
      $("#ExhibitionSDateSpan").show();
    }
    if ($("#ExhibitionEDate").val() == "") {
      Cargo = false;
      $("#ExhibitionEDateSpan").show();
    }
  }

  if (
    $("#declarationType").val() ==
    "BKT : BLANKET [INCLUDING BLANKET GST RELIEF (& DUTY EXEMPTION)]"
  ) {
    if ($("#ExhibitionSDate").val() == "") {
      Cargo = false;
      $("#ExhibitionSDateSpan").show();
    }
  }

  if ($("#CargoInHawb").val() != "") {
    if ($("#FreightForwarderCode").val() == "") {
      Party = false;
      $("#FrightCodeSpan").show();
    }
  }

  if ($("#CargoPackType").val() == "") {
    if (ContainerData.length == 0) {
      CheckCont = false;
    }
  }
  if ($("#inwardTranseportMode").val() != "--Select--") {
    if ($("#inwardTranseportMode").val() == "1 : Sea") {
      if ($("#ArrivalDate").val() == "") {
        Cargo = false;
        $("#ArrivalDateSpan").show();
      }

      if ($("#InNonLoadingPortInput").val() == "") {
        Cargo = false;
        $("#InNonLoadingPortInputSpan").show();
      }
      if ($("#VoyageNumber").val() == "") {
        Cargo = false;
        $("#VoyageNumberSpan").show();
      }

      if ($("#VesselName").val() == "") {
        Cargo = false;
        $("#VesselNameSpan").show();
      }

      if ($("#OceanBillofLadingNo").val() == "") {
        Cargo = false;
        $("#OceanBillofLadingNoSpan").show();
      }
    } else if ($("#inwardTranseportMode").val() == "4 : Air") {
      if ($("#ArrivalDate").val() == "") {
        Cargo = false;
        $("#ArrivalDateSpan").show();
      }

      if ($("#InNonLoadingPortInput").val() == "") {
        Cargo = false;
        $("#InNonLoadingPortInputSpan").show();
      }

      if ($("#FlightNO").val() == "") {
        Cargo = false;
        $("#FlightNOSpan").show();
      }

      if ($("#MasterAirwayBill").val() == "") {
        Cargo = false;
        $("#MasterAirwayBillSpan").show();
      }
    } else if (
      $("#inwardTranseportMode").val() == "2 : Rail" ||
      $("#inwardTranseportMode").val() == "3 : Road" ||
      $("#inwardTranseportMode").val() == "5 : Mail" ||
      $("#inwardTranseportMode").val() == "7 : Pipeline" ||
      $("#inwardTranseportMode").val() == "N : Not Required" ||
      $("#inwardTranseportMode").val() == "6 : Multi-model(Not in use)"
    ) {
      if ($("#ArrivalDate").val() == "") {
        Cargo = false;
        $("#ArrivalDateSpan").show();
      }

      if ($("#InNonLoadingPortInput").val() == "") {
        Cargo = false;
        $("#InNonLoadingPortInputSpan").show();
      }
    }
  }

  if ($("#SummaryMRD").val() == "") {
    $("#SummaryMRDSpan").hide();
    Summary = false;
  }

  if ($("#SummaryTIME").val() == "") {
    $("#SummaryTIMESpan").hide();
    Summary = false;
  }

  if ($("#DeclareIndicator").val() == "False") {
    alert("PLEASE CHECK DECLARATION INDICATOR");
    Summary = false;
  }
  let AmendCheck = true;
  $("#AmendTypeError").hide();
  if ($("#StatusType").val() == "AME") {
    if ($("#AmendType").val() == "--Select--") {
      AmendCheck = false;
      $("#AmendTypeError").show();
    }
    if ($("#AmendDescription").val() == "") {
      AmendCheck = false;
      $("#AmendDescriptionError").show();
    }
    if (!$("#AmendDeclareIndicator").prop("checked")) {
      AmendCheck = false;
      alert("PLEASE CHECK THE INDICATOR")
    }
  }

  let CancelCheck = true;



  let Check = true;
  let Tag = "";
  if (!Header) {
    Check = false;

    Tag += "<h1 class='FinalH1'>PLEASE CHECK THE HEADER PAGE</h1><hr>"
  }

  if (!Cargo) {
    Check = false;
    Tag += "<h1 class='FinalH1'>PLEASE CHECK THE CARGO PAGE</h1><hr>"
  }

  if (!Party) {
    Check = false;
    Tag += "<h1 class='FinalH1'>PLEASE CHECK THE PARTY PAGE</h1><hr>"
  }

  if (!CheckCont) {
    Check = false;
    Tag += "<h1 class='FinalH1'>PLEASE CHECK THE CONTAINER PAGE</h1><hr>"
  }

  if (!Summary) {
    Check = false;
    Tag += "<h1 class='FinalH1'>PLEASE CHECK THE SUMMARY PAGE</h1><hr>"
  }

  if (InvoiceData.length == 0) {
    Check = false;
    Tag += "<h1 class='FinalH1'>PLEASE ADD INVOICE DATA </h1><hr>"
  }

  if (ItemData.length == 0) {
    Check = false;
    Tag += "<h1 class='FinalH1'>PLEASE ADD ITEM DATA </h1><hr>"
  }

  if (!AmendCheck) {
    Check = false;
    Tag += "<h1 class='FinalH1'>PLEASE CHECK THE AMEND</h1><hr>"
  }

  if (Check) {
    SavePermitData();
  }
  else {
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

function DateCalculationSave(Arg) {
  if ($("#" + Arg).val() == "") {
    return "1900-01-01";
  }
  var ArrivalDate = $("#" + Arg)
    .val()
    .split("/");
  ArrivalDate = `${ArrivalDate[2]}/${ArrivalDate[1]}/${ArrivalDate[0]}`;
  return ArrivalDate;
}

function SavePermitData() {
  if ($("#StatusType").val() == "AME") {
    prmtStatus = "AME"
  }
  else if ($("#StatusType").val() == "CNL") {
    prmtStatus = "CNL"
  }
  else {
    prmtStatus = "NEW"
  }
  $("#Loading").show();
  $.ajax({
    url: "/InNonSave/",
    type: "POST",
    data: {
      CpcData: JSON.stringify(CpcSaveFunction()),
      StatusType: prmtStatus,
      Refid: $("#REFID").val(),
      JobId: $("#JOBID").val(),
      MSGId: $("#MSGID").val(),
      PermitId: $("#PermitIDInNon").val(),
      TradeNetMailboxID: $("#MailBoxId").val(),
      MessageType: $("#MsgType").val(),
      DeclarationType: $("#declarationType").val(),
      PreviousPermit: $("#PreviousPermitNo").val(),
      CargoPackType: $("#CargoPackType").val(),
      InwardTransportMode: $("#inwardTranseportMode").val(),
      OutwardTransportMode: $("#OutwardTranseportMode").val(),
      BGIndicator: $("#BgIndicator").val(),
      SupplyIndicator: $("#SupplyIndicator").val(),
      ReferenceDocuments: $("#ReferenceDocuments").val(),
      License: $("#License1").val() + "-" + $("#License2").val() + "-" + $("#License3").val() + "-" + $("#License4").val() + "-" + $("#License5").val(),
      Recipient: $("#Recipient1").val() + "-" + $("#Recipient2").val() + "-" + $("#Recipient3").val(),
      DeclarantCompanyCode: $("#declarationCompanyCode").val(),
      ImporterCompanyCode: $("#InNonImporterCode").val(),
      ExporterCompanyCode: $("#ExporterCode").val(),
      InwardCarrierAgentCode: $("#InwardCode").val(),
      OutwardCarrierAgentCode: $("#OutWardCarreirCode").val(),
      ConsigneeCode: $("#ConsignCode").val(),
      FreightForwarderCode: $("#FreightForwarderCode").val(),
      ClaimantPartyCode: $("#ClaimantName").val(),
      ArrivalDate: DateCalculationSave("ArrivalDate"),
      LoadingPortCode: $("#InNonLoadingPortInput").val(),
      VoyageNumber: $("#VoyageNumber").val(),
      VesselName: $("#VesselName").val(),
      OceanBillofLadingNo: $("#OceanBillofLadingNo").val(),
      ConveyanceRefNo: $("#ConveyanceRefNo").val(),
      TransportId: $("#TransportId").val(),
      FlightNO: $("#FlightNO").val(),
      AircraftRegNo: $("#AircraftRegNo").val(),
      MasterAirwayBill: $("#MasterAirwayBill").val(),
      ReleaseLocation: $("#InNonReleaseInput").val(),
      RecepitLocation: $("#InNonReciptInput").val(),
      RecepilocaName: $("#InNonReciptInputText").val(),
      StorageLocation: $("#InNonStorageInput").val(),
      ExhibitionSDate: DateCalculationSave("ExhibitionSDate"),
      ExhibitionEDate: DateCalculationSave("ExhibitionEDate"),
      BlanketStartDate: DateCalculationSave("BlanketStartDate"),
      TradeRemarks: $("#summaryTradeRemarks").val(),
      InternalRemarks: $("#summaryInternalRemarks").val(),
      DepartureDate: DateCalculationSave("DepartureDate"),
      DischargePort: $("#InNonDisachargeInput").val(),
      FinalDestinationCountry: $("#InNonFinalDestinationSelect").val(),
      OutVoyageNumber: $("#OutVoyageNumber").val(),
      OutVesselName: $("#InNonOutVesselNameInput").val(),
      OutOceanBillofLadingNo: $("#OutOceanBillofLadingNo").val(),
      VesselType: $("#InNonVesselTypeDrop").val(),
      VesselNetRegTon: $("#InNonVesselNetRegisterInput").val(),
      VesselNationality: $("#InNonVesselNationalityDrop").val(),
      TowingVesselID: $("#InNonTowingVesselIdInput").val(),
      TowingVesselName: $("#InNonTowingVesselNameInput").val(),
      NextPort: $("#InNonNextPortInput").val(),
      LastPort: $("#InNonLastPortInput").val(),
      OutConveyanceRefNo: $("#InNonOutConveyanceInput").val(),
      OutTransportId: $("#InNonOutTranseportIdInput").val(),
      OutFlightNO: $("#InNonOutFlightNumberInput").val(),
      OutAircraftRegNo: $("#InNonOutAirCraftInput").val(),
      OutMasterAirwayBill: $("#InNonOutMawbInput").val(),
      TotalOuterPack: $("#InNonTotOuterPackInput").val(),
      TotalOuterPackUOM: $("#InNonTotOuterPackDrop").val(),
      TotalGrossWeight: $("#CargoPermitGrossWeight").val(),
      TotalGrossWeightUOM: $("#InNonTotalGrossWeightDrop").val(),
      GrossReference: $("#GrossReference").val(),
      DeclareIndicator: $("#DeclareIndicator").val(),
      NumberOfItems: $("#summaryNoOfItems").val(),
      TotalCIFFOBValue: $("#summaryTotalCIFFOBValue").val(),
      TotalGSTTaxAmt: $("#summaryTotalGstValue").val(),
      TotalExDutyAmt: $("#summaryExciseDuty").val(),
      TotalCusDutyAmt: $("#summaryCustomsDuty").val(),
      TotalODutyAmt: $("#itemOtherTaxAmountSummary").val(),
      TotalAmtPay: $("#summaryTotalPayable").val(),
      Status: "NEW",
      TouchUser: $("#INONUSERNAME").val(),
      TouchTime: TOUCHTIME,
      PermitNumber: $("#PermitNumberId").val(),
      prmtStatus: prmtStatus,
      ReleaseLocaName: $("#InNonReleaseText").val(),
      Inhabl: $("#CargoInHawb").val(),
      outhbl: $("#InNonOutHblHawbInput").val(),
      seastore: $("#InNonSeaStoreId").val(),
      Cnb: $("#CNB").val(),
      DeclarningFor: $("#DeclaringFor").val(),
      MRDate: DateCalculationSave("SummaryMRD"),
      MRTime: $("#SummaryTIME").val(),

      /*------------------------------AMEND DATAS--------------------------------------*/
      Permitno: $("#AmendPermitNumber").val(),
      AmendmentCount: $("#AmendCount").val(),
      UpdateIndicator: $("#AmendUpdateIndicator").val(),
      ReplacementPermitno: $("#AmendPermitNumberReplacement").val(),
      DescriptionOfReason: $("#AmendDescription").val(),
      PermitExtension: $("#AmendPermitValidity").val(),
      ExtendImportPeriod: $("#AmendExtendPeriod").val(),
      DeclarationIndigator: $("#AmendDeclareIndicator").val(),
      AmendType: $("#AmendType").val(),
      /*--------------------------CANCEL DATAS------------------------------------------*/

      CancelPermitno: $("#CancelPermitNumber").val(),
      CancelUpdateIndicator: $("#CancelUpdateIndicator").val(),
      CancelReplacementPermitno: $("#CancelPermitNumberReplacement").val(),
      ResonForCancel: $("#ResonForCancel").val(),
      CancelDescriptionOfReason: $("#DescriptionOfReason").val(),
      CancelDeclarationIndigator: $("#CancelDeclareIndicator").val(),
      CancelType: $("#CancelationType").val(),

      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (response) {
      window.location.href = response
    }
  });
}


// function SummaryPage() {
  
//   $("#SummaryImporter").html("<p>"+ $("#InNonImporterCruei").val() + "-" + $("#InNonImporterName").val()+ "-" + $("#InNonImporterName1").val()+ "</p>");
//   $("#SummaryTotalGst").html("<p>"+ $("#summaryTotalGstValue").val() + "</p>");
//   // $("#SummaryInMawbObl").html("<p>"+ $("#InNonOutMawbInput").val() + "</p>");
//   $("#SummaryInMawbObl").html("<p>"+ $("#OceanBillofLadingNo").val() + "</p>") ||  $("#SummaryInMawbObl").html("<p>"+ $("#MasterAirwayBill").val() + "</p>")
 
// }

function SummaryPage() {
  $("#SummaryImporter").html("<p>"+ $("#InNonImporterCruei").val() + "-" + $("#InNonImporterName").val()+ "-" + $("#InNonImporterName1").val()+ "</p>");
  $("#SummaryTotalGst").html("<p>"+ $("#summaryTotalGstValue").val() + "</p>");

  var oceanBillOfLadingNo = $("#OceanBillofLadingNo").val();
  var masterAirwayBill = $("#MasterAirwayBill").val();

  if (oceanBillOfLadingNo || masterAirwayBill) {
    $("#SummaryInMawbObl").html("<p>" + (oceanBillOfLadingNo || masterAirwayBill) + "</p>");
  }
}



function SummaryInvoiceSumofInvoiceAmount(invoiceCurAmountARR) {
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

function SummarySumofItemAmd(itemCurAmountARR) {
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

function CpcSaveFunction() {

  var CpcData = [];

  if ($("#Aeo").prop("checked")) {
    let Row = 1
    let InpName = document.getElementsByName("AeoName")
    for (let i = 0; i < InpName.length; i = i + 3) {
      if (InpName[i].value != "") {
        CpcData.push([Row, "AEO", InpName[i].value, InpName[i + 1].value, InpName[i + 2].value])
        Row += 1;
      }

    }
  }

  if ($("#Cwc").prop("checked")) {
    let Row = 1
    let InpName = document.getElementsByName("CwcName")
    for (let i = 0; i < InpName.length; i = i + 3) {
      if (InpName[i].value != "") {
        CpcData.push([Row, "CWC", InpName[i].value, InpName[i + 1].value, InpName[i + 2].value])
        Row += 1;
      }
    }
  }

  if ($("#Sea").prop("checked")) {
    let Row = 1
    let InpName = document.getElementsByName("SeaName")
    for (let i = 0; i < InpName.length; i = i + 3) {
      if (InpName[i].value != "") {
        CpcData.push([Row, "SEASTORE", InpName[i].value, InpName[i + 1].value, InpName[i + 2].value])
        Row += 1;
      }
    }
  }

  if ($("#Scheme").prop("checked")) {
    let Row = 1
    let InpName = document.getElementsByName("SchemeName")
    for (let i = 0; i < InpName.length; i = i + 3) {
      if (InpName[i].value != "") {
        CpcData.push([Row, "SCHEME", InpName[i].value, InpName[i + 1].value, InpName[i + 2].value])
        Row += 1;
      }
    }
  }

  if ($("#Inter").prop("checked")) {
    let Row = 1
    let InpName = document.getElementsByName("InterName")
    for (let i = 0; i < InpName.length; i = i + 3) {
      if (InpName[i].value != "") {
        CpcData.push([Row, "IPE", InpName[i].value, InpName[i + 1].value, InpName[i + 2].value])
        Row += 1;
      }
    }
  }

  return CpcData;

}

function CpcDataLoad() {
  let aeo = "";
  let cwc = "";
  let sea = "";
  let scheme = "";
  let inter = "";
  let aeoCheck = false;
  let cwcCheck = false;
  let seaCheck = false;
  let schemeCheck = false;
  let interCheck = false;
  CpcData.forEach(
    function (cpc) {
      if (cpc.CPCType == "AEO") {
        aeoCheck = true
        $("#Aeo").prop("checked", true)
        $(".AeoClass").show();
        aeo += `<tr>
            <td><input type="text" class="inputStyle"  name = "AeoName" value = "${cpc.ProcessingCode1}"></td>
            <td><input type="text" class="inputStyle" name = "AeoName" value = "${cpc.ProcessingCode2}"></td>
            <td><input type="text" class="inputStyle" name = "AeoName" value = "${cpc.ProcessingCode3}"></td>
            <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCpcDeleteDataBase(this,'${cpc.Id}')"></i></td>
        </tr>`
      }

      if (cpc.CPCType == "CWC") {
        cwcCheck = true;
        $("#Cwc").prop("checked", true)
        $(".CwcClass").show();
        cwc += `<tr>
            <td><input type="text" class="inputStyle"  name = "CwcName" value = "${cpc.ProcessingCode1}"></td>
            <td><input type="text" class="inputStyle" name = "CwcName" value = "${cpc.ProcessingCode2}"></td>
            <td><input type="text" class="inputStyle" name = "CwcName" value = "${cpc.ProcessingCode3}"></td>
            <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCpcDeleteDataBase(this,'${cpc.Id}')"></i></td>
        </tr>`
      }

      if (cpc.CPCType == "SEASTORE") {
        seaCheck = true;
        $("#Sea").prop("checked", true)
        $(".SeaClass").show();
        sea += `<tr>
            <td><input type="text" class="inputStyle"  name = "SeaName" value = "${cpc.ProcessingCode1}"></td>
            <td><input type="text" class="inputStyle" name = "SeaName" value = "${cpc.ProcessingCode2}"></td>
            <td><input type="text" class="inputStyle" name = "SeaName" value = "${cpc.ProcessingCode3}"></td>
            <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCpcDeleteDataBase(this,'${cpc.Id}')"></i></td>
        </tr>`
      }

      if (cpc.CPCType == "SCHEME") {
        schemeCheck = true;
        $("#Scheme").prop("checked", true)
        $(".SchemeClass").show();
        scheme += `<tr>
            <td><input type="text" class="inputStyle"  name = "SchemeName" value = "${cpc.ProcessingCode1}"></td>
            <td><input type="text" class="inputStyle" name = "SchemeName" value = "${cpc.ProcessingCode2}"></td>
            <td><input type="text" class="inputStyle" name = "SchemeName" value = "${cpc.ProcessingCode3}"></td>
            <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCpcDeleteDataBase(this,'${cpc.Id}')"></i></td>
        </tr>`
      }

      if (cpc.CPCType == "IPE") {
        interCheck = true;
        $("#Inter").prop("checked", true)
        $(".InterClass").show();
        inter += `<tr>
            <td><input type="text" class="inputStyle"  name = "InterName" value = "${cpc.ProcessingCode1}"></td>
            <td><input type="text" class="inputStyle" name = "InterName" value = "${cpc.ProcessingCode2}"></td>
            <td><input type="text" class="inputStyle" name = "InterName" value = "${cpc.ProcessingCode3}"></td>
            <td><i class="fa-regular fa-trash-can" style="color: #ff0000;" onclick="DeleteCpcDeleteDataBase(this,'${cpc.Id}')"></i></td>
        </tr>`
      }
    }
  )
  if (aeoCheck) {
    $("#AeoTable tbody").html(aeo)
  }
  if (cwcCheck) {
    $("#CwcTable tbody").html(cwc)
  }
  if (seaCheck) {
    $("#SeaTable tbody").html(sea)
  }
  if (schemeCheck) {
    $("#SchemeTable tbody").html(scheme)
  }
  if (interCheck) {
    $("#InterTable tbody").html(inter)
  }
}

function DeleteCpcDeleteDataBase(TAB, ID) {
  $.ajax({
    url: "/CpcDeleteInNon/" + ID + "/"
  })
  var deletedIndex = $(TAB).closest("tr").index();
  var row = $(TAB).closest("tr");
  if (deletedIndex !== 0) {
    $(TAB).closest("tr").remove();
  } else if (deletedIndex === 0) {
    row.find("input:eq(0)").val("");
    row.find("input:eq(1)").val("");
    row.find("input:eq(2)").val("");
  }
}


function CancelDocumentAttch() {
  let check = true;
  if ($("#CanceldocumentType").val() == "--Select--") {
    check = false;
  }
  if ($("#CancelAttach").val() == "") {
    check = false;
  }
  if (check) {
    var FileName = "CancelAttach";
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
    formData.append("DocumentType", $("#CanceldocumentType").val());
    formData.append("InPaymentId", MeesageID);
    formData.append("FilePath", "/Users/Public/IMG/");
    formData.append("Size", size + " KB");
    formData.append("PermitId", PermitId);
    formData.append("UserName", UserName);
    formData.append("TouchTime", TOUCHTIME);
    formData.append("Type", "CNL");
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
      url: "/AttachInNon/",
      processData: false,
      contentType: false,
      mimeType: "multipart/form-data",
      data: formData,
      success: function (response) {
        $("#Loading").hide();
        CancelAttachLoad(response.attachFile)
      },
    });
  } else {
    alert("PLEASE SELECT THE DOCUMENT TYPE OR INSERT THE FILE ");
  }
}

function CancelAttachLoad(Val) {
  let Ans = "";
  for (let At of Val) {
    Ans += `
    <tr>
      <td><i class="fa-solid fa-trash-can" style="color: #ff0000;" onclick = "CancelDeleteAttach('${At.Id}')"></i></td>
      <td>${At.DocumentType}</td>
      <td><a href = '/AttachDownloadInNon/${At.Id}/' style="text-decoration:none">${At.Name}</a></td>
      <td>${At.Size}</td>
    </tr>`;
  }
  if (Val.length > 0) {
    $("#CancelDocumentTableshow").show();
    $("#CancelAttachTable tbody").html(Ans);
  } else {
    $("#CancelDocumentTableshow").hide();
  }
}

function CancelDeleteAttach(Arg) {
  $.ajax({
    url: "/AttachInNon/",
    data: {
      Method: "DELETE",
      Data: Arg,
      PermitId: $("#PermitIDInNon").val(),
      Type: "CNL"
    },
    success: function (response) {
      CancelAttachLoad(response.attachFile);
    },
  });
}