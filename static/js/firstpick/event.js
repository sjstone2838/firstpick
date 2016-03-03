$(document).ready(function(){
  
	$( "#rating_range" ).val($( "#slider-range" ).slider( "values", 0 ) +
	      " - " + $( "#slider-range" ).slider( "values", 1) + " stars");
	
	$("#map_box").css("max-height","0px");

	// EXPAND MAP TO BECOME VISIBLE; MAP NEEDS TO BE SHOWN TO LOAD PROPERLY
	$("#pac-input").focus(function(){
		$("#map_box").css("max-height","100%");
	});

	$("#pac-input").focusout(function(){
		$("#map_box").css("max-height","0px");
	});
	

	function checkEventComplete(){
		// if ($("#name").val() == ""){
		//	$("#submit_error").removeClass("hide").html("Please name your game");
		//	return false;
		//} else 
		if ($("#sport").val() == null){
			$("#submit_error").removeClass("hide").html("Please choose a sport");
			return false;
		} else if ($("#date").val()  == ""){
			$("#submit_error").removeClass("hide").html("Please choose a date");
			return false;
		} else if ($("#time").val() == ""){
			$("#submit_error").removeClass("hide").html("Please choose a start time");
			return false;
		} else if ($("#duration").val() == null){
			$("#submit_error").removeClass("hide").html("Please choose game duration");
			return false;
		} else if ($("#location_name").val() == ""){
			$("#submit_error").removeClass("hide").html("Please name your location");
			return false;
		} else if ($("#pac-input").val() == "" || $("#lat").html() == "NONE" || $("#lng").html() == "NONE" ){
			$("#submit_error").removeClass("hide").html("Please select a location address");
			return false;
		} else if ($("#gender").val() == null ){
			$("#submit_error").removeClass("hide").html("Please select a gender preference");
			return false;
		} else if ($("#rating_min_slider").val() > $("#rating_max_slider").val() ){
			$("#submit_error").removeClass("hide").html("Max rating must exceed min rating");
			return false;
		} else if ($("#players_needed").val() == null ){
			$("#submit_error").removeClass("hide").html("Please select the number of players you want to recruit");
			return false;
		} else {
			return true;
		}

	}

	$('.submit').click(function(){
		$("#event_created").addClass("hide");
		$("#no_invites_sent_msg").addClass("hide");
		$("#invites_sent_msg").addClass("hide");
		if (checkEventComplete()) {
			var data = {
				'notes': $("#notes").val(),
	        	'sport': $("#sport").val(),
	        	'date': $("#date").val(),
	        	'time': $("#time").val(),
	        	'duration': $("#duration").val(),
	        	'location_name': $("#location_name").val(),
	        	'address': $("#pac-input").val(),
	        	'gender': $("#gender").val(),
	        	'lat': $("#lat").html(),
	        	'lng': $("#lng").html(),
	        	'rating_min': $("#slider-range").slider("values",0),
	        	'rating_max': $("#slider-range").slider("values",1),
	        	'players_needed': $("#players_needed").val(),
			}
			$("#refresh_wheel").removeClass("hide");
			if ($(this).attr("id") == "create_event"){
				$.ajax({
			        type: 'POST',
			        url: '/firstpick/create_event/',
			        data: data,
			        success: function(response) {
			        	$("#refresh_wheel").addClass("hide");
		            	$("#create_box").addClass("hide");
		            	$("#event_created").removeClass("hide");
		            	if (response.invites_sent == 0){
		            		$("#no_invites_sent_msg").removeClass("hide");
		            	} else {
		            		$("#invites_sent_msg").removeClass("hide");
		            		$("#invites_sent").html(response.invites_sent);
		            		if (response.invites_sent == 1){
		            			$("#invites_sent_pluralize").html("player");
		            		} else {
		            			$("#invites_sent_pluralize").html("players");
		            		}
		            	}
		        	}
			    });
			} else if ($(this).attr("id") == "edit_event") {
				data['eventpk'] = $("#eventpk").html();
				$.ajax({
			        type: 'POST',
			        url: '/firstpick/save_event/',
			        data: data,
			        success: function(response) {
			        	console.log(response.status);
		            	$("#refresh_wheel").addClass("hide");
		            	$("#create_box").addClass("hide");
		            	$("#event_saved").removeClass("hide");
		        	}
			    });
			} else {
				data = {'eventpk': $("#eventpk").html()};
				$.ajax({
			        type: 'POST',
			        url: '/firstpick/cancel_event/',
			        data: data,
			        success: function(response) {
			        	console.log(response.status);
		            	$("#refresh_wheel").addClass("hide");
		            	$("#create_box").addClass("hide");
		            	$("#event_saved").removeClass("hide");
		        	}
			    });

			}
		}
	});

	$("#create_another").click(function(){
		$("#create_box").removeClass("hide");
		$("#event_created").addClass("hide");
	});

});