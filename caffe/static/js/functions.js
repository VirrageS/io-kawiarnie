(function ($) {
  "use strict"

  var $window,
      $menu;

  function changeMenuState(e) {
    if ($menu.hasClass('open')) {
      $menu.removeClass('open'); // now, we close menu
      Cookies.set('menu', 'closed', { expires: 7 });
    } else {
      $menu.addClass('open'); // we open menu
      Cookies.set('menu', 'opened', { expires: 7 });
    }
  }

  function checkMenuCookie() {
    var cookieValue = Cookies.get('menu');
    if (cookieValue == "closed") {
      changeMenuState();
    }
  }

  function getHostFromUrl(url) {
    var pathArray = url.split( '/' );
    var protocol = pathArray[0];
    var host = pathArray[2];

    return protocol + '//' + host;
  }

  function init() {
    $("#control-menu").on('click', changeMenuState);
    checkMenuCookie();

    $('button[type=cancel]').click(function() {
      var href = $(this).children('a').attr('href');
      if (!href) {
        window.history.back();
        return false;
      }
    });

    $('button.back-button').click(function() {
      window.history.back();
    })

    // do not show back button on redundant pages
    if (['/reports/', '/', '/calendar/'].indexOf(window.location.pathname) !== -1) {
      $('button.back-button').hide();
    }

    // checkboxes
    $('label input[type=checkbox]').each(function(index) {
      if ($(this).is(':checked')) {
        $(this).parent().addClass('checked-box');
      }
    });

    $('label input[type=checkbox]').on('change', function() {
      $(this).parent().toggleClass('checked-box');
    });
  }

  $(document).ready(function () {
      // variable definitions
      $window = $(window);
      $menu = $(".left-pane");

      init();
  });

})(jQuery);
