$(document).ready(function(){

	$(".slider").click(function(){
		$(this).parent().find("span").html($(this).val())
		if ($("#rating_min_slider").val() > $("#rating_max_slider").val()){
			$("#slider_error").removeClass("hide");
		} else {
			$("#slider_error").addClass("hide");
		}
	});

	$("#pac-input").focusout(function(){
		$(".settings_map").addClass("hide")
	});

	$("#pac-input").focus(function(){
		$(".settings_map").removeClass("hide")
	});

	$('#submit').click(function(){
		$("#event_created").addClass("hide");
		$("#no_invites_sent_msg").addClass("hide");
		$("#invites_sent_msg").addClass("hide");

		if ($("#name").val() == ""){
			$("#submit_error").removeClass("hide").html("Please name your game");
		} else if ($("#sport").val() == null){
			$("#submit_error").removeClass("hide").html("Please choose a sport");
		} else if ($("#date").val()  == ""){
			$("#submit_error").removeClass("hide").html("Please choose a date");
		} else if ($("#time").val() == ""){
			$("#submit_error").removeClass("hide").html("Please choose a start time");
		} else if ($("#location_name").val() == ""){
			$("#submit_error").removeClass("hide").html("Please name your location");
		} else if ($("#pac-input").val() == "" || $("#lat").html() == "NONE" || $("#lng").html() == "NONE" ){
			$("#submit_error").removeClass("hide").html("Please select a location address");
		} else if ($("#gender").val() == null ){
			$("#submit_error").removeClass("hide").html("Please select a gender preference");
		} else if ($("#rating_min_slider").val() > $("#rating_max_slider").val() ){
			$("#submit_error").removeClass("hide").html("Max rating must exceed min rating");
		} else if ($("#players_needed").val() == null ){
			$("#submit_error").removeClass("hide").html("Please select the number of players you want to recruit");
		} else {
			$.ajax({
		        type: 'POST',
		        url: '/firstpick/create_event/',
		        data: {
		        	'name': $("#name").val(),
		        	'sport': $("#sport").val(),
		        	'date': $("#date").val(),
		        	'time': $("#time").val(),
		        	'location_name': $("#location_name").val(),
		        	'gender': $("#gender").val(),
		        	'lat': $("#lat").html(),
		        	'lng': $("#lng").html(),
		        	'rating_min': $("#rating_min").html(),
		        	'rating_max': $("#rating_max").html(),
		        	'players_needed': $("#players_needed").val(),
		        },
		        success: function(response) {
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
		}
	});

	$("#create_another").click(function(){
		$("#create_box").removeClass("hide");
		$("#event_created").addClass("hide");
	});

});