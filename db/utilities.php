<?php 

//  These are mostly internal utilitiy functions (e.g. checking if a particular keyword exists or not)  Functionality for adding a user, etc. should be in dblib.php

/**
 * Translate a result array into a HTML table
 *
 * @author      Aidan Lister <aidan@php.net>
 * @version     1.3.2
 * @link        http://aidanlister.com/2004/04/converting-arrays-to-human-readable-tables/
 * @param       array  $array      The result (numericaly keyed, associative inner) array.
 * @param       bool   $recursive  Recursively generate tables for multi-dimensional arrays
 * @param       string $null       String to output for blank cells
 */
function array2table($array, $recursive = false, $null = '&nbsp;')
{
    // Sanity check
    if (empty($array) || !is_array($array)) {
        return false;
    }
 
    if (!isset($array[0]) || !is_array($array[0])) {
        $array = array($array);
    }
 
    // Start the table
    $table = "<table>\n";
 
    // The header
    $table .= "\t<tr>";
    // Take the keys from the first row as the headings
    foreach (array_keys($array[0]) as $heading) {
        $table .= '<th>' . $heading . '</th>';
    }
    $table .= "</tr>\n";
 
    // The body
    foreach ($array as $row) {
        $table .= "\t<tr>" ;
        foreach ($row as $cell) {
            $table .= '<td>';
 
            // Cast objects
            if (is_object($cell)) { $cell = (array) $cell; }
 
            if ($recursive === true && is_array($cell) && !empty($cell)) {
                // Recursive mode
                $table .= "\n" . array2table($cell, true, true) . "\n";
            } else {
                $table .= (strlen($cell) > 0) ?
                    ((string) $cell) :
                    $null;
            
				}
 
            $table .= '</td>';
        }
 
        $table .= "</tr>\n";
    }
 
    $table .= '</table>';
    return $table;
}


function insertBusType($name,$conn)
{
		$sql_insert_type = "INSERT INTO bustype_tbl (bustype_name, bustype_descr) VALUES ('$name', '$name'); ";
		$res = mysql_query($sql_insert_type);
		if(!$res)
		{
		 	die('Invalid query: ' . mysql_error());
		}

}

function getNameFromBusTypeId($bustypeid, $conn)
{
		$resultingName = mysql_query("SELECT * from bustype_tbl where bustype_id='$bustypeid'");
		if(!$resultingName)
		{
		 	die('Invalid query: ' . mysql_error());
		}
		$rname = mysql_fetch_array($resultingName, MYSQL_BOTH);
		$bustypename = $rname['bustype_name'];

	return $bustypename;
}
function getBusTypeIdFromName($name,$conn)
{
		$resultingId = mysql_query("SELECT * from bustype_tbl where bustype_name='$name'");
		if(!$resultingId)
		{
		 	die('Invalid query: ' . mysql_error());
		}
		$rid = mysql_fetch_array($resultingId, MYSQL_BOTH);
		$bustypeid = $rid['bustype_id'];
	return $bustypeid;
}


// table to characterize all businesses
function insertBusTypeRelPair($busid, $typeid, $conn)
{
	$mysql_insert_pair = "INSERT INTO bustyperel_tbl (bus_id, bustype_id, rating) VALUES ('$busid', '$typeid', 1); ";
	$res = mysql_query($mysql_insert_pair);
	if(!$res)
	{
	 	die('Invalid query: ' . mysql_error());
	}
}

function getBusIdFromName($name,$conn)
{
		$resultingId = mysql_query("SELECT * from business_tbl where bus_name='$name'");
		if(!$resultingId)
		{
		 	die('Invalid query: ' . mysql_error());
		}
		$rid = mysql_fetch_array($resultingId, MYSQL_BOTH);
		return $rid['bus_id'];
}


function businessTypeExists($name,$conn)
{
	$result = mysql_query("SELECT * FROM bustype_tbl WHERE bustype_name='$name'");
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