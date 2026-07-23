from db import get_db
from flask import Flask, request, jsonify

app = Flask(__name__)

# Login credentials
USERNAME = "admin"
PASSWORD = "password123"


# ---------- LOGIN ----------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == USERNAME and password == PASSWORD:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401



# ---------- FLOOR ----------

# CREATING FLOOR DATA
@app.route('/api/floor', methods=['POST'])
def create_floor():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO floor (floor_level, floor_name) VALUES (%s, %s)", 
                   (data['floor_level'], data['floor_name']))
    db.commit()
    return jsonify({"message": "Floor created successfully!"}), 201

# GETTING FLOOR DATA
@app.route('/api/floor/<int:floor_id>', methods=['GET'])
def get_floor(floor_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM floor WHERE floor_id = %s", (floor_id,))
    floor = cursor.fetchone()
    if floor:
        return jsonify(floor), 200
    else:
        return jsonify({"message": "Floor not found"}), 404

# UPDATING FLOOR DATA
@app.route('/api/floor/<int:floor_id>', methods=['PUT'])
def update_floor(floor_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE floor SET floor_level=%s, floor_name=%s WHERE floor_id=%s",
                   (data['floor_level'], data['floor_name'], floor_id))
    db.commit()
    return jsonify({"message": "Floor updated successfully!"}), 200

# DELETING FLOOR DATA
@app.route('/api/floor/<int:floor_id>', methods=['DELETE'])
def delete_floor(floor_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM floor WHERE floor_id=%s", (floor_id,))
    db.commit()
    return jsonify({"message": "Floor deleted successfully!"}), 200



# ---------- ROOM ----------

# CREATING ROOM DATA
@app.route('/api/room', methods=['POST'])
def create_room():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO room (room_capacity, room_number, room_floor) VALUES (%s, %s, %s)", 
                   (data['room_capacity'], data['room_number'], data['room_floor']))
    db.commit()
    return jsonify({"message": "Room created successfully!"}), 201  

# GETTING ROOM DATA
@app.route('/api/room/<int:room_id>', methods=['GET'])
def get_room(room_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT room.*, floor.floor_name, floor.floor_level
        FROM room JOIN floor ON room.room_floor = floor.floor_id WHERE room.room_id = %s""", (room_id,))
    room = cursor.fetchone()
    if room:
        return jsonify(room), 200
    else:
        return jsonify({"message": "Room not found"}), 404 

# UPDATING ROOM DATA
@app.route('/api/room/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE room SET room_capacity=%s, room_number=%s, room_floor=%s WHERE room_id=%s",
                   (data['room_capacity'], data['room_number'], data['room_floor'], room_id))
    db.commit()
    return jsonify({"message": "Room updated successfully!"}), 200

# DELETING ROOM DATA
@app.route('/api/room/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM room WHERE room_id=%s", (room_id,))
    db.commit()
    return jsonify({"message": "Room deleted successfully!"}), 200



# ---------- RESIDENT ----------

# CREATING RESIDENT DATA
@app.route('/api/resident', methods=['POST'])
def create_resident():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO resident (res_first_name, res_last_name, res_age, res_room) VALUES (%s, %s, %s, %s)",
        (data['res_first_name'], data['res_last_name'], data['res_age'], data['res_room']))
    db.commit()
    return jsonify({"message": "Resident created successfully!"}), 201

# GETTING RESIDENT DATA
@app.route('/api/resident/<int:res_id>', methods=['GET'])
def get_resident(res_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(""" SELECT resident.*, room.room_number, floor.floor_name
        FROM resident JOIN room ON resident.res_room = room.room_id
        JOIN floor ON room.room_floor = floor.floor_id WHERE resident.res_id = %s """, (res_id,))
    resident = cursor.fetchone()
    if resident:
        return jsonify(resident), 200
    else:
        return jsonify({"message": "Resident not found"}), 404

# UPDATING RESIDENT DATA
@app.route('/api/resident/<int:res_id>', methods=['PUT'])
def update_resident(res_id):
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE resident SET res_first_name=%s, res_last_name=%s, res_age=%s, res_room=%s WHERE res_id=%s",
                   (data['res_first_name'], data['res_last_name'], data['res_age'], data['res_room'], res_id))
    db.commit()
    return jsonify({"message": "Resident updated successfully!"}), 200

# DELETING RESIDENT DATA
@app.route('/api/resident/<int:res_id>', methods=['DELETE'])
def delete_resident(res_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM resident WHERE res_id=%s", (res_id,))
    db.commit()
    return jsonify({"message": "Resident deleted successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True)