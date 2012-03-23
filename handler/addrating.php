<?php
session_start();
if (empty($_POST['uname']) || $_POST['uname'] != $_SESSION['uname']) {
	$return['error'] = true;
	$return['msg'] = 'No username or username didn\'t match session'.$_SESSION['uname'];
}
else  if(empty($_POST['rating']) || empty($_POST['busid']))  {
	$return['error'] = true;
	$return['msg'] = 'No rating or business ID';
}
else
{
	$busid = $_POST['busid'];
	$rating = $_POST['rating'];
	$uname = $_POST['uname'];
	
	$return['error'] = false;
	$return['msg'] = "thanks for the rating ".$uname;
}

echo json_encode($return); 


?>

