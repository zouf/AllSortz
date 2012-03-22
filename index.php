<?php
	include('template/header.php');

 $conn = mysql_connect("localhost","root","new-password");
 if (!$conn)
   {
   		die('Could not connnect: ' . mysql_error());
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
 mysql_close($conn);

 ?>


<div>
<p id="message"></p>
</div>
<div>
	<a href="display/viewtable.php?table=business_tbl">Businesses</a><br>
	<a href="display/viewtable.php?table=user_tbl">Users</a><br>
	<a href="display/viewtable.php?table=busrat_tbl">Business Ratings</a><br>
	<a href="ratings/userdiff.php">Diff Between Users</a>
</div>

<?php
	include('template/footer.php');

?>
</body>
</html>
