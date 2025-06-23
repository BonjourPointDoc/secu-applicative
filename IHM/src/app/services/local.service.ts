import { Injectable } from '@angular/core';

const ACCESS_TOKEN_KEY = 'juice-access-token';
const REFRESH_TOKEN_KEY = 'juice-refresh-token';

@Injectable({
  providedIn: 'root'
})
export class LocalService {

  constructor() {}

  public setAccessToken(value: string) {
    localStorage.setItem(ACCESS_TOKEN_KEY, value);
  }

  public getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY)
  }
  public rmAccessToken() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
  }

  public setRefreshToken(value: string) {
    localStorage.setItem(REFRESH_TOKEN_KEY, value);
  }

  public getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
  }
  public rmRefreshToken() {
    localStorage.removeItem(REFRESH_TOKEN_KEY);
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

  public setData(key: string, value: string) {
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