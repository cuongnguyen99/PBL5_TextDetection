import Sequelize from 'sequelize';
import sequelize from './db.js';

const address = sequelize.define('address', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  name: {
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

address.associate = function(models) {
  address.belongsToMany(models.order, {
    through: "address_order",
    as: "order",
    foreignKey: "address_id",
  });
};
export default address;