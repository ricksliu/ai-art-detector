import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { API_URL } from '../constants';
import { ImageRequest, ImageResponse } from '../models/api.model';

/** Service for handling the backend API. */
@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  /**
   * Posts an `ImageRequest` to the API to get a prediction.
   * @param body - The `ImageRequest` to get a prediction of.
   * @returns The API's prediction of the `ImageRequest`.
   */
  postImage(body: ImageRequest): Observable<ImageResponse> {
    return this.http.post<ImageResponse>(API_URL + 'images/', body);
  }
}
