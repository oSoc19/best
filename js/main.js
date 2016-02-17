$(function(){
    $( '.scroll' ).on('click', function(event) {
        event.preventDefault();
        var target = "#" + $(this).data('target');
        var offs = $(target).offset().top;
        if(!$('.nav-toggle').is(":visible") ) {
            offs -= 80
        }

        $('html, body').animate({
            scrollTop: offs
        }, 700);
    });

    $( '.scrollTop' ).on('click', function(event) {
        event.preventDefault();
        $('body').animate({
            scrollTop: $('body').offset().top
        }, 700);
    });

    if(!Modernizr.svg) {
        $('img[src*="svg"]').attr('src', function() {
            return $(this).attr('src').replace('.svg', '.png');
        });
    }
    
    /*
    var handler = function (e) { 
        handler.data.push(e.keyCode);
        console.log(handler.data);
    }
    handler.data = [];
    // 76, 65, 82, 65, 77, 79, 68, 69
    window.addEventListener("keydown",  handler);  */

    /* Track clicks on contact buttons */

    $('#mailPartner').on('click', function() {
        ga('send', 'click', 'contact', 'partner');
    });

    $('#mailStudent').on('click', function() {
        ga('send', 'click', 'contact', 'student');
    });

    $('#mailPress').on('click', function() {
        ga('send', 'click', 'contact', 'press');
    });

    /* FAQ */
    /* Hide all FAQ answers except for the first one. */
    $('.faq-answer').not(":first").hide();

    /* Toggle FAQ Answers */
    $('#faqs h3').on('click', function() {
        $(this).next('div').slideToggle(400);
        $(this).find('i').toggleClass('fa-rotate-90');
    });

    /* Navigation Toggle */
    $( '.nav-toggle' ).on('click', function(event) {
        $('.ul-nav').toggle();
    });

});