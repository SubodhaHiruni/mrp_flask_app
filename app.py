from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            # Get user inputs from form
            forecast = [
                int(request.form["month1"]),
                int(request.form["month2"]),
                int(request.form["month3"])
            ]
            initial_stock = int(request.form["stock"])

            # Initialize result lists
            open_stock = []
            demand = []
            supply = []
            end_stock = []

            # MRP logic
            for month in range(3):
                os = initial_stock if month == 0 else end_stock[month - 1]
                open_stock.append(os)

                d = forecast[month]
                b = d  # Buffer = demand
                s = max(d + b - os, 0)
                supply.append(s)

                es = os + s - d
                end_stock.append(es)
                demand.append(d)

            result = {
                "open_stock": open_stock,
                "demand": demand,
                "supply": supply,
                "end_stock": end_stock
            }

        except ValueError:
            result = "Invalid input. Please enter numbers only."

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
