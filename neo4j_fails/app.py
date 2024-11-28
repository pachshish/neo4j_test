from flask import Flask, request, jsonify

from neo4j_fails.phons_bp import phonesBP

app = Flask(__name__)

app.register_blueprint(phonesBP)

@app.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   print(request.json)
   return jsonify({ }), 200


if __name__ == "__main__":
     app.run(debug=True)

# git add .
# git commit -m "Your commit message"
# git push
