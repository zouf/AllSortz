<?php

include('../db/dblib.php');



session_start();
if (empty($_POST['uname']) || $_POST['uname'] != $_SESSION['uname']) {
	$return['error'] = true;
	$return['msg'] = 'No username or username didn\'t match session'.$_SESSION['uname'];
}
else  if( empty($_POST['busid']))  {
	$return['error'] = true;
	$return['msg'] = 'No rating or business ID';
}
else if(empty($_POST['rating']) )
{
	$busid = $_POST['busid'];
	$uname = $_POST['uname'];
	$rating = getRatingIfExists($busid,$uname);
}
else
{

	$busid = $_POST['busid'];
	$rating = $_POST['rating'];
	$uname = $_POST['uname'];
	$response = rateBusinessIfExists($busid,$rating,$uname);
	if($response != "")
	{	
		$return['error'] = true;
		$return['msg'] = mysql_real_escape_string($response);
	}
	else
	{
		$return['error'] = true;
		$return['msg'] = mysql_real_escape_string($response);

	}
}

echo json_encode($return); 


?>

