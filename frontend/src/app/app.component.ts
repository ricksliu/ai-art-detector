import { Component } from '@angular/core';

import { DataService } from './shared/services/data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'AI Art Detector';

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.clear();
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
