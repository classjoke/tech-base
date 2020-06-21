<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<?php 
    $ednom = null;
    $editflag = NULL;
    $buflen = 5;
    $name = "名前";
    $com = "コメント";
    #$pass = "pass";
    $dsn = 'データベース名';
    $user = 'ユーザー名';
    $password = 'パスワード';
    $tablesID = 1;
    $pdo = new PDO($dsn, $user, $password, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_WARNING));
    
    $create_table = "CREATE TABLE IF NOT EXISTS TBboard"
    ." ("
	. "id INT AUTO_INCREMENT PRIMARY KEY,"
	. "name char(32),"
	. "comment TEXT"
    .");";
    //TBboard id name comment
    $stmt = $pdo->query($create_table);
    $show_tables = 'SHOW TABLES';
    $result = $pdo->query($show_tables);
    $i = 0;
    foreach ($result as $row){
        $tablenames[$i]  = $row[0];
//        echo $tablenames[$i]."<BR>";
        $i++;
    }
    //$tablenames[0] を今回の掲示板とする。
    //以下新規書き込み用

 

    if (isset($_POST["submit"]))
    {
        $name = $_POST["name"];
        $com = $_POST["comment"];
        //$pass = $_POST["password"];
        $editflag = $_POST["no"];
        $date = date("Y/m/d　H:i:s");
        
        if($editflag <> null){
            $id = $_POST["no"];
            $name = $_POST["name"];
            $com = $_POST["comment"];
            $edit = "UPDATE $tablenames[0] SET name=:name,comment=:comment WHERE id=:id";
            $stmt = $pdo->prepare($edit);
            $stmt->bindParam(':name', $name, PDO::PARAM_STR);
	        $stmt->bindParam(':comment', $com, PDO::PARAM_STR);
	        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
	        $stmt->execute();
        }else{
        $insert_tmp = "INSERT INTO $tablenames[0](name, comment) VALUES (:name, :comment)";
        $new_writeing = $pdo -> prepare($insert_tmp);
        $new_writeing -> bindParam (":name", $name, PDO::PARAM_STR);
        $new_writeing -> bindParam(":comment", $com, PDO::PARAM_STR);
        $new_writeing -> execute();
        }
        $name = "名前";
        $com = "コメント";
    }
    if($_POST["rmv"])
    {
        //$pass = $_POST["password"];
        //echo "削除します<br>";
        $id = $_POST["rmnom"];
        $delete = "delete from $tablenames[0] where id=:id";
        $stmt = $pdo->prepare($delete);
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->execute();
    
    }
    if($_POST["ed"]){
        $id = $_POST["ednom"];
        $edid_io = "SELECT * FROM $tablenames[0] WHERE id=$id";
        $stmt = $pdo->query($edid_io);
        $edit_buf = $stmt->fetchAll();
        foreach ($edit_buf as $row){
            //$rowの中にはテーブルのカラム名が入る
            $ednom = $row['id'];
            $name = $row['name'];
            $com = $row['comment'];
        }
        $stmt -> execute();
    }
    $sql = "SELECT * FROM $tablenames[0]";
    $stmt = $pdo->query($sql);
    $results = $stmt->fetchAll();
    foreach ($results as $row){
		//$rowの中にはテーブルのカラム名が入る
		echo $row['id'].',';
		echo $row['name'].',';
		echo $row['comment'].'<br>';
    echo "<hr>";
    }
    $stmt -> execute();
    //sqlを閉じる

?>
    <form method="POST" action="">
    <input type = "text" name ="name" value = "<?php echo $name ?>"><br>
    <input type = "text" name ="comment" value = "<?php echo $com ?>"><br>
    <!--<input type = "text" name = "password" value = "-->
    削除番号:<input type = "number" name ="rmnom"><br>
    編集番号:<input type = "number" name = "ednom"><br>
    <input type = "hidden" name = "no" value = "<?php echo $ednom ?>"><br>
    <input type="submit" name="submit">
    <input type= "submit" name= "rmv" value = "削除">
    <input type= "submit" name= "ed" value = "編集">
    </form>
</body>
</html>