<?php

require_once('../db/dblib.php');

session_start();



if (empty($_POST['uname']) || $_POST['uname'] != $_SESSION['uname']) {
		$return['error'] = true;
	if(empty($_POST['uname']))
	{
		$return['msg'] = "empty";
	}
	else
	{
		
	}

	$return['msg'] = 'Must be logged in to add business!';
}
else  if( empty($_POST['name']) || empty($_POST['addr']) ||empty($_POST['city']) ||  empty($_POST['desc']) || empty($_POST['keywords']))  {
	$return['error'] = true;
	$return['msg'] = 'Blanks';
}
else
{

$keyCSV = $_POST['keywords'];
$addr = mysql_real_escape_string($_POST['addr']);
$name = mysql_real_escape_string($_POST['name']);
$desc = mysql_real_escape_string($_POST['desc']);
$city = mysql_real_escape_string($_POST['city']);

$keyArr =  explode(',', $keyCSV); 

$return['error'] = false;
$ret = addBusiness($name, $keyArr, $desc, $addr, $city);

$return['msg'] = $ret['msg'];
}



echo json_encode($return);
?>