class Memoria {
    constructor() {
        this.tablero_bloqueado = true;
        this.primera_carta = null;
        this.segunda_carta = null;
        this.barajarCartas();
        this.tablero_bloqueado = false;

        this.cronometro = new Cronometro();
        this.cronometro.arrancar();
    }

    voltearCarta(carta) {
        if(!(this.tablero_bloqueado || carta.getAttribute("data-state") === "flip" || carta.getAttribute("data-state") === "revelada")){
            
            carta.setAttribute("data-state", "flip");
            if(this.primera_carta === null){
                this.primera_carta = carta;
                return;
            }
            this.segunda_carta = carta;
            if(this.comprobarPareja()){
                this.deshabilitarCartas();
            }else{
                this.cubrirCartas();
            }
        }
        
    }

    barajarCartas() {
        const main = document.querySelector("main");

        const cartasArray = Array.from(main.querySelectorAll("article"));

        for(let i = 0; i < cartasArray.length; i++) {
            let aux = cartasArray[i];
            aux.addEventListener("click", () => this.voltearCarta(aux));
        }

        for (let i = cartasArray.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cartasArray[i], cartasArray[j]] = [cartasArray[j], cartasArray[i]];
        }

        for (let i = 0; i < cartasArray.length; i++) {
            main.appendChild(cartasArray[i]);
        }
    }

    reiniciarAtributos(){
        this.tablero_bloqueado = true;
        this.primera_carta = null;
        this.segunda_carta = null;
    }

    deshabilitarCartas(){
        this.primera_carta.setAttribute("data-state", "revelada");
        this.segunda_carta.setAttribute("data-state", "revelada");
        this.reiniciarAtributos();
        if(this.comprobarJuego()){
            this.cronometro.parar();
        }else{
            this.tablero_bloqueado = false;
        }
    }

    comprobarJuego(){
        const main = document.querySelector("main");

        const cartas = Array.from(main.querySelectorAll("article"));

        for(let i = 0 ; i < cartas.length ; i++) {
            if(cartas[i].getAttribute("data-state") != "revelada"){
                return false;
            }
        }
        return true;
    }

    cubrirCartas(){
        this.tablero_bloqueado = true;
        setTimeout(() => {
            this.primera_carta.setAttribute("data-state", "");
            this.segunda_carta.setAttribute("data-state", "");
            this.reiniciarAtributos();
            this.tablero_bloqueado = false;
        }, 1500);

    }

    comprobarPareja(){
        let img1 = this.primera_carta.querySelector("img").getAttribute("src");
        let img2 = this.segunda_carta.querySelector("img").getAttribute("src");

        return img1 === img2 ? true : false;
    }
}