import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { DataService } from 'src/app/shared/services/data.service';
import { ApiService } from '../../shared/services/api.service';
import { ImageService } from '../../shared/services/image.service';
import { ImageRequest } from 'src/app/shared/models/api.model';
import { ERROR_API, ERROR_FILE_NOT_IMAGE, ERROR_IMAGE_FROM_URL } from 'src/app/shared/constants';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(private router: Router, private dataService: DataService, private apiService: ApiService, private imageService: ImageService) { }

  ngOnInit(): void {
    this.dataService.clear();
  }

  private postImage(image: ImageRequest): void {
    this.dataService.imageRequest = image;
    this.apiService.postImage(image).subscribe({
      next: response => {
        this.dataService.imageResponse = response;
        this.dataService.hideLoader();
        this.router.navigateByUrl('result');
      },
      error: () => {
        this.dataService.imageRequest = undefined;
        this.dataService.hideLoader();
        this.dataService.addError(ERROR_API);
      },
    });
  }

  onUrl(url: string): void {
    this.dataService.showLoader();
    this.imageService.getImageFromUrl(url).then(image => {
      this.postImage(image);
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
    this.imageService.getImageFromBlob(files[0], files[0].name).then(image => {
      this.postImage(image);
    }).catch(() => {
      this.dataService.hideLoader();
      this.dataService.addError(ERROR_IMAGE_FROM_URL);
    });
  }
}
