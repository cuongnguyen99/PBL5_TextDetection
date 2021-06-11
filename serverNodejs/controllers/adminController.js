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
	
	async loginform(req,res){
		res.locals.user = req.session.user;
		res.render("admin/login");
	};
	
	async login(req,res){
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
            var ciphertext =  await this.encrypt(data);
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
    res.render("admin/index");
  }

	// async registerform(req,res){
	// 	res.locals.user = req.session.user;
	// 	res.render("login/register");
	// };

	// async register(req,res){
	// 	await this.db.staffs.create({
	// 		name: req.body.name,
	// 		phone: req.body.username,
	// 		password: CryptoJS.hash(req.body.password),
  //     isAdmin: 1
  //   });

	// 	const roles='admin';
	// 	Session.addSession(req,res,req.body.username, roles);
	// 	transporter.sendMail(mailOptions, function(error, info){
	// 		if (error) {
	// 			console.log(error);
	// 		} else {
	// 			console.log('Email sent: ' + info.response);
	// 		}
	// 	});
	// 	res.redirect('/companies',res,req);
	// };

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