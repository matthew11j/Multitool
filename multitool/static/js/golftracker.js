// golftracker.js

var isFiltered = false;
var deleteFilter = document.getElementById("removeFilter")
deleteFilter.style.display = "none";

function selectFilter() {
    var selectedValue = document.getElementById("courseSelector").value;
    var rows = document.querySelector("#golfTable tbody").rows;
    var deleteFilter = document.getElementById("removeFilter");
    
    // If it is NOT "Show All" then the deleteFilter button will show
    if (selectedValue != "") {
        deleteFilter.style.display = "";
    } else { // otherwise hidden
        deleteFilter.style.display = "none";
    }

    for (var i = 0; i < rows.length; i++) {
        var firstCol = rows[i].cells[1].textContent
        if (firstCol.indexOf(selectedValue) > -1) {
            rows[i].style.display = "";
            isFiltered = false;
        } else {
            rows[i].style.display = "none";
            isFiltered = true;
        }      
    }

    // After filter if selectedValue is NOT "Show All" then deleteFilter will show
    if (selectedValue != "") { 
        deleteFilter.style.display = "";
    } else { // otherwise hidden
        deleteFilter.style.display = "none";
    }
};

function removeCourseFilter() {
    var x = document.getElementById("courseSelector").value;
    document.getElementById("courseSelector").value = ""
    document.getElementById("courseSelector").onchange();
};

$('th').click(function(){
    if (isNaN(this.textContent)) {
        var table = $(this).parents('table').eq(0);
        var rows = table.find('tr:gt(0)').toArray().sort(comparer($(this).index()));
        this.asc = !this.asc;
        if (!this.asc){rows = rows.reverse()};
        for (var i = 0; i < rows.length; i++){table.append(rows[i])};
    }
})

function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index);
        var valATrim = valA.split(" "), valBTrim = valB.split(" ");
        return $.isNumeric(valATrim[0]) && $.isNumeric(valBTrim[0]) ? valATrim[0] - valBTrim[0] : valATrim[0].toString().localeCompare(valBTrim[0]);
    }
}

function getCellValue(row, index){ return $(row).children('td').eq(index).text() }


//document.querySelector('#myInput').addEventListener('keyup', filterTable, false);



// ----- Charts --------------------------------------------------------------------------------
// Courses Played (Pie)
var ctx = document.getElementById('myChart').getContext('2d');
var data = document.getElementById('payload').textContent;    
var obj = JSON.parse(data);

let GCCnt = obj.GCCnt
let BCCnt = obj.BCCnt
let MiscCnt = obj.MiscCnt

var color1 = "rgba(128, 100, 162, 0.7)"
var color2 = "rgba(64, 215, 245, 0.7)"
var color3 = "rgba(50, 217, 89, 0.7)"

var color1b = "rgba(128, 100, 162, 1)"
var color2b = "rgba(64, 215, 245, 1)"
var color3b = "rgba(50, 217, 89, 1)"

var myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Green Crest', 'Beech Creek', 'Misc'],
        datasets: [{
            label: 'Courses Played',
            data: [GCCnt, BCCnt, MiscCnt],
            backgroundColor: [
                color1,
                color2,
                color3
            ],
            borderColor: [
                color1b,
                color2b,
                color3b
            ],
            borderWidth: 1
        }]
    },
    options: {
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                fontColor: '#fff'
            }
        },
        // scales: {
        //     yAxes: [{
        //         ticks: {
        //             beginAtZero: true
        //         }
        //     }]
        // },
        responsive: false
    }
});

// ----- Modals --------------------------------------------------------------------------------
// Add Round
$('span#open-modal').on('click', function(e){
    var url = "/golftracker/addround";
    $.get(url, function(data) {
        $('#addRoundModal .modal-content').html(data);
        $('#addRoundModal').modal();
        validateRound(url, data);
    });
});

// Add Course
$('span#open-modal2').on('click', function(e){
    var url = "/golftracker/addcourse";
    $.get(url, function(data) {
        $('#addCourseModal .modal-content').html(data);
        $('#addCourseModal').modal();
        validateCourse(url, data);
    });
});

// Edit Round
$('i#open-modal3').on('click', function(e){
    var round_id = $(this).data('id');
    var url = "/golftracker/editround/" + round_id;
    $.get(url, function(data) {
        $('#addRoundModal .modal-content').html(data);
        $('#addRoundModal').modal();
        validateRound(url, data);
    });
});

// ----- Validators --------------------------------------------------------------
function validateRound(url, data) {
  $('#submit').click(function(event) {
      event.preventDefault();
      var f = $("#addRoundForm");
      var formData = f.serialize();

      $.post(url, data=formData, function(data, statusCode) {
          if (data.status == 'ok') {
              $('#addRoundModal').modal('hide');
              location.reload();
          }
          else {
            $('#addRoundModal .modal-content').html(data);
            validateRound(url, data)
          }
      });
  });
};

function validateCourse(url, data) {
  $('#submit').click(function(event) {
      event.preventDefault();
      var f = $("#addCourseForm");
      var formData = f.serialize();

      $.post(url, data=formData, function(data, statusCode) {
          if (data.status == 'ok') {
              $('#addCourseModal').modal('hide');
              location.reload();
          }
          else {
            $('#addCourseModal .modal-content').html(data);
            validateCourse(url, data)
          }
      });
  });
};
