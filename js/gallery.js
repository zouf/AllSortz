$(".addProfilePic").live("click", function(e){
	e.preventDefault();
	$("#addProfilePicDiv").toggle();

	
});



$(document).ready(function(){
	$("form[name=addPhoto]").live("submit", function(e){
		e.preventDefault();
		var form = $("form[name=addPhoto]")
		var serial = form.serialize()

		var url = '/pics/add_bus_photo/'
		form.serializeArray().forEach(
			function checkPid(k,v) { 
				if (k.name == 'uid')
					url = '/pics/add_user_photo/'
			}
		);
		$.ajax({ 
	         url   : url,
	         type  : form.attr('method'),
	         data  : serial, // data to be submitted
	         success: function(data){
	        	if (!data.hasOwnProperty("empty") )	
				{
	        		if (url == '/pics/add_user_photo/')
	        		{
	        			$("#pofile_pic").html(data)
	        		}
	        		else
	        		{
	        			$("#photo_list").append(data) 
	        		}
					 	
				}
	        	     
	         }
	    });
	    return false;
	 });
	
});