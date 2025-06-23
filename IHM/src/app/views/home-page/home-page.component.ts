import { Component } from '@angular/core';
import { LocalService } from '../../services/local.service';
import { MatIconModule } from '@angular/material/icon'; 
import { Router } from '@angular/router';
import { Juice } from '../../interfaces';
import { CardItem } from "../../components/card-item/card-item";
import { NgFor } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-home-page',
  imports: [CardItem, NgFor, MatIconModule],
  template: `
    <section>
    <main>
      <header class="brand-name">
        <div class="headerDiv">
          <img class="brand-logo" src="/assets/logo.png" alt="logo" aria-hidden="true" />
          <h1>FRUIT JUICE SHOP</h1>
        </div>
        <!-- <button matFab extended class="primary">
          Cart
        </button> -->
        <button matFab extended (click)="logout()" class="primary">
          <mat-icon>exit_to_app</mat-icon>
          Log out
        </button>
      </header>
      <section class="content">
        <section class="results">
          <app-card-item
            *ngFor="let juice of juices"
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
  readonly baseUrl = 'https://angular.dev/assets/images/tutorials/common';
  cart: Map<number, number> = new Map<number, number>();
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
    console.log(this.cart)
  }

  juices: Juice[] = [
    {
      id: 0,
      name: 'Acme Fresh Start Housing',
      price: 4.00,
      picture: `${this.baseUrl}/bernard-hermant-CLKGGwIBTaY-unsplash.jpg`,
      ingredients: [
        { id: 0, name: "orange", quantity: 2},
        { id: 1, name: "citron", quantity: 1},
        { id: 2, name: "mangue", quantity: 2}
      ]
    },
    {
      id: 1,
      name: 'A113 Transitional Housing',
      price: 2.00,
      picture: `${this.baseUrl}/brandon-griggs-wR11KBaB86U-unsplash.jpg`,
      ingredients: [
        { id: 3, name: "carotte", quantity: 2},
        { id: 4, name: "tomate", quantity: 1}
      ]
    },
    {
      id: 2,
      name: 'Warm Beds Housing Support',
      price: 5.00,
      picture: `${this.baseUrl}/i-do-nothing-but-love-lAyXdl1-Wmc-unsplash.jpg`,
      ingredients: [
        { id: 5, name: "ananas", quantity: 3}
      ]
    },
    {
      id: 3,
      name: 'Homesteady Housing',
      price: 2.50,
      picture: `${this.baseUrl}/ian-macdonald-W8z6aiwfi1E-unsplash.jpg`,
      ingredients: [
        { id: 5, name: "ananas", quantity: 3},
        { id: 2, name: "mangue", quantity: 2},
        { id: 2, name: "noix de coco", quantity: 2}
      ]
    },
    {
      id: 4,
      name: 'Happy Homes Group',
      price: 3.10,
      picture: `${this.baseUrl}/krzysztof-hepner-978RAXoXnH4-unsplash.jpg`,
      ingredients: [
        { id: 5, name: "ananas", quantity: 3},
        { id: 2, name: "mangue", quantity: 2}
      ]
    },
    {
      id: 5,
      name: 'Hopeful Apartment Group',
      price: 1.20,
      picture: `${this.baseUrl}/r-architecture-JvQ0Q5IkeMM-unsplash.jpg`,
      ingredients: [
        { id: 6, name: "pomme", quantity: 4},
      ]
    },
    {
      id: 6,
      name: 'Seriously Safe Towns',
      price: 2.00,
      picture: `${this.baseUrl}/phil-hearing-IYfp2Ixe9nM-unsplash.jpg`,
      ingredients: [
        { id: 5, name: "ananas", quantity: 3},
        { id: 2, name: "mangue", quantity: 2}
      ]
    },
    {
      id: 7,
      name: 'Hopeful Housing Solutions',
      price: 5.30,
      picture: `${this.baseUrl}/r-architecture-GGupkreKwxA-unsplash.jpg`,
      ingredients: [
        { id: 7, name: "avocat", quantity: 2},
        { id: 1, name: "citron", quantity: 2}
      ]
    },
    {
      id: 8,
      name: 'Seriously Safe Towns',
      price: 0.5,
      picture: `${this.baseUrl}/saru-robert-9rP3mxf8qWI-unsplash.jpg`,
      ingredients: [
        { id: 8, name: "fraise", quantity: 15},
        { id: 9, name: "framboise", quantity: 12},
        { id: 10, name: "myrtille", quantity: 8}
      ]
    },
    {
      id: 9,
      name: 'Capital Safe Towns',
      price: 1.10,
      picture: `${this.baseUrl}/webaliser-_TPTXZd9mOo-unsplash.jpg`,
      ingredients: [
        { id: 6, name: "pomme", quantity: 2},
        { id: 9, name: "framboise", quantity: 16}      ]
    },
  ];


}