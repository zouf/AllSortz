<?php

require_once('utilities.php');
function connectToDatabase()
{
	$dbname = "nightout1";
	$conn = mysql_connect("localhost","root","new-password");
	if (!$conn)
	{
		die('Could not connect: ' . mysql_error());
	}
	mysql_select_db($dbname);
	return $conn;

}

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



function businessIdExists($busid, $conn)
{	
	$result = mysql_query("SELECT * FROM business_tbl WHERE bus_id='$busid'");
	if(!mysql_num_rows($result))
		return False;
	return True;
}


function businessAddrExists($name,$addr, $conn)
{	
	$result = mysql_query("SELECT * FROM business_tbl WHERE bus_name='$name' AND bus_addr='$addr'");
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

function getIdFromUname($uname)
{
	$result = mysql_query("SELECT * FROM user_tbl WHERE usr_uname='$uname'");
	if($result)
	{
		$username = mysql_fetch_array($result);
		return $username['usr_id'];
	}

}


function getBusNameFromId($bus_id)
{
	$result = mysql_query("SELECT * FROM business_tbl WHERE bus_id='$bus_id'");
	if($result)
	{
		$username = mysql_fetch_array($result);
		return $username['bus_name'];
	}

}



function getUnameFromId($usr_id)
{
	$result = mysql_query("SELECT * FROM user_tbl WHERE usr_id='$usr_id'");
	if($result)
	{
		$username = mysql_fetch_array($result);
		return $username['usr_uname'];
	}

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

function addBusiness($name, $keywords, $description, $addr, $city)
{ 
	$conn = connectToDatabase();

	
	if(businessAddrExists($name,$addr, $conn))
	{
		$ret['error'] = true;
		$ret['msg'] = "Business already exists!";
		return $ret;
	}
	else
	{
		$sql_insert = "INSERT INTO business_tbl (bus_name, bus_descr, bus_rating, num_ratings, bus_addr, bus_city) VALUES ('$name',  '$description', '0','0', '$addr', '$city'); ";
		$res = mysql_query($sql_insert);
		if(!$res)
		{
		 	die('Invalid query: ' . mysql_error());
		}
		foreach($keywords as &$t)
		{
			$typenm = mysql_real_escape_string($t);
			if(!businessTypeExists($typenm,$conn))  //create type if it doesnt exist
			{
				insertBusType($typenm,$conn);
			}
			$ret['msg'] = $typenm;
			$typeId = getBusTypeIdFromName($typenm);
			$busId = getBusIdFromName($name, $conn);
			insertBusTypeRelPair($busId,$typeId,$conn);
		}
		$ret['error'] = false;
	//	$ret['msg'] = "added";
		
	}
	mysql_close($conn);
	return $ret;
}


function getRatingIfExists($busid,$uname)
{

	$conn = connectToDatabase();

	if(userNameExists($uname,$conn))
	{
		$usrid = getIdFromUname($uname);
		if(businessIdExists($busid,$conn))
		{
			
			$get_rating = "SELECT * FROM  busrat_tbl WHERE usr_id = '$usrid' AND bus_id='$busid'";
			$result = mysql_query($get_rating);
			if(!mysql_num_rows($result))
				return -1;
			$res = mysql_fetch_array($result);
			return $res['rating'];
		}
		return -1;
	}
	return -1;
	mysql_close($conn);

}


/* add 1 to the number of ratings if rating is not 1 (meh). Add 1 to likes if rating == 2*/

function updateBusinessStats($busid, $rating)
{
	if($rating == 1)
		return;
	
	$update_str = "UPDATE business_tbl SET num_ratings=num_ratings+1 Where bus_id='$busid'";
	if(!mysql_query($update_str))
	{
		die("zouf in mysql update".mysql_error() ); 
	}
	if($rating==2)
	{
		$update_str = "UPDATE business_tbl SET bus_rating=bus_rating+1 Where bus_id='$busid'";
		if(!mysql_query($update_str))
		{
			die("zouf2 in mysql update".mysql_error() ); 
		}
	}
}


function rateBusinessIfExists($busid,$rating,$uname)
{
	$conn = connectToDatabase();
	if(userNameExists($uname,$conn))
	{
		$usrid = getIdFromUname($uname);
		if(businessIdExists($busid,$conn))
		{
			
			if($rating=="love" || $rating == 2)
			{
				$rating = 2;
			}
			else if($rating=="hate" || $rating == 0)
			{
				$rating = 0;
			}
			else
			{
				$rating = 1;
			}
			$insert_rating = "";
			
			if(!checkIfRatingPairExists($usrid, $busid, $conn))
			{
				$insert_rating = "INSERT INTO busrat_tbl (usr_id, bus_id, rating) VALUES ('$usrid', '$busid', '$rating')";
				updateBusinessStats($busid, $rating);  // once for each user
			}
			else
			{
				$insert_rating = "UPDATE  busrat_tbl SET rating='$rating' WHERE usr_id='$usrid' and bus_id='$busid'";
			}
			

			if(!mysql_query($insert_rating))
			{
				echo("MYSQL ERROR IN INSERT!");
				return false;
			}
			return true;
		}
		return false;
	}
	return false;

}


function getAllKeywords($dbname,$conn)
{
	$res = mysql_query("SELECT * from bustype_tbl");
	if(!$res)
	{
		die('Bad query '.mysql_error());
	}
	return $res;
}



?>