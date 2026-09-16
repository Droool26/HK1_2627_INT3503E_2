# app2.py — bài 2: GET <id>, PUT, PATCH, DELETE
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

# Mồi sẵn 1 cuốn sách có id=1 để test luôn
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin", "price": 50.0}
]

# —— GET /books/<id> —— Lấy thông tin 1 cuốn sách (có thêm Cache)
@app.get("/books/<int:bid>")
def fetch(bid):
    # Tìm index (i) của cuốn sách trong mảng BOOKS
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None: 
        return jsonify(error="not found"), 404
        
    resp = make_response(jsonify(BOOKS[i]), 200)
    resp.headers["Cache-Control"] = "max-age=60"
    return resp

# —— PUT /books/<id> —— Thay thế TOÀN BỘ cuốn sách
@app.put("/books/<int:bid>")
def put(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None: return jsonify(error="not found"), 404
        
    p = request.get_json(silent=True) or {}
    t, a = p.get("title"), p.get("author")
    
    # PUT bắt buộc phải gửi lại đủ thông tin quan trọng
    if not t or not a: 
        return jsonify(error="need title+author"), 422
        
    # Ghi đè lại hoàn toàn object sách
    BOOKS[i] = {
        "id": bid, 
        "title": t.strip(), 
        "author": a.strip(), 
        "isbn": p.get("isbn"), 
        "price": p.get("price")
    }
    return jsonify(BOOKS[i]), 200

# —— PATCH /books/<id> —— Chỉ cập nhật MỘT PHẦN (vá)
@app.patch("/books/<int:bid>")
def patch(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None: return jsonify(error="not found"), 404
        
    p = request.get_json(silent=True) or {}
    
    if p.get("price", 0) < 0:
        return jsonify(error="price must be positive"), 422
        
    # Lặp qua các key, ngta gửi key nào lên thì mình update key đó
    for k in "title author isbn price".split():
        if k in p: 
            BOOKS[i][k] = p[k]
            
    return jsonify(BOOKS[i]), 200

# —— DELETE /books/<id> —— Xóa sách
@app.delete("/books/<int:bid>")
def delete(bid):
    i = next((k for k, b in enumerate(BOOKS) if b["id"] == bid), None)
    if i is None: return jsonify(error="not found"), 404
        
    BOOKS.pop(i)
    return "", 204
