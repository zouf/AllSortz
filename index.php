<?php
	include('template/header.php');

 $conn = mysql_connect("localhost","root","new-password");
 if (!$conn)
   {
   		die('Could not connnect: ' . mysql_error());
   }
	else
	{
		echo('<div id="formdiv">');
		echo('<form action="" id="mainform" method="post">');
		echo('<input type="text" name="search" id="search" class="bigsearch" value="" />');
		echo('<div class="formbutton"><input type="submit" name="submit" id="submit" value="Find me something to do" /></div>');
		echo('</form>');
		echo('</div>');
	}
 mysql_close($conn);

 ?>


<div>
<p id="message"></p>
</div>
<?php
	include('template/footer.php');

?>
</body>
</html>
