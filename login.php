<?php
	include('template/header.php');
	
	 $conn = mysql_connect("localhost","root","new-password");
	 if (!$conn)
	   {
	   		die('Could not connnect: ' . mysql_error());
	   }
		else
		{
			echo('<form action="" id="addUserForm" method="post">');
			echo('<h1>Nightout Login</h1>');
			echo('<br />');
			echo('<br />');
			echo('<p>Name: <input type="text" name="uname" id="fullName" class="userLogin" value="" /></p>');
			echo('<br />');
			echo('<p>Password: <input type="password" name="email" id="password" class="userLogin" value="" /></p>');
		
			echo('<div class="formbutton"><input type="submit" name="submit" id="loginUser" value="Login" /></div>');
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