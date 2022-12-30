import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { DataService } from 'src/app/shared/services/data.service';
import { ApiService } from '../../shared/services/api.service';
import { ImageService } from '../../shared/services/image.service';
import { RequestImage } from 'src/app/shared/models/api.model';
import { ERROR_API, ERROR_FILE_NOT_IMAGE, ERROR_IMAGE_FROM_URL } from 'src/app/shared/constants';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(private router: Router, private dataService: DataService, private apiService: ApiService, private imageService: ImageService) { }

  ngOnInit(): void {
  }

  private postImage(image: ArrayBuffer, filename: string, url?: string): void {
    const body: RequestImage = { image, filename, url };
    this.dataService.requestImage = body;
    this.apiService.postImage(body).subscribe({
      next: response => {
        this.dataService.responseImage = response;
        this.dataService.hideLoader();
        this.router.navigateByUrl('result');
      },
      error: () => {
        this.dataService.hideLoader();
        this.dataService.addError(ERROR_API);
      },
    });
  }

  onUrl(url: string): void {
    this.dataService.showLoader();
    this.imageService.getImageFromUrl(url).then(image => {
      this.postImage(image, url.split('/').pop() as string, url);
    }).catch(() => {
      this.dataService.hideLoader();
      this.dataService.addError(ERROR_IMAGE_FROM_URL);
    });
  }

  onFiles(files: File[]): void {
    if (files.length < 1 || files[0].type.split('/')[0] !== 'image') {
      this.dataService.addError(ERROR_FILE_NOT_IMAGE);
      return;
    }

    this.dataService.showLoader();
    this.imageService.getImageFromFile(files[0]).then(image => {
      this.postImage(image, files[0].name);
    }).catch(() => {
      this.dataService.hideLoader();
      this.dataService.addError(ERROR_IMAGE_FROM_URL);
    });
  }
}
