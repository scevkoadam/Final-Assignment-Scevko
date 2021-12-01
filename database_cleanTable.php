<?php

header('Access-Control-Allow-Origin: *');
require "database_connect.php";

$sql = "delete from `lightlevel`";

if (mysqli_query($con,$sql))
{
    echo "Table of Light Levels cleaned\n";
}
else
{
	echo "Error while cleaning Light Level table";
}

mysqli_close($con); 
?>