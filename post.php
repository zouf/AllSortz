<?php

/*if (empty($_POST['searchDat'])) {
	$return['error'] = true;
	$return['msg'] = 'You didn\'t enter anything.';
}
else {
	$return['error'] = false;
	$return['msg'] = 'Response form server: ' . $_POST['searchDat'];
}
*/
if (empty($_POST['fullname']) || empty($_POST['email']) || empty($_POST['uname']) || empty($_POST['password'])) {
	$return['error'] = false;
	$return['msg'] = 'You missed something!';
}
else {
	$return['error'] = false;
	$return['msg'] = 'Response form server: ' . $_POST['fullname'];
}
echo json_encode($return); 

?>