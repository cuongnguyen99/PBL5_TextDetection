import CryptoUtill from 'crypto-js';
import models from '../models/index.js';

function makeMoney(length) {
  let characters = '123456789';
  var result = '';
 
  var charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * 
    charactersLength));
  }
  return Number(result + '00000')
}

function make(length, type) {
  var characters = ''
  if (type =="phone") {
    characters = '0123456789';
  } else {
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  }
  var result = '';
 
  var charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * 
    charactersLength));
  }
 return result;
}

function makeName() {
  let lastName= ['Nguyen', 'Le', 'Dao', 'Ho', 'Tran', 'Do', 'Ly', 'Ninh', 'Cao', 'Truong']
  let fisrtName= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  let middleNam= ['Van', 'Thi', 'Ba', 'Viet', 'Thu']
  var charactersLength = fisrtName.length;
  let result = lastName[Math.floor(Math.random() * lastName.length)] + ' ' + middleNam[Math.floor(Math.random() * middleNam.length)]+ ' ' + fisrtName.charAt(Math.floor(Math.random() * charactersLength));
  return result;
}

function makeArea() {
  let District= ['Cam Le', 'Lien Chieu', 'Thanh Khe', 'Hai Chau', 'Ngu Hanh Son', 'Quan Son Tra']
  var charactersLength = District.length;
  let result =  District[(Math.floor(Math.random() * charactersLength))];
  return result;
}

function makeAddress(area){
  let characters = '0123456789';
  if(area == 'Cam Le'){
    let Street= ['Truong Chinh', 'Ton Dan', 'Le Trong Tan', 'Le Dai Hanh', 'Thang Long', 'Xo Viet Nghe Tinh', 'Pham Tu', 'Phan Khoi', 'Le Quang Dinh']
    let result = characters.charAt(Math.floor(Math.random() * 
    characters.length))+ ',' + Street[Math.floor(Math.random() * Street.length)] + ',' + area;
    return result
  }
  if(area == 'Lien Chieu'){
    let Street= ['Nguyen Luong Bang', 'Nguyen Tat Thanh', 'Bau tram', 'Au Co', 'Lac Long Quan', 'Nam Cao', 'Nguyen Sinh Sac', 'Kinh Duong Vuong', 'Nguyen Chanh', 'Tran Dinh Tri', 'Hoang Van Thai', 'To Huu', 'Ton Duc Thang']
    let result = characters.charAt(Math.floor(Math.random() * 
    characters.length))+ ',' + Street[Math.floor(Math.random() * Street.length)] + ',' + area;
    return result
  }
  if(area == 'Thanh Khe'){
    let Street= ['Nguyen Tat Thanh', 'Thai Thi Boi', 'Le Do', 'Truong Chinh', 'Hai Phong','Dien Bien Phu', 'Ha Huy Tap', 'Tran Cao Van', 'Nguyen Tri Phuong', 'Le Loi', 'Hung Vuong', 'Le Dinh Ly', 'Duy Tan', 'Tieu La']
    let result = characters.charAt(Math.floor(Math.random() * 
    characters.length))+ ',' + Street[Math.floor(Math.random() * Street.length)] + ',' + area;
    return result
  }
  if(area == 'Ngu Hanh Son'){
    let Street= ['Vo Nguyen Giap', 'Le Quang Dao','Phan Tu', 'Tran Van Du', 'Ho Xuan Huong', 'Hoai Thanh', 'An Duong Vuong', 'Nguyen Lu', 'Doan Khue', 'Trinh Loi', 'Vo Chi Cong']
    let result = characters.charAt(Math.floor(Math.random() * 
    characters.length))+ ',' + Street[Math.floor(Math.random() * Street.length)] + ',' + area;
    return result
  }
  if(area == 'Hai Chau'){
    let Street= ['Cao Thang', 'Le Dinh Ly', 'Hung Vuong', 'Le Loi', '3.2', 'Nguyen Chi Thanh', 'Tieu La', '2.9', 'Quang Trung', 'Dong Da', 'Nguyen Du', 'Ly Tu Trong', 'Hoang Dieu', 'Ong ich Khiem', 'Nguyen Hoan', 'Thai Phien', 'Le Hong Phong']
    let result = characters.charAt(Math.floor(Math.random() * 
    characters.length))+ ',' + Street[Math.floor(Math.random() * Street.length)] + ',' + area;
    return result
  }
  if(area == 'Quan Son Tra'){
    let Street= ['Yet Kieu', 'Ly Tu Tan', 'Hoang Xa', 'Le Duc Tho', 'Phan Ba Phien', 'Tran Nhan Tong', 'Truog Dinh', 'Chu Huy Man', 'Nai Hien Dong', 'Duong Lam', 'Le Van Duyet', 'Duong Van Nga', 'Le Chan', 'Ngo Quyen']
    let result = characters.charAt(Math.floor(Math.random() * 
    characters.length))+ ',' + Street[Math.floor(Math.random() * Street.length)] + ',' + area;
    return result
  }

}

models()
  .then(db => db.sequelize.transaction(async t => {
    const values = [];
    let data = null;
    let area = null;
    let areaData = null;

    for(var i =0 ; i < 20; i++) {
      areaData = makeArea()
      area = await db.area.create({
        name: areaData,
        city: "Da Nang"
      });

      data = await db.order.create({
        receiver: makeName(),
        phone: `09${make(8, 'phone')}`,
        price: `${makeMoney(2)}`,
        address: makeAddress(areaData),
        content: 'Mua tai nghe khong',
        status: 0,
        areas: [{
          id: area.id,
          area_order:{
            selfGranted: true
          }
        },{
          include: db.area
        }]
      });

      await data.addArea(area, { through: { selfGranted: false } });
      data = null;
      area = null;
    }
    return true;
  }))
  .then(() => {
    console.log('Migrated successfull');
  })
  .catch( err => {
    console.log(err);
  })