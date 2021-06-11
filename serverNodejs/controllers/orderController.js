import CryptoJS  from "crypto-js";

class OrderController {
  constructor(db) {
      this.db = db
  }

  async index(req, res) {
    res.locals.user = req.session.userName;
    let order = await this.db.order.findAll();
    res.render("admin/order/index", { data: order , notify: null});
  };

  async addOrderForm(req,res) {
    const notify = null;
    res.render("admin/order/addOrder");
  }

  async addOrder(req, res) {
    try {
      const params = req.body;
      if(params) {
        
        // const data  = await this.db.order.create({
        //   name: params.name,
        //   username: params.username,
        //   email: params.email,
        //   password: CryptoJS.SHA256(params.password).toString()
        // });

        if(!data) {
          res.redirect('/admin/orders/new_order');
        }
        res.redirect('/admin/orders');
        // res.redirect('..');
      }
      res.redirect('/admin/orders/new_order');
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
        res.redirect('/admin/orders' );
      }
      res.redirect('/admin/orders');
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

      res.render("admin/order/editOrder", { data: Orderedit});
    } else {
      res.redirect('/admin/orders' );
    }
    
  };

  async update(req, res) {
    await this.db.order.update({ 
      name: req.body.name, 
      code: req.body.code 
    }, { 
      where: { id: req.params.id } 
    });
    res.send('success!');
  };
}
export default function(...args) {
  return new OrderController(...args)
}