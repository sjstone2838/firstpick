$(document).ready(function(){
	
	$(".msg_header").click(function(){
		var body = $(this).find(".msg_body");
		if (body.hasClass("hide")){
			body.removeClass("hide");
		} else {
			body.addClass("hide");
		}
	});

});

 