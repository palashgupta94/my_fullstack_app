import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormComponent } from './components/form/form.component';
import { ResponseComponent } from './components/response/response.component';
import {GetUsersMappingComponent} from './components/get-users-mapping/get-users-mapping.component';

const routes: Routes = [
  {path: "", component: GetUsersMappingComponent},
  { path: "add", component: FormComponent },
  { path: "response", component: ResponseComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
