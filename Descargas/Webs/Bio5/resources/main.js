jQuery.noConflict();

jQuery(document).ready(function ($) {
  console.log('Bisonic Ready');
  const $starsBg = $('.stars-bg');
  const $mastheadBG = $('.frontpage-masthead-bg > span');
  const $globalHeader = $('.globalHeader');
  const $pageNav = $('.frontpage-pageNav');
  const $aboutSection = $('.frontpage-about');
  const $projectsSection = $('.frontpage-projects');
  const $leadershipSection = $('.frontpage-teamLeadership');

  if ($globalHeader.length) {
    const $logo = $globalHeader.find('.globalHeader-logo');
    const $toggle = $globalHeader.find('.mobile-nav-toggle');
    const $links = $globalHeader.find('.primary-menu-container ul > li > a');

    $toggle.on('click', () => {
      $globalHeader.toggleClass('is-open');
    });
    $logo.on('click', (e) => {
      if (window.location.pathname === '/') {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      }
    });
    $links.each((i, el) => {
      const $el = $(el);

      $el.on('click', (e) => {
        const href = $el.attr('href').replace('/', '');

        if (href.includes('#')) {
          const $scrollToElement = $(href);

          if ($scrollToElement.length) {
            e.preventDefault();

            if ($globalHeader.hasClass('is-open')) {
              $globalHeader.removeClass('is-open');
            }
            const offset = $scrollToElement.offset();

            window.scrollTo({
              top: offset.top,
              behavior: 'smooth'
            });
          }
        }

      });
    });
  }

  $(window).on('mouseover', (e) => {
    $starsBg.css('background-position-x', `${e.pageX / 150}%`);
  });

  $(window).on('scroll', (e) => {
    var scroll = $(window).scrollTop();
    $starsBg.css('background-position-y', `${scroll / 100}%`);
    $mastheadBG.css('top', `${352 - (scroll / 2)}px`)
  });

  if ($pageNav.length) {
    const sections = document.querySelectorAll('.frontpage-section');
    const $pageNavList = $pageNav.find('.frontpage-pageNav-list');
    let pageNavItems = '';

    sections.forEach((el, i) => {
      pageNavItems += `<li><button data-index="${i}"><span>${String(i).padStart(2, '0')}</span></button ></li >`;
    });
    $pageNavList.html(pageNavItems);

    const $menuLinks = $globalHeader.find('nav#site-navigation li');
    const $bullets = $pageNavList.find('> li');
    const $bulletBtns = $bullets.find('> button');
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach((entry, i) => {
        const $el = $(entry.target);
        if (entry.isIntersecting && entry.intersectionRatio > 0.4) {
          let index = entry.target.el_index;
          $bullets.each((i, el) => {
            $(el).removeClass('is-active');
          });
          $menuLinks.each((i, el) => {
            $(el).removeClass('is-active');
          });
          // Weird navigation logic for how design wants it
          if (index > 4) {
            $($menuLinks[$menuLinks.length - 1]).addClass('is-active');
          } else if (index === 3 || index === 4) {
            $($menuLinks[3]).addClass('is-active');
          } else {
            $($menuLinks[index]).addClass('is-active');
          }
          $($bullets[index]).addClass('is-active');
          $el.addClass('animate-in');
        }
        if (!entry.isIntersecting) {
          $el.removeClass('animate-in');
        }
      });
    }, { threshold: [0, 0.4, 0.5, 1] });

    sections.forEach((el, i) => {
      el.el_index = i;
      observer.observe(el);
    });

    $bulletBtns.each((i, el) => {
      $(el).on('click', () => {
        const index = $(el).data('index');
        window.scrollTo({
          top: sections[index].getBoundingClientRect().top + document.documentElement.scrollTop,
          behavior: 'smooth'
        });
      });
    })
  }

  if ($aboutSection.length) {
    $('.projectsSlider').flexslider({
      slideshow: false,
      controlNav: false
    });
  }

  if ($projectsSection.length) {
    $('.aboutSlider').flexslider({
      slideshow: false,
      controlNav: false
    });
  }

  if ($leadershipSection.length) {
    const $modal = $leadershipSection.find('.teamLeadership-modal');
    const modalEls = {
      close: $modal.find('.teamLeadership-modal-close'),
      controls: $modal.find('.teamLeadership-modal-controls button'),
      title: $modal.find('.teamLeadership-modal-content .teamLeadership-modal-description h2'),
      img: $modal.find('.teamLeadership-modal-content .teamLeadership-modal-image img'),
      role: $modal.find('.teamLeadership-modal-content .teamLeadership-modal-description span'),
      bio: $modal.find('.teamLeadership-modal-content .teamLeadership-modal-description .teamLeadership-modal-description-bio')
    };
    const $items = $leadershipSection.find('.diamond-grid .diamond-item > button');
    const populateModalData = (el) => {
      const $el = $(el);
      const $modalImg = $modal.find('.teamLeadership-modal-image');
      const $modalDescription = $modal.find('.teamLeadership-modal-description');
      const name = $el.find('strong').text();
      const role = $el.data('title');
      const img = $el.find('img').attr('src');
      const bio = $el.find('.leadership-bio').html();
      const isMobile = window.innerWidth <= 1024;

      if ($modal.hasClass('is-open')) {
        gsap.to($modalImg, {
          opacity: 0,
          left: isMobile ? '0' : '-20px',
          top: isMobile ? '-20px' : '0',
          duration: 0.5,
          onComplete: () => {
            modalEls.title.text(name);
            modalEls.img.attr('src', img);
            modalEls.role.text(role);
            modalEls.bio.html(bio);

            gsap.to([$modalImg, $modalDescription], {
              opacity: 1,
              left: 0,
              top: 0,
              delay: 0.15,
              duration: 0.5
            });
          }
        });
        gsap.to($modalDescription, {
          opacity: 0,
          left: isMobile ? '0' : '20px',
          top: isMobile ? '20px' : '0',
          duration: 0.5,
        });
      } else {
        gsap.set($modalImg, {
          opacity: 0,
          left: isMobile ? '0' : '-20px',
          top: isMobile ? '-20px' : '0'
        });
        gsap.set($modalDescription, {
          opacity: 0,
          left: isMobile ? '0' : '20px',
          top: isMobile ? '20px' : '0'
        });
        modalEls.title.text(name);
        modalEls.img.attr('src', img);
        modalEls.role.text(role);
        modalEls.bio.html(bio);
        gsap.to([$modalImg, $modalDescription], {
          opacity: 1,
          left: 0,
          top: 0,
          duration: 0.5
        });
      }

    };
    let modalOpen = false;
    let activeIndex = 0;

    $items.each((i, el) => {
      const $el = $(el);

      $el.on('click', () => {
        if (modalOpen) {
          return;
        }
        populateModalData(el);
        modalOpen = true;
        activeIndex = i;

        $leadershipSection.addClass('modal-open');
        $modal.addClass('is-open');
      });
    });

    modalEls.close.on('click', () => {
      if (!modalOpen) {
        return;
      }
      $leadershipSection.removeClass('modal-open');
      $modal.removeClass('is-open');
      modalOpen = false;
      activeIndex = 0;
    });
    modalEls.controls.each((i, el) => {
      const $btn = $(el);

      $btn.on('click', () => {
        const isPrev = $btn.hasClass('control-prev');
        let newIndex = 0;

        if (isPrev && activeIndex === 0) {
          newIndex = $items.length - 1;
        } else if (!isPrev && activeIndex === $items.length - 1) {
          newIndex = 0;
        } else {
          newIndex = isPrev ? activeIndex - 1 : activeIndex + 1;
        }

        populateModalData($items[newIndex]);
        activeIndex = newIndex;
      });
    });
  }
});
