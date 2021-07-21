import Sequelize from 'sequelize';
import sequelize from './db.js';

const product = sequelize.define('product', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  productCode: {
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
  },
  price: {
    type: Sequelize.DECIMAL(25, 1),
    allowNull: false
  },
  promotePrice: {
    type: Sequelize.DECIMAL(25, 1),
    allowNull: false
  }
},{
  underscored: true,
  freezeTableName: true,
  timestamps: false
}, {
  charset: 'utf8',
  collate: 'utf8_general_ci'
});

product.associate = function(models) {
  product.belongsToMany(models.order, {
    through: "product_order",
    as: "order",
    foreignKey: "product_id",
  });
};

export default product;