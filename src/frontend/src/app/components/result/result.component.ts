import { Component, OnInit } from '@angular/core';

import { DataService } from '../../shared/services/data.service';
import { ImageRequest, ImageResponse } from 'src/app/shared/models/api.model';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss']
})
export class ResultComponent implements OnInit {

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
  }

  confidence(): number {
    if (typeof this.dataService.imageResponse?.model_prediction === 'undefined') {
      return 0;
    }
    if (this.dataService.imageResponse?.model_is_ai_generated) {
      return Math.floor(200 * (this.dataService.imageResponse?.model_prediction - 0.5));
    }
    return Math.floor(200 * (0.5 - this.dataService.imageResponse?.model_prediction));
  }

  imageRequest(): ImageRequest | undefined {
    return this.dataService.imageRequest;
  }

  imageResponse(): ImageResponse | undefined {
    return this.dataService.imageResponse;
  }
}
