<!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <script src="myScript.js"></script>
        <style type="text/css">
            #wrapper {width: 700px; margin-left: auto;margin-right: auto; border: 1px solid black;
            padding-left:30px}
            #header {height: 200px; margin-left:-30px; margin-bottom:40px; font-size: 24pt;color:green; font-weight: bold;
            text-align: center}
            .user_input {width: 375px} select {width: 635px}
            option {font-size: 12pt} tr {height: 35px} .btn {font-size: 12pt;
            width: 100px}
            #content {height: 680px}
            #footer  {height: 30px; font-size: 16pt; color:#CAE1FF;
            margin-left: -30px;padding: 15px 170px; text-align: center;
            background-color:#228B22}
        </style>
        </head>
        <body>
        <title>WELCOME!</title>
        <form method="POST" action="handler.php" onsubmit="return empty_form()">
        <div id="wrapper">
        <div id="header">
        GOOD VERSE MAILER
        <img src="images/header_image.jpg" alt="authors" style="margin: 5px 0px 0px 3px">
        <div style="font-size: 16pt; color:green; margin: -6px 0px 0px 0px; font-weight: normal"> poetry for everyone </div>
        </div>
        <div id="content">
<?php 

#Оработчик формы пишет данные в следующем формате:
#имя;email;quantity_per_day;author1_id,author2_id,author3_id;user(old or new);UTC_time

error_reporting(E_ALL);
ini_set('display_errors', 1);
#Пишем в файлы данные полученные из формы customers_list_raw.txt 
$myfile = fopen("customers_list_raw.txt", "a");
#Пишем данный потребителя:
#Имя
fwrite($myfile, "{$_POST['name']};"); 
#email
fwrite($myfile,"{$_POST['email']};");
#количество стишков в день (quantity per day)
fwrite($myfile,"{$_POST['qpd']};");
#с авторами чуть посложнее, разделяем их запятыми и тоже пишем 
$authors_in_str=join(',', $_POST['author']);
fwrite($myfile, $authors_in_str);
#статус пользователя, новый или нет
fwrite($myfile,";{$_POST['user']};");
#дополним все это для красоты временем, начиная с UTC
$UTC_time=time();
fwrite($myfile,"$UTC_time\n");
fclose($myfile);
echo "<p style=\"margin-bottom: 40px; font-size: 16pt\" align=\"center\">Все прошло успешно!<br> Запрос будет обработан в течение суток :) </p>";
echo "<p align=\"center\"><img src=\"images/lina_kostenko.jpg\" alt=\"lina_kostenko\"></p>";

?>
        </div>

 <div id="footer">Andrew Sotnikov ^ 2016 ^ </div>
        </div>
        </body>
        </html>




