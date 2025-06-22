import { LowerCasePipe } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';

@Component({
  selector: 'app-cart-dialog',
  imports: [MatDividerModule, MatFormFieldModule, FormsModule, MatDialogModule, MatButtonModule, LowerCasePipe],
  template: `
    <h2 mat-dialog-title>Hi {{data.name}}</h2>
    <mat-divider></mat-divider>
    <mat-dialog-content>
      <p>How many <strong> {{ data.name | lowercase }} </strong> would you like to add ?</p>
     
        <mat-label>Quantity</mat-label>
        <input [(ngModel)]="data.quantity" type="number"/>
     
    </mat-dialog-content>
    <mat-dialog-actions>
      <button matButton (click)="onNoClick()">No Thanks</button>
      <button matButton [mat-dialog-close]="data.quantity" cdkFocusInitial>Ok</button>
    </mat-dialog-actions>
  `,
  styleUrl: './cart-dialog.css'
})
export class CartDialog {
  readonly dialogRef = inject(MatDialogRef<CartDialog>);
  data = inject(MAT_DIALOG_DATA);
  quantity = 0;

  onNoClick(): void {
    this.dialogRef.close();
  }
}
