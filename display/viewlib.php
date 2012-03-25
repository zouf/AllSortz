<?php
require_once('../db/dblib.php');
require_once('../search/searchlib.php');
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

function dumpRatingList($busId, $uname)
{
	$rating = getRatingIfExists($busId,$_SESSION['uname']);

	
	$html = '<style>';

	$html = $html.'#like-buttons		';
	$html = $html.'{						';
	$html = $html.'	margin: 0 auto;      ';
	$html = $html.'	text-align:center;   ';
	$html = $html.'	width:50px;          ';
	$html = $html.'}                      ';
	$html = $html.'                       ';
	$html = $html.'ul#like-buttons {      ';
	$html = $html.'margin:0 0;            ';
	$html = $html.'width:150px;           ';
	$html = $html.'}                      ';
    $html = $html.'                       ';
	$html = $html.'ul#ike-buttons li {    ';
	$html = $html.'display:inline         ';
	$html = $html.'}                      ';
    $html = $html.'                       ';
    $html = $html.'                       ';
	$html = $html.'ul#ike-buttons li a {  ';
	$html = $html.'padding-left: 20px;    ';
	$html = $html.'padding-right	: 20px;  ';
	$html = $html.'width:150px;           ';
	$html = $html.'}                      ';
	$html = $html.'                       ';
	$html = $html.'                       ';
	$html = $html.'ul#like-buttons li {   ';
	$html = $html.'	color:navy;          ';
	$html = $html.'display:inline         ';
	$html = $html.'}                      ';
	$html = $html.'</style>               ';
	
	

	
	
	$html = $html.'<div id="like-buttons-div">';
		$html = $html.'<ul id="like-buttons">';
		$html = $html.'<li><a id="hate'.$busId.'" onclick="postRating2('.$busId.', 0);">Hate!</a>&nbsp </li>';
	   	$html = $html.'<li><a id="meh'.$busId.'" onclick="postRating2('.$busId.', 1);">Meh. </a>&nbsp </li>';
	    $html = $html.'<li><a id="love'.$busId.'" onclick="postRating2('.$busId.', 2);">Love! </a>&nbsp </li>';
		$html = $html.'</ul>';
		$html = $html.'</div>';
		$html = $html. '<script> selectButton('.$rating.','.$busId.') </script>';
	return $html;
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

	$buses = mysql_query("SELECT * from business_tbl");

	$i = 0;
	while($busrow = mysql_fetch_array($buses, MYSQL_BOTH)) { 
	
		$busid=$busrow['bus_id'];
		$ratArr[$i]['ID'] = $busid;
		$ratArr[$i]['Name'] = "<a href=../bus/view.php?id=".$busrow['bus_id'].">".$busrow['bus_name']."</a>";
		$ratArr[$i]['Description'] = $busrow['bus_descr'];
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
			$uname = $_SESSION["uname"];
			$rating = mysql_query("SELECT * FROM busrat_tbl WHERE usr_id='$uid' and bus_id='$busid'");

			if(!$rating)
			{
				die("Error in mysql query to get rating". mysql_error());
			}
			$rat = mysql_fetch_array($rating);
		//	$ratArr[$i]["Your Rating"] = $rat['rating'];
			$ratArr[$i]["Your Rating"] = dumpRatingList($busid, $uname);

		}
		$bus_id = $busrow['bus_id'];
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