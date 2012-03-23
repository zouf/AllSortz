<?php

function validateEmail($email)
{
	
	$ret['error']= False;
	return $ret;
}

function validateUname($email)
{
	
	$ret['error']= False;
	return $ret;
}


function validateName($email)
{
	
	$ret['error']= False;
	return $ret;
}

function validateAddress($email)
{
	
	$ret['error']= False;
	return $ret;
}

function validateCity($email)
{
	
	$ret['error']= False;
	return $ret;
}


function handleError($msg)
{
	
}



function businessExists($name,$addr, $conn)
{	

	$result = mysql_query("SELECT * FROM business_tbl WHERE bus_name='$name', bus_addr='$addr'");
	if(!mysql_num_rows($result))
		return False;
	return True;
}

function userNameExists($name,$conn)
{	

	$result = mysql_query("SELECT * FROM user_tbl WHERE usr_uname='$name'");
	if(!mysql_num_rows($result))
		return False;
	return True;
}

function getNameFromUname($uname,$conn)
{
	$result = mysql_query("SELECT * FROM user_tbl WHERE usr_uname='$uname'");
	if($result)
	{
		$username = mysql_fetch_array($result);
		return $username['usr_fullname'];
	}

}

function checkUnamePassword($uname,$password,$conn)
{
	$result = mysql_query("SELECT * FROM user_tbl WHERE usr_uname='$uname' and usr_password='$password'");
	if(!mysql_num_rows($result))
		return False;
	return True;
}


/* Inserts user (handles any problems with the formatting too) */
function addUser($name, $email, $uname, $password, $conn)
{
	
	// Most / all of this validation can be done on the client side. Change in future
	if(userNameExists($uname,$conn))
	{
		$ret['error'] = True;
		$ret['msg'] = "User name ".$uname."exists!";
		return $ret;
	}
	$ret = validateEmail($email);
	if($ret['error'])
	{
		handleError($emailValid);
		return;
	}
	$ret = validateName($name);
	if($ret['error'])
	{
		handleError($ret);
		return;
	}
	$ret = validateUname($uname);
	if($ret['error'])
	{
		handleError($ret);
		return;
	}
	$sql_insert = "INSERT INTO user_tbl (usr_fullname, usr_email, usr_uname, usr_password) VALUES ('$name', '$email', '$uname', '$password');";
	$sqlRet = mysql_query($sql_insert);
	if(!$sqlRet)
	{
		$ret['msg'] = "Error in query: ".mysql_error();
	}
	else
	{
		$ret['msg'] = "User Added successfully";
	}
	return $ret;
}

function addBusiness($name, $keywords, $description, $avgRating, $streetAddress, $city,$conn)
{
	
}





?>