// use live handlers in general. They allow the innerHTML to be changed and still allow the jscript bindings to be teh same


$(function() {
    $('p.rateme').live('click', function(e) {
    	var id = $(this).attr('id').split('_')[1];
		$("#rateBusiness_"+id).toggle();
    });
});

function vote_func(obj,url)
{
	var id = $(obj).parents('div.answer').attr('id').split('_')[1];
	var vote_type = $(obj).hasClass('up') ? 'up' : 'down'; 
	var t1 = $("#vote_pos_"+id).hasClass("selected");
	var t2 = $("#vote_neg_"+id).hasClass("selected");
	if(!t1 && !t2) {
	$.post('/api/'+url, {id: id, type: vote_type}, function(json) {
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
		$.post('/api/rm_'+url, {id: id, type: vote_type}, function(json) {
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
	        

}


$(document).ready(function(){
	$("select[name=ratingDD]").live("change", function(e){
		var rating = this.value
		var id = $(this).parents('form').attr('name').split('_')[1];
	
	
		$.ajax({ 
	         url   : '/api/add_bus_rating/',
	         type  : 'POST',
	         data  : { rating: rating, bid: id }, // data to be submitted
	         success: function(data){
	         	
	         }
	    });
	    return false;
		
	});
});


$(function() {


      $('div.answer div.vote').click(function() {
    	  var vote_on = document.getElementById('vote_on');
          
          
          if(vote_on.value == "business")
          {		
        	  vote_func(this,'vote/')
          }
          else if(vote_on.value =="activity")
          {
        	  vote_func(this,'act_vote/')
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
