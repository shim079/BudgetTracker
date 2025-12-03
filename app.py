from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

budget = 0
expenses = []

@app.route("/category-data")
def category_data():
    summary = {}
    for exp in expenses:
        summary[exp["category"]] = summary.get(exp["category"], 0) + exp["amount"]
    return jsonify(summary)

@app.route("/", methods=["GET", "POST"])
def index():
    global budget, expenses

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "budget":
            budget = float(request.form.get("budget", 0))
        elif form_type == "expense":
            description = request.form.get("description")
            category = request.form.get("category")
            amount_str = request.form.get("amount")

            if not description or not category or not amount_str:
                return redirect(url_for("index"))

            amount = float(amount_str)
            expenses.append({"description": description, "category": category, "amount": amount})

    total_expenses = sum(exp["amount"] for exp in expenses)
    remaining = budget - total_expenses

    return render_template(
        "index.html",
        budget=budget,
        expenses=expenses,
        total=total_expenses,
        remaining=remaining,
    )

if __name__ == "__main__":
    app.run(debug=True)