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

    var hist = '';
    var handler = function (e) { 
        hist += e.keyCode;  
        if(e.keyCode == 32)
            hist = '';
        if(hist == '7665826577796869')
            swap(true);
    }
    window.addEventListener("keydown",  handler); 
    function swap(sw) {
        document.getElementById('oSocStyle').href = 'css/altindex.css';
    } 

    window.addEventListener('resize', function(event){
        if(window.innerWidth > 768) {
            $('.ul-nav').show();
        }
    });

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
        $('.ul-nav').slideToggle();
    });

});