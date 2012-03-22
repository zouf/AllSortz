<?php
/* View a business */

	include('../template/header.php');

$dbname = "nightout1";
$conn = mysql_connect("localhost","root","new-password");
mysql_select_db($dbname);
if (!$conn)
{
	die('Could not connect: ' . mysql_error());
}

if(!isset($_GET['id']))
{
		echo('Invalid URL!');  // redirect to error pag
		die('<a href="javascript:history.go(-1)" title="Return to the previous page">&laquo; Go back</a>');
}

$busId = $_GET['id'];


	$busResult = mysql_query("SELECT * from business_tbl where bus_id=$busId");
	if(!$busResult)
	{
		die('Query error: ' . mysql_error());
	}
	$business = mysql_fetch_array($busResult, MYSQL_BOTH);
	
	echo($business['bus_name']);

	
?>

