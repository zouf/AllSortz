<?php 

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
                    htmlspecialchars((string) $cell) :
                    $null;
            }
 
            $table .= '</td>';
        }
 
        $table .= "</tr>\n";
    }
 
    $table .= '</table>';
    return $table;
}

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