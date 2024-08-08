<?php 
require_once '../config/DbOperations.php';

$db = new DbOperations();
 
if(!empty($_POST["munid"])){ 
    $arrayPostu=$db->viewPostuAjax($_POST['munid']);
	if (is_array($arrayPostu) || is_object($arrayPostu)) {
	echo '<option value="">Select Postu</option>'; 
	foreach($arrayPostu as $r) {
		$munisipiu=$db->viewMunisipiuById('munisipiu',$r['id_munisipiu']);
        echo "<option value='$r[id_postu]'>$munisipiu - $r[postu]</option>"; 
    }
	}
}

if(!empty($_POST["postuid"])){ 
    $arraySuku=$db->viewSukuAjax($_POST['postuid']);
	if (is_array($arraySuku) || is_object($arraySuku)) {
	echo '<option value="">Select Suku</option>'; 
	foreach($arraySuku as $r) {
		$postu=$db->viewPostuById('postu',$r['id_postu']);
        echo "<option value='$r[id_suku]'>$postu - $r[suku]</option>"; 
    }
	}
}
?>