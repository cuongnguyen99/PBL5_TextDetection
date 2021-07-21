import session from "express-session";
import CryptoJS  from "crypto-js";


class apisMiddleware{

	static async rolesApi(req, res, next){
		let token= req.headers.token;
		if(token && token!="undefined"){
			try{
				const decrypted = await apisMiddleware.decryptToken(token);
				if(decrypted.expiredAt > Date.now()/1000){
					return next();
				}else{
					let error="Old token"
					return res.json({ TRAVE: false, messenger: error});
				}
			}catch(err){
				console.log(err);
			}
		}
	};

	static async isBank(req,res,next){
		let token= req.headers.token;
		if(token && token!="undefined"){
			try{
				const decrypted = await apisMiddleware.decryptToken(token);
				
				if(decrypted.roles=='bank'){
					return next();
				}else{
					let error="bank required!!!"
          return res.json({ TRAVE: false, messenger: error});
				}
			}catch(err){
				console.log(err);
			}
		}
	}

  static async isParter(req,res,next){
		let token= req.headers.token;
		if(token && token!="undefined"){
			try{
				const decrypted = await apisMiddleware.decryptToken(token);
				
				if(decrypted.roles=='parter'){
					return next();
				}else{
					let error="parter required!!!"
          return res.json({ TRAVE: false, messenger: error});
				}
			}catch(err){
				console.log(err);
			}
		}
	}

	static async decryptToken(token) {
    return new Promise((resolve, reject) => {
      try {
        let decrypted = CryptoJS.AES.decrypt(token,'abcxyzaaannnasiohandcaoejdfpoqiwe');
        let decryptedData = JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
        if(decryptedData && decryptedData !== '') {
          resolve(decryptedData);
        } else {
          reject(new Error('invalid token'));
        }
      } catch(e) {
        reject(new Error('invalid token'));
        console.log(e);
      }
   	});
	}

}
export default apisMiddleware;