

// Learning JS from some fun

class Fruit {
    // Public attributes
    
    // Privates attributes
    #fruitName;
    constructor(name) {
        this.#fruitName = name;
    }

    getName(){
        return this.#fruitName;
    }

    getType(){
        throw(new Error("Type undefined !"));
    }
}

let Banana = new Fruit("Banana");
console.log(`My fruit is ${Banana.getName()}`);

try {
    Banana.getType();
} catch (e) {
    console.error(e.name);
    console.error(e.message);
}