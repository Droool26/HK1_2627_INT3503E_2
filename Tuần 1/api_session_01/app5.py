from flask import Flask, jsonify

app = Flask(__name__)

# Giả lập Database
ORDERS = {
    "1": {"id": "1", "status": "pending"},
    "2": {"id": "2", "status": "shipped"},
    "3": {"id": "3", "status": "delivered"}
}

# DELETE /orders/<id>
@app.route("/orders/<id>", methods=["DELETE"])
def delete_order(id):
    order = ORDERS.get(id)
    
    # 404 — không tìm thấy
    if order is None:
        return jsonify({"error": "not found"}), 404
        
    # 409 — business rule
    if order["status"] in ("shipped", "delivered"):
        return jsonify({"error": "cannot delete"}), 409
        
    ORDERS.pop(id, None)
    
    # 204 — success, no body
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
