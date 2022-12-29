import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { API_URL } from '../constants';
import { RequestImage } from '../models/api.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  postImage(image: ArrayBuffer, filename: string, url?: string): Observable<RequestImage> {
    const body: RequestImage = { image, filename, url };
    return this.http.post<RequestImage>(API_URL + 'images/', body);
  }
}
