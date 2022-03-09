<?
//obtenemos los datos de la llamada y las guardamos en variables para trabajar de forma más cómoda
$origen_llamada=$_POST["src"];
$destino_llamada=$_POST["dst"];
$userfield=$_POST["userfield"];
$dtmf=$_POST["dtmf"];
$id_llamada=$_POST["ID"];
$api=$_POST["api"];
$comando=$_POST["command"];
$opciones=$_POST["options"];
$estado=$_POST["status"];
$descripcion=$_POST["description"];
$fecha_llamada=$_POST["startcall"];
$duracion_llamada=$_POST["durationcall"];
$duracion_llamada_contestada=$_POST["durationcallanswered"];
if ($origen_llamada!="" && $destino_llamada!="" && $id_llamada!=""){
    if ($userfield==""){
        $userfield=1;
    }
    switch($userfield){
        case "1":
            //reproducimos una locucion esperando una respuesta
            $comando="speak_getdtmf";
            $option="google;es;Bienvenido a mi empresa, por favor escriba a continuacion su usuario;5000;4;1.2";
            $userfield="2";
            break;
        case "2":
            if ($dtmf=="timeout"){
                //tiempo de espera agotado en la respuesta del usuario, volvemos a repetirlo
                $comando="speak_getdtmf";
                $option="netelip;Pedro;Bienvenido a mi empresa, por favor escriba a continuacion su usuario;5000;4";
                $userfield="2";
            }
            else {
                if ($dtmf=="1111") {
                    //el usuario es correcto, reproducimos la locucion esperando la respuesta del llamante
                    $comando="speak_getdtmf";
                    $option="netelip;Pedro;Su usuario es correcto, accedemos al menu del servicio. Pulse uno para hablar con atencion al cliente, pulse dos, para hablar con soporte;5000;1";
                    $userfield="4";
                }
                else {
                    //el usuario no es correcto, reproducimos la locucion de que no funciona y colgamos la llamada
                    $comando="speak";
                    $option="netelip;Pedro;Su usuario es incorrecto, para acceder a este servicio debes de ser usuario";
                    $userfield="3";
                }
            }
            break;
        case "3":
            //colgamos la llamada
            $comando="hangup";
            $option="";
            $userfield="";
            break;
        case "4":
            switch($dtmf) {
                case "timeout":
                    //tiempo de espera agotado en la respuesta del usuario, volvemos a repetirlo
                    $comando="speak_getdtmf";
                    $option="netelip;Pedro; Pulse uno para hablar con atencion al cliente, pulse dos, para hablar con soporte;5000;1";
                    $userfield="4";
                    break;
                case "1":
                    //ejecutamos la cola de la vPBX con prioridad 2
                    $comando="queue";
                    $option="nuevacola;2";
                    $userfield="3";
                    break;
                case "2":
                    //ejecutamos la cola de la vPBX con prioridad 1
                    $comando="queue";
                    $option="nuevacola;1";
                    $userfield="3";
                    break;
            }
        break;
    }
    $cadena=array("command"=>$comando,"options"=>$option,"userfield"=>$userfield);
    echo(json_encode($cadena));
}
else {
    die();
}
?>
