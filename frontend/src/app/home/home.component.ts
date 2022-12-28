import { Component, OnInit } from '@angular/core';

import { ApiService } from '../shared/services/api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(private apiService: ApiService) { }

  ngOnInit(): void { }

  onClick(): void {
    this.apiService.postImage().subscribe({
      next: data => { console.log('data', data) },
      error: error => { console.log('error', error) },
    });
  }
}
