<?php

include('../db/dblib.php');



session_start();
$return['error'] = true;
$return['msg'] = "nothing done really even in the goddamn else";
if (empty($_POST['uname']))
{
	$return['error'] = true;
	$return['msg'] = 'No username 1';
}
else if( empty($_SESSION['uname']) || $_POST['uname'] != $_SESSION['uname'])
{

	$return['error'] = true;
	$return['msg'] = 'No username 1';
}
else  if( empty($_POST['busid']))  {
	$return['error'] = true;
	$return['msg'] = 'No rating or business ID';
}
else if(!isset($_POST['rating']) )
{
	$busid = $_POST['busid'];
	$uname = $_POST['uname'];
	$rating = getRatingIfExists($busid,$uname);
	$return['error'] = true;
	$return['msg'] = 'Empty post';
}
else
{

	$busid = $_POST['busid'];
	$rating = $_POST['rating'];
	$uname = $_POST['uname'];
	$response = rateBusinessIfExists($busid,$rating,$uname);
	if($response)
	{	
		$return['error'] = false;
		$return['msg'] = "RateBusinessIfExists succeeded";
	}
	else
	{
		$return['error'] = true;
		$return['msg'] = "Error in rateBusinessIfExists";

	}
}




echo json_encode($return); 


?>

