<?php
require_once('searchlib.php');

if (empty($_POST['searchDat']) || empty($_POST['location']) ) {
	$return['error'] = true;
	$return['msg'] = 'You didn\'t enter anything.';
}
else    {
	session_start();
	$uname = '';
	if(isset($_SESSION['uname']))
	{
		$uname = $_SESSION['uname'];
	}
	$return['error'] = false;
	$searchTerm = $_POST['searchDat'];
	$city = $_POST['location'];
	
	$return['msg'] = searchKeywordCity(mysql_real_escape_string($searchTerm), mysql_real_escape_string($city), $uname);
}
//echo (searchKeywordCity(mysql_real_escape_string("a"), mysql_real_escape_string("b"), "c"));


echo json_encode($return);

?>