from flask import Flask, jsonify, abort, make_response, request
from models import expenses

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/expenses/", methods=["GET"])
def expenses_list_api_v1():
    return jsonify(expenses.all())

@app.route("/api/v1/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = expenses.get(expense_id)
    if not expense:
        abort(404)
    return jsonify({"expense": expense})
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)
    
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)
    
    
@app.route("/api/v1/expenses/", methods=["POST"])
def create_expense():
    if not request.json or not 'item' in request.json:
        abort(400)
    expense = {
        'id': expenses.all()[-1]['id'] + 1,
        'item': request.json['item'],
        'description': request.json.get('description', ""),
        'bought': False
    }
    expenses.create(expense)
    return jsonify({'expense': expense}), 201


@app.route("/api/v1/expenses/<int:expense_id>", methods=['DELETE'])
def delete_expense(expense_id):
    result = expenses.delete(expense_id)
    if not result:
        abort(404)
    return jsonify({'result': result})
  
@app.route("/api/v1/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    expense = expenses.get(expense_id)
    if not expense:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'item' in data and not isinstance(data.get('item'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'bought' in data and not isinstance(data.get('bought'), bool)
    ]):
        abort(400)
    expense = {
        'item': data.get('item', expense['item']),
        'description': data.get('description', expense['description']),
        'bought': data.get('bought', expense['bought'])
    }
    expenses.update(expense_id, expense)
    return jsonify({'expense': expense})  

if __name__ == "__main__":
    app.run(debug=True)