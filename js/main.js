$(function(){

    var hasNotYetPaused = true;

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

    var iframe = $('#vimeoplayer')[0],
        player = $f(iframe),
        status = $('.status')

    player.addEvent('ready', function() {
        player.addEvent('pause', onPause);
    });

    function onPause(id) {
        hasNotYetPaused = false;
    }

    window.setInterval(function(){
        var viewportWidth = jQuery(window).width(),
            viewportHeight = jQuery(window).height(),

            documentScrollTop = jQuery(document).scrollTop(),
            documentScrollLeft = jQuery(document).scrollLeft(),

            $myElement = jQuery('#vimeoplayer'),

            verticalVisible, horizontalVisible,

            elementOffset = $myElement.offset(),
            elementHeight = $myElement.height(),
            elementWidth = $myElement.width(),

            minTop = documentScrollTop,
            maxTop = documentScrollTop + viewportHeight,
            minLeft = documentScrollLeft,
            maxLeft = documentScrollLeft + viewportWidth;

        if (
            ((elementOffset.top > minTop && elementOffset.top < maxTop) ||
                (elementOffset.top + elementHeight > minTop && elementOffset.top +
                    elementHeight < maxTop))
                &&
                ((elementOffset.left > minLeft && elementOffset.left < maxLeft) ||
                    (elementOffset.left + elementWidth > minLeft && elementOffset.left +
                        elementWidth < maxLeft))
            ) {
            // alert('some portion of the element is visible');
            if (elementOffset.top >= minTop && elementOffset.top + elementHeight
                <= maxTop) {
                verticalVisible = elementHeight;
            } else if (elementOffset.top < minTop) {
                verticalVisible = elementHeight - (minTop - elementOffset.top);
            } else {
                verticalVisible = maxTop - elementOffset.top;
            }

            if (elementOffset.left >= minLeft && elementOffset.left + elementWidth
                <= maxLeft) {
                horizontalVisible = elementWidth;
            } else if (elementOffset.left < minLeft) {
                horizontalVisible = elementWidth - (minLeft - elementOffset.left);
            } else {
                horizontalVisible = maxLeft - elementOffset.left;
            }

            var percentVerticalVisible = (verticalVisible / elementHeight) * 100;
            var percentHorizontalVisible = (horizontalVisible / elementWidth) * 100;

            if (percentVerticalVisible < 50 || percentHorizontalVisible < 50) {
                // alert('less than 50% of element visible; scrolling');
            } else {
                // alert('enough of the element is visible that there is no need to scroll');
                if (hasNotYetPaused == true){
                    player.api('play');
                }
            }

        } else {
            // element is not visible; scroll to it
            // alert('element is not visible; scrolling');
        }
    }, 500);
});