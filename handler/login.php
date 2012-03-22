<?php

	if(isset($_GET['logout']))
	{
		session_unset();
		session_destroy();
		session_write_close();
		setcookie(session_name(),'',0,'/');
		session_regenerate_id(true);
 		header("Location: /");
	}
	
	
	
	
	$dbname = "nightout1";
	$conn = mysql_connect("localhost","root","new-password");
	mysql_select_db($dbname);
	if (!$conn)
	{
		die('Could not connect: ' . mysql_error());
	}

	require_once('../db/dblib.php');

	
	if (empty($_POST['uname']) || empty($_POST['password']) ) {
		$return['error'] = true;
		$return['msg'] = 'You didn\'t enter anything.';
	
	}
	else    
	{
		$return['error'] = false;
		$uname = $_POST['uname'];
		$password = $_POST['password'];
		if(!checkUnamePassword($uname,$password,$conn))
		{
			$return['error'] = true;
			$return['msg'] = "Incorrect username password";
		}
		else
		{
			//login successful
			session_start();
			$_SESSION['uname'] = getNameFromUname($uname,$conn);
			mysql_close($conn);
			header("Location: /");
		}
		//check password
	}

	mysql_close($conn);


	echo json_encode($return);


?>