export type MenuItem = {
	id: string;
	name: string;
	description?: string;
	price: number;
	image?: string;
};

export const MENU: MenuItem[] = [
	{
		id: "popcorn-small",
		name: "Classic Popcorn (Small)",
		description: "Lightly salted, buttery popcorn",
		price: 3.5,
	},
	{
		id: "soda-regular",
		name: "Soda (Regular)",
		description: "Refreshing cola or lemon-lime",
		price: 2.0,
	},
	{
		id: "nachos",
		name: "Nachos",
		description: "Tortilla chips with cheese and jalapeños",
		price: 4.75,
	},
];

