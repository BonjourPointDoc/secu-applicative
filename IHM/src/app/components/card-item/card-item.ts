import {Component, inject, input} from '@angular/core';
import { MatIconModule } from '@angular/material/icon'; 
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { CartDialog } from '../cart-dialog/cart-dialog';
import { Juice } from '../../interfaces';
import { NgFor } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-card-item',
  imports: [NgFor, MatIconModule, MatButtonModule, MatCardModule],
  template: `
    <section class="juices">
      <img
        class="juices-photo"
        [src]="juice().picture"
        crossorigin
      />
      <h2 class="juices-heading">{{ juice().name }} | {{ juice().price }} €</h2>
      <div class="juices-info">
        <ul>
          <li *ngFor="let fruit of juice().ingredients">{{fruit.name}} x{{fruit.quantity}}</li>
        </ul>
        
         <mat-card-actions class="actions">
          <button matFab class="primary addToCart" type="button" (click)="openDialog()">
            <mat-icon>add_shopping_cart</mat-icon>
          </button>
        </mat-card-actions>
      </div>
  `,
  styleUrls: ['./card-item.css'],
})
export class CardItem {
  readonly dialog = inject(MatDialog);
  juice = input.required<Juice>();  
  quantity: number = 0;
 
  openDialog(): void {
    const dialogRef = this.dialog.open(CartDialog, {
      data: {name: this.juice().name, quantity: this.quantity},
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result  !== undefined && result !== 0) {
        this.quantity = result;
        // console.log(this.quantity)
      }
    });
  }
}
