import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  template: `<h1>Fruit juice</h1>`,
  styleUrl: './app.css'
})
export class App {
  protected title = 'froot';
}
