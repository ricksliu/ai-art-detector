import { Component, OnInit } from '@angular/core';

import { ApiService } from '../../shared/services/api.service';
import { ImageService } from '../../shared/services/image.service';
import { RequestImage } from '../../shared/models/api.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(private apiService: ApiService, private imageService: ImageService) { }

  ngOnInit(): void {
  }

  postImage(image: ArrayBuffer, filename: string, url?: string): void {
    this.apiService.postImage(image, filename, url).subscribe({
      next: data => { console.log('data', data) },
      error: error => { console.log('error', error) },
    });
  }

  onUrl(url: string) {
    this.imageService.getImageFromUrl(url).then(image => {
      this.postImage(image, url.split('/').pop() as string, url);
    });
  }

  onFiles(files: File[]) {
    this.imageService.getImageFromFile(files[0]).then(image => {
      this.postImage(image, files[0].name);
    });
  }
}
