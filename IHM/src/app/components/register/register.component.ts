import { Component, output, SecurityContext } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-register',
  imports: [ReactiveFormsModule],
  template: `
      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
        <label for="name">Name: </label>
        <input id="name" type="text" formControlName="name" />

        <label for="surname">Surname: </label>
        <input id="surname" type="text" formControlName="surname" />

        <label for="email">Email: </label>
        <input id="email" type="email" formControlName="email" />
        
        <label for="phone">Phone number: </label>
        <input id="phone" type="text" formControlName="phone" />

        <label for="pwd">Mot de passe : </label>
        <input id="pwd" type="password" required minlength="8" formControlName="password" />

        <label for="pwd2">Confirmez le mot de passe : </label>
        <input id="pwd2" type="password" required minlength="8" formControlName="confirmPwd" />
        
        <button type="submit" [disabled]="!profileForm.valid">Connexion</button>
      </form>
  `,
  styleUrl: './register.component.css'
})

export class RegisterComponent {
  user: any = {name: '', surname: '', email: '', phone: '', password: ''};
  confirmPwd: string = '';
  validUser = output<void>();

  constructor(private api: ApiService, private sanitizer: DomSanitizer){}

  profileForm = new FormGroup({
    name: new FormControl(this.user.name, [
      Validators.required,
      Validators.pattern('^[a-zA-Z0-9_]*$')
    ]),
    surname: new FormControl(this.user.surname, [
      Validators.required,
      Validators.pattern('^[a-zA-Z0-9_-]*$')
    ]),
    email: new FormControl(this.user.email, [
      Validators.required,
      Validators.email,
    ]),
    phone: new FormControl(this.user.phone, [
      Validators.required,
      Validators.pattern('^[0-9_]*$')
    ]),
    password: new FormControl(this.user.password, [
      Validators.required,
      Validators.minLength(8),
    ]),
    confirmPwd: new FormControl(this.confirmPwd, [
      Validators.required,
      Validators.minLength(8),
    ]),
  }, { 
    validators: this.confirmPwdValidator 
  });


  confirmPwdValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get("password");
    const confirm = control.get("confirmPwd");

    if (!password || !confirm) {
        return null;
    }

    const hasUpperCase = /[A-Z]+/.test(password.value);
    const hasLowerCase = /[a-z]+/.test(password.value);
    const hasNumeric = /[0-9]+/.test(password.value);
    const hasSpecialChar = /[!@#$&*]+/.test(password.value);
    const pwdMatch = password.value === confirm.value ? true : false;

    const passwordValid = hasUpperCase && hasLowerCase && hasNumeric && hasSpecialChar && pwdMatch;
    return !passwordValid ? {passwordStrength:true}: null;
  }

  onSubmit(){
    this.user = this.sanitizer.sanitize(SecurityContext.NONE, this.profileForm.value)
    this.api.addUser(this.user);
    // this.validUser.emit()
  }
}
