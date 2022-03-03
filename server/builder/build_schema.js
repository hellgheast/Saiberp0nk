const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const saltRounds = 10;
const example_user = ["Lenok","Zartam","Zlatows","Phylene"];
const example_password = ["Blyat","Urod","Bratan","NoNoobNoArnak"];

const userAccountSchema = new mongoose.Schema({
    username: String,
    password: String
});

// UserAccount collection
const UserAccount = mongoose.model("UserAccount", userAccountSchema);

mongoose.connect('mongodb://localhost:27017/test');

build();

async function build() {

    console.log("Connected to DB");
    for (let index = 0; index < example_user.length; index++) {
        const user = example_user[index];
        const password = example_password[index];

        const hash = bcrypt.hashSync(password, saltRounds);

        const user_pwd = await UserAccount.create({username: user,password:hash});
        
        console.log(`Created user ${user_pwd.username}`);


        //$2a$10$FEBywZh8u9M0Cec/0mWep.1kXrwKeiWDba6tdKvDfEBjyePJnDT7K
    }
    console.log("Query the complete system");
    const accountQuery = await UserAccount.find();
    console.log(accountQuery);

}



