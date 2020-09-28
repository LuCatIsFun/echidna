
function setDarkMode(status){
    if(status===true){
        $('.prism-theme-dark-link').remove();
        $('.prism-theme-light-link').remove();
        $("<link>")
            .attr({ rel: "stylesheet",
                type: "text/css",
                href: "/static/styles/style-dark.css",
                class: "dark-mode-link"
            })
            .appendTo("head");
        $("<link>")
            .attr({ rel: "stylesheet",
                type: "text/css",
                href: "/static/styles/prism-light.css",
                class: "prism-theme-light-link"
            })
            .appendTo("head");
    }else{
        $('.dark-mode-link').remove();
        $('.prism-theme-dark-link').remove();
        $('.prism-theme-light-link').remove();

        $("<link>")
            .attr({ rel: "stylesheet",
                type: "text/css",
                href: "/static/styles/prism.css",
                class: "prism-theme-dark-link"
            })
            .appendTo("head");

    }
    $(".toggle-input").prop("checked",status);
}

function autoSetDarkMode(){
    let now = new Date();
    if(1<now.getHours()&& now.getHours()<2){
        setDarkMode(true)
    }else{
        setDarkMode(false)
    }
}

// document.body.onkeydown = function (event) {
//     let e = window.event || event;
//     alert(e.target.nodeName)
//     if(e.preventDefault){
//         e.preventDefault();
//     }else{
//         window.event.returnValue = false;
//     }
// };

$(document).ready(function() {

    'use strict';

    /*-----------------------------------------------------------------
      Detect device mobile
    -------------------------------------------------------------------*/

    var isMobile = false;
    if( /Android|webOS|iPhone|iPod|iPad|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        $('html').addClass('touch');
        isMobile = true;
    }
    else {
        $('html').addClass('no-touch');
        isMobile = false;
    }

	//IE, Edge
	var isIE = /MSIE 9/i.test(navigator.userAgent) || /rv:11.0/i.test(navigator.userAgent) || /MSIE 10/i.test(navigator.userAgent) || /Edge\/\d+/.test(navigator.userAgent);


    /*-----------------------------------------------------------------
      Loaded
    -------------------------------------------------------------------*/

    anime({
        targets: 'body',
        opacity: 1,
        delay: 400,
        complete: function(anim) {
            progressBar(); //Init progress bar
        }
    });

    $('body, .js-img-load').imagesLoaded({ background: !0 }).always( function( instance ) {
	    preloader(); //Init preloader
    });

    function preloader() {
        var tl = anime.timeline({});
        tl
        .add({
            targets: '.preloader',
            duration: 1,
            opacity: 1
        })
        .add({
            targets: '.circle-pulse',
            duration: 300,
            //delay: 500,
            opacity: 1,
            zIndex: '-1',
            easing: 'easeInOutQuart'
        },'+=500')
        .add({
            targets: '.preloader__progress span',
            duration: 500,
            width: '100%',
			easing: 'easeInOutQuart'
        },'-=500')
        .add({
            targets: '.preloader',
            duration: 500,
            opacity: 0,
            zIndex: '-1',
            easing: 'easeInOutQuart'
        });
    };


    /*-----------------------------------------------------------------
      Carousel
    -------------------------------------------------------------------*/

	// Testimonials
	$('.js-carousel-review').each(function() {
		var carousel = new Swiper('.js-carousel-review', {
            slidesPerView: 1,
			spaceBetween: 30,
			speed: 300,
			grabCursor: true,
			watchOverflow: true,
            pagination: {
                el: '.swiper-pagination',
		        clickable: true
            },
			autoplay: {
                delay: 5000,
            },
			breakpoints: {
                580: {
                    spaceBetween: 20
                }
            }
		});
	});

	// Clients
	$('.js-carousel-clients').each(function() {
		var carousel = new Swiper('.js-carousel-clients', {
            slidesPerView: 4,
			spaceBetween: 30,
			//loop: true,
			grabCursor: true,
			watchOverflow: true,
            pagination: {
                el: '.swiper-pagination',
		        clickable: true
            },
			breakpoints: {
                320: {
                    slidesPerView: 1,
                    spaceBetween: 0
                },
                580: {
                    slidesPerView: 2,
                    spaceBetween: 30
                },
                991: {
                    slidesPerView: 3,
                    spaceBetween: 30
                }
            }
		});
	});


    /*-----------------------------------------------------------------
      Sticky sidebar
    -------------------------------------------------------------------*/

    function activeStickyKit() {
        $('.sticky-column').stick_in_parent({
            parent: '.sticky-parent'
        });

        // bootstrap col position
        $('.sticky-column')
        .on('sticky_kit:bottom', function(e) {
            $(this).parent().css('position', 'static');
        })
        .on('sticky_kit:unbottom', function(e) {
            $(this).parent().css('position', 'relative');
        });
    };
    activeStickyKit();

    function detachStickyKit() {
        $('.sticky-column').trigger("sticky_kit:detach");
    };

    //  stop sticky kit
    //  based on your window width

    var screen = 1200;

    var windowHeight, windowWidth;
    windowWidth = $(window).width();
    if ((windowWidth < screen)) {
        detachStickyKit();
    } else {
        activeStickyKit();
    }

    // windowSize
    // window resize
    function windowSize() {
        windowHeight = window.innerHeight ? window.innerHeight : $(window).height();
        windowWidth = window.innerWidth ? window.innerWidth : $(window).width();
    }
    windowSize();

    function debounce(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };

    $(window).resize(debounce(function(){
        windowSize();
        $(document.body).trigger("sticky_kit:recalc");
        if (windowWidth < screen) {
            detachStickyKit();
        } else {
            activeStickyKit();
        }
    }, 250));


    /*-----------------------------------------------------------------
      Progress bar
    -------------------------------------------------------------------*/

	function progressBar() {
	    $('.progress').each(function() {
		    var ctrl = new ScrollMagic.Controller();
		    new ScrollMagic.Scene({
                triggerElement: '.progress',
	            triggerHook: 'onEnter',
	            duration: 300
            })
            .addTo(ctrl)
		    .on("enter", function (e) {
			    var progressBar = $('.progress-bar');
                progressBar.each(function(indx){
                    $(this).css({'width': $(this).attr('aria-valuenow') + '%', 'z-index': '2'});
                });
		    });
        });
    }


    /*-----------------------------------------------------------------
      Scroll indicator
    -------------------------------------------------------------------*/

    function scrollIndicator() {
        $(window).on('scroll', function() {
            var wintop = $(window).scrollTop(), docheight =
            $(document).height(), winheight = $(window).height();
 	        var scrolled = (wintop/(docheight-winheight))*100;
  	        $('.scroll-line').css('width', (scrolled + '%'));
        });
    }

	scrollIndicator(); //Init


    /*-----------------------------------------------------------------
      Jarallax
    -------------------------------------------------------------------*/

    function parallax() {
        $('.js-parallax').jarallax({
			disableParallax: function () {
			  return isIE
			},
            speed: 0.65,
            type: 'scroll'
        });
	};

	parallax(); //Init*/


    /*-----------------------------------------------------------------
      ScrollTo
    -------------------------------------------------------------------*/

    function scrollToTop() {
        var $backToTop = $('.back-to-top'),
            $showBackTotop = $(window).height();

        $backToTop.hide();


        $(window).scroll( function() {
            var windowScrollTop = $(window).scrollTop();
            if( windowScrollTop > $showBackTotop ) {
                $backToTop.fadeIn('slow');
            } else {
                $backToTop.fadeOut('slow');
            }
        });

		$backToTop.on('click', function (e) {
            e.preventDefault();
            $(' body, html ').animate( {scrollTop : 0}, 'slow' );
        });
    }

	scrollToTop(); //Init

    function unScroll() {
        let top = $(document).scrollTop();

        $(document).on('scroll.unable',function (e) {

            $(document).scrollTop(top);

        })

    }

    function removeUnScroll() {
        $(document).unbind("scroll.unable");
    }


    /*-----------------------------------------------------------------
      Autoresize textarea
    -------------------------------------------------------------------*/

    $('textarea').each(function(){
        autosize(this);
    });


    /*-----------------------------------------------------------------
	  Tabs
    -------------------------------------------------------------------*/

	$('.js-tabs').each(function(){
	    $('.content .tabcontent').hide();
        $('.content .tabcontent:first').show();
        $('.nav__item a').on('click', function () {
            $('.nav__item a').removeClass('active');
            $(this).addClass('active');
            var currentTab = $(this).attr('href');
            $('.content .tabcontent').hide();
            $(currentTab).show();
            $portfolioMasonry.isotope ({
                columnWidth: '.gallery-grid__item',
                gutter: '.gutter-sizer',
                isAnimated: true
            });
			$('.js-scroll').getNiceScroll().resize()
            return false;
        });

		// Mobile close menu
	    var screenMobile = 580;

	    windowWidth = $(window).width();
        if ((windowWidth < screenMobile)) {
			// autoscroll to content
            $(".nav__item a").click(function(e) {
		        e.preventDefault();
		        var offset = -35;

                $('html, body').animate({
                    scrollTop: $("#content").offset().top + offset
                }, 0);
            });
	    } else {

	    }
	});


    /*-----------------------------------------------------------------
      Tooltip
    -------------------------------------------------------------------*/

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });


    /*-----------------------------------------------------------------
      Switch categories & Filter mobile
    -------------------------------------------------------------------*/

    $('.select').on('click','.placeholder',function(){
      var parent = $(this).closest('.select');
      if ( ! parent.hasClass('is-open')){
          parent.addClass('is-open');
          $('.select.is-open').not(parent).removeClass('is-open');
      }else{
          parent.removeClass('is-open');
      }
    }).on('click','ul>li',function(){
        var parent = $(this).closest('.select');
        parent.removeClass('is-open').find('.placeholder').text( $(this).text() );
        parent.find('input[type=hidden]').attr('value', $(this).attr('data-value') );

	    $('.filter__item').removeClass('active');
	    $(this).addClass('active');
	    var selector = $(this).attr('data-filter');

	    $('.js-filter-container').isotope({
	        filter: selector
	    });
	    return false;
    });


    /*-----------------------------------------------------------------
      Masonry
    -------------------------------------------------------------------*/

    // Portfolio grid row
    var $portfolioMasonry = $('.js-grid-row').isotope({
        itemSelector: '.gallery-grid__item',
	    layoutMode: 'fitRows',
        percentPosition: true,
	    transitionDuration: '0.5s',
        hiddenStyle: {
            opacity: 0,
            transform: 'scale(0.001)'
        },
        visibleStyle: {
            opacity: 1,
            transform: 'scale(1)'
        },
        fitRows: {
            gutter: '.gutter-sizer'
        },
        masonry: {
	        columnWidth: '.gallery-grid__item',
            gutter: '.gutter-sizer',
            isAnimated: true
        }
    });

    $portfolioMasonry.imagesLoaded().progress( function() {
        $portfolioMasonry.isotope ({
	        columnWidth: '.gallery-grid__item',
            gutter: '.gutter-sizer',
            isAnimated: true,
	        layoutMode: 'fitRows',
            fitRows: {
                gutter: '.gutter-sizer'
            }
	    });
    });

	// Portfolio grid irregular
	var $portfolioIrregularMasonry = $('.js-grid').isotope({
        itemSelector: '.gallery-grid__item',
        percentPosition: true,
	    transitionDuration: '0.5s',
        hiddenStyle: {
            opacity: 0,
            transform: 'scale(0.001)'
        },
        visibleStyle: {
            opacity: 1,
            transform: 'scale(1)'
        },
        masonry: {
	        columnWidth: '.gallery-grid__item',
            gutter: '.gutter-sizer',
            isAnimated: true
        }
    });

    $portfolioIrregularMasonry.imagesLoaded().progress( function() {
        $portfolioIrregularMasonry.isotope ({
	        columnWidth: '.gallery-grid__item',
            gutter: '.gutter-sizer',
            isAnimated: true
	    });
    });


    /*-----------------------------------------------------------------
      niceScroll
    -------------------------------------------------------------------*/

    $('textarea').niceScroll({
		horizrailenabled:false
	});


    /*-----------------------------------------------------------------
      emoji add in textarea
    -------------------------------------------------------------------*/

    $(function() {
        $('.emoji-wrap img').on('click', function(){
            var emoji = $(this).attr('title');
            $('#commentForm').val($('#commentForm').val()+" "+emoji+" ");
        });
    });


    /*-----------------------------------------------------------------
	  mediumZoom
    -------------------------------------------------------------------*/

    mediumZoom('[data-zoom]', {
        margin: 30
    });


    /*-----------------------------------------------------------------
      Lazyload
    -------------------------------------------------------------------*/

    lazySizes.init();


    /*-----------------------------------------------------------------
      Polyfill object-fit
    -------------------------------------------------------------------*/

    var $someImages = $('img.cover');
    objectFitImages($someImages);

    /*-----------------------------------------------------------------
     Dark mode checkbox monitor
    -------------------------------------------------------------------*/
    $(".toggle-input").change(function() {
        let status = $(".toggle-input").is(':checked');
        setDarkMode(status);
        Cookies.set('dark-mode', status, {expires: 30})
    });

    let mode_status_by_cookie=Cookies.get('dark-mode');
    if([true, false, 'false', 'true'].indexOf(mode_status_by_cookie)!==-1){
        if(typeof mode_status_by_cookie==='string'){
            mode_status_by_cookie = $.parseJSON(mode_status_by_cookie.toLowerCase());
        }
        setDarkMode(mode_status_by_cookie);
    }else{
        autoSetDarkMode()
    }

    /*-----------------------------------------------------------------
     terminal
    -------------------------------------------------------------------*/

    // UTILITY
    function getRandomInt(min, max) {
            return Math.floor(Math.random() * (max - min)) + min;
    }
    // END UTILITY

    // COMMANDS
    function clear() {
        terminal.text("");
    }

    function help() {
        terminal.append("There is no help... MUAHAHAHAHA. >:D\n");
    }
    function login() {
        terminal.append("欢迎来到我的博客，您正在进行登陆操作:\n");
        terminal.append("用户名:");
        is_login=true
    }

    function echo(args) {
        var str = args.join(" ");
        terminal.append(str + "\n");
    }
    // END COMMANDS
    var _t = $(".terminal-box");
    var title = $(".terminal-box .title");
    var terminal = $(".terminal");
    var terminal_box = _t[0];
    var prompt = "➜";
    var path = "~";
    var prepare = false;
    var username = false;
    var password = false;
    var is_login = false;

    var commandHistory = [];
    var historyIndex = 0;

    var command = "";
    var commands = [{
                    "name": "clear",
                    "function": clear
            }, {
                    "name": "help",
                    "function": help
            }, {
                    "name": "login",
                    "function": login
            }, {
                    "name": "echo",
                    "function": echo
            }];
    _t.mouseover(function(){
       unScroll()
    }).mouseleave(function () {
        removeUnScroll()
    });
    function processCommand() {
            var isValid = false;

            // Create args list by splitting the command
            // by space characters and then shift off the
            // actual command.

            var args = command.split(" ");
            var cmd = args[0];
            args.shift();

            // Iterate through the available commands to find a match.
            // Then call that command and pass in any arguments.
            for (var i = 0; i < commands.length; i++) {
                    if (cmd === commands[i].name) {
                            commands[i].function(args);
                            isValid = true;
                            break;
                    }
            }

            // No match was found...
            if(!is_login){
                if (!isValid) {
                    terminal.append("zsh: command not found: " + command + "\n");
                }
                commandHistory.push(command);
                historyIndex = commandHistory.length;
            }
            // Add to command history and clean up.
            if(!is_login){
                command = "";
            }

    }

    function displayPrompt() {
            terminal.append("<span class=\"prompt\">" + prompt + "</span> ");
            terminal.append("<span class=\"path\">" + path + "</span> ");
    }

    // Delete n number of characters from the end of our output
    function erase(n) {
            command = command.slice(0, -n);
            terminal.html(terminal.html().slice(0, -n));
    }

    function clearCommand() {
            if (command.length > 0) {
                    erase(command.length);
            }
    }

    function appendCommand(str) {
            if(is_login&&username&&!password){
                terminal.append("*");
            }else{
                terminal.append(str);
            }
            command += str;
    }

    /*
    //  Keypress doesn't catch special keys,
    //  so we catch the backspace here and
    //  prevent it from navigating to the previous
    //  page. We also handle arrow keys for command history.
    */

    $(document).keydown(function(e) {
            e = e || window.event;
            var keyCode = typeof e.which === "number" ? e.which : e.keyCode;

            // BACKSPACE
            if (keyCode === 8 && e.target.tagName !== "INPUT" && e.target.tagName !== "TEXTAREA") {
                    e.preventDefault();
                    if (command !== "") {
                            erase(1);
                    }
            }
            // UP or DOWN
            if (keyCode === 38 || keyCode === 40) {
                    // Move up or down the history
                    if (keyCode === 38) {
                            // UP
                            historyIndex--;
                            if (historyIndex < 0) {
                                    historyIndex++;
                            }
                    } else if (keyCode === 40) {
                            // DOWN
                            historyIndex++;
                            if (historyIndex > commandHistory.length - 1) {
                                    historyIndex--;
                            }
                    }

                    // Get command
                    var cmd = commandHistory[historyIndex];
                    if (cmd !== undefined) {
                            clearCommand();
                            appendCommand(cmd);
                    }
            }
    });

    function handle_login(){
        $.ajax({
            type: 'post',
            url: '/api/user/login',
            data:{
                username: username.join(""),
                password: password.join("")
            },
            success: function (data) {
                terminal.append(data.msg+'\n');
                if(data.code===0){
                    Cookies.set('token', data.token, { expires: 7, sameSite: 'Lax' });
                    location.reload();
                }else{
                    displayPrompt()
                }
                terminal.scrollTop(terminal[0].scrollHeight);
            },
            error: function (error) {
                alert('request error')
            }
        })
    }

    $(document).keypress(function(e) {
        // Make sure we get the right event
        e = e || window.event;
        var keyCode = typeof e.which === "number" ? e.which : e.keyCode;

        // Which key was pressed?
        switch (keyCode) {
            // ENTER
            case 13:
                {
                    terminal.append("\n");
                    processCommand();
                    if(is_login){
                        if(prepare){
                            if(!username){
                                if(command===""){
                                    terminal.append("用户名不能为空，请重新输入！\n用户名：");
                                }else{
                                    username=command.split(" ");
                                    terminal.append("密码:");
                                }
                                command = "";
                            }else if (username&&!password){
                                if(command===""){
                                    terminal.append("密码不能为空，请重新输入！\n密码：");
                                }else{
                                    password=command.split(" ");
                                    handle_login();
                                    username=false;
                                    password=false;
                                    is_login=false;
                                    prepare=false;
                                    command = "";
                                }

                            }
                        }else{
                            prepare=true;
                            command = "";
                        }

                    }else{
                        displayPrompt();
                    }
                    terminal.scrollTop(terminal[0].scrollHeight);
                    break;
                }
            default:
                {
                    appendCommand(String.fromCharCode(keyCode));
                }
        }
    });

    // Set the window title
    title.text("MacBookPro: ~ (zsh)");

    // Get the date for our fake last-login
    var date = new Date().toString(); date = date.substr(0, date.indexOf("GMT") - 1);

    // Display last-login and promt
    terminal.append("Last login: " + date + " on ttys000\n"); displayPrompt();

    var isMouseDown,
        initX,
        initY,
        height = terminal[0].offsetHeight,
        width = terminal[0].offsetWidth,

        dragBoxBar = document.getElementById('dragBoxBar');


    dragBoxBar.addEventListener('mousedown', function(e) {
        isMouseDown = true;
        document.body.classList.add('no-select');
        terminal[0].classList.add('pointer-events');
        initX = e.offsetX;
        initY = e.offsetY;
        terminal_box.style.opacity = 0.5;
    })

    dragBoxBar.addEventListener('mouseup', function(e) {
        mouseupHandler();
    })

    document.addEventListener('mousemove', function(e) {
        if (isMouseDown) {
            var cx = e.clientX - initX,
                cy = e.clientY - initY;
            if (cx < 0) {
                cx = 0;
            }
            if (cy < 0) {
                cy = 0;
            }
            if (window.innerWidth - e.clientX + initX < width + 16) {
                cx = window.innerWidth - width;
            }
            if (e.clientY > window.innerHeight - height - dragBoxBar.offsetHeight + initY) {
                cy = window.innerHeight - dragBoxBar.offsetHeight - height;
            }
            terminal_box.style.left = cx + 'px';
            terminal_box.style.top = cy + 'px';
        }
    })


    document.addEventListener('mouseup', function(e) {
        if (e.clientY > window.innerWidth || e.clientY < 0 || e.clientX < 0 || e.clientX > window.innerHeight) {
            mouseupHandler();
        }
    });

    function mouseupHandler() {
        isMouseDown = false;
        document.body.classList.remove('no-select');
        terminal[0].classList.remove('pointer-events');
        terminal_box.style.opacity = 1;
    }

});

var terminal_status = false;


$('.close2').on('click',function () {
    $('.terminal-box').hide();
    terminal_status = false
});

$('#show_terminal').on('click', function () {
    // 移除焦点，否则回车时终端会消失
    $('#show_terminal').blur();

    if(!terminal_status){
        $('.terminal-box').show();
        terminal_status = true
    }else{
        $('.terminal-box').hide();
        terminal_status = false
    }
    return false;
});
