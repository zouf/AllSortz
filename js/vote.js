$(function() {

      $('div.answer h3.vote').click(function() {
      var id = $(this).parents('div.answer').attr('id').split('_')[1];
        var vote_type = $(this).hasClass('up') ? 'up' : 'down';
        var t1 = $("#vote_pos_"+id).hasClass("selected");
        var t2 = $("#vote_neg_"+id).hasClass("selected");
        if(!t1 && !t2) {
        $.post('/vote/', {id: id, type: vote_type}, function(json) {
                if(json.success=='true') {
                    document.getElementById('pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('neg_rating_'+json.id).innerHTML=json.neg_rating
					
					if(json.rating == 'pos')
					{
						if(t2)
							$("#vote_neg_"+json.id).removeClass("selected");
                  		$("#vote_pos_"+json.id).addClass("selected");
                   	}
                   	else
                   	{
                   		if(t1)
                   			$("#vote_pos_"+json.id).removeClass("selected");
                   		$("#vote_neg_"+json.id).addClass("selected");
                   	}
                }
                else
                {
                    alert(json)

                }
            });
            } else {
            	$.post('/remove_vote/', {id: id, type: vote_type}, function(json) {
               	 if(json.success == 'true') {
					document.getElementById('pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('neg_rating_'+json.id).innerHTML=json.neg_rating
					if(t2)
						$("#vote_neg_"+json.id).removeClass("selected");
               		if(t1)
                   		$("#vote_pos_"+json.id).removeClass("selected");
                   	
                   
               		 }
               		 else
               		 {
               		 	alert(json)
               		 }
           		 });  	              
        }
            
    });
});