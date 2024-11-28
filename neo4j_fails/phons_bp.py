from flask import Blueprint, jsonify, request

from neo4j_fails.neo4j_service import get_all_bluetooth_users, get_fetch_most_recent_interaction
from neo4j_service import process_interaction, driver, get_connected_devices, get_count_device_connections, \
    get_check_direct_connection

phonesBP = Blueprint('phones', __name__)


@phonesBP.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
    data = request.json
    print(data)
    process_interaction(data)  # שלח את המידע ל-Neo4j
    return jsonify({"message": "Interaction processed"}), 200


@phonesBP.route("/find_bluetooth", methods=['GET'])
def all_bluetooth_users():
   result = get_all_bluetooth_users()
   return result


# יצירת Route ב-Flask
@phonesBP.route('/connected_devices', methods=['GET'])
def connected_devices():
    devices = get_connected_devices()
    return devices


@phonesBP.route('/device/<device_id>/connections', methods=['GET'])
def count_device_connections(device_id):
    result = get_count_device_connections(device_id)
    return result

@phonesBP.route('/devices/connection', methods=['GET'])
def check_direct_connection():

    device1_id = request.args.get('device1_id')
    device2_id = request.args.get('device2_id')

    result = get_check_direct_connection(device1_id, device2_id)
    return result
#     http://localhost:5000/devices/connection?device1_id=a54a9fb6-d32a-4f46-a46a-88e6a8b2fda6&device2_id=5492d571-7d56-484d-bf93-fc72cf9dd7cb
# שתי יוזרים שמחוברים

@phonesBP.route('/device/most_recent_interaction', methods=['GET'])
def fetch_most_recent_interaction():
    device_id = request.args.get('device_id')
    result = get_fetch_most_recent_interaction(device_id)
    return result





