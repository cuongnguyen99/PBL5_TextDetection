import Sequelize from 'sequelize';
import sequelize from './db.js';
const users = sequelize.define('users', {
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  username: {
    type: Sequelize.STRING,
    allowNull: false,
    validate: {
        notEmpty: true,
        len: [2, 32]
    }
  },
  password: {
    type: Sequelize.STRING,
    allowNull: false,
    validate: {
        notEmpty: true,
        len: [2, 255]
    }
  },
  name: {
    type: Sequelize.STRING,
    allowNull: false,
    validate: {
        notEmpty: true,
        len: [2, 255]
    }
  },
  email: {
    type: Sequelize.STRING,
    allowNull: false,
    validate: {
        notEmpty: true,
        len: [2, 150]
    }
  },
  level: {
    type: Sequelize.INTEGER,
    defaultValue: 1 
  },
  status: {
    type: Sequelize.BOOLEAN,
    defaultValue: 1
  },
  create_time: {
    type: Sequelize.DATE,
    defaultValue: sequelize.literal('CURRENT_TIMESTAMP')
  }
},{
  underscored: true,
  freezeTableName: true,
  timestamps: false
});

users.associate = function(models) {
  users.hasMany(models.order);
};

export default users;