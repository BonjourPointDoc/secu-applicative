import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  template: `
    <div>
      <router-outlet />
    </div>
  `,
  styleUrl: './app.css'
})
export class App {
  protected title = 'IHM';
}
