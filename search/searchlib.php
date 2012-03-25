<?php
require_once('../db/dblib.php');
require_once('../display/viewlib.php');


function searchKeywordCity($keyword, $city, $uname)
{
	$conn = connectToDatabase();


	// Get all user_ids so we can populate the rows of this matrix

	//Get businesses differently now
	$busesInCity = mysql_query("SELECT * from business_tbl WHERE bus_city='$city'");
	$html = "msg";
	if(!$busesInCity)
	{
		$html = 	$html.'No Businesses in '.$city;

	}
	else
	{
		$typeId = getBusTypeIdFromName($keyword);
		if($typeId == -1)
		{
			
			$html = 	$html.'No Type '.$keyword;
		}
		else
		{
		
			$html = dumpBusiness($busesInCity, $typeId);
		}
	}

	
	mysql_close($conn);	
	return $html;
}
/*
session_start();
	$_SESSION['uname']= "Tychus";
(searchKeywordCity("sandwiches", "Princeton, NJ",""));*/
//echo(searchKeywordCity("a", "b", "c"));

function dumpBusiness($queryResult, $typeid)
{
	$ratArr = array();
	$i = 0;

	while($busrow = mysql_fetch_array($queryResult, MYSQL_BOTH)) { 
	
		$busid=$busrow['bus_id'];

		if(!checkIfBusContainsType($busid, $typeid))
		{
			continue;
		}
		$ratArr[$i]['ID'] = $busid;
		$ratArr[$i]['Name'] = "<a href=../bus/view.php?id=".$busrow['bus_id'].">".$busrow['bus_name']."</a>";
		$ratArr[$i]['Description'] = $busrow['bus_descr'];
		$ratArr[$i]['City'] = $busrow['bus_city'];
		if($busrow['num_ratings'] != 0)
		{
				$ratArr[$i]['Likes'] = (string)((int)($busrow['bus_rating'] / $busrow['num_ratings'] * 100))."%";
		}
		else
		{
				$ratArr[$i]['Likes'] = "None Yet!";
			}
		if(isset($_SESSION["uname"])){
			
			$uid = getIdFromUname($_SESSION["uname"]);
			//return $_SESSION["uname"];
			$uname = $_SESSION["uname"];
			$rating = mysql_query("SELECT * FROM busrat_tbl WHERE usr_id='$uid' and bus_id='$busid'");

			if(!$rating)
			{
				die("Error in mysql query to get rating". mysql_error());
			}
			$rat = mysql_fetch_array($rating);
	//		echo(dumpRatingList($busid, $rat['rating']));
			$ratArr[$i]["Your Rating"] = dumpRatingList($busid, $rat['rating']);

		}
		
		$bus_id = $busid;
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
			$types[$t] = getNameFromBusTypeId($type['bustype_id']);
			$t++;
		}
		$ratArr[$i]['Keywords'] = $types;
		$i++;
	}
	return array2table($ratArr,true);	
}

?>