<html>
<head>
<title>PHP Test</title>
</head>
<body>
 <?php
require_once('utilities.php');

function createBusinessRatingTable($dbname,$conn)
{
	$tblname = "busrat_tbl";
	if(checkIfExists($tblname,$dbname))
	{
		echo('<p> '.$tblname.' already exist!</p>');
		return;		
	}
	mysql_select_db($dbname);
	$sql_create_dyn_table = "CREATE TABLE ".$tblname."(usr_id INT, bus_id INT, rating INT, ".
		" INDEX user_ind (usr_id), FOREIGN KEY (usr_id) REFERENCES user_tbl(usr_id)     ON DELETE CASCADE ,".
		" INDEX bus_ind  (bus_id), FOREIGN KEY (bus_id) REFERENCES business_tbl(bus_id) ON DELETE CASCADE) ".
		" ENGINE=INNODB;";
		
	mysql_select_db($dbname);
	$retval = mysql_query( $sql_create_dyn_table, $conn );
	if(! $retval )
	{
	  die('Could not create table: ' . mysql_error());
	}

}


function createBusinessCharacteristicsTable($dbname, $conn)
{
	$tblname = "buscharac_tbl";
	if(checkIfExists($tblname,$dbname))
	{
		echo('<p> '.$tblname.' already exist!</p>');
		return;		
	}
	mysql_select_db($dbname);
	$sql_create_dyn_table = "CREATE TABLE ".$tblname."(bus_id INT, charac_id INT, rating INT, ".
		" INDEX bus_ind (bus_id), FOREIGN KEY (bus_id) REFERENCES business_tbl(bus_id)     ON DELETE CASCADE ,".
		" INDEX charac_ind  (charac_id), FOREIGN KEY (charac_id) REFERENCES characteristics_tbl(charac_id) ON DELETE CASCADE) ".
		" ENGINE=INNODB;";
		
	mysql_select_db($dbname);
	$retval = mysql_query( $sql_create_dyn_table, $conn );
	if(! $retval )
	{
	  die('Could not create table: ' . mysql_error());
	}
	
}

function createUserCharacteristicsTable($dbname, $conn)
{
	$tblname = "usercharac_tbl";
	if(checkIfExists($tblname,$dbname))
	{
		echo('<p> '.$tblname.' already exist!</p>');
		return;		
	}
	mysql_select_db($dbname);
	$sql_create_dyn_table = "CREATE TABLE ".$tblname."(usr_id INT, charac_id INT, rating INT, ".
		" INDEX user_ind (usr_id), FOREIGN KEY (usr_id) REFERENCES user_tbl(usr_id)     ON DELETE CASCADE ,".
		" INDEX charac_ind  (charac_id), FOREIGN KEY (charac_id) REFERENCES characteristics_tbl(charac_id) ON DELETE CASCADE) ".
		" ENGINE=INNODB;";
		
	mysql_select_db($dbname);
	$retval = mysql_query( $sql_create_dyn_table, $conn );
	if(! $retval )
	{
	  die('Could not create table: ' . mysql_error());
	}
	
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
		echo('<p> '.$tableName.' already exist!</p>');
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
		  " PRIMARY KEY ( usr_id ) ) ENGINE=INNODB;   ";

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


	$dbname = "nightout1";
 	$conn = mysql_connect("localhost","root","new-password");
 	if (!$conn)
 	{
		die('Could not connect: ' . mysql_error());
	}
	createUserTable($dbname,$conn);
	createCharaceristicsTable($dbname,$conn);
	createBusinessTable($dbname,$conn);
	createUserCharacteristicsTable($dbname,$conn);
	createBusinessCharacteristicsTable($dbname,$conn);
	createBusinessRatingTable($dbname,$conn);
 	mysql_close($conn);
 ?>
</body>
</html>
