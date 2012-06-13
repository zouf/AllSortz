// use live handlers in general. They allow the innerHTML to be changed and still allow the jscript bindings to be teh same


$(function() {

      $('div.answer div.vote').click(function() {
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

$(function() {

      $('div.tip div.vote').live("click", function () {
      var id = $(this).parents('div.tip').attr('id').split('_')[1];
        var vote_type = $(this).hasClass('up') ? 'up' : 'down';
        var t1 = $("#tip_vote_pos_"+id).hasClass("selected");
        var t2 = $("#tip_vote_neg_"+id).hasClass("selected");
        if(!t1 && !t2) {
        $.post('/tip_vote/', {id: id, type: vote_type}, function(json) {
                if(json.success=='true') {
                    document.getElementById('tip_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('tip_neg_rating_'+json.id).innerHTML=json.neg_rating
					
					if(json.rating == 'pos')
					{
						if(t2)
							$("#tip_vote_neg_"+json.id).removeClass("selected");
                  		$("#tip_vote_pos_"+json.id).addClass("selected");
                   	}
                   	else
                   	{
                   		if(t1)
                   			$("#tip_vote_pos_"+json.id).removeClass("selected");
                   		$("#tip_vote_neg_"+json.id).addClass("selected");
                   	}
                }
                else
                {
                    alert(json)

                }
            });
            } else {
            	$.post('/remove_tip_vote/', {id: id, type: vote_type}, function(json) {
               	 if(json.success == 'true') {
					document.getElementById('tip_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('tip_neg_rating_'+json.id).innerHTML=json.neg_rating
					if(t2)
						$("#tip_vote_neg_"+json.id).removeClass("selected");
               		if(t1)
                   		$("#tip_vote_pos_"+json.id).removeClass("selected");
                   	
                   
               		 }
               		 else
               		 {
               		 	alert(json)
               		 }
           		 });  	              
        }
            
    });
});



$(function() {

      $('div.review div.vote').live("click", function () {
      var id = $(this).parents('div.review').attr('id').split('_')[1];
        var vote_type = $(this).hasClass('up') ? 'up' : 'down';
        var t1 = $("#rev_vote_pos_"+id).hasClass("selected");
        var t2 = $("#rev_vote_neg_"+id).hasClass("selected");
        if(!t1 && !t2) {
        $.post('/review_vote/', {id: id, type: vote_type}, function(json) {
                if(json.success=='true') {
                    document.getElementById('rev_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('rev_neg_rating_'+json.id).innerHTML=json.neg_rating
					
					if(json.rating == 'pos')
					{
						if(t2)
							$("#rev_vote_neg_"+json.id).removeClass("selected");
                  		$("#rev_vote_pos_"+json.id).addClass("selected");
                   	}
                   	else
                   	{
                   		if(t1)
                   			$("#rev_vote_pos_"+json.id).removeClass("selected");
                   		$("#rev_vote_neg_"+json.id).addClass("selected");
                   	}
                }
                else
                {
                    alert(json)

                }
            });
            } else {
            	$.post('/remove_review_vote/', {id: id, type: vote_type}, function(json) {
               	 if(json.success == 'true') {
					document.getElementById('rev_pos_rating_'+json.id).innerHTML=json.pos_rating
                    document.getElementById('rev_neg_rating_'+json.id).innerHTML=json.neg_rating
					if(t2)
						$("#rev_vote_neg_"+json.id).removeClass("selected");
               		if(t1)
                   		$("#rev_vote_pos_"+json.id).removeClass("selected");
                   	
                   
               		 }
               		 else
               		 {
               		 	alert(json)
               		 }
           		 });  	              
        }
            
    });
});
