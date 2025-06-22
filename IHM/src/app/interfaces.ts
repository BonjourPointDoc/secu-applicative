
export interface Ingredient {
    id: number;
    name: string;
    quantity: number;
}

export interface Juice {
    id: number;
    name: string;
    price: number;
    picture: string;
    ingredients: Ingredient[];
}
