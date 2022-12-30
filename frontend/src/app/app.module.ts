import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from "@angular/common/http";

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { FileInputComponent } from './shared/components/file-input/file-input.component';
import { TextInputComponent } from './shared/components/text-input/text-input.component';
import { LoaderComponent } from './shared/components/loader/loader.component';
import { ResultComponent } from './components/result/result.component';
import { ToastComponent } from './shared/components/toast/toast.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    FileInputComponent,
    TextInputComponent,
    LoaderComponent,
    ResultComponent,
    ToastComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
