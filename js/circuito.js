class Circuito{
    constructor(){
        this.comprobarApiFile();
    }

    comprobarApiFile(){
        const soportado = window.File && window.FileReader && window.FileList && window.Blob;

        if (!soportado) {
            alert('La API File no es soportada en este navegador.');
        }
    }

    leerArchivoHTML(){
        var archivo = "/xml/infoCircuito.html";
        var tipoHTML = /\.html$/i;
        if(archivo.type.match(tipoHTML)){
            var lector = new FileReader();
            lector.onload = function(e) {
                var contenido = lector.result;
            };
            lector.readAsText(archivo);
        } else{
            alert("Por favor, selecciona un archivo HTML.");
        }
    }


}

class CargadorSVG{
    constructor(){
        $("input[type='file']").addEventListener('change', this.leerArchivoSVG(this.files).bind(this), false);
    }
    leerArchivoSVG(files){
        const archivo = files[0];
        const tipoSVG = /\.svg$/i;
        if(archivo.type.match(tipoSVG)){
            const lector = new FileReader();
            lector.onload = (e) => {
                const contenido = lector.result;
                this.insertarSVG(contenido);
            };
            lector.readAsText(archivo);
        } else{
            alert("Por favor, selecciona un archivo SVG.");
        }
    }

    insertarSVG(contenido){
        const $section = $("<section></section>");
        $section.html(contenido);
        $('body > main').append($section);
    }
}

class CargadorKML{
    constructor(){
        $("input[type='file']").addEventListener('change', this.leerArchivoKML(this.files).bind(this), false);
    }
    leerArchivoKML(files){
        const archivo = files[0];
        const tipoKML = /\.kml$/i;
        if(archivo.type.match(tipoKML)){
            const lector = new FileReader();
            lector.onload = (e) => {
                const contenido = lector.result;
                this.insertarCapaKML(contenido);
            };
            lector.readAsText(archivo);
        } else{
            alert("Por favor, selecciona un archivo KML.");
        }
    }
    insertarCapaKML(){

    }
}