<?php
    session_start();
    class Cronometro {
        public $inicio;
        public $tiempoTranscurrido;

        public function __construct() {
            $this->inicio = 0;
            $this->tiempoTranscurrido = 0;
        }

        public function arrancar() {
            $this->inicio = microtime(true);
        }

        public function parar() {
            if ($this->inicio > 0) {
                $this->tiempoTranscurrido = microtime(true) - $this->inicio;
            }
        }

        public function mostrar() {
            $minutos = floor($this->tiempoTranscurrido / 60);
            $segundos = sprintf("%04.1f", $this->tiempoTranscurrido - ($minutos * 60));

            echo "<p>" . $minutos . ":" . $segundos . "</p>";
        }
    }


    if (!isset($_SESSION["cronometro"])) {
        $_SESSION["cronometro"] = new Cronometro();
    }

    if (isset($_POST["arrancar"])) {
        $_SESSION["cronometro"]->arrancar();
    }

    if (isset($_POST["parar"])) {
        $_SESSION["cronometro"]->parar();
    }
?>
<!DOCTYPE HTML>

<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />
    <title>MotoGP-Juegos</title>
    <meta name ="author" content ="Gonzalo Garcia Castro" /> 
    <meta name ="description" content ="HTML correspondiente a los juegos del proyecto" /> 
    <meta name ="keywords" content ="" /> 
    <meta name ="viewport" content ="width=device-width, initial-scale=1.0" /> 
    <link rel="stylesheet" type="text/css" href="estilo/estilo.css"/>
    <link rel="stylesheet" type="text/css" href="estilo/layout.css"/>
    <link rel="icon" href="multimedia/favicon.png" />
</head>
<body>
    <!-- Datos con el contenidos que aparece en el navegador -->
    <header>
        <h1><a href='index.html' title='Pagina principal'>MotoGP Desktop</a></h1>
        <nav>
            <a href='index.html' title='Pagina principal'>Inicio</a>
            <a href='piloto.html' title='Información del piloto'>Piloto</a>
            <a href='circuito.html' title='Información del circuito'>Circuito</a>
            <a href='meteorologia.html' title='Información sobre la meteorología'>Meteorología</a>
            <a href='clasificaciones.php' title='Información sobre las clasificaciones'>Clasificaciones</a>
            <a href='juegos.html' title='Pagina sobre juegos' class='active'>Juegos</a>
            <a href='ayuda.html' title='Información sobre la ayuda'>Ayuda</a>
        </nav>
    </header>
    <p>Estás en: <a href='index.html'>Inicio</a> | Juegos | <strong>Cronómetro</strong></p>
    <main>
        <form action='#' method='post'>
            <button type='submit' name='arrancar'>Arrancar</button>
            <button type='submit' name='parar'>Parar</button>
            <button type='submit' name='mostrar'>Mostrar</button>
        </form>
        <?php
            if (isset($_POST["mostrar"])) {
                $_SESSION["cronometro"]->mostrar();
            }
        ?>
    </main>
</body>

</html>