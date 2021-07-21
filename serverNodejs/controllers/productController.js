import CryptoJS  from "crypto-js";

class ProductController {
  constructor(db) {
      this.db = db
  }

  async index(req, res) {
    res.locals.user = req.session.userName;
    let product = await this.db.product.findAll({ attributes: ['id', 'username', 'name', 'mst'] });
    res.render("admin/product/index", { data: product , notify: null});
  };

  
}
export default function(...args) {
  return new ProductController(...args)
}