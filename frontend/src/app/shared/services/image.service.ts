import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  constructor(private http: HttpClient) { }

  async getImageFromUrl(url: string): Promise<ArrayBuffer> {
    return new Promise((resolve, reject) => {
      this.http.get(url, { responseType: 'blob' }).subscribe({
        next: data => { resolve(this.getImageFromFile(data)) },
        error: () => { reject(null) },
      });
    });
  }

  async getImageFromFile(file: Blob): Promise<ArrayBuffer> {
    return new Promise((resolve, reject) => {
      let reader = new FileReader();
      reader.onload = () => { resolve(reader.result as ArrayBuffer) };
      reader.onerror = () => { reject(null) };
      reader.readAsArrayBuffer(file);
    });
  }
}
