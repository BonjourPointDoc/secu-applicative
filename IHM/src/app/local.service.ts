import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LocalService {

  constructor() { }

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