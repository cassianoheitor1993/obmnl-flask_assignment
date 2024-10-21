# Import libraries
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    total = sum(t['amount'] for t in transactions)
    return render_template("transactions.html", transactions=transactions, total_amount=total)

# Create operation: Display add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))
    
    return render_template("form.html")

# Update operation: Display edit transaction form
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)

    if transaction is None:
        return "Transaction not found", 404

    if request.method == 'POST':
        transaction['date'] = request.form['date']
        transaction['amount'] = float(request.form['amount'])
        return redirect(url_for("get_transactions"))

    return render_template("edit.html", transaction=transaction)

# Delete operation
@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    index = next((i for i, t in enumerate(transactions) if t['id'] == transaction_id), None)

    if index is None:
        return "Transaction not found", 404

    del transactions[index]
    return redirect(url_for("get_transactions"))

# Search operation
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])

        # Server-side validation
        if min_amount >= max_amount:
            return "Minimum amount must be less than maximum amount", 400
        
        # Filter transactions based on min and max amount
        search_results = [
            t for t in transactions 
            if min_amount <= t['amount'] <= max_amount
        ]

        total = sum(t['amount'] for t in search_results)

        return render_template("transactions.html", transactions=search_results, 
                               min_value=min_amount, max_value=max_amount, filtered=True, total_amount=total)

    return render_template("search.html")



# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
