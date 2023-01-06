import { Injectable } from '@angular/core';

import { ImageRequest, ImageResponse } from '../models/api.model';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  loader = false;
  errors: string[] = [];
  imageRequest?: ImageRequest;
  imageResponse?: ImageResponse;

  constructor() { }

  clear(): void {
    this.loader = false;
    this.errors = [];
    this.imageRequest = undefined;
    this.imageResponse = undefined;
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
