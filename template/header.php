
<!DOCTYPE html>
<html>
<head>
	<link rel='stylesheet' type='text/css' href='/css/main.css' />
	<link href='http://fonts.googleapis.com/css?family=IM+Fell+French+Canon+SC' rel='stylesheet' type='text/css'>
	<link href='http://fonts.googleapis.com/css?family=Trykker' rel='stylesheet' type='text/css'>
	

	<link rel="stylesheet" href="/css/smoothness/jquery-ui-1.8.18.custom.css">
	<script type="text/javascript" src="/js/jquery-1.7.1.min.js"></script>
	<script type="text/javascript" src="/js/jquery-ui-1.8.18.custom.min.js"></script>
	<script type="text/javascript" src="/js/ajax_submit.js"></script>
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
	session_start();
	if(isset($_SESSION['uname']))
	{
		echo('<p>Welcome '.$_SESSION['uname'].'</p>');
		echo('<a href="/handler/login.php?logout=1">Logout</a>');
	}
	else
	{
		echo('<a href="/index.php">Nightout</a><br>');
		echo('<a href="/login.php">Login</a><br>');
		echo('<a href="/display/add.php?user">Create</a><br>');
	}

?>