import { Component, OnInit, Input, Output, EventEmitter, HostBinding } from '@angular/core';

/** Toast message. */
@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss']
})
export class ToastComponent implements OnInit {
  @Input() type = '';
  @Input() message = '';
  @Output() closeEvent = new EventEmitter<void>();
  @HostBinding('class.error') classError = false;

  constructor() { }

  ngOnInit(): void {
    this.classError = this.type === 'error';
  }

  onClose(): void {
    this.closeEvent.emit();
  }
}
