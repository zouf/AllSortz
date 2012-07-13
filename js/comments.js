


$(function() {

      $('div.comment div.vote').live("click", function () {
      var id = $(this).parents('div.comment').attr('id').split('_')[1];
        var vote_type = $(this).hasClass('up') ? 'up' : 'down';
        var t1 = $("#comment_vote_pos_"+id).hasClass("selected");
        var t2 = $("#comment_vote_neg_"+id).hasClass("selected");
        if(!t1 && !t2) {
        	// You're upvoting or downvoting, so change the direction of the arrow right away  
        	if(vote_type == 'up') {
				if(t2)
					$("#comment_vote_neg_"+id).removeClass("selected");
	      		$("#comment_vote_pos_"+id).addClass("selected");
            } else	{
           		if(t1)
           			$("#comment_vote_pos_"+id).removeClass("selected");
           		$("#comment_vote_neg_"+id).addClass("selected");
            }
	
		// post the change in rating to the server. the server will update hte positive and negative ratings appropriately
	
        $.post('/api/comment_vote/', {id: id, type: vote_type}, function(json) {
                if(json.success=='true') {
                    document.getElementById('comment_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('comment_neg_rating_'+json.id).innerHTML=json.neg_rating					
                } else  {
                    alert(json)
                }
            });
            } else {
            	//you're removing a vote
            	if(t2)
					$("#comment_vote_neg_"+id).removeClass("selected");
               	if(t1)
                   	$("#comment_vote_pos_"+id).removeClass("selected");
            	//then remove it from the server!
            	$.post('/api/remove_comment_vote/', {id: id, type: vote_type}, function(json) {
               	 if(json.success == 'true') {
					document.getElementById('comment_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('comment_neg_rating_'+json.id).innerHTML=json.neg_rating
					} else {
               		 	alert(json)
               		 }
           		 });  	              
        }
            
    });
});




$(document).ready(function(){
	$("form[name=addTagComment]").live("submit", function(e){
		e.preventDefault();
		var form = $("form[name=addTagComment]")
		
		var serial = form.serialize()
		var url = '/api/add_tag_comment/'
		form.serializeArray().forEach(
			function checkPid(k,v) { 
				if (k.name == 'pid')
					url = '/api/add_photo_comment/'
			}
		);
	
		
		
		
	    $.ajax({ 
	         url   : url,
	         type  : form.attr('method'),
	         data  : serial, // data to be submitted
	         success: function(data){
	         	var elem = document.getElementById("comment_list")
	         	elem.innerHTML = data
	         	$(".buttonme").button();
	         }
	    });
	    return false;
	 });
	});



$(document).ready(function(){
	$("form[name=addTagReply]").live("submit", function(e){
		e.preventDefault();
		var id = $(this).parents('div.comment').attr('id').split('_')[1];
		var form = $("form[id=comment_form_"+id+"]")
		
		
		var url = '/api/add_tag_comment/'
		form.serializeArray().forEach(
			function checkPid(k,v) { 
				if (k.name == 'pid')
					url = '/api/add_photo_comment/'
			}
		);
		
		$.ajax({
			url   : url,
	         type  : form.attr('method'),
	         data  : form.serialize(), // data to be submitted
	         success: function(data){
	         	document.getElementById("comment_list").innerHTML = data
	         	$(".buttonme").button();
	         }	
	     });
		
		
	    return false;
	 });
	});



$(document).ready(function(){
	$('.replybox').live("keydown", function(e) {
	     if(e.keyCode == 13) {
	       e.preventDefault(); // Makes no difference
	     $(this).parent().submit(); // Submit form it belongs to
	   }
	});
	
	
$("form[name=addReply]").live("submit", function(e){
	e.preventDefault();
	var id = $(this).parents('div.comment').attr('id').split('_')[1];
	var form = $("form[id=comment_form_"+id+"]")
	var serial = form.serialize()

	var url = '/api/add_tag_comment/'
	form.serializeArray().forEach(
		function checkPid(k,v) { 
			if (k.name == 'pid')
				url = '/api/add_photo_comment/'
		}
	);
	$.ajax({
		url   : url,
         type  : form.attr('method'),
         data  : form.serialize(), // data to be submitted
         success: function(data){
         	document.getElementById("comment_list").innerHTML = data   
         	$(".buttonme").button();
         }
     });
	
	
    return false;
 });
});


$(".addReply").live("click", function(e){
	e.preventDefault();
	var cid = $(this).attr('id').split('_')[1];
	$("#commentDiv"+cid).toggle();

	
});


$("#prev1").live("click", function(e){
	e.preventDefault();
	
	$.ajax({
		url   : '/api/add_tag_comment/',
         type  : form.attr('method'),
         data  : form.serialize(), // data to be submitted
         success: function(data){
         	document.getElementById("comment_list").innerHTML = data   
         	$(".buttonme").button();
         }
     });

});






