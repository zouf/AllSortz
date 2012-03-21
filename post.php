<?php

if (empty($_POST['searchDat'])) {
	$return['error'] = true;
	$return['msg'] = 'You didn\'t enter anything.';
}
else {
	$return['error'] = false;
	$return['msg'] = 'Response form server: ' . $_POST['searchDat'];
}

echo json_encode($return); 

?>