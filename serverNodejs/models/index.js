import Sequelize from 'sequelize';
import sequelize from './db.js';

export default async() => {
  let db = {};
  
  let modelUsers = await import(`./users.js`);
    modelUsers = modelUsers.default;
    db[modelUsers.tableName] = modelUsers;
      
  // let modelAddress = await import(`./address.js`);
  //   modelAddress = modelAddress.default;
  //   db[modelAddress.tableName] = modelAddress;

  let modelOrder = await import(`./order.js`);
    modelOrder = modelOrder.default;
    db[modelOrder.tableName] = modelOrder;

  // let modelProduct = await import(`./product.js`);
  //   modelProduct = modelProduct.default;
  //   db[modelProduct.tableName] = modelProduct;

  // let modelShop = await import(`./shop.js`);
  //   modelShop = modelShop.default;
  //   db[modelShop.tableName] = modelShop;

  Object.keys(db).forEach(modelName => {
    if (db[modelName].associate) {
      db[modelName].associate(db);
    }
  });
  
  db.sequelize = sequelize;
  db.Sequelize = Sequelize;
  db.Op = Sequelize.Op;
  return db
   
};