import {Component, input} from '@angular/core';
import { Juice } from '../../interfaces';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-card-item',
  imports: [NgFor],
  template: `
    <section class="juices">
      <img
        class="juices-photo"
        [src]="juice().picture"
        crossorigin
      />
      <h2 class="juices-heading">{{ juice().name }}</h2>
      <div class="juices-info">
        <p >{{ juice().price }} €</p>
        <ul class="juices-info">
          <li *ngFor="let fruit of juice().ingredients">{{fruit.name}} x{{fruit.quantity}}</li>
        </ul>
      </div>
  `,
  styleUrls: ['./card-item.css'],
})
export class CardItem {
  juice = input.required<Juice>();
}
