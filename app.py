import py_eureka_client.eureka_client as eureka_client
from flask import Flask, request, jsonify

from models import db, Transaction

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://operator:operator@localhost:5431/transaction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

your_rest_server_port = 5000

with app.app_context():
    db.create_all()
    eureka_client.init(eureka_server="http://localhost:8761",
                       instance_host="localhost",
                       instance_ip="SPB-NB-083.esphere.local",
                       app_name="transaction",
                       instance_port=your_rest_server_port)


@app.route('/api/v1/transaction', methods=['POST'])
def add_transaction():
    data = request.json
    new_transaction = Transaction(customer_id=data['customerId'], message=data['message'])
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(
        {"message": "Transaction added!",
         "transaction": {"id": new_transaction.id,
                         "customerId": new_transaction.customer_id,
                         "message": new_transaction.message}}), 201


@app.route('/api/v1/transaction/search', methods=['POST'])
def get_transactions():
    data = request.json
    customer_id = data['customerId']

    query = Transaction.query

    if customer_id:
        query = query.filter(Transaction.customer_id.ilike(f"%{customer_id}%"))

    transactions = query.all()

    return jsonify(
        [{"id": transaction.id, "customerId": transaction.customer_id, "message": transaction.message} for transaction
         in transactions]
    )


if __name__ == '__main__':
    app.run(debug=True, port=your_rest_server_port)
