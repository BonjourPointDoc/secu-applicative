import { inject } from "@angular/core";
import { Router } from "@angular/router";
import { LocalService } from "./services/local.service";

export const AuthGuard = () => {
    const localStorage = inject(LocalService);
    const router = inject(Router);

    if(!localStorage.getUser()) {
        router.navigateByUrl('/login')
        return false
    }
    return true
}