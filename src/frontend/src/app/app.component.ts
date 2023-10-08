import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { DataService } from './shared/services/data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'AI Art Detector';

  constructor(private router: Router, private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.clear();
  }

  showNav(): boolean {
    return this.router.url !== '/home';
  }

  onNavBack(): void {
    this.router.navigateByUrl('home');
  }

  showLoader(): boolean {
    return this.dataService.loader;
  }

  errors(): string[] {
    return this.dataService.errors;
  }

  onCloseError(i: number): void {
    this.dataService.errors.splice(i, 1);
  }
}
