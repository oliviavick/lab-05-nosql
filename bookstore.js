// Lab 05 - NoSQL
// Case Study 1: Bookstore Inventory

// Step 2: Select the bookstore database
db = db.getSiblingDB("bookstore");

// Step 3: Load authors
db.authors.drop();
var doc = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(doc);

// Step 4: Load books
db.books.drop();
doc = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(doc);

// Step 5: List authors and books
print("ALL AUTHORS:");
db.authors.find().forEach(printjson);

print("ALL BOOKS:");
db.books.find().forEach(printjson);

// Step 6: Insert two new books
db.books.insertMany([
    {
      title: "The Great Gatsby",
      published_year: 1925,
      author_ids: ["author_004"]
    },
    {
        {
            title: "Emma",
            published_year: 1815,
            author_ids: ["author_001"]
          }
    }
  ]);
  
  // Step 7: Add missing author
  db.authors.insertOne({
    _id: "author_004",
    name: "F. Scott Fitzgerald",
    nationality: "American",
    bio: {
      short: "American novelist known for The Great Gatsby.",
      long: "F. Scott Fitzgerald was an American writer known for his novels about the Jazz Age."
    }
  });
  
  // Step 8: Filter books by selected authors
  print("BOOKS BY SELECTED AUTHORS:");
  
  db.books.find({
    author_ids: {
      $in: ["author_001", "author_004"]
    }
  }).forEach(printjson);
