from __init__ import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

from flask import render_template, g
from bson import ObjectId

@app.route("/admin/orders")
def admin_orders():
    orders = list(orders_collection.find())
    return render_template("admin/orders.html", orders=orders, t=g.translations)

from flask import request, redirect, url_for

@app.route("/admin/orders/update/<order_id>", methods=["POST"])
def update_order_status(order_id):
    new_status = request.form.get("status")
    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": new_status}}
    )
    return redirect(url_for("admin_orders"))