// golftrackerUser.js
var cssColor = getComputedStyle(document.body).getPropertyValue('--color');

// WIP for re-rendering chart on theme change
// document.body.addEventListener("change", function() {
//     cssColor = getComputedStyle(document.body).getPropertyValue('--color');
//     render_course_chart();
// });

var isFiltered = false;
var deleteFilter = document.getElementById("removeFilter");

var data = document.getElementById('payload').textContent;    
if (data) {
    if (deleteFilter)
        deleteFilter.style.display = "none";
        
    setRoundListCounter();
    
    var obj = JSON.parse(data);

    // IMPROVE THIS

    let GCCnt = obj.GCCnt;
    let BCCnt = obj.BCCnt;
    let AFCnt = obj.AFCnt;
    let MiscCnt = obj.MiscCnt;
    if (GCCnt != 0 || BCCnt != 0 || AFCnt != 0 || MiscCnt != 0) {
        render_course_chart(obj);
    }
}

function selectFilter(val) {
    var selectedValue = "";
    if (val != undefined) {
        selectedValue = val;
        document.getElementById("courseSelector").value = val;
    } else {
        selectedValue = document.getElementById("courseSelector").value;
    }
    var rows = document.querySelector("#golfTable tbody").rows;
    var deleteFilter = document.getElementById("removeFilter");
    
    // If it is NOT "Show All" then the deleteFilter button will show
    if (selectedValue != "") {
        deleteFilter.style.display = "";
    } else { // otherwise hidden
        deleteFilter.style.display = "none";
    }

    let displayedRowCnt = 0;
    for (var i = 0; i < rows.length; i++) {
        var firstCol = rows[i].cells[1].textContent
        if (firstCol.indexOf(selectedValue) > -1) {
            rows[i].style.display = "";
            isFiltered = false;
            displayedRowCnt++;
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
    setRoundListCounter(selectedValue, displayedRowCnt);
};

function removeCourseFilter() {
    var x = document.getElementById("courseSelector").value;
    document.getElementById("courseSelector").value = "";
    document.getElementById("courseSelector").onchange();
};

function setRoundListCounter(course, val) {
    var rowCount = 0;
    var courseName = "All Courses";
    if (val != undefined && course != null ) {
        rowCount = val;
        if (course != "")
            courseName = course;
    } else {
        rowCount = $('#golfTable tr').length - 1;
    }
    var header = courseName + " (" + rowCount + ")";
    document.getElementById("golf-table-header").textContent = header;
};

// Filter on <th> click
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
function render_course_chart(obj) {
    let fontColor = cssColor;
    var canvas = document.getElementById('myChart');
    var ctx = canvas.getContext('2d');

    let GCCnt = obj.GCCnt
    let BCCnt = obj.BCCnt
    let AFCnt = obj.AFCnt
    let MiscCnt = obj.MiscCnt

    var color1 = "rgba(170, 179, 243, 1)"   // Purple
    var color2 = "rgba(152, 222, 243, 1)"   // Blue
    var color3 = "rgba(194, 243, 159, 1)"   // Green
    var color4 = "rgba(253, 244, 171, 1)"   // Yellow
    var color5 = "rgba(248, 194, 206, 1)"   // Red
    var color6 = "rgba(219, 181, 247, 1)"   // Violet

    var color1b = "rgba(170, 179, 243, 1)"
    var color2b = "rgba(152, 222, 243, 1)"
    var color3b = "rgba(194, 243, 159, 1)"
    var color4b = "rgba(253, 249, 237, 1)"
    var color5b = "rgba(248, 194, 206, 1)"
    var color6b = "rgba(219, 181, 247, 1)"

    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Beech Creek', 'Green Crest', 'Avon Fields'],
            datasets: [{
                label: 'Courses Played',
                data: [BCCnt, GCCnt, AFCnt],
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
                    fontColor: fontColor
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

    canvas.onclick = function(evt) {
        var activePoints = myChart.getElementsAtEvent(evt);
        if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
    
          var label = chartData.labels[idx];
          if (document.getElementById("courseSelector").value == label) {
            removeCourseFilter();
          } else {
            selectFilter(label);
          }
        }
    };
}

// ----- Modals --------------------------------------------------------------------------------
var username = document.getElementById('username').textContent;    

// Add Round
$('span#open-modal').on('click', function(e){
    var url = "/golftracker/" + username + "/addround";
    $.get(url, function(data) {
        $('#addRoundModal .modal-content').html(data);
        $('#addRoundModal').modal();
        validateRound(url, data);
    });
});

// Add Course
$('span#open-modal2').on('click', function(e){
    var url = "/golftracker/" + username + "/addcourse";
    $.get(url, function(data) {
        $('#addCourseModal .modal-content').html(data);
        $('#addCourseModal').modal();
        validateCourse(url, data);
    });
});

// Edit Round
$('i#open-modal3').on('click', function(e){
    var round_id = $(this).data('id');
    var url = "/golftracker/" + username + "/editround/" + round_id;
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
