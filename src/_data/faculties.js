const file = './data/organiclinks_db.csv'

const fs = require('fs');
const csv = require('@fast-csv/parse');

module.exports = () => {
  return new Promise((resolve, reject) => {
    var objects = []
    csv.parseFile(file, {'headers': true})
    .on('error', error => console.error(error))
    .on('data', row => {
      // console.log(`ROW=${JSON.stringify(row)}`)

      objects.push(row)
    })
    .on('end', rowCount => {
      // console.log(`Parsed ${rowCount} rows`)
      // console.log(objects)
      return resolve(objects)
    });
  })
}
