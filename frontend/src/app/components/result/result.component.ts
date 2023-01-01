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
    if (typeof this.dataService.imageResponse?.model_target === 'undefined') {
      return 0;
    }
    if (this.dataService.imageResponse?.model_is_ai_generated) {
      return Math.floor(100 * this.dataService.imageResponse?.model_target);
    }
    return Math.floor(100 - 100 * this.dataService.imageResponse?.model_target);
  }

  imageRequest(): ImageRequest | undefined {
    return this.dataService.imageRequest;
  }

  imageResponse(): ImageResponse | undefined {
    return this.dataService.imageResponse;
  }
}
