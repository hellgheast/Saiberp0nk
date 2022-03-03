var express = require('express');
var router = express.Router();
const jwt = require("jsonwebtoken");


// var passport = require('passport');
// var LocalStrategy = require('passport-local');
// var crypto = require('crypto');
// var db = require('../db');


// Inspired from https://www.loginradius.com/blog/async/implementing-authentication-on-vuejs-using-jwt/
// https://www.passportjs.org/tutorials/password/prompt/

router.post("/login?",function (req,res,next) {
    const priv_user = "lenok";
    const priv_pass = "triumph";

    const {username, password} = req.body;
    console.log(req.body);
    if(username === priv_user && password == priv_pass) {
      const user = {
        id: 1,
        name: "lenok triumph",
        username: "lenok"
      };
      res.header("Access-Control-Allow-Origin", "*");
      res.status(200);
      res.json({
        message: "Correct login"
      });
    } else {
      res.header("Access-Control-Allow-Origin", "*");
      res.status(403);
      res.json({
        message: "Wrong login"
      });
    }
  
  })
  

module.exports = router;