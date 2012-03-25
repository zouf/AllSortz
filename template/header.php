
<!DOCTYPE html>
<html>
<head>
	<link rel='stylesheet' type='text/css' href='/css/main.css' />
	<link rel='stylesheet' type='text/css' href='/css/header_footer.css' />
	<link href='http://fonts.googleapis.com/css?family=IM+Fell+French+Canon+SC' rel='stylesheet' type='text/css'>
	<link href='http://fonts.googleapis.com/css?family=Trykker' rel='stylesheet' type='text/css'>
	

	<link rel="stylesheet" href="/css/smoothness/jquery-ui-1.8.18.custom.css">
	<script type="text/javascript" src="/js/jquery-1.7.1.min.js"></script>
	<script type="text/javascript" src="/js/jquery-ui-1.8.18.custom.min.js"></script>
	<script type="text/javascript" src="/js/ajax_submit.js"></script>
	<script type="text/javascript" src="/js/mainsearch.js"></script>
	<script type="text/javascript" src="/js/ratings.js"></script>
	<script type="text/javascript" src="/js/addbusiness.js"></script>
	<script>
		$(function() {
			$( "input:submit, a, button", ".formbutton" ).button();
			$( "a", ".formbutton" ).click(function() { return false; });
		});
	</script>

<title>Nightout App</title>
</head>
<body>
<div id="pagecontainer">

<?php
	session_start();
	echo('<div id="account-bar">');
	if(isset($_SESSION['uname']))
	{
		
		echo('<ul id="list-nav">');
		echo('<li><a href="/index.php">'.$_SESSION['uname'].'</a></li>');
		echo('<li><a href="/handler/login.php?logout=1">Logout</a></li>');
		echo('</ul>');
	}
	else
	{
		echo('<ul id="list-nav">');
		echo('<li><a href="/login.php">Login</a></li>');
		echo('<li><a href="/display/add.php?user">Create</a></li>');
		echo('</ul>');
		
		
	}
	echo('</div>');
	
	echo('<div id="nav-bar">');
		echo('<ul id="list-nav">');
		echo('<li><a  id="nightoutHome" href="/index.php"><h1>Nightout</h1></a></li>');
	   	echo('<li><a href="/display/view.php?table=business_tbl">Business List</a></li>');
	    echo('<li><a href="/display/add.php?business">Add Business</a><li>');
//	   	echo('<li><a href="/display/view.php?table=user_tbl">Users</a><li>');
//	   	echo('<li><a href="/display/view.php?table=busrat_tbl">Business Ratings</a><li>');
//	   	echo('<li><a href="/ratings/userdiff.php">Diff Between Users</a></li>');
		echo('</ul>');	
	echo('</div>');
	

?>