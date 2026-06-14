
/** STRING */

let lastname = 'John';

// Declaration with specific types can be done as such:
// This allows the editor to populate string specific methods and helps with code clarity

let lname : string;

lname = 'Rao';

let newname = lname.toUpperCase();

console.log(newname);

// The below line is not allowed in TypeScript since TS has Type Safety
// lastname = 10; 

/** NUMBER */

let age : number;

// number encompasses both integer, float and decimal in JS and TS

age = 25;
age = 25.5;

/** BOOLEAN */

// In TypeScript, boolean is not by default assigned and is by default undefined

let isValid : boolean = false;

// console.log(isValid);

/** ARRAY */

// TypeScript don't have lists, JavaScript and TypeScript has array only

let emptyList = [];

// Two ways of declaring a String array

let emptyStringList : string[];

let emptyStringList2 : Array<string>;

let numList : Array<number>;

numList = [1,2,3,4,5];

// We can pass a comparator or predicate as it is called in TypeScript
// This below method returns a list of all numbers > 2 from numList into results
// results is an array due to TypeScript's type inference

let results = numList.filter((number) => number > 2);

console.log(results);

// Equality in JavaScript is 3 equal signs shown below, which is also used for string equality
// This returns the value if found, otherwise returns undefined

let result = numList.find((number) => number === 2);

console.log(result);

// The below reduce function works by iterating through the array
// where par1 is the accumulator and num is the current value that is being traversed
// We can then use that accumulator and add each number to get total sum of array

let sum = numList.reduce((currentSum, num) => currentSum + num);

/** ENUM */

// For enums, We use const to condense the compiled JavaScript
// This will remove the initialization for our code on line 87
// and will only be converted to .. let c = 2 /* BLUE */;

const enum Color
{
    RED,
    GREEN,
    BLUE
}

let c : Color = Color.BLUE;

/** TUPLE */

let tuple : [firstNumber : number, secondNumber : number];

// This function takes in 2 numbers and returns a tuple of 2 numbers

function swapNumbers(num1 : number, num2 : number) : [number,number]
{
    return [num2,num1];
}

tuple = swapNumbers(1,2);

// Tuple values can be accessed as below

tuple[0];
tuple[1];

/** HASHMAP + SET */

// Not too different from maps and sets that we know from Java

let map = new Map<string, string>();

let set = new Set<number>();

/** any */

// Try not to use any since it doesn't do type checks

// Same as let department;

let department : any;

department = "IT";
department = 10;

