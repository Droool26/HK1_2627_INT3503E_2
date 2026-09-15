from flask import Flask, jsonify, request

app = Flask(__name__)

# --- GỐC: Data và biến tăng tự động (Slide 24) ---
_next = 3
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin", "year": 2008},
    {"id": 2, "title": "Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999}
]

def find(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)

# --- 1. LIST & SEARCH (GET /books) ---
@app.route("/books", methods=["GET"])
def list_books():
    # MỞ RỘNG (a) & (b): Lấy tham số tìm kiếm và sắp xếp
    q = request.args.get("q", "").strip().lower()
    sort_by = request.args.get("sort", "").strip().lower()
    limit = int(request.args.get("limit", 100)) # Gốc: Giới hạn số lượng

    filtered_books = BOOKS
    
    # MỞ RỘNG (a): Tìm kiếm GET /books?q=...
    if q:
        filtered_books = [b for b in filtered_books if q in b["title"].lower()]

    # MỞ RỘNG (b): Sắp xếp GET /books?sort=title
    if sort_by == "title":
        filtered_books = sorted(filtered_books, key=lambda x: x["title"].lower())

    return jsonify(filtered_books[:limit]), 200

# --- 2. DETAIL (GET /books/<id>) ---
# GỐC (Hoàn toàn không có mở rộng)
@app.route("/books/<int:bid>", methods=["GET"])
def get_book(bid):
    book = find(bid)
    if not book:
        return jsonify({"error": "not found"}), 404
    return jsonify(book), 200

# --- 3. CREATE (POST /books) ---
@app.route("/books", methods=["POST"])
def create_book():
    global _next
    body = request.get_json(silent=True) or {}
    t = body.get("title")
    a = body.get("author")
    
    # GỐC: Bắt buộc title và author
    if not t or not a:
        return jsonify({"error": "need title+author"}), 400
        
    # MỞ RỘNG (c): Bắt buộc field year là số >= 1900
    year = body.get("year")
    if not isinstance(year, int) or year < 1900:
        return jsonify({"error": "year must be an integer >= 1900"}), 400
        
    # GỐC: Thêm sách mới
    book = {"id": _next, "title": t, "author": a, "year": year}
    _next += 1
    BOOKS.append(book)
    return jsonify(book), 201, {"Location": f"/books/{book['id']}"}

# --- 4 & 5. UPDATE (PUT) VÀ DELETE (DELETE) ---
@app.route("/books/<int:bid>", methods=["PUT", "DELETE"])
def modify_book(bid):
    book = find(bid)
    if not book:
        return jsonify({"error": "not found"}), 404
        
    if request.method == "PUT":
        body = request.get_json(silent=True) or {}
        
        # MỞ RỘNG: Vì update (PUT) có thể thay đổi year, ta cũng cần validate
        if "year" in body:
            year = body["year"]
            if not isinstance(year, int) or year < 1900:
                return jsonify({"error": "year must be an integer >= 1900"}), 400
                
        # GỐC: Cập nhật object book
        book.update(body)
        return jsonify(book), 200
        
    # GỐC: method == DELETE
    BOOKS.remove(book)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
