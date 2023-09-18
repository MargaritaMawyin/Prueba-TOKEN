import { Component } from '@angular/core';
import { RegistroService } from '../servicios/registro.service';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-tabla',
  templateUrl: './tabla.component.html',
  styleUrls: ['./tabla.component.css']
})
export class TablaComponent {


  constructor(private registroService: RegistroService) { }


  displayedColumns: string[] = ['id', 'token', 'usuario'];
  dataSource = [];
  usuarios: any = [];
  selected: any = { usuario: 'User' };
  nada = false;

  mostrarPorUser() {
    this.registroService.obtenerRegistrosPorUsuario(this.selected.usuario).subscribe(
      data => {
        if (this.selected != undefined) {
          console.log(this.selected)
          console.log(data.registros)
          console.log(Object.values(data.registros))
          if (this.dataSource != null) {
            this.dataSource = Object.values(data.registros) as any
          }
          if (this.dataSource != null) {
            this.nada = true;
          }
          // console.log(this.dataSource)
        }
      });
  }

  ngOnInit(): void {
    this.registroService.obtenerRegistros().subscribe(
      data => {
        this.dataSource = data.registros;
        this.usuarios = data.registros;
        console.log("data: ", data.registros);

      });
  }
}
