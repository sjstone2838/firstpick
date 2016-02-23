$(document).ready(function(){
  
	$(".event_header" ).click(function(){
		details = $(this).parent().children(".event_details");
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

	//Show google map for event when "show map" clicked
	$(".togglemap").click(function(){
		var eventpk = $(this).attr("id").split("_")[1];	
		if ($(this).text() == "Show map"){
			$("#map_" + eventpk).css("height","300px");
			var pos = {lat: parseFloat($(this).attr("id").split("_")[2]), lng: parseFloat($(this).attr("id").split("_")[3])};
			
			var map = new google.maps.Map(document.getElementById('map_'+ eventpk), {
			  center: pos,
			  zoom: 12,
			  scrollwheel: false,
			  mapTypeControl:false,  
			});
		    var marker = new google.maps.Marker({
		        map: map,
		        position: pos,
		        draggable: false,
		    });
			$(this).text("Hide map");
		} else {
			$(this).text("Show map");
			$("#map_" + eventpk).css("height","0px");
		}
	});

});