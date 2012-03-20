<html>
<head>
<title>PHP Test</title>
</head>
<body>
 <?php


function createDynamicUserCharacteristics($dbname, $conn)
{
	$tblname = "usercharac_tbl";
	if(checkIfExists($tblname,$dbname))
	{
		return;		
	}
	mysql_select_db($dbname);
	//Creates User (Row) -> Characteristic (Col)
	$result = mysql_query("SELECT charac_name FROM characteristics_tbl");
	
	$sql_create_dyn_table = "CREATE TABLE ".$tblname."( uchr_id INT NOT NULL AUTO_INCREMENT, ";
	while ($row = mysql_fetch_array($result, MYSQL_BOTH)) {
		$str = $row["charac_name"];
		$sql_create_dyn_table = $sql_create_dyn_table. $str." VARCHAR(100) NOT NULL, ";
	}
	$sql_create_dyn_table = $sql_create_dyn_table. " PRIMARY KEY (uchr_id ) );";
	mysql_select_db($dbname);
	$retval = mysql_query( $sql_create_dyn_table, $conn );
	if(! $retval )
	{
	  die('Could not create table: ' . mysql_error());
	}
	echo($sql_create_dyn_table);
	
}

//Table to include businesses, but also things to do like "Central Park Visit", or "Go TO Museum"
function createBusinessTable($dbname, $conn)
{
	$tableName = "business_tbl";
	if(!checkIfExists($tableName,$dbname))
	{
			$sql_create_table = 
				" CREATE TABLE ".$tableName."(  ".
				" bus_id INT NOT NULL AUTO_INCREMENT, ".
				" bus_name  VARCHAR(200) NOT NULL, ".
				" bus_keyword  VARCHAR(500) NOT NULL, ".
				" bus_descr VARCHAR(500) NOT NULL, ".
				" bus_rating FLOAT(2,1), ".
				" PRIMARY KEY ( bus_id ) );   ";
			mysql_select_db($dbname);
			$retval = mysql_query( $sql_create_table, $conn );
			if(! $retval)
			{
				 die('Could not create table: ' . mysql_error());
			}
			echo "Table for businesses created successfully\n";
	}
}


function createCharaceristicsTable($dbname, $conn)
{	
	$tableName = "characteristics_tbl";
	if(!checkIfExists($tableName,$dbname))
	{
		
		$sql_create_characteristics =  
		  " CREATE TABLE ".$tableName."( ".
		  " charac_id INT NOT NULL AUTO_INCREMENT, ".
		  " charac_name VARCHAR(200) NOT NULL, ".
		  " charac_descr VARCHAR(200) NOT NULL,   ".
		  " PRIMARY KEY ( charac_id ) );   ";
		mysql_select_db($dbname);
		$retval = mysql_query( $sql_create_characteristics, $conn );
		if(! $retval )
		{
		  die('Could not create table: ' . mysql_error());
		}
		echo "Table for interests created successfully\n";
	}
	else
	{
		echo('<p> Characteristics already exist!</p>');
	}
	return;
}

function createUserTable($dbname, $conn)
{	
	$tableName = "user_tbl";
	if(!checkIfExists($tableName,$dbname))
	{
		echo('<p>Connected!</p>');
		$sql_create_user =  
		  " CREATE TABLE ".$tableName."( ".
		  " usr_id INT NOT NULL AUTO_INCREMENT, ".
		  " usr_fullname VARCHAR(100) NOT NULL, ".
		  " usr_email VARCHAR(40) NOT NULL,   ".
		  " usr_uname VARCHAR(40),	 ".
		  " PRIMARY KEY ( usr_id ) );   ";

		mysql_select_db($dbname);
		$retval = mysql_query( $sql_create_user, $conn );
		if(! $retval )
		{
		  die('Could not create table: ' . mysql_error());
		}
		echo('Table for users created successfully\n');
	}
	else
	{
		echo('<p> Users already exist!</p>');
	}
	return;
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
	$dbname = "nightout1";
 	$conn = mysql_connect("localhost","root","new-password");
 	if (!$conn)
 	{
		die('Could not connect: ' . mysql_error());
	}
	createUserTable($dbname,$conn);
	createCharaceristicsTable($dbname,$conn);
	createBusinessTable($dbname,$conn);
	createDynamicUserCharacteristics($dbname,$conn);
 	mysql_close($conn);
 ?>
</body>
</html>
