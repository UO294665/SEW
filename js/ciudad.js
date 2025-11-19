class Ciudad {
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio= gentilicio;
    }

    rellenar(){
        this.poblacion = 384.244;
        this.coordenadas = {latitud: 2.6947, longitud: 101.7505};
    }

    getNombre(){
        return this.nombre;
    }

    getPais(){
        return this.pais;
    }

    getInfo(){
        return "<ul><li>"+this.gentilicio+"</li><li>Población: "+this.población+"</li></ul>";
    }

    escribirCoordenadas(){
        const mensaje = document.createElement("p");
        mensaje.textContent = "Coordenadas: "+this.coordenadas.latitud+","+this.coordenadas.longitud;
        document.querySelector("main").appendChild(mensaje);

    }

    getMeteorologiaCarrera(){
        $.ajax({
            dataType: "json",
            url: "https://archive-api.open-meteo.com/v1/archive?latitude=2.76056&longitude=101.73750&start_date=2025-10-26&end_date=2025-10-26&hourly=temperature_2m,apparent_temperature,precipitation,relative_humidity_2m,windspeed_10m,winddirection_10m&daily=sunrise,sunset&timezone=Asia/Kuala_Lumpur",
            method: "GET",
            success: (data) => {
                this.procesarJSONCarrera(data);
                this.getMeteorologiaEntrenos();
            }
        });
    }

    procesarJSONCarrera(data){
        this.temperatura_2m = data.hourly.temperature_2m[10];
        this.sensacion_termica = data.hourly.apparent_temperature[10];
        this.lluvia = data.hourly.precipitation[10];
        this.humedad_2m = data.hourly.relative_humidity_2m[10];
        this.viento_10m = data.hourly.windspeed_10m[10];
        this.viento_direccion_10m = data.hourly.winddirection_10m[10];
        this.salida_sol = data.daily.sunrise[0];
        this.puesta_sol = data.daily.sunset[0];

        this.mostrarMeteorologia();
        
    }

    mostrarMeteorologia() {
        const $section = $("<section></section>");
        const $titulo = $("<h3>Condiciones meteorológicas – Sepang (26/10/2025)</h3>");

        const $lista = $(`
            <ul>
                <li>Temperatura (2 m): ${this.temperatura_2m} °C</li>
                <li>Sensación térmica: ${this.sensacion_termica} °C</li>
                <li>Lluvia: ${this.lluvia} mm</li>
                <li>Humedad relativa (2 m): ${this.humedad_2m} %</li>
                <li>Velocidad del viento (10 m): ${this.viento_10m} km/h</li>
                <li>Dirección del viento (10 m): ${this.viento_direccion_10m}°</li>
                <li>Salida del sol: ${this.salida_sol}</li>
                <li>Puesta del sol: ${this.puesta_sol}</li>
            </ul>
        `);

        $section.append($titulo);
        $titulo.after($lista)
        $("body > main").append($section);
    }

    getMeteorologiaEntrenos(){
        $.ajax({
            url: "https://archive-api.open-meteo.com/v1/archive?latitude=2.76056&longitude=101.73750&start_date=2025-10-23&end_date=2025-10-25&hourly=temperature_2m,precipitation,relative_humidity_2m,windspeed_10m",
            method: "GET",
            success: (data) => {
                this.procesarJSONEntrenos(data);
            }
        })
    }

    procesarJSONEntrenos(data){

        this.temperatura_2m_entreno1 = data.hourly.temperature_2m[10];
        this.temperatura_2m_entreno2 = data.hourly.temperature_2m[10 + 24];
        this.temperatura_2m_entreno3 = data.hourly.temperature_2m[10 + 48];
        this.temperatura_2m_media = Math.round(
            (this.temperatura_2m_entreno1 + this.temperatura_2m_entreno2 + this.temperatura_2m_entreno3) / 3 * 100
        ) / 100;

        this.lluvia_entreno1 = data.hourly.precipitation[10];
        this.lluvia_entreno2 = data.hourly.precipitation[10 + 24];
        this.lluvia_entreno3 = data.hourly.precipitation[10 + 48];
        this.lluvia_media = Math.round(
            (this.lluvia_entreno1 + this.lluvia_entreno2 + this.lluvia_entreno3) / 3 * 100
        ) / 100;

        this.humedad_2m_entreno1 = data.hourly.relative_humidity_2m[10];
        this.humedad_2m_entreno2 = data.hourly.relative_humidity_2m[10 + 24];
        this.humedad_2m_entreno3 = data.hourly.relative_humidity_2m[10 + 48];
        this.humedad_2m_media = Math.round(
            (this.humedad_2m_entreno1 + this.humedad_2m_entreno2 + this.humedad_2m_entreno3) / 3 * 100
        ) / 100;

        this.viento_10m_entreno1 = data.hourly.windspeed_10m[10];
        this.viento_10m_entreno2 = data.hourly.windspeed_10m[10 + 24];
        this.viento_10m_entreno3 = data.hourly.windspeed_10m[10 + 48];
        this.viento_10m_media = Math.round(
            (this.viento_10m_entreno1 + this.viento_10m_entreno2 + this.viento_10m_entreno3) / 3 * 100
        ) / 100;

        this.mostrarMeteorologiaEntrenos();
    }

    mostrarMeteorologiaEntrenos() {
        const $section = $("<section></section>");
        const $titulo = $("<h3>Condiciones meteorológicas de los entrenos – Sepang (23/10/2025) - (25/10/2025)</h3>");

        const $lista = $(`
            <ul>
                <li>Temperatura media (2 m): ${this.temperatura_2m_media} °C</li>
                <li>Lluvia media: ${this.lluvia_media} mm</li>
                <li>Humedad media (2 m): ${this.humedad_2m_media} %</li>
                <li>Velocidad media del viento (10 m): ${this.viento_10m_media} km/h</li>
            </ul>
        `);

        $section.append($titulo);
        $titulo.after($lista);
        $("body > main > section").after($section);
    }
}

let ciudad = new Ciudad("Sepang", "Malasia", "Selangoriano");

const pais = document.createElement("p");
pais.textContent = "País: "+ciudad.getPais();
document.querySelector("main").appendChild(pais);

const nombre = document.createElement("p");
nombre.textContent = "Ciudad: "+ciudad.getNombre();
document.querySelector("main").appendChild(nombre);

ciudad.rellenar();
ciudad.escribirCoordenadas();

document.querySelector("main").insertAdjacentHTML('beforeend',ciudad.getInfo());
ciudad.getMeteorologiaCarrera();