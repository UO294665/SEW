<?php
if (count($_POST)>0) 
    {   
        $formularioPOST  = $_POST;

        // Comprueba que el nombre no está en blanco
        if($_POST["nombre"] == ""){
            $errorNombre = " * El nombre es obligatorio ";
            $errorFormulario = true;
        }

        // Comprueba que los apellidos no están en blanco
        if($_POST["apellidos"] == ""){
             $errorApellidos = " * Los apellidos son obligatorios";
             $errorFormulario = true;
        }

        // Comprueba que se ha elegido el género
        if (empty($_POST["genero"])) {
            $errorGenero = " * El género es obligatorio";
            $errorFormulario = true;
        } 

        // Comprueba que el e-mail es válido
        if(filter_var($_POST["e-mail"], FILTER_VALIDATE_EMAIL) === false){
            $errorEmail = " * e-mail no válido";
            $errorFormulario = true;
        }
    }
echo"
    <form action='#' method='post' name='formulario'>
            <p>Nombre</p> 
            <p>
                <input type='text' name='nombre'/>
                <span>" . $errorNombre . "</span>
            </p>
            <p>Apellidos</p>
            <p>
                <input type='text' name='apellidos'/>
                <span>" . $errorApellidos . "</span>
            </p>
            <p>Género</p>
            <p>
                <input type='radio' name='genero' value='Hombre'/>Hombre
                <input type='radio' name='genero' value='Mujer'/>Mujer
                <input type='radio' name='genero' value='Otros'/>Otros
                <span>" . $errorGenero . "</span>             
            </p>
            <p>e-mail</p>
            <p>
                <input type='email' name='e-mail'/>
                <span>" . $errorEmail . "</span>
            </p>
            <p>Pais <select name='opcion'>
                <option value='ES'>España</option>
                <option value='CO'>Colombia</option>
                <option value='PE'>Perú</option>
                <option value='MX'>México</option>
                <option value='AR'>Argentina</option>
                </select></p>
            <p>Commentario</p>
            <p>
                <textarea name='commentario' rows='5' cols='40'>
                </textarea>
            </p>
            <p>
                <input type='submit' value='Enviar'/>
            </p>
        </form>
";
?>