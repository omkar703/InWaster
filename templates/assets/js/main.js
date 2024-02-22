(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim();
    if (all) {
      return [...document.querySelectorAll(el)];
    } else {
      return document.querySelector(el);
    }
  };

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all);
    if (selectEl) {
      if (all) {
        selectEl.forEach((e) => e.addEventListener(type, listener));
      } else {
        selectEl.addEventListener(type, listener);
      }
    }
  };

  /**
   * Easy on scroll event listener
   */
  const onscroll = (el, listener) => {
    el.addEventListener("scroll", listener);
  };

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select("#navbar .scrollto", true);
  const navbarlinksActive = () => {
    let position = window.scrollY + 200;
    navbarlinks.forEach((navbarlink) => {
      if (!navbarlink.hash) return;
      let section = select(navbarlink.hash);
      if (!section) return;
      if (
        position >= section.offsetTop &&
        position <= section.offsetTop + section.offsetHeight
      ) {
        navbarlink.classList.add("active");
      } else {
        navbarlink.classList.remove("active");
      }
    });
  };
  window.addEventListener("load", navbarlinksActive);
  onscroll(document, navbarlinksActive);

  /**
   * Scroll links with a class name .scrollto
   */
  on(
    "click",
    ".scrollto",
    function (e) {
      if (select(this.hash)) {
        if (window.innerWidth <= 992) {
          select("body").classList.toggle("mobile-nav-active");
          select(".mobile-nav-toggle").classList.toggle("fa-bars");
          select(".mobile-nav-toggle").classList.toggle("fa-times");
        }
      }
    },
    true
  );

  /**
   * Mobile nav toggle
   */
  on("click", ".mobile-nav-toggle", function (e) {
    select("body").classList.toggle("mobile-nav-active");
    this.classList.toggle("fa-bars");
    this.classList.toggle("fa-times");
  });

  /**
   * Back to top button
   */
  let backtotop = select(".back-to-top");
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add("active");
      } else {
        backtotop.classList.remove("active");
      }
    };
    window.addEventListener("load", toggleBacktotop);
    onscroll(document, toggleBacktotop);
  }

  /**
   * Hero carousel indicators
   */
  let heroCarouselIndicators = select("#hero-carousel-indicators");
  let heroCarouselItems = select("#heroCarousel .carousel-item", true);

  heroCarouselItems.forEach((item, index) => {
    index === 0
      ? (heroCarouselIndicators.innerHTML +=
          "<li data-bs-target='#heroCarousel' data-bs-slide-to='" +
          index +
          "' class='active'></li>")
      : (heroCarouselIndicators.innerHTML +=
          "<li data-bs-target='#heroCarousel' data-bs-slide-to='" +
          index +
          "'></li>");
  });

  /**
   * Toggle .header-scrolled class when page is scrolled
   */
  let selectHeader = select("#logo-header");
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100 || select(".header-sticky-top")) {
        selectHeader.classList.add("header-scrolled");
        select(".mobile-nav-toggle").style.color = "white";
      } else {
        selectHeader.classList.remove("header-scrolled");
        select(".mobile-nav-toggle").style.color = getComputedStyle(
          select(":root")
        ).getPropertyValue("--primary-color");
      }
    };
    window.addEventListener("load", headerScrolled);
    onscroll(document, headerScrolled);
  }

  /**
   * Preloader
   */
  let preloader = document.querySelector("#preloader");
  if (preloader) {
    window.addEventListener(
      "load",
      () => {
        preloader.remove();
      },
      {
        passive: true,
      }
    );
  }

  /**
   * Hero Height
   */
  function findHeroHeight() {
    if (window.innerWidth <= 758) {
      select(":root").style.setProperty(
        "--hero-section-height",
        `${window.innerHeight - select("#logo-header").offsetHeight}px`
      );
    } else {
      select(":root").style.setProperty("--hero-section-height", "100vh");
    }
  }
  findHeroHeight();

  /**
   * Partners slider
   */
  new Swiper(".partners-slider", {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    slidesPerView: "auto",
    pagination: {
      el: ".swiper-pagination",
      type: "bullets",
      clickable: true,
    },
  });

  // window resize
  window.onresize = () => {
    findHeroHeight();
  };
})();
