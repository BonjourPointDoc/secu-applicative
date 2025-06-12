import { Routes } from '@angular/router';
import { LoginPage } from './views/login-page/login-page.component';
import { HomePage } from './views/home-page/home-page.component';
import { AuthGuard } from './auth.guard';

export const routes: Routes = [
    { path: '', component: HomePage, canActivate: [AuthGuard] },
    { path: 'login', component: LoginPage },
];
