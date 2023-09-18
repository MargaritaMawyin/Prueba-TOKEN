import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { EnviarToken } from '../interfaces/enviar-token';

@Injectable({
  providedIn: 'root'
})
export class RegistroService {

  constructor(private http: HttpClient) { }


  obtenerRegistros():Observable<any> {
    return this.http.get('http://127.0.0.1:8000/myapp/token/')
  }

  obtenerRegistrosPorUsuario(user:string):Observable<any> {
    return this.http.get('http://127.0.0.1:8000/myapp/token/'+user)
  }

  enviarRegistros(body:EnviarToken) {
    return this.http.post('http://127.0.0.1:8000/myapp/token/',body)
  }
}
