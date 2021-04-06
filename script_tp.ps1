#Problème de parsing avec sid1.json

PS C:\Users\lasagne\Desktop> mongoimport --db dbname --collection restaurants --drop --file sid1.json --jsonArray
2021-03-02T17:13:57.071+0100    connected to: mongodb://localhost/
2021-03-02T17:13:57.108+0100    dropping: dbname.restaurants
2021-03-02T17:13:57.108+0100    Failed: error reading separator after document #1: bad JSON array format - found no opening bracket '[' in input source
2021-03-02T17:13:57.108+0100    0 document(s) imported successfully. 0 document(s) failed to import.
PS C:\Users\lasagne\Desktop>

#Ça marche avec data.json

PS C:\Users\lasagne\Desktop> mongoimport --db dbname --collection restaurants --drop --file data.json --jsonArray
2021-03-02T17:19:46.781+0100    connected to: mongodb://localhost/
2021-03-02T17:19:46.817+0100    dropping: dbname.restaurants
2021-03-02T17:19:47.004+0100    3772 document(s) imported successfully. 0 document(s) failed to import.
PS C:\Users\lasagne\Desktop>

db.restaurants.find().pretty()

db.restaurants.find({},{ restaurant_id: 1, name: 1, borough: 1, cuisine: 1 }).pretty()

db.restaurants.find({},{ restaurant_id: 1, name: 1, borough: 1, cuisine: 1, _id: 0 }).pretty()

db.restaurants.find({},{ "restaurant_id": 1, "name": 1, "borough": 1, "cuisine": 1, "address.zipcode": 1, "_id": 0 }).pretty()

db.restaurants.find({ "borough": "Bronx" }).pretty()

db.restaurants.find({ "borough": "Bronx" }).limit(5).pretty()

db.restaurants.find({ "borough": "Bronx" }).limit(5).skip(5).pretty()

db.restaurants.find({ "borough": "Bronx" }).pretty()

db.restaurants.find({ "borough": "Bronx" }).pretty()

db.restaurants.find({ "grades.score": { $gt: 90 }}).pretty()

db.restaurants.find({ "grades.score": { $gt: 80, $lt: 100 }}).pretty()

db.restaurants.find({ "address.coord": { $lt: -95.754168 }}).pretty()

db.restaurants.find({$and:[
        { "cuisine": { $ne: "American " }}, 
        { "grades.score": { $gt: 70 }}, 
        { "address.coord": { $lt: -65.754168 }}
]}).pretty()

db.restaurants.find({
        "cuisine": { $ne: "American " }, 
        "grades.score": { $gt: 70 }, 
        "borough": { $ne: "Bronx" }
}).pretty()

db.restaurants.find({
        "cuisine": { $ne: "American " }, 
        "grades.grade": "A", 
        "borough": { $ne: "Brooklyn" }
}).sort({ "cuisine":-1 }).pretty()

db.restaurants.find(
        { "name": /^Wil/ },
        { "restaurant_id": 1, 
        "name":1,
        "borough":1,
        "cuisine":1
        }).pretty()

db.restaurants.find(
        { "name": /ces$/ },
        { "restaurant_id": 1, 
        "name":1,
        "borough":1,
        "cuisine":1
        }).pretty()

db.restaurants.find(
        { "name": /.*Reg.*/ },
        { "restaurant_id": 1, 
        "name":1,
        "borough":1,
        "cuisine":1
        }).pretty()

db.restaurants.find({
    $or: [
        {"cuisine": "American "}, 
        {"cuisine": "Chinese"}
    ], "borough": "Bronx" 
}).pretty()

db.restaurants.find(
{"borough": {$in :["Staten Island", "Queens", "Bronx", "Brooklyn"]}},
{
"restaurant_id": 1,
"borough": 1,
"name": 1,
"cuisine": 1
}).pretty()

db.restaurants.find(
{"borough": {$nin :["Staten Island", "Queens", "Bronx", "Brooklyn"]}},
{
"restaurant_id": 1,
"borough": 1,
"name": 1,
"cuisine": 1
}).pretty()

db.restaurants.find(
{"grades.score" : {$lt : 10}},
{
"restaurant_id": 1,
"borough": 1,
"name": 1,
"cuisine": 1
}).pretty()

db.restaurants.find(
{$or: [ 
    {"cuisine": {$ne: "American "}, 
     "cuisine": {$ne: "Chinese"}
   }, { name: /^Wil/ }
]},
{
"restaurant_id": 1,
"borough": 1,
"name": 1,
"cuisine": 1
}).pretty()

db.restaurants.find( 
{
    "grades.date": ISODate("2014-08-11T00:00:00Z"), 
    "grades.grade": "A", 
    "grades.score" : 11
}, 
{
    "restaurant_id": 1,
    "borough": 1,
    "name": 1,
    "grades": 1
}).pretty()

db.restaurants.find( 
{ 
    "grades.1.date": ISODate("2014-08-11T00:00:00Z"), 
    "grades.1.grade": "A", 
    "grades.1.score": 9
}, 
{
    "restaurant_id": 1,
    "borough": 1,
    "name": 1,
    "grades": 1
}).pretty()



db.restaurants.find( 
{ 
    "address.coord.1": { $gt : 42, $lt : 52 }
},
{
    "restaurant_id": 1,
    "borough": 1,
    "name": 1,
    "cuisine": 1
}).pretty()

db.restaurants.find().sort({"name": 1}).pretty()

db.restaurants.find().sort({"name": -1}).pretty()

db.restaurants.find().sort({"cuisine": 1, "borough": -1,}).pretty()

db.restaurants.find({"address.street" : { $exists : true }}).count()
#compared to 
db.restaurants.find({}, {"address.street": 1}).count()

db.restaurants.find({ "address.coord": { $type: "double"} }).pretty()

db.restaurants.find(
{
    "grades.score": { $mod: [7, 0]}
},
{
    "restaurant_id": 1,
    "name": 1,
    "grades": 1
}).pretty()

db.restaurants.find(
{ "name" :  /.*mon.*/ },
{
    "name": 1,
    "borough": 1,
    "address.coord": 1,
    "cuisine": 1
}
).pretty()

db.restaurants.find(
{ "name" :  /^Mad/ },
{
    "name": 1,
    "borough": 1,
    "address.coord": 1,
    "cuisine": 1
}
).pretty()