const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const saltRounds = 10;

const userAccountSchema = new mongoose.Schema({
    username:String,
    password: String
});

const UserAccount = mongoose.model("UserAccount", userAccountSchema);

mongoose.connect('mongodb://localhost:27017/test');

update();

async function update(){
    let account = await UserAccount.find({username:"Lenok"});
    
    console.log("Old password");    
    console.log(account[0].password);

    console.log("New password");
    const new_password = bcrypt.hashSync(account[0].password, saltRounds);
    console.log(new_password);
    const res = await UserAccount.updateOne({username:"Lenok"},{password:new_password});
    
    console.log(res);


}