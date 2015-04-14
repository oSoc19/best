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

    $('#faqs h3').each(function() {
        var tis = $(this), state = false, answer = tis.next('div').hide().css('height','auto').slideUp();
        tis.click(function() {
            state = !state;
            answer.slideToggle(state);
            tis.toggleClass('active',state);
        });
    });

    /* Fancy active links/sections */
    /* $(".ul-nav li a").click(function () {
        $(".ul-nav li a").removeClass("active");
        $(this).addClass("active");
    });

    $(".oSoc-logo a").click(function () {
        $(".ul-nav li a").removeClass("active");
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
    $(window).scroll(function() {

        if($(window).scrollTop() < $('#video').offset().top - 90) {
            $(".ul-nav li a").removeClass("active");
        }
        else if($(window).scrollTop() <= $('#location').offset().top - 90) {
            if(!$('a[href$="#video"]').hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                $('a[href$="#video"]').addClass("active");
            }
        }
        else if($(window).scrollTop() <= $('#studentsparticipate').offset().top - 90) {
            if(!$('a[href$="#location"]').hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                $('a[href$="#location"]').addClass("active");
            }
        }
        else if($(window).scrollTop() <= $('#partners').offset().top - 90) {
            if(!$('a[href$="#studentsparticipate"]').hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                $('a[href$="#studentsparticipate"]').addClass("active");
            }
        }
        else if($(window).scrollTop() <= $('#participate').offset().top - 90) {
            if(!$('a[href$="#partners"]').hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                $('a[href$="#partners"]').addClass("active");
            }
        }
        else {
            if(!$('a[href$="#participate"]').hasClass("active")) {
                $(".ul-nav li a").removeClass("active");
                $('a[href$="#participate"]').addClass("active");
            }
        }
    });
});