function resize_nav_text() {
    if($('.navbar-toggle').css('display') != 'none'){
        a_big_number = 2048;
        $('.navbar-text').css('max-width', (a_big_number + 'px'));
        $('.navbar-text').removeClass('nav-text-big');
    } else {
        var calculated_width = $('a.navbar-brand').width() + $('ul.navbar-nav').width() + 78;
        max_width = $( window ).width() - calculated_width;
        $('.navbar-text').css('max-width', (max_width + 'px'));
        $('.navbar-text').addClass('nav-text-big');
    }
}

function config_share_button() {
    var sharebutton = new ShareButton({
        ui: {
            flyout: 'sb-bottom sb-right',
            buttonText: '',
            buttonFont: false
        },
        networks: {
            pinterest: {
                enabled: false
            },
            reddit: {
                enabled: false
            }
        }
    });

    function is_shared_button_open() {
        var sharebar = $('share-button div.sb-social');
        return sharebar.hasClass('active');
    }

    function position_to_right_share_button() {
        var sharebar = $('share-button div.sb-social');
        var x = $( window ).width() - sharebar.width();
        sharebar.css('left', x);
    };
    var container = $('share-button div.sb-social');
    $(document).mouseup(function (e) {
        var sharelink = $('a.share-button');
        if ((!container.is(e.target) && container.has(e.target).length === 0)
            &&
            (!sharelink.is(e.target) && sharelink.has(e.target).length === 0))
        {
            if (is_shared_button_open()) {
                sharebutton.toggle();
            }

        }
    });
    $(window).resize(position_to_right_share_button);
    position_to_right_share_button();
    $("a.share-button").click(function () {sharebutton.toggle();});
}

function config_top_button() {
    if ($(window).height() < $(document).height() ) {
        $('#top-link-block').removeClass('hidden').affix({
            offset: {top:100}
        });
    }
}

$(document).ready(function () {
    config_share_button();
    config_top_button();
    $(window).resize(resize_nav_text);
    resize_nav_text();
});
