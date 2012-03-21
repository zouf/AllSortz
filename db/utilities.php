<?php 

function businessExists($name,$conn)
{	

	$result = mysql_query("SELECT * FROM business_tbl WHERE bus_name='$name'");
	if(!mysql_num_rows($result))
		return False;
	return True;
}


function userExists($name,$conn)
{	

	$result = mysql_query("SELECT * FROM user_tbl WHERE usr_fullname='$name'");
	if(!mysql_num_rows($result))
		return False;
	return True;
}


function checkIfExists($name,$dbname ) {
	$sql = "SHOW TABLES FROM $dbname";
	$result = mysql_query($sql);
	$fd = False;
	while ($row = mysql_fetch_row($result)) {
		if(!strcmp($row[0], $name))
		{
			$fd = True;
		}
	}
	return $fd;
}

function checkIfRatingPairExists($usr_id, $bus_id, $conn)
{
	$result = mysql_query("SELECT * FROM busrat_tbl WHERE usr_id='$usr_id' AND bus_id='$bus_id'");
	if(!mysql_num_rows($result))
		return False;
	return True;
}

?>