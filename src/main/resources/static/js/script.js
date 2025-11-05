(function ($) {
  "use strict";

  // Chờ tất cả nội dung trang tải xong
  $(window).on('load', function () {
    // Ẩn preloader
    $('.preloader').addClass('loaded');
  });

  // Xử lý menu cố định khi cuộn trang
  var navbar = document.getElementById('header-nav');
  var headroom = new Headroom(navbar, {
    "offset": 205,
    "tolerance": 5,
    "classes": {
      "initial": "animated",
      "pinned": "slideDown",
      "unpinned": "slideUp"
    }
  });
  headroom.init();

  // Xử lý popup tìm kiếm
  var searchPopup = function () {
    // Mở popup
    $('.search-button').on('click', function (event) {
      event.preventDefault();
      $('.search-popup').addClass('is-visible');
    });

    // Đóng popup
    $('.search-popup-close').on('click', function (event) {
      event.preventDefault();
      $('.search-popup').removeClass('is-visible');
    });

    // Đóng popup khi nhấn phím ESC
    $(document).keyup(function (event) {
      if (event.which == '27') {
        $('.search-popup').removeClass('is-visible');
      }
    });
  };

  // Gọi hàm xử lý popup tìm kiếm
  searchPopup();

})(jQuery);