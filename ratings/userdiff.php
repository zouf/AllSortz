<?php
	require_once('../db/utilities.php');
	include('../template/header.php');
	require_once('../db/dblib.php');
	require_once('ratinglib.php');
function getUserDiff()
{
	$conn = connectToDatabase();
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
		$ratArr[$row][$col] = (string)($rating);
	}
	
	$u1 = 0;
	while($u1 < $row)
	{
		$u2 = $u1 + 1;
		while($u2 < $row)
		{
			$diff = 0;
			$bus = 1;
			while($bus < $col-1)
			{
				if(isset($ratArr[$u1][$bus]) && isset($ratArr[$u2][$bus]))
				{
					$user1Rating = $ratArr[$u1][$bus];
					$user2Rating = $ratArr[$u2][$bus];
					$diff += abs($user1Rating-$user2Rating);
				}
				$bus++;
			}
			$u2++;
			echo("<p>Difference in interest ".(string)$ratArr[$u1]['Name']." and ".(string)$ratArr[$u2]['Name']." is ".(string)$diff."</p>");
		}
		$u1++;
	}
	mysql_close($conn);
}


getDiffForSignedInUser();






?>