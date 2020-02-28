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

document.getElementById("course-column").addEventListener("click", function() {
   // columnFilterClick(0);
}, false);

document.getElementById("date-played-column").addEventListener("click", function() {
   // columnFilterClick(1);
}, false);

// WIP
function columnFilterClick(n) {
    var rows = document.querySelector("#golfTable tbody").rows;
    var xdd = $("tbody tr:nth-child(8)");
    for (var i = 0; i < (rows.length-1); i++) {
        let inc = i + 1;
        var firstRow = rows[i].cells[1].textContent[0];
        var secondRow = rows[inc].cells[1].textContent[0];
        // < a ------- > z ----------- J > G
        if (firstRow > secondRow) {
            var temp = rows[i].rowIndex;
            rows[i].rowIndex = 2
            //rows[i].rowIndex[i] = rows[inc].rowIndex[inc];
            //rows[inc].rowIndex[inc] = temp;
        } else {
            //rows[i].style.display = "none";
            //isFiltered = true;
        }      
    }
}

$(document).ready(function($) {
    /* $('table').hide();
    $('#mySelector').change(function() {
      $('table').show();
      var selection = $(this).val();
      var dataset = $('#myTable tbody').find('tr');
      // show all rows first
      dataset.show();
      // filter the rows that should be hidden
      dataset.filter(function(index, item) {
        return $(item).find('td:first-child').text().split(',').indexOf(selection) === -1;
      }).hide();
  
    }); */
  });

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
