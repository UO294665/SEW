class Circuito{
    constructor(){
        this.comprobarApiFile();
    }

    comprobarApiFile(){
        const soportado = window.File && window.FileReader && window.FileList && window.Blob;

        if (!soportado) {
            document.write('La API File no es soportada en este navegador.');
        }
    }

    leerArchivoHTML(){
        var archivo = "/xml/infoCircuito.html";
        var tipoHTML = /\.html$/i;
        if(archivo.type.match(tipoHTML)){
            var lector = new FileReader();
            var self = this;
            lector.onload = function(e) {
                var contenido = e.target.result;
            };
            lector.readAsText(archivo);
        } else{
            document.write("Por favor, selecciona un archivo HTML.");
        }
    }


}

class CargadorSVG{
    constructor(){
        var input = document.querySelectorAll("input[type='file']");
        input[0].addEventListener('change', (event) => {
            this.leerArchivoSVG(event.target.files);
        });
    }
    leerArchivoSVG(files){
        const archivo = files[0];
        const tipoSVG = /\.svg$/i;
         if(tipoSVG.test(archivo.name)){
            var lector = new FileReader();
            var self = this;
            
            lector.onload =  function(e) {
                self.insertarSVG(e.target.result);
            };
            lector.readAsText(archivo);
        } else{
            document.write("Por favor, selecciona un archivo KML.");
        }
    }

    insertarSVG(contenido){
        const parser = new DOMParser();
        const documentoSVG = parser.parseFromString(contenido, "image/svg+xml");
        const elementoSVG = documentoSVG.documentElement;
        $('body > main').append(elementoSVG);
    }
}

class CargadorKML{
    constructor(){
        var input = document.querySelectorAll("input[type='file']");
        input[1].addEventListener('change', (event) => {
            this.leerArchivoKML(event.target.files);
        });
    }
    leerArchivoKML(files){
        const archivo = files[0];
        const tipoKML = /\.kml$/i;
        if(tipoKML.test(archivo.name)){
            var lector = new FileReader();
            var self = this;
            
            lector.onload =  function(e) {

                const textoKML = $.parseXML(lector.result);
                var coordArray = $("Placemark coordinates", textoKML).text().trim().split(/\s+/);

                var coordenadas = [];

                for (var i = 0; i < coordArray.length; i++) {
                    var partes = coordArray[i].split(",");
                    coordenadas.push([parseFloat(partes[0]), parseFloat(partes[1]), parseFloat(partes[2])]);
                }

                self.insertarCapaKML(coordenadas);
            };
            lector.readAsText(archivo);
        } else{
            document.write("Por favor, selecciona un archivo KML.");
        }
    }
    insertarCapaKML(datos){
        $('<div></div>').appendTo('body > main');
        var contenedor = $('body > main > div')[0];
        var origen = new google.maps.LatLng(datos[0][1], datos[0][0])
        var mapa = new google.maps.Map(contenedor, {
            zoom: 15,
            center: origen
        });

        var listaCoordenadas = [];
        var origenMarcador = new google.maps.Marker({
            position: origen,
            map: mapa,
            title: 'Origen'
        });

        listaCoordenadas.push(origen);
        
        for (var i = 0; i < datos.length; i++) {
            listaCoordenadas.push(new google.maps.LatLng(datos[i][1], datos[i][0]));
        }

        var polyline = new google.maps.Polyline({
            path: listaCoordenadas,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 4
        });

        polyline.setMap(mapa);

    }
}