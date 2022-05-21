from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ms")
def ms():
    row = []
    a = """ <tr><td><img src="assets/images/coin/BTC.png" alt="" class="img-fluid avatar mx-1"><span class="text-uppercase fw-bold"> BTC </span> <span class="text-muted"> Bitcoin</span></td>
        <td><span class="color-price-down">$44,090.69</span></td>
        <td><span class="color-price-up">+4.92%</span></td>
        <td>32,826.51M</td>
        <td>$830,324.82M</td>
        <td>$830,324.82M</td>
        <td>$830,324.82M</td>
        <td>$830,324.82M</td></tr> """

    row.append(a)
    row.append(a)
    return jsonify(row)

