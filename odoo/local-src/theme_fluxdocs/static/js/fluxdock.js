$(document).ready(function() {
	
    
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
		var rightArrow = membersWrap.find('.arrow-right');
		var leftArrow = membersWrap.find('.arrow-left');
		var memberSlideIndex = 0;
		
		leftArrow.addClass('disabled');
		
		//Set width 
		var boxes = Math.ceil(membersWrap.find('.members-box').length / 2);
		console.log(boxes);
		var width = boxes * boxWidth;
		membersSlide.css('width', width);
		
		function updateArrows(membersWrap){
			if(memberSlideIndex == 0){
				leftArrow.addClass('disabled');
			}else{
				leftArrow.removeClass('disabled');
			}
			
			if(memberSlideIndex == boxes-1){
				rightArrow.addClass('disabled');
			}else{
				rightArrow.removeClass('disabled');
			}
		}
		
		function slideTo(membersWrap){
			membersSlide.animate({left: -memberSlideIndex*boxWidth}, 250)
		}
		
		//Events
		leftArrow.click(function() {
			if(memberSlideIndex > 0){
				memberSlideIndex--;
				slideTo();
			}
			
			//Update arrows
			updateArrows(membersWrap);
		});
		rightArrow.click(function() {
			if(memberSlideIndex < boxes-1){
				memberSlideIndex++;
				slideTo();
			}
			
			//Update arrows
			updateArrows(membersWrap);
		});
		
	});
	
	
	
	
});