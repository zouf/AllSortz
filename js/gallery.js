$.fn.spin = function(opts) {
  this.each(function() {
    var $this = $(this),
        data = $this.data();

    if (data.spinner) {
      data.spinner.stop();
      delete data.spinner;
    }
    if (opts !== false) {
      data.spinner = new Spinner($.extend({color: $this.css('color')}, opts)).spin(this);
    }
  });
  return this;
};


$(document).ready(function(){
	$("form[name=subscribeUser]").live("submit",function(e){
		e.preventDefault();
		var form =  $(this);//$("form[name=subscribeUser]")
		subUser(form.serializeArray()[0].name,form.serializeArray()[0].value);  //get the name of the tag

	});
	
	$("form[name=unsubscribeUser]").live("submit",function(e){
		e.preventDefault();
		var form = $(this);//"form[name=unsubscribeUser]")
		unsubUser(form.serializeArray()[0].name,form.serializeArray()[0].value);
		
	});
	
	
	
	
	$("form[name=addPhoto]").live("submit", function(e){
		e.preventDefault();
		var form = $("form[name=addPhoto]")
		var serial = form.serialize()

		$.ajax({ 
	         url   : '/pics/add_bus_photo/',
	         type  : form.attr('method'),
	         data  : serial, // data to be submitted
	         success: function(data){
	        	 if  (!data.hasOwnProperty("empty"))	
				{
						$("#photo_list").append(data)  
				
				}
	        	     
	         }
	    });
	    return false;
	 });
	
});