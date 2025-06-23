import { MAT_BOTTOM_SHEET_DATA } from '@angular/material/bottom-sheet';
import { Component, EventEmitter, Inject, Output} from '@angular/core';
import {KeyValuePipe, NgIf} from '@angular/common';
import {MatDividerModule} from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon'; 
import { Juice } from '../../interfaces';
import { NgFor } from '@angular/common';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-cart-content',
  imports: [NgFor, NgIf, KeyValuePipe, MatDividerModule, MatIconModule],
  template: `
    <h2>My cart</h2>
    <ul *ngIf="data.cart.size > 0; else elseBlock">
        <li *ngFor="let item of data.cart | keyvalue"> 
            <mat-divider></mat-divider>
            <div class="item-container">
              <p>{{data.juices.get(item.key)?.name}}</p>
              <div class="item-infos">
                <p class="quantity">x {{item.value}}</p>
                <button matFab extended class="primary" (click)="deleteItem(item.key)">
                  <mat-icon>delete</mat-icon>
                </button>
              </div>
            </div>
        </li>
    </ul>

    <ng-template  #elseBlock>
      <p>Your cart is currently empty</p>
    </ng-template >
  `,
  styleUrl: './cart-content.css'
})
export class CartContent {
   public dataEmitter = new Subject<number>();
  constructor(@Inject(MAT_BOTTOM_SHEET_DATA) public data: {juices: Map<number, Juice>, cart: Map<number, number>}) {}

  deleteItem(id: number):void{
    var choice = confirm("Are you sure you want to delete this item from your cart ?");
    if (choice === true) {
       this.dataEmitter.next(id);
    }
  }
}