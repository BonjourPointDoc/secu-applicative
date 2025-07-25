// src/app/task.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject, from, of, switchMap } from 'rxjs';
import { Router } from '@angular/router';
import { LocalService } from './local.service';

@Injectable({
  providedIn: 'root',
})
export class ApiService {

  isAuthenticated: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  currentAccessToken:string | null = null;
  currentRefreshToken:string | null = null;
  private url:string = "https://juicy-world.org/api";

  constructor(private storage: LocalService, private router: Router) {
    this.loadToken();
  }

  loadToken() {
    const token = this.storage.getAccessToken();
    if (token) {
      this.currentAccessToken = token;
      this.isAuthenticated.next(true);
    }else{
      this.isAuthenticated.next(false);
    }
  }

  async refreshToken(){
    let data = await fetch(`${this.url}/token/access`,{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${this.currentRefreshToken}`
      },
      }).then((response) => {return response.json()
      }).then((data) => { 
        this.currentAccessToken = data['access_token'];
        if(this.currentAccessToken){
          this.storage.setAccessToken(this.currentAccessToken);
          this.isAuthenticated.next(true);
          this.router.navigateByUrl('/', { replaceUrl: true });
        }
      }); 
  }

  async login(login:string, pwd:string){
    let postData = {"login": login, "password": pwd }
    let data = await fetch(`${this.url}/login`,{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({login: login, password: pwd})
      }).then((response) => {return response.json()
      }).then((data) => { 
        this.currentRefreshToken = data['api_key']; 
        if(this.currentRefreshToken){
            this.storage.setRefreshToken(this.currentRefreshToken);
        }
      }); 
      
      if(this.currentRefreshToken){
        await this.refreshToken()
        this.isAuthenticated.next(true);
        this.router.navigateByUrl('/', { replaceUrl: true });
      }
  }

  async addUser(user: any){
    let postData = {
      nom: user.name,
      prenom: user.surname,
      email: user.email,
      telephone: user.phone,
      mot_de_passe: user.password
    }
    let data = await fetch(`${this.url}/login/user`,{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(postData)
      }).then((response) => {
        return response.status
      })
    if(data === 200){
      await this.login(postData.email, postData.mot_de_passe)
    }
  }
  
  logout(){
    this.storage.clearData()
    this.isAuthenticated.next(false);
    this.router.navigateByUrl('/login', { replaceUrl: true });
  }

  
}

