import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CartContent } from './cart-content';

describe('CartContent', () => {
  let component: CartContent;
  let fixture: ComponentFixture<CartContent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CartContent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CartContent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
