import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormComponent } from './components/form/form.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ResponseComponent } from './components/response/response.component';
import {GetUsersMappingComponent} from './components/get-users-mapping/get-users-mapping.component';
import {MatIcon} from '@angular/material/icon';
import {CommonModule} from '@angular/common';
import { UpdateUserComponent } from './components/update-user/update-user.component';
import { DeleteUserComponent } from './components/delete-user/delete-user.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { ShowUserComponent } from './components/show-user/show-user.component';

@NgModule({
  declarations: [
    AppComponent,
    FormComponent,
    ResponseComponent,
    GetUsersMappingComponent,
    UpdateUserComponent,
    DeleteUserComponent,
    ShowUserComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatIcon,
    CommonModule,
    BrowserAnimationsModule
  ],
  providers: [ ApiService ],
  bootstrap: [AppComponent]
})
export class AppModule { }
