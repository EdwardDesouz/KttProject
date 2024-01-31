$(document).ready(function () {
    $("#OUT").css("background-color", "white");
    $("#OUT a").css("color", "green");
    $("#INPAYMENT").css("background-color", "rgb(25, 135, 84)");
    $("#INPAYMENT a").css("color", "white");
    /*--------------------------------Urls--------------------------------*/
});

function NewButton() {
    window.location.href = '/Out/';
}


var listBoxData = [];
$("#Loading").hide();

$(document).ready(function () {
    var table = $('#InonPaymentTable').DataTable({
        "ajax": {
            "processing": true,
            "url": "/outListTable/",
            "dataSrc": "",
        },
        "initComplete": function (data) {
            listBoxData = data.json;
        },
        "dom": 'rtip',
        "columns": [{
            "data": "ID"//0
        },
        {
            "data": "ID"
        },
        {
            "data": "ID"
        },
        {
            "data": "PermitId"
        },
        {
            "data": "JOBID"//4
        },
        {
            "data": "MSGID"
        },
        {
            "data": "DECDATE"
        },
        {
            "data": "DECTYPE"
        },
        {
            "data": "CREATE"
        },
        {
            "data": "DECID"//9
        },
        {
            "data": "ETD"
        },
        {
            "data": "PERMITNO"
        },
        {
            "data": "EXPORTER"
        },
        {
            "data": "HAWB"
        },
        {
            "data": "MAWBOBL"
        },
        {
            "data": "POD"
        },
        {
            "data": "COTYPE"//16
        },
        {
            "data": "CERTTYPE"//17
        },
        {
            "data": "CERTNO"//18
        },
        {
            "data": "MSGTYPE"//19
        },
        {
            "data": "TPT"//20
        },
        {
            "data": "PREPMT"//21
        },
        {
            "data": "XREF"//22
        },
        {
            "data": "INTREM"
        },
        {
            "data": "STATUS"
        },
        ],
        "ordering": false,
        "autoWidth": false,
        'columnDefs': [{
            'targets': 0,
            'searchable': false,
            'orderable': false,
            'render': function (data, type, full, meta) {
                return `<input type="checkbox" name="InNonPayementCheckBox" value="${data}"  onclick="listChcekBoxFunction()">`;
            }
        },
        {
            'targets': 1,
            "width": "10px",
            "className": "text-center",
            'render': function (data, type, full, meta) {
                return `<i class="fa-solid fa-trash-can" style="color: #ff0000;" onclick = "InpaymentDelete('${data}')"></i>`
            }
        },
        {
            'targets': 2,
            "width": "10px",
            "className": "text-center",
            'render': function (data, type, full, meta) {
                if (full.STATUS == "NEW" || full.STATUS == "DRF") {
                    return `<a href="/outEdit/${data}/"><i class="fa-regular fa-pen-to-square" style="color: #ff0000;"></i></a>`
                } else {
                    return `<i class="fa-regular fa-pen-to-square disable" style="color: #ff0000;" ></i>`
                }
            }
        },
        {
            'targets': 3,
            "width": "10px",
            "className": "text-center",
            'render': function (data, type, full, meta) {
                return `<i class="fa-regular fa-eye" style="color: #ff0000;" onclick = "InpaymentShow('${data}')"></i>`
            }
        },
        {
            "width": "50px",
            "targets": [4, 9, 16, 17, 18, 19, 20, 21, 22],
            "className": "text-center",
            "visible": false,
        },
        {
            "width": "50px",
            "targets": 5,
            "className": "text-center"
        },
        {
            "width": "70px",
            "targets": 6,
            "className": "text-center"
        },
        {
            "width": "70px",
            "targets": 10,
            "className": "text-center"
        },
        {
            "width": "300px",
            "targets": 12,
        },
        {
            "width": "100px",
            "targets": 16,
        },
        ],
    });
    $('#InnonPaymentNoofRows').on('change', function () {
        var selectedValue = $(this).val();
        $('#InonPaymentTable').DataTable().page.len(selectedValue).draw();
    });
    $("#InonPaymentTable tfoot tr input").on('keyup change', function () {
        table
            .column($(this).parent().index() + ':visible')
            .search(this.value)
            .draw();
    });
    $('#InonPaymentTableSearch').keyup(function () {
        table.search($(this).val()).draw();
        console.log($(this).val());
    });
});

function InNonPaymentEdit(arg) {
    console.log("The Arg : ", arg)
    $.ajax({
        url: "/InonPayementEdit/",
        type: "GET",
        data: {
            "InNonId": arg,
        },
        success: function (response) {
            window.location.href = response.url; 
        }
    })
    console.log(arg)
}

function InpaymentShow(Arg) {
    console.log(Arg)
}

function InpaymentDelete(Arg) {

    console.log(Arg)


    $.ajax({
        url: "/OutDelete/" + Arg + "/",
        type: "GET",
        success: function (response) {
            window.location.href = "";
        }
    })
}

function FilterPermits() {
    $('#FootStatus').val($("#InonPaymentFilter").val());
    var selectedValue = $('#InonPaymentFilter').val();
    console.log(selectedValue)
    var dataTable = $('#InonPaymentTable').DataTable();
    dataTable.column(24).search(selectedValue).draw();
}

function HtaHide(val1, ID) {
    let cbox = document.getElementById(ID);
    var table = $('#InonPaymentTable').DataTable();
    if (cbox.checked) {
        table.column(Number(val1) + 3).visible(true);
    } else {
        table.column(Number(val1) + 3).visible(false);
    }
}

function InNonCopy() {
    var ChechValue = document.getElementsByName("InNonPayementCheckBox")
    ChechValue.forEach(
        function (v) {
            if (v.checked) {
                console.log(v.value);
                window.location.href = '/OutPaymentCopy/' + v.value + '/'
                // $.ajax({
                //     url: "/CopyInNonPayment/",
                //     data: {
                //         "Id": v.value
                //     },
                //     success: function (response) {
                //         console.log(response)
                //         window.location.href = "/InonPayementEdit/"
                //     }
                // })
            }
        }
    )
}

function InNonAmend() {
    var ChechValue = document.getElementsByName("InNonPayementCheckBox")
    ChechValue.forEach(
        function (v) {
            if (v.checked) {
                window.location.href = "/InonPayementAmend/" + v.value + "/";
            }
        }
    )
}
function InNonCanecl() {
    document.getElementsByName("InNonPayementCheckBox").forEach(
        function (v) {
            if (v.checked) {
                window.location.href = "/InonPayementCancel/" + v.value + "/";
            }
        }
    )
}

function TransmitDataClick() {
    let ArrayVal = [];
    var ChechValue = document.getElementsByName("InNonPayementCheckBox");
    let TrasnMitValue = $("#InnonPaymentTransmitData").val()
    ChechValue.forEach(
        function (Val) {
            if (Val.checked) {
                ArrayVal.push(Val.value)
            }
        }
    )
    console.log(ArrayVal)

    if (ArrayVal.length > 0 && TrasnMitValue != "--Select--") {
        $("#Loading").show();
        $.ajax({
            url: "/InNonTransmitData/",
            type: "GET",
            data: {
                my_data: JSON.stringify(ArrayVal),
                mailId: TrasnMitValue
            },
            success: function (response) {
                $("#Loading").hide();
                console.log(response)
                window.location.href = "/InonPaymentList/";
            }
        });
    }
    else {
        alert("PLEASE SELECT THE TRANSMIT DATA VALUE")
    }
}

function ListAllCheckSubmit() {
    let check = document.getElementById("ListAllCheckSubmitId")
    let downCheck = document.getElementsByName("inpaymentCheck");
    for (let i of downCheck) {
        if (check.checked) {
            i.checked = true;
        } else {
            i.checked = false;
        }
    }
    listChcekBoxFunction();
}

function listChcekBoxFunction() {
    let BoxVal = [];
    let CheckBoxs = document.getElementsByName("InNonPayementCheckBox")

    listBoxData.forEach(
        function (data) {
            CheckBoxs.forEach(
                function (Val) {
                    if (Val.checked) {
                        if (Val.value == data.id) {
                            BoxVal.push(data.STATUS)
                        }
                    }
                }
            )
        }
    )

    $(".InnonPayemnt-list-Buttons button").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
    $("#SubmitBtn").prop("disabled", false).css("background-color", 'indianred')
    if (BoxVal.length == 1) {
        if (BoxVal[0] == "APR" || BoxVal[0] == "AME") {
            $("#SubmitBtn").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#PrintStatusBtn").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#DeleteAllBtn").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
        }
        else if (BoxVal[0] == "DEL" || BoxVal[0] == "ERR") {
            $(".InnonPayemnt-list-Buttons button").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#NewBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#CopyBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#MergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#UnMergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
        }
        else if (BoxVal[0] == "NEW" || BoxVal[0] == "DRF") {
            $("#AmendBtn").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#CancelBtn").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#PrintStatusBtn").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#DeleteAllBtn").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
        }
        else if (BoxVal[0] == "QRY" || BoxVal[0] == "REJ") {
            $(".InnonPayemnt-list-Buttons button").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#NewBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#CopyBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#PrintStatusBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#MergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#UnMergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
        }
        else if (BoxVal[0] == "CNL") {
            $(".InnonPayemnt-list-Buttons button").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#NewBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#PrintStatusBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#MergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#UnMergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
        }
    }
    else if (BoxVal.length > 1) {
        let check = true;
        let FstVal = BoxVal[0]
        BoxVal.forEach(
            function (Res) {
                if (Res == FstVal) {
                    check = true;
                }
                else {
                    check = false;
                    return;
                }
            }
        )

        if (check) {
            $(".InnonPayemnt-list-Buttons button").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#NewBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#MergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#UnMergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#PrintCcpBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })

            if (FstVal == "APR") {
                $("#DownloadCcpBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
                $("#DownloadDataBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            }
            else if (FstVal == "NEW") {
                $("#SubmitBtn").prop("disabled", false).css({ "background-color": 'indianred', 'color': "#fff" })
                $("#DownloadDataBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
                $("#DeleteAllBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            }
            else if (FstVal == "DRF") {
                $("#DownloadDataBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
                $("#DeleteAllBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            }
            else if (FstVal == "AME") {
                $("#DownloadCcpBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            }
            else if (FstVal == "CNL" || FstVal == "QRY" || FstVal == "REJ" || FstVal == "ERR" || FstVal == "DEL") {
                //$("#PrintCcpBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
                $("#PrintCcpBtn").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            }
        }
        else {
            $(".InnonPayemnt-list-Buttons button").prop("disabled", true).css({ "background-color": 'rgb(246, 255, 223)', "color": 'rgb(25, 135, 84)' })
            $("#NewBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#MergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
            $("#UnMergeBtn").prop("disabled", false).css({ "background-color": 'rgb(25, 135, 84)', 'color': "#fff" })
        }
    }
}

function XmlInNon() {
    let ArrayVal = [];
    var ChechValue = document.getElementsByName("InNonPayementCheckBox");
    ChechValue.forEach(
        function (Val) {
            if (Val.checked) {
                ArrayVal.push(Val.value)
            }
        }
    )
    if (ArrayVal.length > 0) {
        $("#Loading").hide();
        $.ajax({
            url: "/XmlGenInNon/",
            type: "GET",
            data: {
                my_data: JSON.stringify(ArrayVal),
            },
            success: function (response) {
                $("#Loading").hide();
                console.log(response)
            }
        });
    }
}

function PrintCcpInNon() {
    let ccp = [];
    var ChechValue = document.getElementsByName("InNonPayementCheckBox")
    ChechValue.forEach(
        function (v) {
            if (v.checked) {
                ccp.push(v.value)
            }
        }
    )
    if (ccp != "") {
        window.location.href = "/InNonPaymentCcp/" + ccp.join(",") + "/";
    }
}

function DownloadCcpInNon() {
    let ccp = [];
    var ChechValue = document.getElementsByName("InNonPayementCheckBox")
    ChechValue.forEach(
        function (v) {
            if (v.checked) {
                ccp.push(v.value)
            }
        }
    )
    if (ccp != "") {
        window.location.href = "/DownloadCcpInNon/" + ccp.join(",") + "/";
    }
}

function PrintGstInNon() {
    let downCheck = document.getElementsByName("InNonPayementCheckBox");
    for (let i of downCheck) {
        if (i.checked) {
            window.location.assign("/PrintGstInNon/" + i.value + "/");
        }
    }
}

function InNonPrintStatus() {
    let downCheck = document.getElementsByName("InNonPayementCheckBox");
    for (let i of downCheck) {
        if (i.checked) {
            window.location.assign("/PrintStatusInNon/" + i.value + "/");
        }
    }
}

function DeleteAllInNon() {
    let ccp = [];
    var ChechValue = document.getElementsByName("InNonPayementCheckBox")
    ChechValue.forEach(
        function (v) {
            if (v.checked) {
                ccp.push(v.value)
            }
        }
    )
    if (ccp != "") {
        window.location.href = "/DeleteAllInNon/" + ccp.join(",") + "/";
    }
}

function DownloadDataInNon() {
    let ccp = [];
    var ChechValue = document.getElementsByName("InNonPayementCheckBox")
    ChechValue.forEach(
        function (v) {
            if (v.checked) {
                ccp.push(v.value)
            }
        }
    )
    if (ccp != "") {
        window.location.href = "/DownloadDataInNon/" + ccp.join(",") + "/";
    }
}

function InNonSubmit() {
    var checkArr = [];
    var check = false;
    let downCheck = document.getElementsByName('InNonPayementCheckBox');
    for (let i of downCheck) {
        if (i.checked) {
            check = true;
            checkArr.push(i.value)
        }
    }
    if (check) {
        $('#Loading').show();
        PermitNumber = JSON.stringify(checkArr)
        $.ajax({
            type: "GET",
            url: "/outTransmit/",
            data: {
                "PermitNumber": PermitNumber,
            },
            success: function (data) {
                alert("All Data SuccessFully Submitted")
                $('#Loading').hide();
            },
            error: function () {
                alert("Error")
                $('#Loading').hide();
            }
        })
    }
}