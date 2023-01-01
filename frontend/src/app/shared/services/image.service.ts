import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { ImageRequest } from '../models/api.model';

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  constructor(private http: HttpClient) { }

  async getImageFromUrl(url: string): Promise<ImageRequest> {
    return new Promise((resolve, reject) => {
      this.http.get(url, { responseType: 'blob' }).subscribe({
        next: blob => { resolve(this.getImageFromBlob(blob, url.split('/').pop() as string, url)) },
        error: () => { reject() },
      });
    });
  }

  async getImageFromBlob(blob: Blob, filename: string, url?: string): Promise<ImageRequest> {
    return new Promise((resolve, reject) => {
      const imageElem = new Image();
      imageElem.onload = () => {
        let reader = new FileReader();
        reader.onload = () => {
          const image: ImageRequest = {
            filename: filename,
            url: url,
            image: reader.result as string,
            size: blob.size,
            type: blob.type.split('/')[1],
            width: imageElem.width,
            height: imageElem.height,
          }
          resolve(image);
        };
        reader.onerror = () => { reject() };
        reader.readAsDataURL(blob);
      };
      imageElem.onerror = () => { reject() };
      imageElem.src = URL.createObjectURL(blob);
    });
  }
}
