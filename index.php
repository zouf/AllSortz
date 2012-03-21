<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<link rel='stylesheet' type='text/css' href='css/main.css' />
	<link href='http://fonts.googleapis.com/css?family=IM+Fell+French+Canon+SC' rel='stylesheet' type='text/css'>
	<link href='http://fonts.googleapis.com/css?family=Trykker' rel='stylesheet' type='text/css'>
	

	<link rel="stylesheet" href="css/smoothness/jquery-ui-1.8.18.custom.css">
	<script type="text/javascript" src="js/jquery-1.7.1.min.js"></script>
	<script type="text/javascript" src="js/jquery-ui-1.8.18.custom.min.js"></script>
	<script type="text/javascript" src="js/ajax_submit.js"></script>
	<script>
		$(function() {
			$( "input:submit, a, button", ".formbutton" ).button();
			$( "a", ".formbutton" ).click(function() { return false; });
		});
	</script>

<title>Nightout App</title>
</head>
<body>

 <?php
 $con = mysql_connect("localhost","root","new-password");
 if (!$con)
   {
   		die('Could not connect: ' . mysql_error());
   }
	else
	{
		echo('<form action="" id="mainform" method="post">');
		echo('<h1>Nightout</h1>');
		echo('<br />');
		echo('<br />');
		echo('<input type="text" name="search" id="search" class="bigsearch" value="" />');
		echo('<div class="formbutton"><input type="submit" name="submit" id="submit" value="Find me something to do" /></div>');
		echo('</form>');
	}
 mysql_close($con);

 ?>


<div>
<p id="message"></p>
</div>
<div>
	<a href="display/viewtable.php?table=business_tbl">Businesses</a><br>
	<a href="display/viewtable.php?table=user_tbl">Users</a><br>
	<a href="display/viewtable.php?table=busrat_tbl">Business Ratings</a>
</div>


</body>
</html>
