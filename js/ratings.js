function postRating(rating)
{
	var busid =  getUrlParams().id;
	var uname = getCookie('uname');
	alert('click'); 
	$.ajax({
		type : 'POST',
		url : '/handler/addrating.php',
		dataType : 'json',
		data: {	
				busid : busid, uname : uname, rating : rating
		},
		success : function(data){
			alert(data.msg)
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
	return true;
	
}

function getRating(rating)
{
	var busid =  getUrlParams().id;
	var uname = getCookie('uname');
	alert('getRating'); 
	$.ajax({
		type : 'POST',
		url : '/handler/addrating.php',
		dataType : 'json',
		data: {	
				busid : busid, uname : uname
		},
		success : function(data){
			return(data.msg)				
		},
		error : function(XMLHttpRequest, textStatus, errorThrown) {
			alert(errorThrown);
		}
	});
	return true;
	
}


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

//http://tuvian.wordpress.com/2011/07/14/how-to-access-url-or-url-parts-using-javascript-get-the-website-url-using-javascript/
function getUrlParams() {
	var params = {};
	window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi,
	function (str, key, value) {
		params[key] = value;
	});
	return params;
}
