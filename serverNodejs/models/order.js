import Sequelize from 'sequelize';
import sequelize from './db.js';

const order = sequelize.define('order', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  receiver: {
    type: Sequelize.STRING,
  },
  phone: {
    type: Sequelize.STRING,
  },
  price: {
    type: Sequelize.STRING,
  },
  address: {
    type: Sequelize.STRING,
  },
  content:{
    type: Sequelize.TEXT,
  },
  status: {
    type: Sequelize.INTEGER,
    defaultValue: 0 
  }

},{
  underscored: true,
  freezeTableName: true,
  timestamps: true
}, {
  charset: 'utf8',
  collate: 'utf8_general_ci'
});

order.associate = function(models) {
  order.belongsToMany(models.area, {
    through: "area_order",
    as: "area",
    foreignKey: "order_id",  
  });
};


export default order;