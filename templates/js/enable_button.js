// Enables disabled button when all fields are filled
(function() {
    $('.inp').keyup(function() {

        var empty = false;
        $('.inp').each(function() {
            if ($(this).val() == '') {
                empty = true;
            }
        });

        if (empty) {
            $('.btn').attr('disabled', 'disabled');
        } else {
            $('.btn').removeAttr('disabled');
        }
    });
})()
