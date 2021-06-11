import CryptoUtill from 'crypto-js';
import models from '../models/index.js';

models()
  .then(db => db.sequelize.transaction(t => {
    let options = { raw: true , transaction: t};
    return db.users.create({
      username: 'superadmin',
      name:  'Admin',
      email: 'admin01@gmail.com',
      password: CryptoUtill.SHA256(`admin123`).toString(),
      level : 1,
      status: 1
    }, options);
  }))
  .then(() => {
    console.log('Migrated successfull');
  })
  .catch( err => {
    console.log(JSON.stringify(err));
  })