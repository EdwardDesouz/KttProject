var listBoxData = [];
let delStatusArray = [];
$("#Loading").hide();
$(document).ready(function () {
    $("#COOLIST").css("background-color", "white");
    $("#COOLIST a").css("color", "green");
    $("#INPAYMENT").css("background-color", "rgb(25, 135, 84)");
    $("#INPAYMENT a").css("color", "white");

    /*--------------------------------Urls--------------------------------*/
});

function NewButton() {
    window.location.href = '/coonew/';  
    
}

$(document).ready(function () {
    var table = $('#CooListTable').DataTable({
        "ajax": {
            "processing": true,
            "url": "/coolistTable/",
            "dataSrc": "",
        },
        "initComplete": function (data) {
            listBoxData = data.json;
            // console.log(listBoxData);
            table.rows().every(function () {
                var data = this.data();
               if(data.STATUS==='DEL'){
                    $(this.node()).addClass('hidden-row');
                }
                
            });
                
        },
        "dom": 'rtip',
        "columns": [{
            "data": "ID"//0
        },
        {
            "data": "ID"
        },
        {
            "data": "ID"//19
        },
        {
            "data": "ID"
        },
        {
            "data": "JOBID"//4//18
        },
        {
            "data": "MSGID"//17
        },
        {
            "data": "DECDATE"//16
        },
        {
            "data": "DECTYPE"//15
        },
        {
            "data": "CREATE"//14
        },
        {
            "data": "DECID"//9//13
        },
        {
            "data": "ETD"//12
        },
        {
            "data": "PERMITNO"//11
        },
        {
            "data": "EXPORTER"//10
        },
        {
            "data": "POD"//9
        },
        {
            "data": "COTYPE"//16//8
        },
        {
            "data": "CERTTYPE"//17//8
        },
        {
            "data": "CERTNO"//18//7
        },
        {
            "data": "MSGTYPE"//19//6
        },
        {
            "data": "TPT"//20//5
        },
        {
            "data": "PREPMT"//21//4
        },
        {
            "data": "XREF"//22//3
        },
        {
            "data": "INTREM"//2
        },
        {
            "data": "STATUS"//1
            
        },
       
        ],
        "ordering": false,
        "autoWidth": false,
        'columnDefs': [{
            'targets': 0,
            'searchable': false,
            'orderable': false,
            'render': function (data, type, full, meta) {
                return `<input type="checkbox" id="${data}" name="InNonPayementCheckBox" value="${data}"  onclick="listChcekBoxFunction()">`;
            }
        },
        {
            'targets': 1,
            "width": "10px",
            "className": "text-center",
            'render': function (data, type, full, meta) {
                return `<i class="fa-solid fa-trash-can" style="color: #ff0000;" onclick = "CooListtDelete('${data}')"></i>`
            }
        },
        {
            'targets': 2,
            "width": "10px",
            "className": "text-center",
            'render': function (data, type, full, meta) {
                if (full.STATUS == "NEW" || full.STATUS == "DRF") {
                    return `<a href="/Cooedit/${data}/"><i class="fa-regular fa-pen-to-square" style="color: #ff0000;"></i></a>`
                    console.log("page is loading")
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
                // console.log("Data Value:",data)
                return `<a href="#" onclick="openCooEditWindow('/SHOW/${data}/'); return false;"><i class="fa-regular fa-eye" style="color: #ff0000;"></i></a>`
            }
        },
        {
            "width": "50px",
            "targets": [ 4,9,15,16, 17, 18, 19, 20,],
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
    
    $('#CooRowLength').on('change', function () {
        var selectedValue = $(this).val();
        $('#CooListTable').DataTable().page.len(selectedValue).draw();
    });
  
    // $("#CooListTable tfoot tr input").on('keyup change', function () {
    //     table
    //         .column($(this).parent().index() + ':visible')
    //         .search(this.value)
    //         .draw();

            
    // });

    $('#CooTableSearch').keyup(function () {
        table.search($(this).val()).draw();
        console.log($(this).val());
    });



    // $('#statusFilterInput').on('keyup', function() {
    //     var filterValue = $(this).val().toUpperCase(); 
    //     table.rows().every(function ()  {
    //         var data = this.data();
    //         if(data.STATUS.toUpperCase() === filterValue || filterValue === 'DEL') {
    //             $(this.node()).removeClass('hidden-row');
    //         } else {
    //             $(this.node()).addClass('hidden-row');  
    //         }
    //     });
    // });

    $('#statusFilterInput').on('keyup change', function() {
        var filterValue = $(this).val().toUpperCase(); 
    
        if (filterValue === '') {
            table.rows().every(function ()  {
                if (this.data().STATUS.toUpperCase() !== 'DEL') {
                    $(this.node()).removeClass('hidden-row');
                } else {
                    $(this.node()).addClass('hidden-row');
                }
            });
        } else {
            table.rows().every(function ()  {
                var data = this.data();
                var status = data.STATUS.toUpperCase();
                if (filterValue === 'DEL') {
                    if (status === 'DEL') {
                        $(this.node()).removeClass('hidden-row');
                    } else {
                        $(this.node()).addClass('hidden-row');
                    }
                } else {
                    if (status.includes(filterValue)) {
                        $(this.node()).removeClass('hidden-row');
                    } else {
                        $(this.node()).addClass('hidden-row');  
                    }
                }
            });
        }
    });
    
    $("#CooListTable tfoot tr input").on('keyup change', function () {
        var columnIndex = $(this).parent().index();
        table
            .column(columnIndex + ':visible')
            .search(this.value)
            .draw();
    });
    

    

   
  
});

function searchInpaymentTable(arg) {
    $('#CooListTable').DataTable().search(arg).draw();
}

function filterPermits() {
    $('#footlastInput').val($("#filterPermitsId").val());
    var selectedValue = $('#filterPermitsId').val();
    console.log(selectedValue)
    var dataTable = $('#CooListTable').DataTable();
    dataTable.column(22).search(selectedValue).draw();
}

function CooListtDelete(Arg) {
    filterPermits();
    console.log(Arg)
    $.ajax({
        url: "/CooListDelete/" + Arg + "/",
        type: "GET",
        success: function (response) {
            window.location.href = "";
        }
    })

}

// CooList Checkbox

function ListAllCheckSubmit() {
    let check = document.getElementById("ListAllCheckSubmitId")
    let downCheck = document.getElementsByName("InNonPayementCheckBox");
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

/*------------------------List copy -----------------------------------------*/ 
function InNonCopy() {
    var ChechValue = document.getElementsByName("InNonPayementCheckBox");
    ChechValue.forEach(
        function (v) {
        if (v.checked) {

            try{
            $.ajax({
                url: "/CopyCoo/",
                data: {
                    "Id": v.value
                },
                success: function (response) {
                    console.log(response);
                    window.location.href = "/Cooedit/" + v.value +"/";
                },
               
            });
        }catch(error){
            console.error('Error in AJAX request:', error);
        }
        }
    });
}

/*---------------------List show---------------------------------------*/
function openCooEditWindow(url) {
    var width = 1900;
    var height = 800;
    var left = (screen.width - width) / 2;
    var top = (screen.height - height) / 2;
    window.open(url, 'cooapp', 'width=' + width + ', height=' + height + ', left=' + left + ', top=' + top);
}

function HtaHide(val1, ID) {
    let cbox = document.getElementById(ID);
    var table = $('#CooListTable').DataTable();
    if (cbox.checked) {
        table.column(Number(val1) + 3).visible(true);
    } else {
        table.column(Number(val1) + 3).visible(false);
    }
}

function TransmitDataClick() {
    let ArrayVal = [];
    var ChechValue = document.getElementsByName("InNonPayementCheckBox");
    console.log('ChechValue',ChechValue)
    let TrasnMitValue = $("#InnonPaymentTransmitData").val()
    console.log('TrasnMitValue',TrasnMitValue)
    ChechValue.forEach(
        function (Val) {
            if (Val.checked) {
                ArrayVal.push(Val.value)
            }
        }
    )
    console.log('ArrayVal',ArrayVal)

    if (ArrayVal.length > 0 && TrasnMitValue != "--Select--") {
        $("#Loading").show();
        $.ajax({
            url: "/CooTransmitData/",
            type: "GET",
            data: {
                my_data: JSON.stringify(ArrayVal),
                mailId: TrasnMitValue
            },
            success: function (response) {
                $("#Loading").hide();
                console.log(response)
                window.location.href = "/coolist/";
            }
        });
    }
    else {
        alert("PLEASE SELECT THE TRANSMIT DATA VALUE")
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
        window.location.href = "/DownloadDataCoo/" + ccp.join(",") + "/";
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
            url: "/CooTransmit/",
            data: {
                "PermitNumber": PermitNumber,
            },
            success: function (data) {
                window.location.href = "";
                alert("xmldownload")
                $('#Loading').hide();
            },
            error: function () {
                alert("Error")
                $('#Loading').hide();
            }
        })
    }
}