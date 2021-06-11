import models from "../models/index.js";

models()
  .then(db => db.sequelize.transaction(t => {
    let options = { raw: true , transaction: t};
    return db.sequelize.sync({ force: true });
  }))
  .then(() => {
    console.log('Migrated successfull');
  })
  .catch( err => {
    console.log(JSON.stringify(err));
  })
