import Sequelize from 'sequelize';
import sequelize from './db.js';

const area = sequelize.define('area', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  name: {
    type: Sequelize.STRING,
    allowNull: false
  },
  city: {
    type: Sequelize.STRING,
  }
},{
  underscored: true,
  freezeTableName: true,
  timestamps: false
}, {
  charset: 'utf8',
  collate: 'utf8_general_ci'
});

area.associate = function(models) {
  area.belongsToMany(models.order,{
    through: "area_order",
    as: "order",
    foreignKey: "area_id", 
  });
};
export default area;