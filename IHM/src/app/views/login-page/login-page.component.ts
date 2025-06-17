import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from "../../components/login/login.component";
import { RegisterComponent } from "../../components/register/register.component";
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  imports: [CommonModule, LoginComponent, RegisterComponent],
  template: `
    <div class="container">
     <div id="loginPageForm">
      <div id="loginButtonsContainer">
        <button (click)="switchForms()" [disabled]="loginForm">Login</button>
        <button (click)="switchForms()" [disabled]="!loginForm">Register</button>
      </div>
      <app-login *ngIf="loginForm; else elseBlock" (validUser)="onValidation()"/>
      <ng-template #elseBlock>
        <app-register (validUser)="onValidation()"/>
      </ng-template>
      </div>
    </div>
  `,
  styleUrl: './login-page.component.css'
})

export class LoginPage {
  loginForm: boolean = true;

  constructor(private router: Router){}

  switchForms(){
    this.loginForm = ! this.loginForm
  }

  onValidation(){
    this.router.navigate(['/']);
  }
}
