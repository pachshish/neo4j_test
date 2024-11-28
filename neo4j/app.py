from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   print(request.json)
   return jsonify({ }), 200


if __name__ == "__main__":
     app.run(debug=True)