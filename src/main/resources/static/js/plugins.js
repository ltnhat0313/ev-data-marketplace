(function ($) {
  "use strict";

  // Khởi tạo hiệu ứng chữ (Splitting.js)
  Splitting();

  // Khởi tạo hiệu ứng khi cuộn trang (AOS - Animate On Scroll)
  AOS.init({
    duration: 1200, // Thời gian hiệu ứng
    once: true, // Chỉ chạy hiệu ứng một lần
  });

  // Khởi tạo Swiper cho slider chính (main-swiper)
  var mainSwiper = new Swiper(".main-swiper", {
    speed: 800,
    loop: true,
    slidesPerView: 3,
    spaceBetween: 30,
    pagination: {
      el: ".main-swiper .swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".main-swiper .icon-arrow-right",
      prevEl: ".main-swiper .icon-arrow-left",
    },
    breakpoints: {
      0: {
        slidesPerView: 1,
        spaceBetween: 20,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      1200: {
        slidesPerView: 3,
        spaceBetween: 30,
      },
    },
  });

  // Khởi tạo Swiper cho các carousel sản phẩm (product-swiper)
  var productSwiper = new Swiper(".product-swiper", {
    speed: 800,
    loop: true,
    slidesPerView: 4,
    spaceBetween: 30,
    pagination: {
      el: ".product-swiper .swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".product-swiper .icon-arrow-right",
      prevEl: ".product-swiper .icon-arrow-left",
    },
    breakpoints: {
      0: {
        slidesPerView: 1,
        spaceBetween: 20,
      },
      768: {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 20,
      },
      1200: {
        slidesPerView: 4,
        spaceBetween: 30,
      },
    },
  });

  // Khởi tạo Swiper cho phần đánh giá của khách hàng (testimonial-swiper)
  var testimonialSwiper = new Swiper(".testimonial-swiper", {
    loop: true,
    effect: "coverflow",
    coverflowEffect: {
      rotate: 50,
      stretch: 0,
      depth: 100,
      modifier: 1,
      slideShadows: true,
    },
    pagination: {
      el: ".testimonial-swiper-pagination",
      clickable: true,
    },
  });

  // Khởi tạo GLightbox (dành cho popup video/ảnh)
  var lightbox = GLightbox({
    touchNavigation: true,
    loop: true,
    autoplayVideos: true,
  });

})(jQuery);