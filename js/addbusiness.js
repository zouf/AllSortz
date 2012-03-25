
$(document).ready(function(){

	$('#submitBusiness').click(function() {
	var uname = getCookie('uname'); 
	alert(uname);
			$.ajax({
				type : 'POST',
				url : '../handler/addbusiness.php',
				dataType : 'json',
				data: {
				uname : uname, 	name : $('#busName').val(), city : $('#busCity').val(),	desc : $('#busDesc').val(),	addr : $('#busAddr').val(), keywords : $('#busKey').val()
				},
				success : function(data){
					alert(data.msg);
					$('#waiting').hide(500);
					$('#message').removeClass().addClass((data.error === true) ? 'error' : 'success')
						.text(data.msg).show(500);
					if (data.error === true)
						$('#demoForm').show(500);
				},
				error : function(XMLHttpRequest, textStatus, errorThrown) {
					alert(errorThrown);
					$('#waiting').hide(500);
					$('#message').removeClass().addClass('error')
						.text('There was an error.').show(500);
					$('#demoForm').show(500);
				}
			});
		
		return false;

	});
});


function getCookie(c_name)
{
var i,x,y,ARRcookies=document.cookie.split(";");
for (i=0;i<ARRcookies.length;i++)
{
  x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
  y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
  x=x.replace(/^\s+|\s+$/g,"");
  if (x==c_name)
    {
    return unescape(y);
    }
  }
}

