import py_eureka_client.eureka_client as eureka_client
from flask import Flask, request, jsonify

from models import db, Book

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dm4nk:anime_the_best@localhost:5431/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

your_rest_server_port = 5000

with app.app_context():
    db.create_all()
    eureka_client.init(eureka_server="http://localhost:8761",
                       instance_host="localhost",
                       instance_ip="SPB-NB-083.esphere.local",
                       app_name="book",
                       instance_port=your_rest_server_port)


@app.route('/api/v1/book', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(name=data['name'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(
        {"message": "Book added!", "book": {"id": new_book.id, "name": new_book.name, "author": new_book.author}}), 201


@app.route('/api/v1/book/<string:book_id>/assign', methods=['PUT'])
def assign_customer(book_id):
    customer_id = request.json.get('customerId')
    book = Book.query.get(book_id)
    if book:
        book.customer_id = customer_id
        db.session.commit()
        return jsonify(
            {"message": "Customer assigned to book!", "book_id": book.id, "customer_id": book.customer_id}), 200
    return jsonify({"message": "Book not found!"}), 404


@app.route('/api/v1/book/<string:book_id>/unassign', methods=['DELETE'])
def unassign_customer(book_id):
    book = Book.query.get(book_id)
    if book:
        book.customer_id = None
        db.session.commit()
        return jsonify({"message": "Customer unassigned from book!", "book_id": book.id}), 200
    return jsonify({"message": "Book not found!"}), 404


@app.route('/api/v1/book', methods=['GET'])
def get_books():
    author = request.args.get('author', '')
    name = request.args.get('name', '')

    query = Book.query

    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))

    if name:
        query = query.filter(Book.name.ilike(f"%{name}%"))

    books = query.all()

    return jsonify(
        [{"id": book.id, "name": book.name, "author": book.author, "customerId": book.customer_id} for book in books]
    )


if __name__ == '__main__':
    app.run(debug=True, port=your_rest_server_port)
