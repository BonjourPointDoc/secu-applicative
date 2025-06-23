import { Component, output, SecurityContext } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { LocalService } from '../../services/local.service';
import { DomSanitizer } from '@angular/platform-browser';
import { NONE_TYPE } from '@angular/compiler';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-login',
  imports: [ ReactiveFormsModule ],
  template: `
    <img src="assets/logo.png" />
      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
        <label for="email">Email: </label>
        <input id="email" type="email" formControlName="email" />

        <label for="pwd">Mot de passe : </label>
        <input id="pwd" type="password" formControlName="password" />

        <button type="submit" [disabled]="!profileForm.valid">Connexion</button>
      </form>
  `,
  styleUrl: './login.component.css'
})
export class LoginComponent {
  user: any = { email: '', password: '' };
  validUser = output<void>();
  
  profileForm = new FormGroup({
    email: new FormControl(this.user.email, [
      Validators.required,
      Validators.email,
    ]),
    password: new FormControl(this.user.password, [
      Validators.required,
    ]),

  });

  constructor(private localStorage : LocalService, private api : ApiService, private sanitizer: DomSanitizer){}

  onSubmit(){
    this.user = this.sanitizer.sanitize(SecurityContext.NONE, this.profileForm.value)
    // this.localStorage.storeUser(this.user);
    this.api.login(this.user.email, this.user.password);
    // this.validUser.emit()
  }
}
