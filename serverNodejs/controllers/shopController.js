import CryptoJS  from "crypto-js";

class ShopController {
  constructor(db) {
      this.db = db
  }

  async index(req, res) {
    res.locals.user = req.session.userName;
    let shop = await this.db.shop.findAll({ attributes: ['id', 'shop_code', 'name'] });
    res.render("admin/shop/index", { data: shop , notify: null});
  };

  
}
export default function(...args) {
  return new ShopController(...args)
}