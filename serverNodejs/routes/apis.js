import express from 'express';
import ApisOrderController from '../controllers/apisOrderController.js';
import Middleware from '../middleware/apis-middleware.js';

export default ({db}) =>{
	const router = express.Router();
	const apisOrderController = new ApisOrderController(db);

	router.post('/orders', (req,res)=>apisOrderController.insertData(req,res));

	return router;
}