from flask import Blueprint, jsonify, request
from neo4j_service import process_interaction, driver, get_connected_devices

phonesBP = Blueprint('phones', __name__)


@phonesBP.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
    data = request.json
    print(data)
    process_interaction(data)  # שלח את המידע ל-Neo4j
    return jsonify({"message": "Interaction processed"}), 200


@phonesBP.route("/find_bluetooth", methods=['GET'])
def get_all_bluetooth_users():
    query = """
    MATCH (start:Device)
    MATCH (end:Device)
    WHERE start <> end
    MATCH path = shortestPath((start)-[:CONNECTED*]->(end))
    WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
    WITH path, length(path) as pathLength
    ORDER BY pathLength DESC
    LIMIT 1
    RETURN length(path)
    """
    with driver.session() as session:
        result = session.run(query)
        users_with_bluetooth_devices = [record for record in result]

    return jsonify(users_with_bluetooth_devices), 200



# יצירת Route ב-Flask
@phonesBP.route('/connected_devices', methods=['GET'])
def connected_devices():
    devices = get_connected_devices()
    return jsonify(devices)


@phonesBP.route('/device/<device_id>/connections', methods=['GET'])
def count_device_connections(device_id):

    query = """
    MATCH (d:Device {id: $device_id})-[r:CONNECTED]-(other:Device)
    RETURN count(other) AS connection_count
    """
    try:
        with driver.session() as session:
            result = session.run(query, device_id=device_id)
            count = result.single()["connection_count"]

        return jsonify({
            "device_id": device_id,
            "connection_count": count
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

