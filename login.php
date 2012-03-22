<?php
	
	if(isset($_GET['logout']))
	{
		session_destroy();
		
	}

	include('template/header.php');

	if(isset($_GET['logout']))
	{
		echo('<div>you\'ve been logged out!</div>');
	}


	$conn = mysql_connect("localhost","root","new-password");
	if (!$conn)
	{
		die('Could not connnect: ' . mysql_error());
	}
	else
	{


		echo('<form id="addUserForm" action="handler/login.php" method="post">');
		echo('<h1>Nightout Login</h1>');
		echo('<br />');
		echo('<br />');
		echo('<p>Name: <input type="text" name="uname" id="uname" class="userLogin" value="" /></p>');
		echo('<br />');
		echo('<p>Password: <input type="password" name="password" id="password" class="userLogin" value="" /></p>');

		echo('<div class="formbutton"><input type="submit" name="submit" id="loginUser2" value="Login" /></div>');
		echo('</form>');


	}
	mysql_close($conn);




	 ?>


	<div>
	<p id="message"></p>
	</div>


<?php
	include('tmeplate/footer.php');

?>