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
    charset: 'utf8',
    collate: 'utf8_general_ci', 
    timestamps: true
  },
  logging:false
};
const sequelize = new Sequelize('doanki2', 'root', 'adminPhuc@123', connectionOptions);

export default sequelize; 