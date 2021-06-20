import CryptoJS  from "crypto-js";

class OrderController {
  constructor(db) {
      this.db = db
  }

  async index(req, res) {
    try {
      let order = null;
      
      res.locals.user = req.session.userName;
      if(req.query.search) {
        order = await this.db.order.findAll({
          where: {
            [this.db.Op.or]: [
              { receiver: req.query.search },
              { phone: req.query.search },
              { address: req.query.search }
            ]
          }
        })


      } else {
        order = await this.db.order.findAll();
      }
      
      res.render("admin/order/index", { data: order , notify: null});
      
    } catch (error) {
      console.log(error)
    }
   
  };

  async addOrderForm(req,res) {
    const notify = null;
    res.render("admin/order/addOrder");
  }

  async addOrder(req, res) {
    try {
      const params = req.body;
      if(!params.area || !params.receiver || !params.phone || !params.price || !params.address) {
  		  return res.redirect('/admin/orders/new_order');
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
        return res.redirect('/admin/orders/new_order');
      }

    	return res.status(200).redirect('/admin/orders');
      
    } catch (error) {
      console.log(error);
      res.redirect('/admin/orders/new_order');
    }
  };

  async delete(req, res) {
    try {
      const data = await this.db.order.destroy({
        where: {
            id: req.params.id
        },
        force: true
      });

      if( !data) {
        return res.redirect('/admin/orders' );
      }

      return res.redirect('/admin/orders');
    } catch (error) {
      console.log(error);
    }
  };

  
  async editform(req, res) {
    if(req.params.id) {
      let Orderedit = await this.db.order.findOne({
        where: {
            id: req.params.id
        },
        force: true
      });

      if(!Orderedit) {
        res.redirect('/admin/orders' );
      }

      return res.render("admin/order/editOrder", { data: Orderedit});
    } else {
      return res.redirect('/admin/orders' );
    }
    
  };

  async update(req, res) {
    try {
      if(req.params.id) {
        const params = req.body;

        if(!params.area || !params.receiver || !params.phone || !params.price || !params.address) {
          return res.redirect('/admin/orders/new_order');
        }

        const data = await this.db.order.update({ 
          receiver: params.receiver,
          area: params.area,
          phone: params.phone,
          price: params.price,
          address: params.address,
          content: params.content,
          status: 2
        }, { 
          where: { id: req.params.id } 
        });

        if(!data) {
          return res.redirect('/admin/orders/edit/'+ req.params.id );
        }

        return res.redirect('/admin/orders');
      }

      return res.status(400).redirect('/admin/orders/');
      
    } catch (error) {
      return res.redirect('/admin/orders' );
    }
    
  };
}
export default function(...args) {
  return new OrderController(...args)
}