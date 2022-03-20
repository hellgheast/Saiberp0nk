
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var createError = require('http-errors');
var cors = require('cors');

const mongoose = require('mongoose');
const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');


const app = express();
app.use(cors()); // Don't know why we need this package ?

const server = createServer(app);
const io = new Server(server,
  {
    cors: {
      origin: "http://localhost:8080"
    }
  });


var indexRouter = require('./routes/index');
var authRouter = require('./routes/auth');

// Connect to the localhost DB
// mongoose.connect('mongodb://localhost:27017/sb_test');

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
app.use('/', authRouter);


// Multiplayer version
const players = {};


function getRandomRgb() {
  var num = Math.round(0xffffff * Math.random());
  var r = num >> 16;
  var g = num >> 8 & 255;
  var b = num & 255;
  return 'rgb(' + r + ', ' + g + ', ' + b + ')';
}

// Handle Socket IO events
io.on('connection', (socket) => {
  console.log("A user connected");
  // register new player
  players[socket.id] = {
    x:200,
    y:200,
    size: 20,
    c: getRandomRgb()
  }
  
  socket.on("disconnect", () =>{
    delete players[socket.id];
    console.log("user disconnected");
  });

  socket.on("my message",(msg) => {
    console.log("rx msg: " + msg);
    io.emit("my broadcast", `server ${msg}`)
  });

  socket.on("chatmsg",(msg) => {
    console.log(msg);
    io.emit("chatmsg",msg);
  });

  socket.on("position_req",(data) => {
    io.emit("players_list",Object.values(players));
  });

  socket.on("move",(data) => {
    switch(data) {
      case "left":
        players[socket.id].x -= 20;
        break;
      case "right":
        players[socket.id].x += 20;
        break;
      case "down":
        players[socket.id].y += 20;
        break;
      case "up":
        players[socket.id].y -= 20;
        break;
    }
    update();
     
  });

});

function update() {
  io.volatile.emit('players_list', Object.values(players));
}

setInterval(update, 500);

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
