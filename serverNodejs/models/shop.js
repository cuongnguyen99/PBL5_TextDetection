import Sequelize from 'sequelize';
import sequelize from './db.js';

const shop = sequelize.define('shop', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  shopCode: {
    type: Sequelize.STRING,
  	allowNull: {
  		notEmpty: true,
 	    len: [1, 255]
  	}
  },
  name: {
    type: Sequelize.STRING,
  	allowNull: {
  		notEmpty: true,
 	    len: [1, 255]
  	}
  }
},{
  underscored: true,
  freezeTableName: true,
  timestamps: false
}, {
  charset: 'utf8',
  collate: 'utf8_general_ci'
});

shop.associate = function(models) {
  shop.hasMany(models.order);
};

export default shop;