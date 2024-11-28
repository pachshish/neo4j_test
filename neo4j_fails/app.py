from flask import Flask

from neo4j_fails.phons_bp import phonesBP

app = Flask(__name__)

app.register_blueprint(phonesBP)


if __name__ == "__main__":
     app.run(debug=True)

# git add .
# git commit -m "Your commit message"
# git push
