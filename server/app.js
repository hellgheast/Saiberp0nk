
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var createError = require('http-errors');

const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');


const app = express();
const server = createServer(app);
const io = new Server(server,
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


// Simple game data
var position = {
  x:200,
  y:200
}


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

  socket.on("chatmsg",(msg) => {
    console.log(msg);
    io.emit("chatmsg",msg);
  });

  socket.on("position_req",(data) => {
    io.emit("position",position);
  });

  socket.on("move",(data) => {
    switch(data) {
      case "left":
        position.x -= 20;
        break;
      case "right":
        position.x += 20;
        break;
      case "down":
        position.y += 20;
        break;
      case "up":
        position.y -= 20;
        break;
    }
    io.emit("position",position);
     
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
