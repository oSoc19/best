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
    /*
    $('#faqs h3').on('click', function() {
        $(this).next('div').slideToggle(400);
    }); */

    /*
    $('#faqs h3').each(function() {
        var tis = $(this), state = false, answer = tis.next('div').hide().css('height','auto').slideUp();
        tis.click(function() {
            state = !state;
            answer.slideToggle(state);
            tis.toggleClass('active',state);
        });
    }); */


    /*
        Possible scrollTargets:
        -top
        -video
        -location
        -studentsparticipate
        -partners
        -participate
     */

    // Preload offsets:
    var vidOffset = $('#video').offset().top - 90;
    var locOffset = $('#location').offset().top - 90;
    var studOffset = $('#studentsparticipate').offset().top - 90;
    var partOffset = $('#partners').offset().top - 90;
    var particOffset = $('#participate').offset().top - 90;
    var vidLink = $('a[href$="#video"]');
    var locLink = $('a[href$="#location"]');
    var studLink = $('a[href$="#studentsparticipate"]');
    var partLink = $('a[href$="#partners"]');
    var particLink = $('a[href$="#participate"]');

    $(window).scroll(function() {

        if($(window).scrollTop() < vidOffset) {
            $(".ul-nav li a").removeClass("active");
        }
        else if($(window).scrollTop() <= locOffset) {
            if(!vidLink.hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                vidLink.addClass("active");
            }
        }
        else if($(window).scrollTop() <= studOffset) {
            if(!locLink.hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                locLink.addClass("active");
            }
        }
        else if($(window).scrollTop() <= partOffset) {
            if(!studLink.hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                studLink.addClass("active");
            }
        }
        else if($(window).scrollTop() <= particOffset) {
            if(!partLink.hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                partLink.addClass("active");
            }
        }
        else {
            if(!particLink.hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                particLink.addClass("active");
            }
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
        partOffset = $('#partners').offset().top - 90;
        particOffset = $('#participate').offset().top - 90;

        if($('.nav-toggle').is(":visible") ) {
            $('.ul-nav').hide();
        } else {
            $('.ul-nav').show();
        }
    });
});