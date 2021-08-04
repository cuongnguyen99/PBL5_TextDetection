class Query {
  static async getPagingData(data, page, limit) {
    try {
     
      const { count: totalItems, rows: value } = data;
      const currentPage = page ? +page : 0;
      const totalPages = Math.ceil(totalItems / limit);

      return { totalItems, value, totalPages, currentPage };
     
    } catch (error) {
      console.log(error)
    }
   
  };

  static async getPagination(page, size) {
    const limit = size ? +size : 10;
    const offset = page ? page * limit : 0;
  
    return { limit, offset };
  };
}


export default Query;