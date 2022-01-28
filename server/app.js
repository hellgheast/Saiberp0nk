var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server,
  {
    cors: {
      origin: "http://localhost:8080"
    }
  });


var indexRouter = require('./routes/index');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));


// Adds socket.io in our event loop
app.use(function(req, res, next){
  res.io = io;
  next();
});

// Add the router
app.use('/', indexRouter);


// Handle Socket IO events
io.on('connection', (socket) => {
  console.log("A user connected");
  
  socket.on("disconnect", () =>{
    console.log("user disconnected");
  });

  socket.on("my message",(msg) => {
    console.log("rx msg: " + msg);
    console.log("broadcast it back !");
    io.emit("my broadcast", `server ${msg}`)
  });

});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});	

module.exports = {app: app, server: server};
