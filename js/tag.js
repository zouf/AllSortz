$(function() {

      $('div.tag div.vote').live("click", function () {
      var id = $(this).parents('div.tag').attr('id').split('_')[1];
        var vote_type = $(this).hasClass('up') ? 'up' : 'down';
        var t1 = $("#tag_vote_pos_"+id).hasClass("selected");
        var t2 = $("#tag_vote_neg_"+id).hasClass("selected");
        if(!t1 && !t2) {
        	
        	// remove up / down vote icon first
        	if(vote_type == 'up')
			{
				if(t2)
					$("#tag_vote_neg_"+id).removeClass("selected");
          		$("#tag_vote_pos_"+id).addClass("selected");
           	} else {
           		if(t1)
           			$("#tag_vote_pos_"+id).removeClass("selected");
           		$("#tag_vote_neg_"+id).addClass("selected");
           	}
        	
        $.post('/tag_vote/', {id: id, type: vote_type}, function(json) {
                if(json.success=='true') {
                    document.getElementById('tag_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('tag_neg_rating_'+json.id).innerHTML=json.neg_rating
                } else {
                    alert(json)
                }
            });
            } else {
            	
            	// Remove the actual icon first
				if(t2)
					$("#tag_vote_neg_"+id).removeClass("selected");
           		if(t1)
               		$("#tag_vote_pos_"+id).removeClass("selected");
            	$.post('/remove_tag_vote/', {id: id, type: vote_type}, function(json) {
               	 if(json.success == 'true') {
					document.getElementById('tag_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('tag_neg_rating_'+json.id).innerHTML=json.neg_rating

               		 } else {
               		 	alert(json)
               		 }
           		 });  	              
        }
            
    });
});

$(document).ready(function(){


  $("#tag").autocomplete({
    source: "/api/get_tags/",
    minLength: 2,
  });
}); 
 
$(document).ready(function(){
$("form[name=addTag]").live("submit", function(e){
	e.preventDefault();
	var form = $("form[name=addTag]")
	var serial = form.serialize()
    
	$.ajax({ 
         url   : '/api/add_tag/',
         type  : form.attr('method'),
         data  : serial, // data to be submitted
         success: function(data){
         	document.getElementById("tag_list").innerHTML = data         
         }
    });
    return false;
 });
});

