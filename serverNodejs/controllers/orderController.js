import CryptoJS  from "crypto-js";
import queryOption from '../helpers/query.js';

class OrderController {
  constructor(db) {
      this.db = db
  }

  async index(req, res) {
    try {
      let order = null;
      
      res.locals.user = req.session.userName;

      const { page, size } = req.query;
      const { limit, offset } = await queryOption.getPagination(page-1, size);

      if(req.query.search) {
        order = await this.db.order.findAndCountAll({
          distinct:true,
          limit: limit,
          offset: offset,
          where: {
            [this.db.Op.or]: [
              { receiver:  { [this.db.Op.like] : '%' + req.query.search + '%' } },
              { phone:  { [this.db.Op.like] : '%' + req.query.search + '%' } },
              { address:  { [this.db.Op.like] : '%' + req.query.search + '%' } },
            ]
          },
          include:{
            model: this.db.area,
            as: "area"
          }
        })


      } else {
        order = await this.db.order.findAndCountAll({
          include:{
            model: this.db.area,
            as: "area"
          },
          distinct:true,
          limit: limit,
          offset: offset,
        });
      }
      order.rows.forEach(element => {
        console.log(element.area[0])
      });
    //  console.log(order)
      
      order = await queryOption.getPagingData(order, page-1, limit);
      
      res.render("admin/order/index", { data: order , notify: null});
      
    } catch (error) {
      console.log(error)
    }
   
  };

  async processedItems(req, res) {
    try {
      let order = null;
      
      res.locals.user = req.session.userName;

      const { page, size } = req.query;
      const { limit, offset } = await queryOption.getPagination(page-1, size);

      if(req.query.search) {
        order = await this.db.order.findAndCountAll({
          where: {
            [this.db.Op.or]: [
              { receiver: req.query.search },
              { phone: req.query.search },
              { address: req.query.search }
            ]
          },
          distinct:true,
          limit: limit,
          offset: offset
        })


      } else {
        order = await this.db.order.findAndCountAll({
          where: {
            status: 2
          },
          distinct:true,
          limit: limit,
          offset: offset,
        });
      }
      
      order = await queryOption.getPagingData(order, page-1, limit);
      
      res.render("admin/order/index", { data: order , notify: null});
    } catch (error) {
      console.log(error)
    }
  }

}
export default function(...args) {
  return new OrderController(...args)
}