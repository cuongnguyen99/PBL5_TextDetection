import express from 'express';
import AdminController from "../controllers/adminController.js";
import OrderController from '../controllers/orderController.js';
import ProductController from '../controllers/productController.js';
import ShopController from '../controllers/shopController.js';
import UserController from '../controllers/userController.js';
// import Middleware from '../middleware/apis-middleware.js';
import Middleware from '../middleware/admin-middleware.js';

export default ({db}) =>{
	const router = express.Router();
  const adminController = new AdminController(db);
	const orderController = new OrderController(db);
	const productController = new ProductController(db);
	const shopController = new ShopController(db);
	const userController = new UserController(db);

	router.get('/login', Middleware.checkLogin , (req,res)=>adminController.loginform(req,res));
	router.post('/login', Middleware.checkLogin ,(req,res)=>adminController.login(req,res));
	router.post('/logout' , (req,res)=>adminController.logout(req,res));
	router.get('/' , (req,res)=>adminController.dashboard(req,res));

	// order
	router.get('/orders', (req,res)=>orderController.index(req,res));
	router.get('/orders/new_order', (req,res)=>orderController.addOrderForm(req,res));
	router.post('/orders/new_order', (req,res)=>orderController.addOrder(req,res));
	router.post('/orders/:id',(req,res)=>orderController.delete(req,res));

	// products
	router.get('/products', (req,res)=>productController.index(req,res));

	// shops
	router.get('/shops', (req,res)=>shopController.index(req,res));

	// users
	router.get('/users', (req,res)=>userController.index(req,res));

	
	return router;
} 