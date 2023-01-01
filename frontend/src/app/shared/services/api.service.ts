import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { API_URL } from '../constants';
import { ImageRequest, ImageResponse } from '../models/api.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  postImage(body: ImageRequest): Observable<ImageResponse> {
    return this.http.post<ImageResponse>(API_URL + 'images/', body);
  }
}
