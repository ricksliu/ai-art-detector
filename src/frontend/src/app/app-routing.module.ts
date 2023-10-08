import { Observable } from 'rxjs';
import { NgModule, Injectable } from '@angular/core';
import { RouterModule, Routes, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router, UrlTree } from '@angular/router';

import { HomeComponent } from "./components/home/home.component";
import { ResultComponent } from "./components/result/result.component";

@Injectable({ providedIn: 'root' })
class PreventDirectNavigationGuard implements CanActivate {
  constructor(private router: Router) { }
  canActivate(): boolean {
    if (!this.router.navigated) {
      this.router.navigateByUrl('home');
      return false;
    }
    return true;
  }
}

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'result', component: ResultComponent, canActivate: [PreventDirectNavigationGuard] },
  { path: '', redirectTo: 'home', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
