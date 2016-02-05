$(document).ready(function(){
	var page = 0;
	var sports = [];
	var RADIUS_DEFAULT = 5;

	$("#settings_page-1").css("max-height","0px");

	$("#next-0").click(function(){
		$("#settings_page-1").css("max-height","100%");
	});

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

	// VERIFY ALL FIELDS FILLED IN BEFORE SHOWING NEXT PAGE
	$(".settings_next").click(function(){
		n = parseInt($(this).attr("id").split("-")[1]);
		if (n == 0 && ($("#first_name").val() == "" || $("#last_name").val() == "" || $("#email").val() == "" || $("#gender").val() == "")) {
			$("#settings_error-" + n).removeClass("hide")
		} else if (n == 1 && ($("#home_lat").html() == "None" || $("#home_lat").html() == "None")){
			$("#settings_error-" + n).removeClass("hide")
		} else if (n == 2 && $("#sport_selection").find('input:checked').length == 0){
			$("#settings_error-" + n).removeClass("hide")
		// NOTHING TO CHECK FOR page 3; page 4 handled separately
		} else {
			$("#settings_error-" + n).addClass("hide")
			showNext (n)
		}
	});

	// show dist and stars for selected sports
	$("#next-2").click(function(){
		sports = $("#sport_selection").find('input:checked').map(function () {
  			return this.value;
		}).get();

		$("#sport_radius, #self_rating").html("");
		$.each(sports, function(i, sport){
			x = "<p>" +  sport +"<span class = 'sport_dist'><span class = 'hide adjust_dist decrement_dist' id = '" +sport+"_down'>&#9660</span> <span id = '" +sport+"_dist'>" + RADIUS_DEFAULT + "</span> <span id = '" +sport+"_miles'> miles </span><span class = 'adjust_dist increment_dist'id = '" +sport+"_up'>&#9650</span></span></p>"
			$("#sport_radius").append(x);
			y = "<p>" + sport + "<span class = 'stars " + sport + "_star'> <span class = 'star' id = '"+ sport + "_star_1'> &#9734 </span> <span class = 'star' id = '"+ sport + "_star_2'> &#9734 </span> <span class = 'star' id = '"+ sport + "_star_3'> &#9734 </span> <span class = 'star' id = '"+ sport + "_star_4'> &#9734 </span> <span class = 'star' id = '"+ sport + "_star_5'> &#9734 </span> </span></p>"
			$("#self_rating").append(y);
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
			$("." + sport + "_star").children().each(function(){
				$(this).html("&#9734").removeClass("active");
				i = $(this).attr("id").split("_")[2];
				if (i <= n){
					$(this).html("&#9733").addClass("active");
				}
			});
		})
	});
	
	// submit data
	$("#submit").click(function(){
		var ratings = 0;
		$.each(sports, function(i, sport){
			if( $("." + sport + "_star").children(".active").length == 0){
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
				temp['stars'] = $("." + sport + "_star").children(".active").length;
				sport_profiles.push(temp);
			});
			$.ajax({
		        type: 'POST',
		        url: '/firstpick/save_profile/',
		        data: {
		        	'first_name': $("#first_name").val(),
		        	'last_name': $("#last_name").val(),
		        	'email': $("#email").val(),
		        	'gender': $("#gender").val(),
		        	'home_lat': $("#home_lat").html(),
		        	'home_lng': $("#home_lng").html(),
		        	'sport_profiles': sport_profiles,
		        	'sport_count': sports.length,
		        },
		        success: function(response) {
	            	location.href = "/firstpick/";
	        	}
		    });
	    }
	});

});

 