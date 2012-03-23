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

<?php

require_once('../db/dblib.php');

$conn = connectToDatabase();

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
	
	$rating = getRatingIfExists($busId,$_SESSION['uname']);
	echo('<div id="ratingList">');
	echo('<ol id="selectable">');

			echo('<li class="ui-state-default" id=hate>Hate it!</li>');
			echo('<li class="ui-state-default" id=ok>It\'s OK</li>');
			echo('<li class="ui-state-default" id=love>Love it!</li>');

	echo('</ol>');
	?>
	<script>
	$(function() {
		$("#selectable").selectable({
		    selected: function (event, ui) {
		       if(!postRating(ui.selected.id))
				{
					alert('error in posting a rating');
				}
		    },
		 	create: function(event, ui) 
			{ 
				var rating = <?php echo($rating);?>;
				if(rating == -1)
					return;
				var v;
				if(rating==0)
				{
					jQuery('#hate').addClass('ui-selected');
				}
				else if(rating==1)
				{
					jQuery('#ok').addClass('ui-selected');
				}
				else if(rating==2)
				{
					jQuery('#love').addClass('ui-selected');
				}
			
				
			}
		});
	});
	</script>	

	<?php
	
	echo('</div>');
	mysql_close($conn);
	include('../template/footer.php');

?>
