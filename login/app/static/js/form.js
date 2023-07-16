$('#setForm').submit(function(e) {
  
    $.ajax({
        data : {
            high : $('#highInput').val(),
            low : $('#lowInput').val()
        },
        type : 'POST',
        url : '/process'
    })
    .done(function(data) {

        if (data.inputError) {
            $('#toLowInput').text(data.inputError).show();
            $('#successAlert').hide();
        }
        else {
            $('#GuessAlert').text(data.set).show();
            $('#lowAlert').text(data.lowest).show();
            $('#highAlert').text(data.highest).show();
            $('#guessNumber').text(data.guesses).show();

            $('#lowInput, #highInput').attr('readOnly','true');
            $('#guesInput').prop('readOnly','');
            
            
            $("#setButton").attr("disabled", 'true');
            $('#GuessButton').prop('disabled','');

            $('#guessBox').css('display', '');
            $('#toLowInput').hide();
            $('#errorAlert').hide();
        }

    });
    e.preventDefault();
});

$('#guessForm').submit(function(e) {

$.ajax({
    data : {
        guess : $('#guesInput').val(),
    },
    type : 'POST',
    url : '/process'
})
.done(function(data) {

    if (data.error) {
        $('#errorAlert').text(data.error).show();
        $('#victory').text(data.score).show();
        $('#guessNumber').text(data.guesses).show();

        $("#setForm")[0].reset();
        $("#guessForm")[0].reset();

        $('#lowInput, #highInput').prop('readOnly','');
        $('#guesInput').prop('readOnly','true');
        $('#GuessButton').prop('disabled','true');
        $("#setButton").prop("disabled", '');

        $('#GuessAlert').hide();
    }
    else if (data.won) {
        $('#victory').text(data.score).show();
        $('#GuessAlert').text(data.won).show();

        $("#setForm")[0].reset();
        $("#guessForm")[0].reset();

        $('#lowInput, #highInput').prop('readOnly','');
        $('#guesInput').attr('readOnly','true');

        $('#GuessButton').attr('disabled','true');
        $("#setButton").prop("disabled", '');

        $('#errorAlert').hide();
    }
    else {
        $('#GuessAlert').text(data.wrong).show();
        $('#guessNumber').text(data.guesses).show();
        $('#errorAlert').hide();
    }

});
e.preventDefault();
});