from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-string"  # needed for logins
DB = "store.db"

# DEMO admin account (for a real store, use hashed passwords!)
ADMIN_USER = "admin"
ADMIN_PASS = "techzone123"

def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def require_admin():
    """Block the request if the user is not logged in as admin."""
    if not session.get("is_admin"):
        return jsonify({"error": "Admin login required"}), 403

# ---------- PUBLIC PAGES ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- AUTH ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json(force=True)
        if data.get("username") == ADMIN_USER and data.get("password") == ADMIN_PASS:
            session["is_admin"] = True
            return jsonify({"ok": True})
        return jsonify({"error": "Wrong username or password"}), 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin")
def admin_panel():
    if not session.get("is_admin"):
        return redirect(url_for("login"))
    return render_template("admin.html")

# ---------- PUBLIC API ----------
@app.route("/api/products")
def products():
    con = get_db()
    rows = con.execute("SELECT * FROM products").fetchall()
    con.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/buy", methods=["POST"])
def buy():
    data = request.json
    con = get_db()
    row = con.execute("SELECT * FROM products WHERE id = ?", (data["id"],)).fetchone()
    if not row:
        con.close()
        return jsonify({"error": "Product not found"}), 404
    if row["stock"] < data["qty"]:
        con.close()
        return jsonify({"error": "Not enough stock!"}), 400
    con.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (data["qty"], data["id"]))
    con.commit()
    new_stock = con.execute("SELECT stock FROM products WHERE id = ?", (data["id"],)).fetchone()["stock"]
    con.close()
    return jsonify({"id": data["id"], "stock": new_stock, "message": "Purchase successful!"})

# ---------- ADMIN-ONLY API ----------
@app.route("/api/restock", methods=["POST"])
def restock():
    blocked = require_admin()
    if blocked: return blocked
    data = request.json
    con = get_db()
    con.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (data["qty"], data["id"]))
    con.commit(); con.close()
    return jsonify({"message": "Restocked!"})

@app.route("/api/add_product", methods=["POST"])
def add_product():
    blocked = require_admin()
    if blocked: return blocked
    data = request.json
    con = get_db()
    con.execute("INSERT INTO products (name, price, stock, emoji) VALUES (?, ?, ?, ?)",
                (data["name"], data["price"], data["stock"], data.get("emoji", "📦")))
    con.commit(); con.close()
    return jsonify({"message": "Product added!"})

if __name__ == "__main__":
    app.run(debug=True)
