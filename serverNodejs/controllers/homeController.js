class HomeController {
  constructor(db) {
    this.db = db
  }

  async getHome(req, res) {
    const locals = {
        title: 'Index',
        description: 'Page Description',
        header: 'Index Page'
    };
   
    
    res.render("index");
  }
}

export default function(...args) {
  return new HomeController(...args)
}