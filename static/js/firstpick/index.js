$(document).ready(function(){
  
	$(".event_box" ).click(function(){
		details = $(this).children(".event_details");
		if (details.hasClass("hide")){
			details.removeClass("hide");
		} else {
			details.addClass("hide");
		}
	});

	$(".events_header" ).click(function(){
		details = $(this).parent().children(".events_list");
		if (details.hasClass("hide")){
			details.removeClass("hide");
		} else {
			details.addClass("hide");
		}
	});

});