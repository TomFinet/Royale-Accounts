jQuery(document).ready(function ($) {

	var accessDetailLink = $(".toggle-access-details")
	var accessDetails = $(".access-details")

	accessDetailLink.click(function(){
    	if (accessDetails.style.display === "none") {
        	x.style.display = "block";
    	} else {
        	x.style.display = "none";
    	}
	});

});