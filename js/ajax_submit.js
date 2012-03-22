function validateEmail(email)
{

	var atpos=email.indexOf("@");
	var dotpos=email.lastIndexOf(".");
	if (atpos<1 || dotpos<atpos+2 || dotpos+2>=email.length)
	{
	  return false;
	}
	return true;
}

function validateName(name)
{
	if(!name)
		return false;
	return true;

}


function validateUname(uname)
{
	if(!uname)
		return false;
	return true;

}



function validatePassword(password)
{
	if(!password)
		return false;
	return true;

}

$(document).ready(function(){
	$('#submit').click(function() {

	//	$('#waiting').show(500);
	//	$('#demoForm').hide(0);
	//	$('#message').hide(0);

		$.ajax({
			type : 'POST',
			url : 'post.php',
			dataType : 'json',
			data: {
				searchDat : $('#search').val()
			},
			success : function(data){
				$('#waiting').hide(500);
				$('#message').removeClass().addClass((data.error === true) ? 'error' : 'success')
					.text(data.msg).show(500);
				if (data.error === true)
					$('#demoForm').show(500);
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				$('#waiting').hide(500);
				$('#message').removeClass().addClass('error')
					.text('There was an error.').show(500);
				$('#demoForm').show(500);
			}
		});

		return false;
	});
	
	$('#loginUser').click(function() {

			$.ajax({
				type : 'POST',
				url : 'handler/login.php',
				dataType : 'json',
				data: {
					username : $('#uname').val(), password : $('#password').val()
				},
				success : function(data){
						alert('good');
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
	
	
	$('#submitUser').click(function() {

		$('#email').removeClass('error');
		$('#uname').removeClass('error');
		$('#fullName').removeClass('error');
		$('#password').removeClass('error');
		
	
	
		var error = false;
		if(!validateEmail($('#email').val()))
		{
			$('#email').addClass('error');
			error = true;
		}
		if(!validateUname($('#uname').val()))
		{
			$('#uname').addClass('error');
			error = true;
		}
		if(!validateName($('#fullName').val()))
		{
			$('#fullName').addClass('error');
			error = true;
		}
		if(!validatePassword($('#password').val()))
		{
			$('#password').addClass('error');
			error = true;
	
		}
		if(error)
			return false;

			$.ajax({
				type : 'POST',
				url : '../handler/dbadd.php',
				dataType : 'json',
				data: {
					fullname : $('#fullName').val(), email : $('#email').val(),	uname : $('#uname').val(),	password : $('#password').val()
				},
				success : function(data){
					$('#waiting').hide(500);
					$('#message').removeClass().addClass((data.error === true) ? 'error' : 'success')
						.text(data.msg).show(500);
					if (data.error === true)
						$('#demoForm').show(500);
					window.location= "../index.php";
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
