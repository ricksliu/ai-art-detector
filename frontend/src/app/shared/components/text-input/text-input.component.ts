import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-text-input',
  templateUrl: './text-input.component.html',
  styleUrls: ['./text-input.component.scss']
})
export class TextInputComponent implements OnInit {
  @Output() inputEvent = new EventEmitter<string>();
  text = '';

  constructor() { }

  ngOnInit(): void {
  }

  onKeyup(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      this.onSubmit();
    } else {
      this.text = (event.target as HTMLInputElement).value;
    }
  }

  onSubmit() {
    this.inputEvent.emit(this.text);
  }
}
