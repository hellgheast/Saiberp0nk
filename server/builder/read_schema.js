const mongoose = require('mongoose');


const userAccountSchema = new mongoose.Schema({
    username:String,
    password: String
});

const UserAccount = mongoose.model("UserAccount", userAccountSchema);

mongoose.connect('mongodb://localhost:27017/test');

read();

async function read(){
    let account = await UserAccount.find({username:"Lenok"})
    console.log(account);
}