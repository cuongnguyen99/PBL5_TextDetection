import CryptoJS  from "crypto-js";

class UserController {
  constructor(db) {
      this.db = db
  }

  async index(req, res) {
    res.locals.user = req.session.userName;
    let users = await this.db.users.findAll({ attributes: ['id', 'username', 'name', 'email'] });
    res.render("admin/user/index", { data: users , notify: null});
  };

}
export default function(...args) {
  return new UserController(...args)
}