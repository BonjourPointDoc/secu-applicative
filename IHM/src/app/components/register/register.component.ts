import { Component, output } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  imports: [ReactiveFormsModule],
  template: `
      <form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
        <label for="username">Username: </label>
        <input id="username" type="text" formControlName="username" />

        <label for="email">Email: </label>
        <input id="email" type="email" formControlName="email" />

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
  user: any = {username: '', email: '', password: '', img: ''};
  confirmPwd: string = '';
  validUser = output<void>();

  profileForm = new FormGroup({
    username: new FormControl(this.user.username, [
      Validators.required,
    ]),
    email: new FormControl(this.user.email, [
      Validators.required,
      Validators.email,
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
    if(!password || !confirm){
      return null
    }
 
    if (password.value != confirm.value) { 
      return { 'noMatch': true } 
    }
 
    return null
 
  }
  
  onSubmit(){
    this.user = this.profileForm.value
    // Ajout vérif user avec bdd
    // Ajout user au store si ok

    this.validUser.emit();
  }
}
