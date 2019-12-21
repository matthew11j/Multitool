$(document).ready(function(){
    $('button#open-modal').on('click', function(e){
        var url = "{{ url_for('golf.add_round') }}";
        $.get(url, function(data) {
            $('#addRoundModal .modal-content').html(data);
            $('#addRoundModal').modal();

            $('#submit').click(function(event) {
                event.preventDefault();
                $.post(url, data=$('#addRoundForm').serialize(), function(data) {
                    if (data.status == 'ok') {
                        $('#addRoundModal').modal('hide');
                        location.reload();
                    }
                    else {
                        $('#addRoundModal .modal-content').html(data);
                    }
                });
            });
        });
    });
});