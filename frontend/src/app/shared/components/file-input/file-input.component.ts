import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-file-input',
  templateUrl: './file-input.component.html',
  styleUrls: ['./file-input.component.scss']
})
export class FileInputComponent implements OnInit {
  @Input() accept = '';
  @Output() inputEvent = new EventEmitter<File[]>();

  constructor() { }

  ngOnInit(): void {
  }

  onSubmit(event: Event) {
    const files: File[] = Array.from((event.target as HTMLInputElement).files ?? []);
    this.inputEvent.emit(files);
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    const files: File[] = event.dataTransfer?.items
      ? Array.from(event.dataTransfer?.items ?? []).filter(item => item.kind === 'file').map(item => item.getAsFile()).filter(file => file) as File[]
      : Array.from(event.dataTransfer?.files ?? []);
    this.inputEvent.emit(files);
  }

  onDragover(event: Event) {
    event.preventDefault();
  }
}
