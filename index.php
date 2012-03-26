<?php
	include('template/header.php');

?>
	<style>
	#feedback { font-size: 1.em; }
	#selectable .ui-selecting { background: #FECA40; }
	#selectable .ui-selected { background: #F39814; color: white; }
	#selectable { list-style-type: none; margin: 0; padding: 0; text-align:center; }
	#selectable li { margin: 3px; padding: 1px; float: left; width: 100px; height: 80px; font-size: 2em; text-align: center; }
	</style>
hello!
<?php
 $conn = mysql_connect("localhost","root","new-password");
 if (!$conn)
   {
   		die('Could not connnect: ' . mysql_error());
   }
	else
	{
		echo('<div id="formdiv">');
		echo('<form action="" id="mainform" method="post">');
		echo('<input type="text" name="search" id="search" class="bigsearch" value="Type"  onfocus="if(!this._haschanged){this.value=\'\'};this._haschanged=true;" /> ');
		echo('<input type="text" name="search" id="location" class="bigsearch" value="Location"  onfocus="if(!this._haschanged){this.value=\'\'};this._haschanged=true;" />');
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
