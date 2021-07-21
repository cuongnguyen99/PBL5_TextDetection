import Sequelize from 'sequelize';

const connectionOptions = {
  host: 'localhost',
  dialect: 'mysql',

  pool: {
    max: 5,
    min: 0,
    idle: 10000
  },
  define: {
    timestamps: true
  }
};
const sequelize = new Sequelize('doanki2', 'root', 'admin123', connectionOptions);

export default sequelize; 