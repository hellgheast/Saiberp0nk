var express = require('express');
var router = express.Router();


//const indexController = require('../controllers/indexController')
const userController = require('../controllers/userController')


/* GET home page. */
// router.get('/', indexController.index);

// router.get('/script',function(req, res, next) {
//   res.render('script', {title: "Script page"});
// });

router.get('/', function(req, res, next) {
  res.io.emit("socketToMe", "users");
  res.send('<h1>Chat server running with Socket.io</h1>');
});


router.get('/users',userController.user);

module.exports = router;
