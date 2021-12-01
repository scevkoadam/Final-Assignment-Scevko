<?php

header('Access-Control-Allow-Origin: *');
require "database_connect.php";

$count = $_GET["count"];
$data  = $_GET["data"];
$datum = date("Y-m-d H:i:s");

$sql = "INSERT INTO `lightlevel`(`count`, `data`, `datum`) VALUES ('$count','$data','$datum')";

echo $count . '\n' . 
$data . '\n' . 
$datum;

if (mysqli_query($con,$sql))
{
    echo "Light level with number $count added to database\n";
}
else
{
	echo "Error while adding light level to database";
}

mysqli_close($con); 
?>