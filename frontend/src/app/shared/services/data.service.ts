import { Injectable } from '@angular/core';

import { RequestImage } from '../models/api.model';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  loader = false;
  errors: string[] = [];
  requestImage?: RequestImage;
  responseImage?: RequestImage;

  constructor() { }

  clear(): void {
    this.loader = false;
    this.errors = [];
    this.requestImage = undefined;
    this.responseImage = undefined;
  }

  showLoader(): void {
    this.loader = true;
  }

  hideLoader(): void {
    this.loader = false;
  }

  addError(error: string): void {
    this.errors.push(error);
  }
}
