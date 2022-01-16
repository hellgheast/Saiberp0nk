var express = require('express');
var router = express.Router();


const indexController = require('../controllers/indexController')
const userController = require('../controllers/userController')


/* GET home page. */
router.get('/', indexController.index);
router.get('/users',userController.user);
router.get('/script',function(req, res, next) {
  res.render('script', {title: "Script page"});
});

module.exports = router;
