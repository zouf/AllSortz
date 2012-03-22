<?php
	require_once('../db/utilities.php');
	require_once('viewlib.php');

	
	
	
	$dbname = "nightout1";
	$conn = mysql_connect("localhost","root","new-password");
	if (!$conn)
	{
		die('Could not connect: ' . mysql_error());
	}
	
	if(!isset($_GET['table']))
	{
			echo('Invalid URL!');  // redirect to error pag
			die('<a href="javascript:history.go(-1)" title="Return to the previous page">&laquo; Go back</a>');
	}
	
	$table = $_GET['table'];


	
	//switch
	switch($table)
	{
		case "busrat_tbl":
			printBusRatTable($dbname,$conn);
			break;
		case "user_tbl":
			printUserTable($dbname,$conn);
			break;
		case "business_tbl":
			printBusinessTable($dbname,$conn);
			break;
		 default:
				echo('Invalid URL!');  // redirect to error pag
				die('<a href="javascript:history.go(-1)" title="Return to the previous page">&laquo; Go back</a>');	
				break;
			
	}
		
	mysql_close($conn);


?>