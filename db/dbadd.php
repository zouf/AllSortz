<?php


$dbname = "nightout1";
$conn = mysql_connect("localhost","root","new-password");
mysql_select_db($dbname);
if (!$conn)
{
	die('Could not connect: ' . mysql_error());
}



	require_once('dblib.php');
if (empty($_POST['fullname']) || empty($_POST['email']) || empty($_POST['uname']) || empty($_POST['password'])) {
	$return['error'] = true;
	$return['msg'] = 'You missed something!';
}
else {
	$return['error'] = false;
	$escapedName = mysql_real_escape_string($_POST['fullname']);
	$escapedEmail = mysql_real_escape_string($_POST['email']);
	$escapedUname = mysql_real_escape_string($_POST['uname']);	
	$escapedPassword = mysql_real_escape_string($_POST['password']);	
	
	$response = addUser($escapedName, $escapedEmail, $escapedUname, $escapedPassword, $conn);
	if($response['error'])
	{
		$return['msg'] = $response['msg'];
	}
	else
	{
		$return['msg'] = $response['msg'];

	}
}
mysql_close($conn);


echo json_encode($return); 

?>