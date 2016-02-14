$(document).ready(function(){

	// Collect array of "attended = Yes" players, show ratings_block
	$(".attendance").click(function(){
	  	$(this).parent().find("span").removeClass("clicked").removeClass("btn-primary").addClass("btn-default");
	  	$(this).addClass("clicked").addClass("btn-primary");
	  	
	  	// if attendance for all players selected
	  	if ($("span.clicked").length == $(".participant").length){
	  		$("#attendance_page").addClass("hide");
	  		$("#rating_page").removeClass("hide");

	  		$(".Yes.clicked").each(function(){
	  			var pk = $(this).attr("id").split("_")[1];
	  			$("#rating_"+pk).removeClass("hide");
	  		})
	  	}

	  	// adjust stars
		$(".rating_star").click(function(){
			sport = $(this).attr("id").split("_")[0];
			n = $(this).attr("id").split("_")[1];
			$(this).parent().children().each(function(){
				$(this).html("&#9734").removeClass("active");
				i = $(this).attr("id").split("_")[1];
				if (i <= n){
					$(this).html("&#9733").addClass("active");
				}
			});
		});
	});

	/*
	*/
	$("#submit").click(function(){
		var participants = [];
		var query = {}
		
		// http://jquery-howto.blogspot.com/2009/09/get-url-parameters-values-with-jquery.html
	    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	    for(var i = 0; i < hashes.length; i++) {
	        var hash = hashes[i].split('=');
	        query[hash[0]] = hash[1];
	    }

		$(".participant").each(function(){
			var participant = {}
			var pk = $(this).attr("id").split("_")[1]
			var attendance = $(this).find(".attendance.clicked").attr("id").split("_")[0];
			var stars = $("#stars_" + pk).find(".rating_star.active").length
			participant['pk'] = pk;
			participant['attendance'] = attendance;
			participant['stars'] = stars;
			participants.push(participant);
		});

		$("#refresh_wheel").removeClass("hide");
		$.ajax({
	        type: 'POST',
	        url: '/firstpick/handle_rating/',
	        data: {
	        	'participants':JSON.stringify(participants),
	        	'query': query
	        },
	        success: function(response) {
	    		console.log(response);	
	    		$("#refresh_wheel").addClass("hide");
	    		$("#rating_page").addClass("hide");
	        	if (response.status == "success"){
	        		$("#confirmation").removeClass("hide");	
	        	} else {
	        		$("#error").removeClass("hide");

	        		$("#error_msg").text(response.error_msg);
	        	}
	    	}
	    });
	});	

	$("#back").click(function(){
		$("#attendance_page").removeClass("hide");
	  	$("#rating_page").addClass("hide");	
	});

});

 