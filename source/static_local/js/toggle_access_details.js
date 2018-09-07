jQuery(document).ready(function ($) {

	var accessDetailButton = $(".toggle-access-details")
	var accessDetails = $(".access-details")

	accessDetailButton.click(function(){
    	if (accessDetails.hasClass('hidden')) {
        	accessDetails.removeClass('hidden')
        	$('.fa-chevron-down').removeClass("fa-chevron-down").addClass("fa-chevron-up")
    	} else {
        	accessDetails.addClass('hidden')
        	$(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down")
    	}
	});

});