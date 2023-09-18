import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TokenComponent } from './token/token.component';
import { MainComponent } from './main/main.component';
import { TablaComponent } from './tabla/tabla.component';

const routes: Routes = [
  { path: "token", component: TokenComponent },
  { path: "main", component: MainComponent },
  { path: "tabla", component: TablaComponent },
  { path: "**", redirectTo: "main" },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
