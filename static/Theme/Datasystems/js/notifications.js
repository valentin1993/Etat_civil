
$(document).ready(function() {
    // messages timeout for 10 sec 
    setTimeout(function() {
        $('.alert.alert-success.alert-dismissible.alert-error').fadeOut('slow');
    }, 3000); // <-- time in milliseconds, 1000 =  1 sec

    // delete message
    $('.del-msg').on('click',function(){
        $('.del-msg').parent().attr('style', 'display:none;');
    })
});
