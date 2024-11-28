from neo4j_fails.init_db import init_neo4j

driver = init_neo4j()

def process_interaction(data):
    device1 = data["devices"][0]
    device2 = data["devices"][1]
    interaction = data["interaction"]

    params = {
        # פרטים עבור מכשיר 1
        "device1_id": device1["id"],
        "device1_name": device1["name"],
        "device1_brand": device1["brand"],
        "device1_model": device1["model"],
        "device1_os": device1["os"],
        "device1_latitude": device1["location"]["latitude"],
        "device1_longitude": device1["location"]["longitude"],
        "device1_altitude": device1["location"]["altitude_meters"],
        "device1_accuracy": device1["location"]["accuracy_meters"],
        # פרטים עבור מכשיר 2
        "device2_id": device2["id"],
        "device2_name": device2["name"],
        "device2_brand": device2["brand"],
        "device2_model": device2["model"],
        "device2_os": device2["os"],
        "device2_latitude": device2["location"]["latitude"],
        "device2_longitude": device2["location"]["longitude"],
        "device2_altitude": device2["location"]["altitude_meters"],
        "device2_accuracy": device2["location"]["accuracy_meters"],
        # פרטי האינטראקציה
        "interaction_method": interaction["method"],
        "interaction_bluetooth_version": interaction["bluetooth_version"],
        "interaction_signal_strength": interaction["signal_strength_dbm"],
        "interaction_distance": interaction["distance_meters"],
        "interaction_duration": interaction["duration_seconds"],
        "interaction_timestamp": interaction["timestamp"],
    }

    query = """
        MERGE (d1:Device {id: $device1_id})
        SET d1.name = $device1_name,
            d1.device_id = $device1_id,  
            d1.brand = $device1_brand, 
            d1.model = $device1_model, 
            d1.os = $device1_os, 
            d1.latitude = $device1_latitude, 
            d1.longitude = $device1_longitude, 
            d1.altitude_meters = $device1_altitude, 
            d1.accuracy_meters = $device1_accuracy

        MERGE (d2:Device {id: $device2_id})
        SET d2.name = $device2_name,
            d2.device_id = $device2_id,  
            d2.brand = $device2_brand, 
            d2.model = $device2_model, 
            d2.os = $device2_os, 
            d2.latitude = $device2_latitude, 
            d2.longitude = $device2_longitude, 
            d2.altitude_meters = $device2_altitude, 
            d2.accuracy_meters = $device2_accuracy

        MERGE (d1)-[r:CONNECTED {
            method: $interaction_method, 
            bluetooth_version: $interaction_bluetooth_version, 
            signal_strength_dbm: $interaction_signal_strength, 
            distance_meters: $interaction_distance, 
            duration_seconds: $interaction_duration, 
            timestamp: $interaction_timestamp
        }]->(d2)
        """

    # ביצוע השאילתה
    with driver.session() as session:
        session.run(query, **params)


def get_connected_devices():
    query = """
    MATCH (d1:Device)-[c:CONNECTED]->(d2:Device)
    WHERE c.signal_strength_dbm > -60
    RETURN d1.id AS device1_id, d1.name AS device1_name, 
           d2.id AS device2_id, d2.name AS device2_name, 
           c.signal_strength_dbm
    """
    try:
        with driver.session() as session:
            result = session.run(query)
            devices = []
            for record in result:
                devices.append({
                    "device1_id": record["device1_id"],
                    "device1_name": record["device1_name"],
                    "device2_id": record["device2_id"],
                    "device2_name": record["device2_name"],
                    "signal_strength_dbm": record["signal_strength_dbm"]
                })
            return devices
    except Exception as e:
        print(f"Error: {e}")

