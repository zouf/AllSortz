<html>
<head>
<title>Populate Tables</title>
</head>
<body>
 <?php


require_once('../db/utilities.php');
function insertUser($name,$conn)
{
	$name = mysql_real_escape_string($name);
	if(userExists($name,$conn))
	{
		echo('User '.$name.' already exists!\n');
		return;
	}
	$ret = mysql_query("INSERT INTO user_tbl (usr_fullname, usr_email, usr_uname) VALUES ('$name', 'test@gmail.com', '$name')");
	if(!$ret)
	{
		die('Could not create table: ' . mysql_error());
	}
	echo("User ".$name." Inserted!\n");
}

function populateUserTable($dbname, $conn)
{
	mysql_select_db($dbname);
	insertUser("Matt Zoufaly",$conn);
	insertUser("Jim Raynor",$conn);	
	insertUser("Sarah Kerrigan",$conn);
	insertUser("Zeratul",$conn);
	insertUser("Tychus",$conn);
}


function populateBusRatTable($dbname, $conn)
{	
	mysql_select_db($dbname);
	// Get all user_ids so we can populate the rows of this matrix
	$allUsers = mysql_query("SELECT * FROM user_tbl");

	while ($userrow = mysql_fetch_array($allUsers, MYSQL_BOTH)) {   // iterate through all users
		$userRef = $userrow["usr_id"];
		// get all businesses
		$allBusinesses = mysql_query("SELECT bus_id FROM business_tbl");
		while($busrow = mysql_fetch_array($allBusinesses, MYSQL_BOTH)) {    // to iterate through all businesses
			$busRef = $busrow["bus_id"];  
			$rand = rand ( 0,2);
			if(!checkIfRatingPairExists($userRef, $busRef,$conn))
			{
				$sql_insert = "INSERT INTO busrat_tbl (usr_id, bus_id, rating) VALUES ('$userRef', '$busRef', $rand)";
				$res = mysql_query($sql_insert);
				if(!$res)
				{
					die('Could not populate business rating table: '.mysql_error());
				}
			}
			else
			{
				echo("Pair already exists. Update possibly");
			}		
		}
	}
}

$dbname = "nightout1";
$conn = mysql_connect("localhost","root","new-password");
if (!$conn)
{
	die('Could not connect: ' . mysql_error());
}

populateUserTable($dbname, $conn);
populateBusRatTable($dbname, $conn);


mysql_close($conn);
	
 ?>
</body>
</html>
