import session from "express-session";

class Middleware{
	static isLoggedIn(req, res, next) {
    let sess= req.session;
    if (sess.userName!=null ){
        return next();
    }else{
    	  res.redirect('/login');
    }
	};

	static checkLogin(req,res,next){
		let sess= req.session;
		if(sess.userName!=null){
			res.redirect('/');
		}else{
			return next();
		}
	};
	
  static isAdmin(req,res,next){
  	let sess= req.session;
  	if(sess.roles=='admin'){
  		return next();
  	}else{
  		res.redirect('/');
  	}
  }
}
export default Middleware;