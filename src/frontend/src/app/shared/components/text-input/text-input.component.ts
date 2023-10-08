import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

/** Text input. */
@Component({
  selector: 'app-text-input',
  templateUrl: './text-input.component.html',
  styleUrls: ['./text-input.component.scss']
})
export class TextInputComponent implements OnInit {
  @Input() placeholder = '';
  @Input() submitLabel = '';
  @Output() inputEvent = new EventEmitter<string>();
  text = '';

  constructor() { }

  ngOnInit(): void {
  }

  onKeyup(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.onSubmit();
    } else {
      this.text = (event.target as HTMLInputElement).value;
    }
  }

  onSubmit(): void {
    this.inputEvent.emit(this.text);
  }
}
