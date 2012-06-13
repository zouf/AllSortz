
$(function() {

      $('div.comment div.vote').live("click", function () {
      var id = $(this).parents('div.comment').attr('id').split('_')[1];
        var vote_type = $(this).hasClass('up') ? 'up' : 'down';
        var t1 = $("#comment_vote_pos_"+id).hasClass("selected");
        var t2 = $("#comment_vote_neg_"+id).hasClass("selected");
        if(!t1 && !t2) {
        $.post('/api/comment_vote/', {id: id, type: vote_type}, function(json) {
                if(json.success=='true') {
                    document.getElementById('comment_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('comment_neg_rating_'+json.id).innerHTML=json.neg_rating
					
					if(json.rating == 'pos')
					{
						if(t2)
							$("#comment_vote_neg_"+json.id).removeClass("selected");
                  		$("#comment_vote_pos_"+json.id).addClass("selected");
                   	}
                   	else
                   	{
                   		if(t1)
                   			$("#comment_vote_pos_"+json.id).removeClass("selected");
                   		$("#comment_vote_neg_"+json.id).addClass("selected");
                   	}
                }
                else
                {
                    alert(json)

                }
            });
            } else {
            	$.post('/api/remove_comment_vote/', {id: id, type: vote_type}, function(json) {
               	 if(json.success == 'true') {
					document.getElementById('comment_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('comment_neg_rating_'+json.id).innerHTML=json.neg_rating
					if(t2)
						$("#comment_vote_neg_"+json.id).removeClass("selected");
               		if(t1)
                   		$("#comment_vote_pos_"+json.id).removeClass("selected");
                   	
                   
               		 }
               		 else
               		 {
               		 	alert(json)
               		 }
           		 });  	              
        }
            
    });
});

$(document).ready(function(){
$("form[name=addComment]").live("submit", function(e){
	e.preventDefault();
	var form = $("form[name=addComment]")
	var serial = form.serialize()
    $.ajax({ 
         url   : '/api/add_comment/',
         type  : form.attr('method'),
         data  : serial, // data to be submitted
         success: function(data){
         	alert(data)
         	var elem = document.getElementById("comment_list")
         	elem.innerHTML = data
         }
    });
    return false;
 });
});




$(document).ready(function(){
$("form[name=addReply]").live("submit", function(e){
	e.preventDefault();
	var id = $(this).parents('div.comment').attr('id').split('_')[1];
	var form = $("form[id=comment_form_"+id+"]")
	
	
	$.ajax({
		url   : '/api/add_comment/',
         type  : form.attr('method'),
         data  : form.serialize(), // data to be submitted
         success: function(data){
         	document.getElementById("comment_list").innerHTML = data         
         }
     });
	
	
    return false;
 });
});




