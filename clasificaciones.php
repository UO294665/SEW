<?php
    class Clasificaciones {
        protected $documento;
        public function __construct() {
            $this->documento = "./xml/circuitoEsquema.xml";
        }

        public function consultar(){
            $datos = file_get_contents($this->documento);
            $datos =preg_replace("/>\s*</",">\n<",$datos);
            $xml = new SimpleXMLElement($datos);

            $xml->registerXPathNamespace('ns', 'http://www.uniovi.es');
            $circuito = $xml->xpath('//ns:circuito')[0];

            return $circuito;
        }
    }
?>
<!DOCTYPE HTML>

<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />
    <title>MotoGP-Clasificaciones</title>
    <meta name ="author" content ="Gonzalo Garcia Castro" /> 
    <meta name ="description" content ="HTML correspondiente a las clasificaciones" /> 
    <meta name ="keywords" content ="" /> 
    <meta name ="viewport" content ="width=device-width, initial-scale=1.0" /> 
    <link rel="stylesheet" type="text/css" href="estilo/estilo.css"/>
    <link rel="stylesheet" type="text/css" href="estilo/layout.css"/>
    <link rel="icon" href="multimedia/favicon.png" />
</head>

<body>
    <!-- Datos con el contenidos que aparece en el navegador -->
    <header>
        <h1><a href="index.html" title="Pagina principal">MotoGP Desktop</a></h1>
        <nav>
            <a href="index.html" title="Pagina principal">Inicio</a>
            <a href="piloto.html" title="Información del piloto">Piloto</a>
            <a href="circuito.html" title="Información del circuito">Circuito</a>
            <a href="meteorologia.html" title="Información sobre la meteorología">Meteorología</a>
            <a href="clasificaciones.php" title="Información sobre las clasificaciones" class="active">Clasificaciones</a>
            <a href="juegos.html" title="Pagina sobre juegos">Juegos</a>
            <a href="ayuda.html" title="Información sobre la ayuda">Ayuda</a>
        </nav>
    </header>
    <p>Estás en: <a href="index.html">Inicio</a> | <strong>Clasificaciones</strong></p>

    <h2>Clasificaciones de MotoGP-Desktop</h2>
    <?php
        $clasificaciones = new Clasificaciones();
        $circuito = $clasificaciones->consultar();
        echo "<section>";
        echo "<h3>Ganador de la Carrera</h3>";
        echo "<p>Piloto: " . $circuito->vencedor . "</p>";
        echo "<p>Tiempo: " . $circuito->tiempo_carrera . "</p>";
        echo "</section>";
        echo "<section>";
        echo "<h3>Clasificación Del Mundial Después de la Carrera</h3>";
        echo "<ol>
        <li>".$circuito->clasificacion->piloto[0]."</li>
        <li>".$circuito->clasificacion->piloto[1]."</li>
        <li>".$circuito->clasificacion->piloto[2]."</li>
        </ol>";
        echo "</section>";
    ?>
</body>
</html>