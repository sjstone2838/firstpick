$(document).ready(function(){
	
	$(".rsvp").click(function(){
		var vars = {}
		var rsvp = $(this).attr('id');
		console.log(rsvp);
		
		// http://jquery-howto.blogspot.com/2009/09/get-url-parameters-values-with-jquery.html
	    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	    for(var i = 0; i < hashes.length; i++) {
	        var hash = hashes[i].split('=');
	        vars[hash[0]] = hash[1];
	    }
	    $("#refresh_wheel").removeClass("hide");
		$.ajax({
	        type: 'POST',
	        url: '/firstpick/handle_rsvp/',
	        data: {
	        	'vars': vars,
	        	'rsvp': rsvp,
	        },
	        success: function(response) {
	    		$("#refresh_wheel").addClass("hide");
	        	$("#event_description").addClass("hide");
	        	$("#rsvp_response").removeClass("hide");
	        	$("#rsvp_response_msg").html(response.status);
	    	}
	    });
	});

});

 