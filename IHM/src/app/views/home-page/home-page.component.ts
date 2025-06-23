import { Component, inject, Input } from '@angular/core';
import { MatBadgeModule } from '@angular/material/badge';
import { MatIconModule } from '@angular/material/icon'; 
import { Router } from '@angular/router';
import { Juice } from '../../interfaces';
import { CardItem } from "../../components/card-item/card-item";
import { NgFor, NgIf } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { MatBottomSheet } from '@angular/material/bottom-sheet';
import { CartContent } from '../../components/cart-content/cart-content';

@Component({
  selector: 'app-home-page',
  imports: [CardItem, NgFor, NgIf, MatIconModule, MatBadgeModule],
  template: `
    <section>
    <main>
      <header class="header">
        <div class="header-title">
          <img class="brand-logo" src="/assets/logo.png" alt="logo" aria-hidden="true" />
          <h1>FRUIT JUICE SHOP</h1>
        </div>
        <div class="header-menu"s>
          <button matFab extended class="primary" 
            [matBadge]="cart.size" 
            [matBadgeHidden]="cart.size === 0" 
            (click)="displayCart()">
            <mat-icon>local_grocery_store</mat-icon>
            My cart
          </button>
          <button matFab extended (click)="logout()" class="primary">
            <mat-icon>exit_to_app</mat-icon>
            Log out
          </button>
        </div>
        
      </header>
      <section class="content">
        <section class="results" *ngIf="displayedData">
          <app-card-item
            *ngFor="let juice of displayedData"
            [juice]="juice"
            (itemAdded)="addToCart($event)"
          ></app-card-item>
        </section>
      </section>
    </main>
  `,
  styleUrl: './home-page.component.css'
})
export class HomePage {
  private _cartSheet = inject(MatBottomSheet);
  readonly baseUrl = 'https://angular.dev/assets/images/tutorials/common';
  cart: Map<number, number> = new Map<number, number>();
  juices: Map<number, Juice>  = new Map([
    [
      0,
      {
        id: 0,
        name: 'Acme Fresh Start Housing',
        price: 4.00,
        picture: `https://angular.dev/assets/images/tutorials/common/bernard-hermant-CLKGGwIBTaY-unsplash.jpg`,
        ingredients: [
          { id: 0, name: "orange", quantity: 2},
          { id: 1, name: "citron", quantity: 1},
          { id: 2, name: "mangue", quantity: 2}
        ]
      }
    ],
    [
      1,
      {
        id: 1,
        name: 'A113 Transitional Housing',
        price: 2.00,
        picture: `https://angular.dev/assets/images/tutorials/common/brandon-griggs-wR11KBaB86U-unsplash.jpg`,
        ingredients: [
          { id: 3, name: "carotte", quantity: 2},
          { id: 4, name: "tomate", quantity: 1}
        ]
      }
    ],
    [
      2,
      {
        id: 2,
        name: 'Warm Beds Housing Support',
        price: 5.00,
        picture: `https://angular.dev/assets/images/tutorials/common/i-do-nothing-but-love-lAyXdl1-Wmc-unsplash.jpg`,
        ingredients: [
          { id: 5, name: "ananas", quantity: 3}
        ]
      }
    ],
    [
      3, 
      {
        id: 3,
        name: 'Homesteady Housing',
        price: 2.50,
        picture: `https://angular.dev/assets/images/tutorials/common/ian-macdonald-W8z6aiwfi1E-unsplash.jpg`,
        ingredients: [
          { id: 5, name: "ananas", quantity: 3},
          { id: 2, name: "mangue", quantity: 2},
          { id: 2, name: "noix de coco", quantity: 2}
        ]
      }
    ],
    [
      4,
      {
        id: 4,
        name: 'Happy Homes Group',
        price: 3.10,
        picture: `https://angular.dev/assets/images/tutorials/common/krzysztof-hepner-978RAXoXnH4-unsplash.jpg`,
        ingredients: [
          { id: 5, name: "ananas", quantity: 3},
          { id: 2, name: "mangue", quantity: 2}
        ]
      }
    ],
    [
      5,
      {
        id: 5,
        name: 'Hopeful Apartment Group',
        price: 1.20,
        picture: `https://angular.dev/assets/images/tutorials/common/r-architecture-JvQ0Q5IkeMM-unsplash.jpg`,
        ingredients: [
          { id: 6, name: "pomme", quantity: 4},
        ]
      }
    ],
    [
      6,
      {
        id: 6,
        name: 'Seriously Safe Towns',
        price: 2.00,
        picture: `https://angular.dev/assets/images/tutorials/common/phil-hearing-IYfp2Ixe9nM-unsplash.jpg`,
        ingredients: [
          { id: 5, name: "ananas", quantity: 3},
          { id: 2, name: "mangue", quantity: 2}
        ]
      }
    ],
    [
      7, 
      {
        id: 7,
        name: 'Hopeful Housing Solutions',
        price: 5.30,
        picture: `https://angular.dev/assets/images/tutorials/common/r-architecture-GGupkreKwxA-unsplash.jpg`,
        ingredients: [
          { id: 7, name: "avocat", quantity: 2},
          { id: 1, name: "citron", quantity: 2}
        ]
      }
    ],
    [
      8,
     {
        id: 8,
        name: 'Seriously Safe Towns',
        price: 0.5,
        picture: `https://angular.dev/assets/images/tutorials/common/saru-robert-9rP3mxf8qWI-unsplash.jpg`,
        ingredients: [
          { id: 8, name: "fraise", quantity: 15},
          { id: 9, name: "framboise", quantity: 12},
          { id: 10, name: "myrtille", quantity: 8}
        ]
      }
    ],
    [
      9,
      {
        id: 9,
        name: 'Capital Safe Towns',
        price: 1.10,
        picture: `https://angular.dev/assets/images/tutorials/common/webaliser-_TPTXZd9mOo-unsplash.jpg`,
        ingredients: [
          { id: 6, name: "pomme", quantity: 2},
          { id: 9, name: "framboise", quantity: 16}
        ]
      }
    ]
  ]);
  displayedData: Juice[] =  Array.from(this.juices.values());
  constructor(private api: ApiService, private router: Router){}

  logout(){
    this.api.logout()
  }

  addToCart(data:any){
    let quantity = data.amount
    if(this.cart.has(data.item)){
      quantity += this.cart.get(data.item)
    }
    this.cart.set(data.item, quantity)
   
  }

  displayCart(){
     const cartRef = this._cartSheet.open(CartContent, {
      data: { juices: this.juices, cart: this.cart},
    }); 
    const subscribeDialog = cartRef.instance.dataEmitter.subscribe((data) => {
      this.cart.delete(data)
    });
  }
}