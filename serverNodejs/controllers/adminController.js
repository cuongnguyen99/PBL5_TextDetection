import Middleware from '../middleware/admin-middleware.js';
import sha256 from 'crypto-js/sha256.js';
import Base64 from 'crypto-js/enc-base64.js';
import session from "express-session";
import CryptoJS  from "crypto-js";

const key ="abcxyzaaannnasiohandcaoejdfpoqiwe";


class AdminController{
	constructor(db){
      this.db =db
  };
	
	async loginform(req,res) {
		res.locals.user = req.session.user;
		res.render("admin/login");
	};
	
	async login(req,res) {
		if(req.body.username){
			let admin = await this.db.users.findOne({
				attributes:['id','username','email','password'],
				where:{
					username: req.body.username
				}
			});
      
	    if(admin){
		   	if(await this.compare(admin.password,req.body.password)){
            const roles='admin';
            await this.addSession(req , res , req.body.username, roles);
            var data = [{ userId: admin.id}, { userName: admin.phone}, {roles: roles }, { expiredAt: Math.floor(Date.now() / 1000) + (60 * 60)}]
            return res.redirect('/admin',res,req);
			  }else{
			   	return res.redirect('/admin/login');
			  }
			}
      return res.redirect('/admin/login');
		}else{
		  return res.redirect('/admin/login');
		}
	};

	async logout(req,res){
		if(this.destroySession(req,res)){
			return res.redirect('/');
		}else{
			console.log("error");
		}
	}

  async dashboard(req,res) {
		let date_ob = new Date();
    let date = ("0" + date_ob.getDate()).slice(-2);

    // current month
    let month = ("0" + (date_ob.getMonth() + 1)).slice(-2);
		// current year
		let year = date_ob.getFullYear();
    
		const data = year+'-'+month+'-'+date
    

		const Op = this.db.Op;

		let OrderInDay=await this.db.order.count({
			where: await this.db.Sequelize.where(await this.db.Sequelize.fn('DATE', await this.db.Sequelize.col('created_at')), data)
    })

		let OrderInMonth=await this.db.order.count({
     
			where: [ 
				await this.db.Sequelize.where(await this.db.Sequelize.fn('MONTH', await this.db.Sequelize.col('created_at')), month),
				await this.db.Sequelize.where(await this.db.Sequelize.fn('YEAR', await this.db.Sequelize.col('created_at')), year)
			]
    })

		let ErrorOrder = await this.db.order.count({
			where: {
				status: 1
			}
		})

		let UpdatedErrorOrder = await this.db.order.count({
			where: {
				status: 2
			}
		})

    const data2 = {
      orderInDay : OrderInDay,
			orderInMonth: OrderInMonth,
			errorOrder: ErrorOrder,
			updatedErrorOrder: UpdatedErrorOrder,
    }

    res.render("admin/index", { data: data2});
  }

  async compare(password,code){
    const crypt= await this.hash(code);
    if(crypt === password){
      return true;
    }else{
      return false;
    }
  }

  async encrypt(data){
    const ciphertext = CryptoJS.AES.encrypt(JSON.stringify(data), key).toString();
    return ciphertext;
  }

  async decrypt(data){
    var bytes  = CryptoJS.AES.decrypt(data, key);
    var decryptedData = JSON.parse(bytes.toString(CryptoJS.enc.Utf8));
    return decryptedData;
  }

  async hash(data){
    return sha256(data).toString();
  }

  async addSession(req,res,userName, roles){
    req.session.userName=userName;
    req.session.roles=roles;
    return true;
  }

  async destroySession(req,res){
    return new Promise((resolved, reject) => {
      req.session.destroy((err) => {
        if(err) {
          reject(false);
        }
      });
      resolved(true);
    });
  }
}
export default function(...args) {
    return new AdminController(...args)
}