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

  function init() {
    $("#control-menu").on('click', changeMenuState);
    checkMenuCookie();
  }

  $(document).ready(function () {
      // variable definitions
      $window = $(window);
      $menu = $(".left-pane");

      init();
  });

})(jQuery);
