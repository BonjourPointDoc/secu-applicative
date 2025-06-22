import { Injectable } from '@angular/core';

const ACCESS_TOKEN_KEY = 'access-token';

@Injectable({
  providedIn: 'root'
})
export class LocalService {

  constructor() { }

  public setToken(value: string) {
    localStorage.setItem(ACCESS_TOKEN_KEY, value);
  }

  public getToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  }

  public removeToken() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
  }  

  public storeUser(user: any){
    localStorage.setItem('user', JSON.stringify(user));
  }

  public getUser(){
    let retrievedObject = localStorage.getItem('user')
    if(retrievedObject)
      return JSON.parse(retrievedObject)
    else
      return null
  }

  public saveData(key: string, value: string) {
    localStorage.setItem(key, value);
  }

  public getData(key: string) {
    return localStorage.getItem(key)
  }
  public removeData(key: string) {
    localStorage.removeItem(key);
  }

  public clearData() {
    localStorage.clear();
  }
}