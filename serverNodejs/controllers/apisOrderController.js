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
    let area = null
    try {
      if(params.area) {
        area = await this.db.area.findOne({
          where: {
            name: params.area
          }
        })
      } 

			if(!params.area || !params.receiver || !params.phone || !params.price || !params.address) {
        
        const errorData = await this.db.order.create({
          receiver: params.receiver,
          phone: params.phone,
          price: params.price,
          address: params.address,
          content: params.content,
          status: 1
        });

  			return res.status(400).json({ TRAVE: false, messenger: 'something are invalid'});
  		}

      if(!area) {
        area = await this.db.area.create({
          name: params.area,
          city: "Đà Nẵng"
        });
      }

      const data = await this.db.order.create({
        receiver: params.receiver,
        phone: params.phone,
        price: params.price,
        address: params.address,
        content: params.content,
        status: 2,
        areas: [{
          id: area.id,
          area_order:{
            selfGranted: true
          }
        },{
          include: await this.db.area
        }]
      });
      await data.addArea(area, { through: { selfGranted: false } });
      // const areaOrder = await this.db.area_order.create({
      //   orderId: data.id,
      //   areaId: area.id
      // })


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