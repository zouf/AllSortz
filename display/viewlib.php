<?php
function printBusRatTable($dbname,$conn)
{
	mysql_select_db($dbname);
	// Get all user_ids so we can populate the rows of this matrix
	$ratArr = array();

	$i = 0;
	$ratings = mysql_query("SELECT * from busrat_tbl");
	$users = mysql_query("SELECT * from user_tbl");

	while($userrow = mysql_fetch_array($users, MYSQL_BOTH)) { 
		$ratArr[$i]['Name'] = $userrow['usr_fullname'];
		$i++;
	}
			
	$row = 0;
	$col = 1;
	while($ratingRow = mysql_fetch_array($ratings, MYSQL_BOTH)) {    // to iterate through all businesses
		if(isset($busid) && $ratingRow["bus_id"] != $busid)
		{
			$col++;		
		}
		$busid = $ratingRow["bus_id"];  
		if(isset($usrid) && $ratingRow["usr_id"] != $usrid)
		{
			$row++;
			$col = 1;
		}
		$usrid = $ratingRow["usr_id"];  
		$rating = $ratingRow["rating"];  
		$getbus = "SELECT * FROM business_tbl where bus_id=$busid;";
		$result = mysql_fetch_array(mysql_query($getbus));
		$name = $result['bus_name'];
		$ratArr[$row][$name] = (string)($rating);
	}
	echo array2table($ratArr);	
}

function printUserTable($dbname,$conn)
{
	mysql_select_db($dbname);
	// Get all user_ids so we can populate the rows of this matrix
	$ratArr = array();

	$users = mysql_query("SELECT * from user_tbl");

	$i = 0;
	while($userrow = mysql_fetch_array($users, MYSQL_BOTH)) { 
		$ratArr[$i]['Name'] = $userrow['usr_fullname'];
		$ratArr[$i]['ID'] = $userrow['usr_id'];
		$ratArr[$i]['Email'] = $userrow['usr_email'];
		$ratArr[$i]['UserName'] = $userrow['usr_uname'];
		$i++;
	}

	echo array2table($ratArr);	
}

function printBusinessTable($dbname,$conn)
{
	mysql_select_db($dbname);
	// Get all user_ids so we can populate the rows of this matrix
	$ratArr = array();

	$users = mysql_query("SELECT * from business_tbl");

	$i = 0;
	while($userrow = mysql_fetch_array($users, MYSQL_BOTH)) { 
		$ratArr[$i]['Name'] = $userrow['bus_name'];
		$ratArr[$i]['ID'] = $userrow['bus_id'];
		$ratArr[$i]['Description'] = $userrow['bus_descr'];
		$bus_id = $userrow['bus_id'];
		$mysql_get_keywords = "SELECT * FROM bustyperel_tbl where bus_id='$bus_id'";
		$type_results = mysql_query($mysql_get_keywords);
		if(!$type_results)
		{
			die('Error in access : ' . mysql_error());
		}
		$types = array();
		$t = 0;
		while($type = mysql_fetch_array($type_results, MYSQL_BOTH))
		{
			$types[$t] = getNameFromBusTypeId($type['bustype_id'],$conn);
			$t++;
		}
		$ratArr[$i]['Keywords'] = $types;
		$i++;
	}

	echo array2table($ratArr,true);	
}

?>