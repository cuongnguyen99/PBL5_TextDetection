import createError from 'http-errors';
import express from 'express';
import path from 'path';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import session from 'express-session';
import http from 'http';
import middleware from "./middleware/admin-middleware.js";
import bodyParser from 'body-parser';
import multer from 'multer';
const upload = multer();
import cors from 'cors';


import adminRouter from './routes/admin.js';
import apiRouter from './routes/apis.js';

import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

import models from "./models/index.js";

import { render } from 'ejs';

const app = express();
var server = http.createServer(app);
// view engine setup

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');


app.use(logger('dev'));
// app.use(express.json());
// app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(cors());

app.use(session({
  name: 'sid',
  secret: 'keyboard cat',
  resave: false,
  saveUninitialized: true,
  cookie: { secure : false }
}));

app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: false }));
app.use(upload.array()); 
app.use(express.static('./uploads'));

app.use(function(err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
});

const db = await models();

app.use('/admin', adminRouter({ db }));
app.use('/apis', apiRouter({ db }));

function normalizePort(val) {
  var port = parseInt(val, 10);

  if (isNaN(port)) {
    // named pipe
    return val;
  }

  if (port >= 0) {
    // port number
    return port;
  }

  return false;
}

function onError(error) {
  if (error.syscall !== 'listen') {
    throw error;
  }

  var bind = typeof port === 'string'
    ? 'Pipe ' + port
    : 'Port ' + port;

  // handle specific listen errors with friendly messages
  switch (error.code) {
    case 'EACCES':
      console.error(bind + ' requires elevated privileges');
      process.exit(1);
      break;
    case 'EADDRINUSE':
      console.error(bind + ' is already in use');
      process.exit(1);
      break;
    default:
      throw error;
  }
}

function onListening() {
  var addr = server.address();
  var bind = typeof addr === 'string'
    ? 'pipe ' + addr
    : 'port ' + addr.port;
  debug('Listening on ' + bind);
}

app.listen(8000, function() {
  console.log("server is running on port 8000");
});
server.on('error', onError);
server.on('listening', onListening);

export default app;
