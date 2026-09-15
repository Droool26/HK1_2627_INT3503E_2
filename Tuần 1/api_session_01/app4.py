from flask import Flask, jsonify, request

app = Flask(__name__)

# Giả lập database
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin"},
    {"id": 2, "title": "Pragmatic Programmer", "author": "Andrew Hunt"},
    {"id": 3, "title": "Python Crash Course", "author": "Eric Matthes"}
]

# Tìm sách theo ID
def find_by_id(book_id):
    return next((b for b in BOOKS if b["id"] == book_id), None)

#Path param - biến trong URL
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_by_id(book_id)
    
    if book is None:
        return jsonify({"error": "not found"}), 404
        
    return jsonify(book), 200

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    return jsonify({"id": item_id}), 200

# Query strings - bộ lọc/phân trang
@app.route("/books", methods=["GET"])
def list_books():
    limit = int(request.args.get("limit", 100))
    
    q = request.args.get("q", "").strip().lower()
    
    filtered_books = [book for book in BOOKS if q in book["title"].lower()]
    
    return jsonify({"items": filtered_books[:limit]}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
