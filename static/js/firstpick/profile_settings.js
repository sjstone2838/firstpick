$(document).ready(function(){
	var page = 0;
	var sports = [];
	var RADIUS_DEFAULT = 5;

	$("#settings_page-1").css("max-height","0px");


	function showNext(n){
		$("#settings_page-" + n).addClass("hide");
		n += 1;
		$("#settings_page-" + n).removeClass("hide");
	}

	$(".settings_back").click(function(){
		n = $(this).attr("id").split("-")[1];
		$("#settings_page-" + n).addClass("hide");
		n -= 1;
		$("#settings_page-" + n).removeClass("hide");
	});	

	$("#reset_password").click(function(){
		$("#reset_password_box").toggle();
	})

	// VERIFY ALL FIELDS FILLED IN BEFORE SHOWING NEXT PAGE
	$(".settings_next").click(function(){
		n = parseInt($(this).attr("id").split("-")[1]);
		if (n == 0 && ($("#first_name").val() == "" || $("#last_name").val() == "" || $("#email").val() == "" || $("#gender").val() == null)) {
			$("#settings_error-" + n).removeClass("hide");
	 	} else if ($("#new_pw").val() != $("#new_pw_confirm").val()){
	 		$("#password_error").removeClass("hide");
		} else if (n == 1 && ($("#home_lat").val() == "None" || $("#home_lat").val() == "None")){
			$("#settings_error-" + n).removeClass("hide");
		} else if (n == 2 && $("#sport_selection").find('input:checked').length == 0){
			$("#settings_error-" + n).removeClass("hide");
		// NOTHING TO CHECK FOR page 3; page 4 handled separately
		} else {
			// EXPAND MAP TO BECOME VISIBLE; MAP NEEDS TO BE SHOWN TO LOAD PROPERLY
			if (n == 0){
				$("#settings_page-1").css("max-height","100%");
			}
			$("#settings_error-" + n).addClass("hide");
			$("#password_error").addClass("hide");
			showNext (n);
		}
	});

	// show dist and stars for selected sports
	$("#next-2").click(function(){
		$(".dist_data").addClass("hide");
		$(".stars").addClass("hide");
		sports = $("#sport_selection").find('input:checked').map(function () {
  			return this.value;
		}).get();
		
		$.each(sports, function(i, sport){
			$("#" + sport + "_dist_data").removeClass("hide");
			$("#" + sport + "_stars").removeClass("hide");
		});
	});

	// adjust distance
	$(".adjust_dist").click(function(){
		var sport = $(this).attr("id").split("_")[0];
		var radius = parseInt($("#" + sport + "_dist").html());
		if ($(this).hasClass("increment_dist")){
			radius += 1;
		} else {
			if (radius != 1){
				radius -= 1;
			}
		}
		$("#" + sport + "_dist").html(radius);
		if (radius == 1){
			$("#" + sport + "_miles").html("mile");
			$("#" + sport + "_down").addClass("hide");
		} else {
			$("#" + sport + "_miles").html("miles");
			$("#" + sport + "_down").removeClass("hide");
		}
	});

	// adjust stars
	$(".star").click(function(){
		sport = $(this).attr("id").split("_")[0];
		n = $(this).attr("id").split("_")[2];
		$("#" + sport + "_stars").find(".star").each(function(){
			$(this).html("&#9734").removeClass("active");
			i = $(this).attr("id").split("_")[2];
			if (i <= n){
				$(this).html("&#9733").addClass("active");
			}
		});
	})
	
	// submit data
	$("#submit").click(function(){
		var ratings = 0;
		
		$.each(sports, function(i, sport){
			if( $("#" + sport + "_stars").find(".star.active").length == 0){
				$("#settings_error-4").removeClass("hide");
				ratings += 1;
			}
		});
		if (ratings == 0){
			sport_profiles = []
			$.each(sports, function(i, sport){
				temp = {};
				temp['sport'] = sport;
				temp['radius'] = $("#" + sport + "_dist").html()
				temp['stars'] = $("#" + sport + "_stars").find(".active").length;
				sport_profiles.push(temp);
			});
			$("#refresh_wheel").removeClass("hide");
			$.ajax({
		        type: 'POST',
		        url: '/firstpick/save_profile/',
		        data: {
		        	'first_name': $("#first_name").val(),
		        	'last_name': $("#last_name").val(),
		        	'email': $("#email").val(),
		        	'username': $("#username").val(),
		        	'gender': $("#gender").val(),
		        	'new_pw': $("#new_pw").val(),
		        	'new_pw_confirm': $("#new_pw_confirm").val(),
		        	'address': $("#pac-input").val(),
		        	'home_lat': $("#home_lat").val(),
		        	'home_lng': $("#home_lng").val(),
		        	'sport_profiles': sport_profiles,
		        	'sport_count': sports.length,
		        },
		        success: function(response) {
					$("#refresh_wheel").addClass("hide");
	            	if (response.status == "Passwords do not match"){
	            		$(".settings_page").addClass("hide");
	            		$("#settings_page-0").removeClass("hide");
	            		$("#password_error").removeClass("hide");
	            	} else {
	            		location.href = "/firstpick/";
	            	}
	        	}
		    });
	    }
	});

});

 