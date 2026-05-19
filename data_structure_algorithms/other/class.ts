import { Address,User,Login } from "./interface";

class Employee implements Login
{
    // # means private, we can also use private keyword
    #id : number;
    name : string;
    address : Address;

    // Static methods can be used without creating an instance of Employee
    // e.g. Employee.getEmployeeCount()

    static getEmployeeCount() : number
    {
        return 50;
    }

    // getter/setters

    get empId() : number
    {
        return this.#id;
    }

    set empId(id : number)
    {
        this.#id = id;
    }

    Login() : User 
    {
        return {name: "John", id : 4, email : ""};
    }

    // Constructor

    constructor(id : number, name : string, address : Address)
    {
        this.#id = id;
        this.name = name;
        this.address = address;
    }

    getNameWithAddress() : string
    {
        return `${this.name} lives at ${this.address}`;
        // return this.name + " " + this.address;
    }
}

// In TS, you can't have a default constructor and parameterized constructor

let john = new Employee(1,"John",{street : "Hello", city : "NY", state : "NY", zipcode: "10001"});

console.log(john.getNameWithAddress());

// We can set #id by calling the setter directly
john.empId = 2;

