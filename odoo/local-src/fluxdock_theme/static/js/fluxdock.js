$(document).ready(function() {

	function openMobileMenu() {
		//OPEN MENU
		$('#mobile-menu-trigger').addClass('open');
		$('nav.mobile-menu').animate(
			{right: "0"},
			260,
			function() {
				$('nav.mobile-menu').addClass('menu-open');
			});

		$('body #wrapwrap, body #wrapwrap #fluxdock_header').animate(
			{
				left: "-260",
				right: "260",
			},
			260);
	}

	function closeMobileMenu() {
		//CLOSE MENU
		$('#mobile-menu-trigger').removeClass('open');
		$('nav.mobile-menu').animate({
			right: "-260"
		}, 260).removeClass('menu-open');

		$('body #wrapwrap, body #wrapwrap #fluxdock_header').animate({
			left: "0",
			right: "0",
		}, 260);
	}

	$('#mobile-menu-trigger').on('click', function() {

		if($('#mobile-menu-trigger').hasClass('open')){
			closeMobileMenu();
		}else{
			openMobileMenu();
		}

	});

	$('body #wrapwrap').on('touchstart click', function() {
		if($('nav.mobile-menu').hasClass('menu-open')){
			closeMobileMenu();
		}
	});

	//Header logo fadein
	if($('section.animated-logo').length > 0){
		$(window).scroll(function(event) {
			var scrollPosition = $(window).scrollTop();
			var logo = $('.fluxdock-header-logo');
			if(scrollPosition > 500){
				logo.addClass('visible-scroll');
			}else{
				logo.removeClass('visible-scroll');
			}
	    });
	}else{
		$('.fluxdock-header-logo').addClass('visible-scroll');
	}

	// FIXME: since the slider is a snippet we should move this to snippet JS
	var boxWidth = 157;
	var setup_members_slider = function set_members_slide(membersWrap){
		var membersSlide = membersWrap.find('.members-slide');
		var membersContainer = membersWrap.find('.members-container');
		var rightArrow = membersWrap.find('.arrow-right');
		var leftArrow = membersWrap.find('.arrow-left');
		var memberSlideIndex = 0;

		leftArrow.addClass('disabled');

		//Set width
		var boxRows = Math.ceil(membersWrap.find('.members-box').length / 2);
		var width = boxRows * boxWidth;
		membersSlide.css('width', width);

		function updateArrows(membersWrap){
			if(memberSlideIndex == 0){
				leftArrow.addClass('disabled');
			}else{
				leftArrow.removeClass('disabled');
			}

			if(memberSlideIndex == boxRows - getVisibleRows()){
				rightArrow.addClass('disabled');
			}else{
				rightArrow.removeClass('disabled');
			}
		}

		function slideTo(){
			membersSlide.animate({left: -memberSlideIndex*boxWidth}, 250)
		}

		/*
		 * Returns if 2 or 4 rows are visible
		 */
		function getVisibleRows(){
			console.log(membersContainer.width());
			if(membersContainer.width() > 292){
				return 4;
			}else{
				return 2;
			}
		}

		function indexBounds(index){
			if(index < 0){
				index = 0;
			}
			else if(index > boxRows-getVisibleRows()){
				index = boxRows-getVisibleRows();
			}
			return index;
		}


		//Events
		leftArrow.click(function() {
			if(memberSlideIndex > 0){
				memberSlideIndex = memberSlideIndex - getVisibleRows();
				memberSlideIndex = indexBounds(memberSlideIndex);
				slideTo();
			}

			//Update arrows
			updateArrows(membersWrap);
		});

		rightArrow.click(function() {
			if(memberSlideIndex <= boxRows-getVisibleRows()){
				memberSlideIndex = memberSlideIndex + getVisibleRows();
				memberSlideIndex = indexBounds(memberSlideIndex);
				slideTo();
			}

			//Update arrows
			updateArrows(membersWrap);
		});
	}

	//Members slider
	// NOTE: sometime the ajax call could fail because of this error.
	// If it happens again we should add a trailing slash at the end of the url.
	// http://stackoverflow.com/questions/37314650/ajax-calls-to-fail-with-mixed-content-http-https-errors-cant-force-https
	// http://stackoverflow.com/questions/41865180/mixed-content-jquery-ajax-https-request-has-been-blocked-on-laravel
	var member_template = '<div class="members-box">' +
		'<a href="<%- url %>" title="<%- name %>">' +
			'<img src="<%- avatar_url %>" />' +
		'</a>' +
	'</div>';
	$('.members-wrap').each(function() {
		var template = _.template(member_template)
		var membersWrap = $(this);
		var slider = membersWrap.find('.members-slide');
		// collect members from backend
		$.getJSON('/members/json').done(function(response) {
		    if(response.ok){
				// prepare and inject final html
				var html = '';
				$.each(response.members, function(){
					html += template(this);
				})
				slider.html(html);
				// is hidden by default
				membersWrap.fadeIn('slow');
				// init the slider
				setup_members_slider(membersWrap);
			}
		});
	});


	//Project search
	$('form.projects-search-panel').submit(function(event) {
		event.preventDefault();
		filter();
	});

	$('input.filter').keyup(function(event) {
		console.log('typed something');
		filter();
	});

	$('select.filter').change(function(event) {
		filter();
	});

	function filter(){
		//show all
		$('.filterable').show();

		//Filter title
		$('input[type="text"].filter').each(function() {
			var facet = $(this).data('facet');
			if(facet == 'title'){
				var searchString = $(this).val();
				$('.filterable').each(function() {
					var title = $(this).find('.title').text();
					console.log(title, searchString);
					if(title.toLowerCase().indexOf(searchString.toLowerCase().trim()) == -1){
						$(this).hide();
					}
				});
			}
		});

		//Filter selects
		$('select.filter').each(function() {
			var facet = $(this).data('facet');
			var value = $(this).val();
			if(value != 'all'){
				$('.filterable:not([data-facet-'+facet+'="'+value+'"])').hide();
			}
		});

	}

	//Init Carousel with bxslider
	$('.bxslider').each(function(){
		var data = $(this).data('slider') ? $(this).data('slider'): {};
		var only_one = $(this).children().length < 2;
		if(only_one){
			data['auto'] = false;
		}
		$(this).bxSlider(data);
		if(only_one){
			// remove useless controls
			$(this).closest('.bx-wrapper').find('.bx-controls').remove();
		}
	})

	//Accordion
	$('.accordion-trigger').on('click', function(event) {
		var accordion = $(event.currentTarget).closest('.accordion');
		accordion.toggleClass('open');
		if(accordion.hasClass('open')){
			accordion.find('.accordion-content').slideDown();
		}else{
			accordion.find('.accordion-content').slideUp();
		}

	});

	// disable links and buttons
	$('a.disabled, button.disabled').click(function(evt){
		evt.preventDefault();
		return false;
	})

});
