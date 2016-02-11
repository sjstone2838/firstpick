$(document).ready(function(){
  
	$(".event_box" ).click(function(){
		details = $(this).children(".event_details");
		if (details.hasClass("hide")){
			details.removeClass("hide");
		} else {
			details.addClass("hide");
		}
	});
	

});