<html>
<head>
<title>Access YELP</title>
</head>
<body>
 <?php
require_once ('../yelp/OAuth.php');
require_once ('utilities.php');


function yelpAddTypeByCity($dbname, $city, $type)
{

	$conn =  mysql_connect("localhost","root","new-password");
	// For examaple, search for 'tacos' in 'sf'
	$unsigned_url = "http://api.yelp.com/v2/search?term=".$type."&location=".$city;


	// Set your keys here
	$consumer_key = "z-5AyqiKIUREnt2YdCoQ1w";
	$consumer_secret = "_f0lb3ZMq6Lhih53fW1-sLX2ZMk";
	$token = "_l_RyYYi5CdzCclU668qkXF_65iHDNXU";
	$token_secret = "GMcrzmglHenNdy-J3QhvVBn7d4E";

	// Token object built using the OAuth library
	$token = new OAuthToken($token, $token_secret);

	// Consumer object built using the OAuth library
	$consumer = new OAuthConsumer($consumer_key, $consumer_secret);

	// Yelp uses HMAC SHA1 encoding
	$signature_method = new OAuthSignatureMethod_HMAC_SHA1();

	// Build OAuth Request using the OAuth PHP library. Uses the consumer and token object created above.
	$oauthrequest = OAuthRequest::from_consumer_and_token($consumer, $token, 'GET', $unsigned_url);

	// Sign the request
	$oauthrequest->sign_request($signature_method, $consumer, $token);

	// Get the signed URL
	$signed_url = $oauthrequest->to_url();

	// Send Yelp API Call
	$ch = curl_init($signed_url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_HEADER, 0);
	$data = curl_exec($ch); // Yelp response
	curl_close($ch);

	// Handle Yelp response data
	$response = json_decode($data,true);

	// Print it for debugging

		mysql_select_db($dbname);
		foreach($response['businesses'] as $bus)
		{
			$nm = mysql_real_escape_string($bus['name']);
			if(!businessExists($nm,$conn))
			{
				$rating =  $bus['rating'];
				$sql_insert = "INSERT INTO business_tbl (bus_name, bus_keyword, bus_descr, bus_rating) VALUES ('$nm', '$type', 'test desc', '$rating' ); ";
				$res = mysql_query($sql_insert);
				if(!$res)
				{
				 	die('Invalid query: ' . mysql_error());
				}
			}	
	    }
	 mysql_close($conn);
}
$dbname = "nightout1";
$city = "New+York,+NY";
$type = "bar";

yelpAddTypeByCity($dbname, $city, $type);

 ?>
</body>
</html>
