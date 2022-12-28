import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

import { API_URL } from '../constants';
import { RequestImage } from '../models/api.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  postImage(): Observable<RequestImage> {
    let body: RequestImage =  {
      image: '',
      filename: 'test.jpg',
      url: undefined,
    };
    return this.http.post<RequestImage>(API_URL + 'images/', body);
  }
}
