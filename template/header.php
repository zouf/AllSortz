
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

		echo('<div id="accountbar"><a href="/index.php">Nightout</a> Account Bar</div><a href="/login.php">Login</a>');
	

?>