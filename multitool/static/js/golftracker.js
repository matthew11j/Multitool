$('span#open-modal').on('click', function(e){
    var url = "/golftracker/addround";
    $.get(url, function(data) {
        $('#addRoundModal .modal-content').html(data);
        $('#addRoundModal').modal();
        validateRound(url, data);
    });
});

$('span#open-modal2').on('click', function(e){
    var url = "/golftracker/addcourse";
    $.get(url, function(data) {
        $('#addCourseModal .modal-content').html(data);
        $('#addCourseModal').modal();
        validateCourse(url, data);
    });
});

$('i#open-modal3').on('click', function(e){
    var round_id = $(this).data('id');
    var url = "/golftracker/editround/" + round_id;
    $.get(url, function(data) {
        $('#addRoundModal .modal-content').html(data);
        $('#addRoundModal').modal();
        validateRound(url, data);
    });
});

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