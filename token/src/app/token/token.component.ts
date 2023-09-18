import { Component, OnInit } from '@angular/core';
import { interval } from 'rxjs';
import { takeWhile } from 'rxjs/operators';
import { RegistroService } from '../servicios/registro.service'

@Component({
  selector: 'app-token',
  templateUrl: './token.component.html',
  styleUrls: ['./token.component.css'],
  providers: [RegistroService],
})
export class TokenComponent {
  
  tokenNumber!: string;
  tokenExpiry!: string;
  counter: number = 0; // Número inicial de segundos
  isCounting: boolean = true; // Variable para controlar la visibilidad

  constructor(private registroService: RegistroService) { }
 
  
  
  ngOnInit(): void {
    this.registroService.obtenerRegistros().subscribe(
      data =>{
      console.log("data: ",data);

    });

    const min = 100000;
    const max = 999999;
    // Crea un observable que emite un valor cada segundo
    const source = interval(600);
    // this.tokenNumber=this.generateRandomToken();
    this.tokenNumber = this.generateRandomToken();
   
    
    // Usa takeWhile para detener el contador cuando llegue a cero
    source.pipe(
      takeWhile(() => this.counter < 100)
    ).subscribe(() => {
      this.counter++;
      while (this.counter === 100) {
        this.counter = 0;
        this.tokenNumber = this.generateRandomToken();
        let bodyToken ={
          "token" : this.tokenNumber,
          "usuario" : "User"
        }
        this.registroService.enviarRegistros(bodyToken).subscribe(
          data =>{
          console.log("bodyToken: ",data);
    
        });
      }
    });
  }



  generateRandomToken() {
    const min = 100000;
    const max = 999999;
    let token = "";
    // Genera un número aleatorio entre 100000 y 999999 (ambos inclusive)
    const randomNumber = Math.floor(Math.random() * (max - min + 1)) + min;
    // Convierte el número aleatorio en una cadena de 6 dígitos (agregando ceros a la izquierda si es necesario)
    token = randomNumber.toString().padStart(6, '0');

    return token;
  }




}
