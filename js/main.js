$(function(){
    $( '.scroll' ).on('click', function(event) {
        event.preventDefault();
        var target = "#" + $(this).data('target');
        $('html, body').animate({
            scrollTop: $(target).offset().top - 80
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
    
    $(document).ready(function() {
    $('#faqs h3').each(function() {
        var tis = $(this), state = false, answer = tis.next('div').hide().css('height','auto').slideUp();
        tis.click(function() {
            state = !state;
            answer.slideToggle(state);
            tis.toggleClass('active',state);
        });
    });
});
});