import express from 'express';
import AdminController from "../controllers/adminController.js";
import OrderController from '../controllers/orderController.js';
// import Middleware from '../middleware/apis-middleware.js';
import Middleware from '../middleware/admin-middleware.js';

export default ({db}) =>{
	const router = express.Router();
  const adminController = new AdminController(db);
	const orderController = new OrderController(db);

	router.get('/login', Middleware.checkLogin , (req,res)=>adminController.loginform(req,res));
	router.post('/login', Middleware.checkLogin ,(req,res)=>adminController.login(req,res));
	router.post('/logout' , (req,res)=>adminController.logout(req,res));
	router.get('/',Middleware.isLoggedIn , (req,res)=>adminController.dashboard(req,res));

	// order
	router.get('/orders',Middleware.isLoggedIn , (req,res)=>orderController.index(req,res));
	router.get('/orders/processed-items',Middleware.isLoggedIn, (req,res)=>orderController.processedItems(req,res));

	
	return router;
} 