<?php

header('Access-Control-Allow-Origin: *');

$servername = "localhost";
$username   = "id13888041_adam";
$password   = "/tC5)q&p>bn&r3OD";
$database   = "id13888041_lightlevellogs";

$con = mysqli_connect($servername,$username,$password,$database);
//echo nl2br ("connection: ");

if ($con)
{
    //echo nl2br ("OK\n");
}
else
{
    //echo nl2br ("ERROR\n");
}

?>