<html>
<head>
<title>PHP Test</title>
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
		echo('<p>Connected</p>');
	}
 mysql_close($con);
 ?>
</body>
</html>
