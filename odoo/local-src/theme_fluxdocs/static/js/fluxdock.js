$(document).ready(function() {
	
	console.log('fluxdocs.js is here :-)');
    
	
	$(window).scroll(function(event) {
		var scrollPosition = $(window).scrollTop();
		var logo = $('.fluxdock-header-logo');
		if(scrollPosition > 500){
			logo.addClass('visible-scroll');
		}else{
			logo.removeClass('visible-scroll');
		}
    });
	
});