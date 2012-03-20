<?php 

function businessExists($name,$conn)
{	

	$result = mysql_query("SELECT * FROM business_tbl WHERE bus_name='$name'");
	if(!mysql_num_rows($result))
		return False;
	return True;
}


?>