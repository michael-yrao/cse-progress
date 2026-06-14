export interface User
{
    name : string;
    age? : number; // Putting question mark makes this field optional
    id : number;
    email : string;
}

// This is called destructuring and allows name and email to be aliased and used as their separate variables
// Not sure the use cases for this

let {name : userName, email : userLogin} : User = {name : "John", id : 1, email : ""};

export interface Address
{
    street : string;
    city : string;
    state : string;
    zipcode : string;
}

let user : User = 
{
    name : "John",
    id : 1,
    email : ""
};

interface Employees extends User
{
    salary : number;
}

let employee : Employees = 
{
    name : "John",
    id : 1,
    email : "",
    salary : 5,
}

export interface Login
{
    Login() : User;
}

// Array destructuring with rest parameters

let [user1, user2,...restUsers] : User[] = [ {name : "John", id : 1, email : "",}, {name : "John2", id : 2, email : "",}, {name : "John3", id : 3, email : "",}];

console.log(user1);
console.log(user2);
console.log(restUsers);