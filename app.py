from flask import Flask, render_template, request, jsonify
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Configure MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["library"]
booklist=db["books"]
# mongo = pymongo(app)
# db = mongo.db.books

# Initial data to be inserted into the database
initial_data = [
    {
        "name": "Harry Potter and the Order of the Phoenix",
        "img": "https://bit.ly/2IcnSwz",
        "summary": "Harry Potter and Dumbledore's warning about the return of Lord Voldemort is not heeded by the wizard authorities who, in turn, look to undermine Dumbledore's authority at Hogwarts and discredit Harry."
    },
    {
        "name": "The Lord of the Rings: The Fellowship of the Ring",
        "img": "https://bit.ly/2tC1Lcg",
        "summary": "A young hobbit, Frodo, who has found the One Ring that belongs to the Dark Lord Sauron, begins his journey with eight companions to Mount Doom, the only place where it can be destroyed."
    },
    {
        "name": "Avengers: Endgame",
        "img": "https://bit.ly/2Pzczlb",
        "summary": "Adrift in space with no food or water, Tony Stark sends a message to Pepper Potts as his oxygen supply starts to dwindle. Meanwhile, the remaining Avengers -- Thor, Black Widow, Captain America, and Bruce Banner -- must figure out a way to bring back their vanquished allies for an epic showdown with Thanos -- the evil demigod who decimated the planet and the universe."
    }
]

# Insert initial data into the database if it's empty
if booklist.count_documents({}) == 0:
    booklist.insert_many(initial_data)

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = list(booklist.find())
    for book in books:
        book['_id'] = str(book['_id'])
    return jsonify(books)

# Route to get a single book by ID
@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = booklist.find_one({"_id": ObjectId(id)})
    if book:
        book['_id'] = str(book['_id'])
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Route to create a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book_id = booklist.insert_one(data).inserted_id
    new_book = booklist.find_one({"_id": ObjectId(book_id)})
    new_book['_id'] = str(new_book['_id'])
    return jsonify(new_book), 201

# Route to update a book by ID
@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    data = request.json
    booklist.update_one({"_id": ObjectId(id)}, {"$set": data})
    updated_book = booklist.find_one({"_id": ObjectId(id)})
    if updated_book:
        updated_book['_id'] = str(updated_book['_id'])
        return jsonify(updated_book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Route to delete a book by ID
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    result = booklist.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Book deleted successfully"})
    else:
        return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)