

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
    let date_ob = new Date();
    let date = ("0" + date_ob.getDate()).slice(-2);

    // current month
    let month = ("0" + (date_ob.getMonth() + 1)).slice(-2);

    res.render("index");
  }
}

export default function(...args) {
  return new HomeController(...args)
}