import { Injectable } from '@angular/core';

import { ImageRequest, ImageResponse } from '../models/api.model';

/** Service for handling the app state. */
@Injectable({
  providedIn: 'root'
})
export class DataService {
  loader = false;
  errors: string[] = [];
  imageRequest?: ImageRequest;
  imageResponse?: ImageResponse;

  constructor() { }

  /** Clears the app state. */
  clear(): void {
    this.loader = false;
    this.errors = [];
    this.imageRequest = undefined;
    this.imageResponse = undefined;
  }

  /** Shows the loader. */
  showLoader(): void {
    this.loader = true;
  }

  /** Hides the loader. */
  hideLoader(): void {
    this.loader = false;
  }

  /** Pushes a new error to the list of errors displayed. */
  addError(error: string): void {
    this.errors.push(error);
  }
}
