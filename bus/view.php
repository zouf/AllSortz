<?php
/* View a business */

	include('../template/header.php');
?>


<style>
#feedback { font-size: 1.em; }
#selectable .ui-selecting { background: #FECA40; }
#selectable .ui-selected { background: #F39814; color: white; }
#selectable { list-style-type: none; margin: 0; padding: 0; text-align:center; }
#selectable li { margin: 3px; padding: 1px; float: left; width: 100px; height: 80px; font-size: 2em; text-align: center; }
</style>
<script>
$(function() {
	$("#selectable").selectable({
	    selected: function (event, ui) {
	       if(!postRating(ui.selected.id))
			{
				alert('error in posting a rating');
			}
	    },
	    unselected: function (event, ui) {
	        $(ui.unselected).removeClass('selectedfilter');
	    }
	});
});
</script>
<?php

$dbname = "nightout1";
$conn = mysql_connect("localhost","root","new-password");
mysql_select_db($dbname);
if (!$conn)
{
	die('Could not connect: ' . mysql_error());
}

if(!isset($_GET['id']))
{
		echo('Invalid URL!');  // redirect to error pag
		die('<a href="javascript:history.go(-1)" title="Return to the previous page">&laquo; Go back</a>');
}

$busId = $_GET['id'];


	$busResult = mysql_query("SELECT * from business_tbl where bus_id=$busId");
	if(!$busResult)
	{
		die('Query error: ' . mysql_error());
	}
	$business = mysql_fetch_array($busResult, MYSQL_BOTH);
	
	echo('<h1>'.$business['bus_name']."</h1>");
	
	echo('<div id="ratingList">');
	echo('<ol id="selectable">');
	echo('<li class="ui-state-default" id=hate>Hate it!</li>');
	echo('<li class="ui-state-default" id=ok>It\'s OK</li>');
	echo('<li class="ui-state-default" id=love>Love it!</li>');
	echo('</ol>');
	echo('</div>');

	include('../template/footer.php');

?>
