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

    /*
    $('#faqs h3').each(function() {
        var tis = $(this), state = false, answer = tis.next('div').hide().css('height','auto').slideUp();
        tis.click(function() {
            state = !state;
            answer.slideToggle(state);
            tis.toggleClass('active',state);
        });
    }); */

    /* Script for updating the active link in the top-navigation when user is at a certain part of the site */
    /*
        Possible scrollTargets:
        -top
        -video
        -location
        -studentsparticipate
        -partners
        -faq
     */

    // Preload offsets:
    var vidOffset = $('#video').offset().top - 90;
    var locOffset = $('#location').offset().top - 90;
    var studOffset = $('#studentsparticipate').offset().top - 90;
    var particOffset = $('#participate').offset().top - 90;
    var faqOffset = $('#faq').offset().top - 90;

    var vidLink = $('a[href$="#video"]');
    var locLink = $('a[href$="#location"]');
    var studLink = $('a[href$="#studentsparticipate"]');
    var particLink = $('a[href$="#participate"]');
    var faqLink = $('a[href$="#faq"]');

    $(window).scroll(function() {

        if($(window).scrollTop() < vidOffset) {
            $('.ul-nav li a.active').removeClass("active");
        }
        else if($(window).scrollTop() <= locOffset) {

                $('.ul-nav li a.active').removeClass("active");
                vidLink.addClass("active");

        }
        else if($(window).scrollTop() <= studOffset) {
                $('.ul-nav li a.active').removeClass("active");
                locLink.addClass("active");

        }
        else if($(window).scrollTop() <= particOffset) {
            $('.ul-nav li a.active').removeClass("active");
            studLink.addClass("active");
        }
        else if($(window).scrollTop() <= faqOffset) {
                $('.ul-nav li a.active').removeClass("active");
                particLink.addClass("active");

        }
        else  {
            $('.ul-nav li a.active').removeClass("active");
            faqLink.addClass("active");
        }
    });

    /* Navigation Toggle */
    $( '.nav-toggle' ).on('click', function(event) {
        $('.ul-nav').toggle();
    });

    /* Reset navigation and offsets on resize */
    $( window ).resize(function() {
        vidOffset = $('#video').offset().top - 90;
        locOffset = $('#location').offset().top - 90;
        studOffset = $('#studentsparticipate').offset().top - 90;
        particOffset = $('#participate').offset().top - 90;
        faqOffset = $('#faq').offset().top - 90;

        if($('.nav-toggle').is(":visible") ) {
            $('.ul-nav').hide();
        } else {
            $('.ul-nav').show();
        }
    });
});