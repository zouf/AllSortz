<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<link rel='stylesheet' type='text/css' href='../css/main.css' />
	<link href='http://fonts.googleapis.com/css?family=IM+Fell+French+Canon+SC' rel='stylesheet' type='text/css'>
	<link href='http://fonts.googleapis.com/css?family=Trykker' rel='stylesheet' type='text/css'>
	

	<link rel="stylesheet" href="../css/smoothness/jquery-ui-1.8.18.custom.css">
	<script type="text/javascript" src="../js/jquery-1.7.1.min.js"></script>
	<script type="text/javascript" src="../js/jquery-ui-1.8.18.custom.min.js"></script>
	<script type="text/javascript" src="../js/ajax_submit.js"></script>
	<script>
		$(function() {
			$( "input:submit, a, button", ".formbutton" ).button();
			$( "a", ".formbutton" ).click(function() { return false; });
		});
	</script>

<title>Nightout App</title>
</head>
<body>

<?php 

require_once('viewlib.php');



if(isset($_GET['user']))
{
	echo('<form action="" id="addUserForm" method="post">');
	echo('<h1>Nightout Add User</h1>');
	echo('<br />');
	echo('<br />');
	echo('<p>Name: <input type="text" name="fullName" id="fullName" class="adduser" value="" /></p>');
	echo('<br />');
	echo('<p>Email: <input type="text" name="email" id="email" class="adduser" value="" /></p>');
	echo('<br />');
	echo('<p>Username: <input type="text" name="uname" id="uname" class="adduser" value="" /></p>');
	echo('<br />');
	echo('<p>Password: <input type="password" name="password" id="password" class="adduser" value="" /></p>');
	echo('<br />');
	echo('<div class="formbutton"><input type="submit" name="submit" id="submitUser" value="Add me!" /></div>');
	echo('</form>');
}
else if(isset($_GET['business']))
{
	echo('<form action="" id="addBusinessForm" method="post">');
	echo('<h1>Nightout Add Business</h1>');
	echo('<br />');
	echo('<br />');
	echo('<p>Name: <input type="text" name="busName" id="busName" class="adduser" value="" /></p>');
	echo('<br />');
	echo('<p>City / State: <input type="text" name="busCity" id="busCity" class="adduser" value="" /></p>');
	echo('<br />');
	echo('<div class="formbutton"><input type="submit" name="submit" id="submitUser" value="Add By Region & Keyword!" /></div>');
	echo('</form>');
}




?>


<div>
<p id="message"></p>
</div>

</body>