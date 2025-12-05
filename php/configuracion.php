<?php
    class Configuracion {
        private $servername = "localhost";
        private $username = "DBUSER2025";
        private $password = "DBPSWD2025";
        private $dbname = "uo294665_db";
        private $db = null;

        private function openConnection(){
            $this->db = new mysqli($this->servername, $this->username, $this->password, $this->dbname);
            if($this->db->connect_error) {
                exit ("<p>ERROR de conexión: ".$this->db->connect_error."</p>");  
            }
        }

        private function closeConnection(){
        if($this->db !== null) {
            $this->db->close();
            $this->db = null;
            }
        }

        public function reiniciar() {
            $this->openConnection();
            
            $this->db->query("DELETE FROM observaciones");
            $this->db->query("DELETE FROM resultados");
            $this->db->query("DELETE FROM usuario");
            
            $this->closeConnection();
        }

        public function eliminar() {
            $this->openConnection();
            
            $consulta = "DROP DATABASE uo294665_db";
            $this->db->query($consulta);
            
            $this->closeConnection();
        }

        public function exportar() {
            $this->openConnection();
            
            $nombreArchivo = "resultados.csv";

            header('Content-Type: text/csv; charset=utf-8');
            header('Content-Disposition: attachment; filename="' . $nombreArchivo . '"');

            $output = fopen('php://output', 'w');

            $resultado = $this->db->query("SELECT * FROM resultados");

            if ($resultado->num_rows > 0) {
                // Escribir encabezados
                $primeraFila = $resultado->fetch_assoc();
                fputcsv($output, array_keys($primeraFila), ';');

                // Escribir primera fila
                fputcsv($output, $primeraFila, ';');

                // Escribir resto
                while ($fila = $resultado->fetch_assoc()) {
                    fputcsv($output, $fila, ';');
                }
            }

            fclose($output);
            
            $this->closeConnection();
        }
    }

    $conf = new Configuracion();

    if (isset($_POST["reiniciar"])) {
        $conf->reiniciar();
    }

    if (isset($_POST["eliminar"])) {
        $conf->eliminar();
    }

    if (isset($_POST["exportar"])) {
        $conf->exportar();
    }
?>
<!DOCTYPE html>
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
    <form action='#' method='post'>
        <button type='submit' name='reiniciar'>Reiniciar Base de Datos</button>
        <button type='submit' name='eliminar'>Eliminar Base de Datos</button>
        <button type='submit' name='exportar'>Exportar datos en formato CSV</button>
    </form>
</body>