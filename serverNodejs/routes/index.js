import express from 'express';
import HomeController from '../Controllers/homeController.js';


export default ({ db }) => {
  // create new instance of route
  const router = express.Router();
  // test
  const homeController = new HomeController(db);
  // test
  router.get('/', (req, res) => homeController.getHome(req, res));


  return router;
};
