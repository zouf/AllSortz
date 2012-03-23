<html>
<head>
<title>Access Google</title>
</head>
<body>
 <?php

require_once('utilities.php');
function googleAddTypeByCity($dbname, $city, $type)
{
	$APIKey = "AIzaSyB4Fk4hFw0kadSPl_FNYRr9El82HonORms";   //TODO fix key / security
	
	$conn =  mysql_connect("localhost","root","new-password");

	$geocode = "http://maps.googleapis.com/maps/api/geocode/json?address=".$city."&sensor=false";  //get location of some city
	$ch = curl_init($geocode);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_HEADER, 0);
	$data = curl_exec($ch); 
	echo($data);
	curl_close($ch);
	
	$response = json_decode($data,true);
	$lat = $response['results'][0]['geometry']['location']['lat'];
	$lng = $response['results'][0]['geometry']['location']['lng'];
	

	$CityRestauarants = "https://maps.googleapis.com/maps/api/place/search/json?location=".$lat.",".$lng."&radius=500&types=".$type."&sensor=false&key=".$APIKey;
	
	
	echo($CityRestauarants);
	$ch = curl_init($CityRestauarants);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	$data = curl_exec($ch); // Yelp response

	curl_close($ch);
	echo($data);

	$response = json_decode($data,true);

	mysql_select_db($dbname);
	foreach($response['results'] as $bus)
	{	
		$nm = mysql_real_escape_string($bus['name']);
		$addr = mysql_real_escape_string($bus['vicinity']);
		if(!businessExists($nm,$addr,$conn))
		{
			if(isset($bus['rating']))  // if possible seed with businesses
			{
				$rating = $bus['rating'];
				$sql_insert = "INSERT INTO business_tbl (bus_name, bus_descr, bus_rating, bus_addr, bus_city) VALUES ('$nm',  'test desc', '$rating', '$addr', '$city'); ";
			}
			else
			{
				$sql_insert = "INSERT INTO business_tbl (bus_name, bus_descr, bus_addr, bus_city) VALUES ('$nm', 'test desc', '$addr', '$city' ); ";
			}
			echo($sql_insert);
			$res = mysql_query($sql_insert);
			if(!$res)
			{
			 	die('Invalid query: ' . mysql_error());
			}
			$types = $bus['types'];
			foreach($types as &$t)
			{
				$typenm = mysql_real_escape_string($t);
				echo($typenm);
				echo('\n        ');
				if(!businessTypeExists($typenm,$conn))  //create type if it doesnt exist
				{
					insertBusType($typenm,$conn);
				}
				$typeId = getBusTypeIdFromName($typenm,$conn);
				$busId = getBusIdFromName($nm, $conn);
				insertBusTypeRelPair($busId,$typeId,$conn);
			}
		}
	}
	echo('Done!');
	mysql_close($conn);
}

$locations = array(urlencode("Brooklyn, NY"), urlencode("Flushing, NY"), urlencode("Bayside, NY"));
$keywords = array(urlencode("night_club"), urlencode("bar"), urlencode("restaurant"), urlencode("sushi"), urlencode("lunch"), urlencode("brunch"));

		$dbname = "nightout1";
foreach($locations as $l)
{
	foreach($keywords as $k)
	{
		googleAddTypeByCity($dbname, $l, $k);
	}
}


 ?>
</body>
</html>
