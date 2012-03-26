<?php
require_once('../db/dblib.php');
function getRatingTable()
{
	$pull_all_ratings = mysql_query("SELECT * from busrat_tbl;");
	if(!$pull_all_ratings)
	{
		die("Query was bad!");
	}
	
	$ratArr = array();
	
	while($busrat_row = mysql_fetch_array($pull_all_ratings, MYSQL_BOTH)) { 
		$busid = $busrat_row['bus_id'];
		$usrid = $busrat_row['usr_id'];
		$rating = $busrat_row['rating'];
		$ratArr[$usrid][$busid] = $rating;
	}
	
	
	return $ratArr;
}

/* works for logged in user only */


function getRecommendationFor($busid)
{
	
	$recommendations = getDiffForSignedInUser();
	if(isset($recommendations[$busid]))
		return $recommendations[$busid];
}

function getDiffForSignedInUser()
{
	$conn = connectToDatabase();
	if(!isset($_SESSION['uname']))
	{
		die('Please sign in!');
	}
	$uname = $_SESSION['uname'];


	$loggedInUsr = getIdFromUname($uname);
	
	$ratingTable = getRatingTable(); //table with the rows as users and columns as usrers.

	$compareToArr = $ratingTable[$loggedInUsr];
	

	$usrList = array();
	foreach($ratingTable as $usrid => $busArr)
	{
		if($usrid != $loggedInUsr)
		{
			$diff = 0;
			foreach($busArr as $busid => $rating)
			{
				if(isset($compareToArr[$busid]))
				{
					$diff += abs($rating - $compareToArr[$busid]);
				}
			}
			$other = getUnameFromId($usrid);
		
			$usrList[$usrid] = $diff;
		}
	}

	asort($usrList);
	$sat= false;  //iterate until we've filled enough recommendations
	
	$recommendation = array(); //recommendation array;
	foreach($usrList as $usrid => $diff)
	{
		$bestRelatedBusArr = $ratingTable[$usrid];
		foreach($bestRelatedBusArr as $busid =>  $rating)
		{
			
			// if someone loves it and the user hasn't seen it
			if($rating == 2 && !isset($ratingTable[$loggedInUsr][$busid]))
			{
			
				// If the recommendation hasn't been set  .. TODO weight this!
				if(!isset($recommendation[$busid]))
				{
					$recommendation[$busid] = 2;
					
				}
			
			}
		}
	}

	return $recommendation;
	
	

}




?>