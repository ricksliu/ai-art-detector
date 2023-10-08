import { Component, OnInit, Input, HostBinding } from '@angular/core';

/** App-wide loading effect. */
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
