#Task 1:


# Step 1: Create a New Flask Project and Set Up a Virtual Environment

# Open terminal or command prompt
# Navigate to your project directory
# Create a new virtual environment
# Activate the virtual environment


# Step 2: Install Necessary Packages

# pip install Flask Flask-Marshmallow mysql-connector-python


# Step 3: Establish a Connection to Your MySQL Database

# Create python file
# Set up the Flask application and database connection


from flask import Flask
from flask_marshmallow import Marshmallow
import mysql.connector

# Initialize the Flask application
app = Flask(__name__)

# Initialize Marshmallow
ma = Marshmallow(app)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'Finroy1121!',
    'host': '127.0.0.1',
    'database': 'fitness_center',
}

# Establish connection to the MySQL database
try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Successfully connected to the database")
except mysql.connector.Error as err:
    print(f"Error: {err}")

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)

# Run  the script




# Task 2:


from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Finroy1121!'
app.config['MYSQL_DB'] = 'fitness_center'

# Initialize MySQL and Marshmallow
mysql = MySQL(app)
ma = Marshmallow(app)

# Member schema using Marshmallow
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'age')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

# CRUD Operations for Members

# Create a new member 
@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    email = request.json['email']
    age = request.json['age']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO Members (name, email, age) VALUES (%s, %s, %s)', (name, email, age))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Member added successfully!'}), 201

# Retrieve a single member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Members WHERE id = %s', (id,))
    member = cursor.fetchone()
    cursor.close()

    if member:
        return jsonify(member_schema.dump(member))
    else:
        return jsonify({'message': 'Member not found!'}), 404

# Retrieve all members 
@app.route('/members', methods=['GET'])
def get_members():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Members')
    members = cursor.fetchall()
    cursor.close()

    return jsonify(members_schema.dump(members))

# Update a member by ID 
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    name = request.json['name']
    email = request.json['email']
    age = request.json['age']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Members WHERE id = %s', (id,))
    member = cursor.fetchone()
    
    if member:
        cursor.execute('UPDATE Members SET name = %s, email = %s, age = %s WHERE id = %s', (name, email, age, id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Member updated successfully!'})
    else:
        return jsonify({'message': 'Member not found!'}), 404

# Delete a member by ID 
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Members WHERE id = %s', (id,))
    member = cursor.fetchone()
    
    if member:
        cursor.execute('DELETE FROM Members WHERE id = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Member deleted successfully!'})
    else:
        return jsonify({'message': 'Member not found!'}), 404

# Error handling for missing routes
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)



# Task 3:


from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector

app = Flask(__name__)
ma = Marshmallow(app)

# Database connection configuration
db_config = {
    'user': 'root',  
    'password': 'Finroy1121!',  
    'host': '127.0.0.1',
    'database': 'fitness_center',  
}

# Function to get the database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# WorkoutSession Schema
class WorkoutSessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'member_id', 'session_date', 'duration', 'type')

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# Route to schedule a new workout session
@app.route('/workout_sessions', methods=['POST'])
def schedule_workout_session():
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    duration = request.json['duration']
    workout_type = request.json['type']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO WorkoutSessions (member_id, session_date, duration, type) VALUES (%s, %s, %s, %s)"
    
    try:
        cursor.execute(query, (member_id, session_date, duration, workout_type))
        conn.commit()
        return workout_session_schema.jsonify({
            'id': cursor.lastrowid,
            'member_id': member_id,
            'session_date': session_date,
            'duration': duration,
            'type': workout_type
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Route to update an existing workout session
@app.route('/workout_sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    session_date = request.json.get('session_date')
    duration = request.json.get('duration')
    workout_type = request.json.get('type')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE WorkoutSessions SET session_date=%s, duration=%s, type=%s WHERE id=%s"
    
    try:
        cursor.execute(query, (session_date, duration, workout_type, id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Workout session not found'}), 404
        return workout_session_schema.jsonify({'id': id, 'session_date': session_date, 'duration': duration, 'type': workout_type})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# Route to get a specific workout session by ID
@app.route('/workout_sessions/<int:id>', methods=['GET'])
def get_workout_session(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM WorkoutSessions WHERE id=%s"
    cursor.execute(query, (id,))
    workout_session = cursor.fetchone()

    cursor.close()
    conn.close()

    if workout_session is None:
        return jsonify({'error': 'Workout session not found'}), 404
    
    return workout_session_schema.jsonify(workout_session)

# Route to get all workout sessions for a specific member
@app.route('/members/<int:member_id>/workout_sessions', methods=['GET'])
def get_workout_sessions_for_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM WorkoutSessions WHERE member_id=%s"
    cursor.execute(query, (member_id,))
    workout_sessions = cursor.fetchall()

    cursor.close()
    conn.close()

    return workout_sessions_schema.jsonify(workout_sessions)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)