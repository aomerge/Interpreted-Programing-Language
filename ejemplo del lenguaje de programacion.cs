// diseño de mi lenguaje de programacion
caracteristicas: 
- es un lenguaje de programacion orientado a objetos

uso del lenguaje:
- se utiliza para practicar en timepo real la programacion orientada a objetos de una manera didactica y sencilla para el usuario.
ejemplo: 

Codigo:
``` .cssx
---
    class Persona {    
        //metodos
        public Persona(){
            const nombre: string = "Juan";
            let edad: init = 18;
            print("Hola, mi nombre es "+nombre+" y tengo "+edad+" años");
        }
    }
    class car{
        public vars : string;
        //metodos
        public car(){
            const marca: string = "Nissan";
            let modelo: init = 2020;
            print("Hola, mi carro es un "+marca+" y es modelo "+modelo);
        }
    }

    //funcion principal
    // por defecto el namespace es main
    // los namespace no se pueden repetir
    // una vez añadido un namespace solo pude correr elementos de ese namespace
    class main extends Persona, car{
        public couter: init = 0;
        //metodos
        // esto es un constructor 
        public main( name: string,   ){}
        public element(){
            // para correr coddigo html dentro de astro se debe de hacer de la siguiente manera
            return (
                <div>
                    <h1>hola mundo</h1>
                    // con las {} dentro de un ^^ se pude correr codigo astro y hacer uso de la classe y los elementos que extiendan de ella
                    // para correr codigo astro dentro de otro codigo astro se debe de hacer de la siguiente manera
                    // el codigo que este dentro de los {} devolvera por pantalla el resultado de la funcion, variable, clase o elemento que se este llamando.
                    // en caso de que la variable 
                    {
                        this.couter = this.couter + 1;
                    }
                </div>
            );
        }
    }
---
    // Para poder correr el codigo es necesario que ejecutes document y dentro de run.
    // como en el ejemplo siguiente:
    <document>
        <run element=true states={
            "name": "Juan",
            "edad": 18
        } Class=Persona />
        <run element=true states={
            "marca": "Nissan",
            "modelo": 2020
        } Class=car />
        <run href='./main/hooks' />
    </document>

    // En el uso de otros archivos se puede utilizar el namespace por defecto 
    // o crear un namespace nuevo.
    ###./main/hooks.cssx
    ---
        class Persona{    
            //metodos
            public main(){
                const nombre: string = "Juan";
                let edad: init = 18;
                print("Hola, mi nombre es "+nombre+" y tengo "+edad+" años");
            }
        }
        class main{
            //metodos
            public main(){
                const persona = new Persona();                
            }
        }

        ## en el caso de que quieras crear un name space seria de la sigiene manera:
        class main namespace Persona{
            //metodos
            public main(){
                const persona = new Persona();
                persona.main();
            }
        }
        class Persona namespace Persona{{    
            //metodos
            // esto es un constructor
            // los constructores no pueden ser llamados desde otro lado
            // para definir un constructor se debe de llamar igual que la clase
            public Persona(){
                const nombre: string = "Juan";
                let edad: init = 18;
                print("Hola, mi nombre es "+nombre+" y tengo "+edad+" años");
            }
        }
            
``