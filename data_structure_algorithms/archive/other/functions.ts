

// Don't have to have a return type in TypeScript since there is type inference
// However, try to add the return type to make sure we have a return statement

function add(num1 : number, num2 : number) : number
{
    return num1 + num2;
}

console.log(add(1,3));


// another way to write a function in TypeScript

const subtract = (num1 : number, num2 : number) : number => num1 - num2;

console.log(subtract(4,2));

// third way to write function

const multiply = function(num1 : number, num2 : number) : number 
{
    return num1 * num2;
}

console.log(multiply(1,6));

// Mandatory and optional parameters

function anotherAdd(num1 : number, num2 : number, num3? : number) : number
{
    return num3?num1 + num2 + num3:num1+num2;
}

console.log(anotherAdd(1,2));
console.log(anotherAdd(1,2,3));

// Mandatory and default parameters

// num3 defaults to 10 unless passed as a parameter

function anotherSubtract(num1 : number, num2 : number, num3 = 10) : number
{
    return num3 - num2 - num1;
}

console.log(anotherSubtract(1,2));
console.log(anotherSubtract(1,2,5));

// Rest parameters
// Not sure what this is actually used for but it is cool at least

function oneMoreAdd(num1 : number, num2 : number, ...num3 : number[]) : number
{
    return num1 + num2 + num3.reduce((a,b) => a+b, 0);
}

console.log(oneMoreAdd(1,2,3,4,5,6,7,8,9,10,11,12));

// Generics

function getItems<Type>(items : Type[]) : Type[]
{
    return new Array<Type>().concat(items);
}

let concatResult = getItems([1,2,3,4,5]);
let concatString = getItems(["1","2","3"]);