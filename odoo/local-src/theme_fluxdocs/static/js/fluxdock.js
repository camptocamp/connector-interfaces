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
		
		$('body #wrapwrap, body #wrapwrap #my_header').animate(
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
		
		$('body #wrapwrap, body #wrapwrap #my_header').animate({
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
	
	//Members slider
	var boxWidth = 157;
	$('.members-wrap').each(function() {
		var membersWrap = $(this);
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
		
	});
	
	
	//Project search
	$('form.search-panel').submit(function(event) {
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
	$('.bxslider').bxSlider();
	
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
	
});
