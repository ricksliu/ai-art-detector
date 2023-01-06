import { Component, OnInit, Input, HostBinding } from '@angular/core';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
  styleUrls: ['./loader.component.scss']
})
export class LoaderComponent implements OnInit {
  @HostBinding('class.show') @Input() show = false;

  constructor() { }

  ngOnInit(): void {
  }

}
