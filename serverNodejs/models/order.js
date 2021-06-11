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
  	allowNull: {
  		notEmpty: true,
 	    len: [1, 255]
  	}
  },
  area: {
    type: Sequelize.STRING,
  	allowNull: {
  		notEmpty: true,
 	    len: [1, 255]
  	}
  },
  phone: {
    type: Sequelize.STRING,
  	allowNull: {
  		notEmpty: true,
 	    len: [1, 255]
  	}
  },
  price: {
    type: Sequelize.DECIMAL(25, 1),
    allowNull: false
  },
  address: {
    type: Sequelize.STRING,
  	allowNull: {
  		notEmpty: true,
 	    len: [1, 255]
  	}
  },
  content:{
    type: Sequelize.TEXT,
    allowNull: {
  		notEmpty: true,
 	    len: [1, 255]
  	}
  }
  // orderCode: {
  //   type: Sequelize.STRING,
  // 	allowNull: {
  // 		notEmpty: true,
 	//     len: [1, 255]
  // 	}
  // },
  // name: {
  //   type: Sequelize.STRING,
  // 	allowNull: {
  // 		notEmpty: true,
 	//     len: [1, 255]
  // 	}
  // },
  // subPrice: {
  //   type: Sequelize.DECIMAL(25, 1),
  //   allowNull: false
  // },
  // shipPrice: {
  //   type: Sequelize.DECIMAL(25, 1),
  //   allowNull: false
  // },
  // totalPrice: {
  //   type: Sequelize.DECIMAL(25, 1),
  //   allowNull: false
  // }

},{
  underscored: true,
  freezeTableName: true,
  timestamps: false
}, {
  charset: 'utf8',
  collate: 'utf8_general_ci'
});

// order.associate = function(models) {
//   order.belongsToMany(models.address, {
//     through: "address_order",
//     as: "address",
//     foreignKey: "order_id",
//   });
// };

// order.associate = function(models) {
//   order.belongsToMany(models.product, {
//     through: "product_order",
//     as: "product",
//     foreignKey: "order_id",
//   });
// };

// order.associate = function(models) {
//   order.belongsTo(models.users);
// };

// order.associate = function(models) {
//   order.belongsTo(models.shop);
// };

export default order;