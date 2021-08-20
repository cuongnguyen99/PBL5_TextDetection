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
            return res.redirect('/',res,req);
			  }else{
			   	return res.redirect('/login');
			  }
			}
      return res.redirect('/login');
		}else{
		  return res.redirect('/login');
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

		let OrderInDay = await this.db.order.count({
			where: await this.db.Sequelize.where(await this.db.Sequelize.fn('DATE', await this.db.Sequelize.col('created_at')), data)
    })

		let OrderInMonth = await this.db.order.count({
			where: [ 
				await this.db.Sequelize.where(await this.db.Sequelize.fn('MONTH', await this.db.Sequelize.col('created_at')), month),
				await this.db.Sequelize.where(await this.db.Sequelize.fn('YEAR', await this.db.Sequelize.col('created_at')), year)
			]
    })

		let AllOrder = await this.db.order.count({
			status: 0
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

		let allAreaInMonth = await this.db.area.findAll({
			group: ['name'],
			include: [{
				model: this.db.order, 
				as:"order",
				where: [ 
					await this.db.Sequelize.where(await this.db.Sequelize.fn('MONTH', await this.db.Sequelize.col('order.created_at')), month),
					await this.db.Sequelize.where(await this.db.Sequelize.fn('YEAR', await this.db.Sequelize.col('order.created_at')), year)
				]
			}],
			attributes: ['name', [this.db.Sequelize.fn('COUNT', this.db.Sequelize.col('order.id')),'num']],
		})

		let allAreaInDay = await this.db.area.findAll({
			
			include: [{
					model: this.db.order, 
					as:"order",
					where: [ 
						await this.db.Sequelize.where(await this.db.Sequelize.fn('DATE', await this.db.Sequelize.col('order.created_at')), data)
					]
			}],
		})

		let arrayAreaMonth = [];
		let totalMonth = null;
		let JsondataMonth = {}
		allAreaInMonth.forEach(element => {
			totalMonth += element.dataValues.num;
			JsondataMonth[element.name]=element.dataValues.num;
			arrayAreaMonth.push(element.name);
		});

		
		let arrayAreaDay = [];
		let totalDay = null;
		let JsondataDay = {}
		allAreaInDay.forEach(element => {
			totalDay += element.order.length;
			JsondataDay[element.name]= element.order.length;
			arrayAreaDay.push(element.name);
		});
		

    const data2 = {
      orderInDay : OrderInDay,
			orderInMonth: OrderInMonth,
			errorOrder: ErrorOrder,
			updatedErrorOrder: UpdatedErrorOrder,
			arrayAreaMonth: arrayAreaMonth,
			totalMonth: totalMonth,
			JsondataMonth: JSON.stringify(JsondataMonth),
			allAreaInDay: allAreaInDay,
			allOrder:AllOrder,
			arrayColor: ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'],
			
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