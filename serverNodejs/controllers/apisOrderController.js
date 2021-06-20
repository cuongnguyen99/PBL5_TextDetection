import CryptoJS  from "crypto-js";
import sha256 from 'crypto-js/sha256.js';
import Base64 from 'crypto-js/enc-base64.js';
import Middleware from '../middleware/apis-middleware.js';
import dotenv from 'dotenv';
dotenv.config();

const key = process.env.Key_JWT;


class apisOrderController {
	constructor(db) {
		this.db= db;
	}

  async insertData(req, res) {
    const params = req.body;
    try {
      
			if(!params.area || !params.receiver || !params.phone || !params.price || !params.address) {
        const errorData = await this.db.order.create({
          receiver: params.receiver,
          area: params.area,
          phone: params.phone,
          price: params.price,
          address: params.address,
          content: params.content,
          status: 1
        });

  			return res.status(400).json({ TRAVE: false, messenger: 'something are invalid'});
  		}

      const data = await this.db.order.create({
        receiver: params.receiver,
        area: params.area,
        phone: params.phone,
        price: params.price,
        address: params.address,
        content: params.content
      });

      if(!data) {
        return res.status(400).json({ TRAVE: false, messenger: 'Error create data'});
      }
      
    	return res.status(200).json({ TRAVE: true, messenger: 'Insert data is success'});
    } catch (err) {
    	console.log(err);
			return res.status(400).json({ TRAVE: false, messenger: 'Internal server error'});
    }
  }
}

export default function(...args) {
  return new apisOrderController(...args)
}