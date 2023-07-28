import json

from flask import Flask, jsonify

app = Flask(__name__)

course = None
food = None
general = None


def load_course_data():
    with open("courses.json", "r") as json_file:
        return json.load(json_file)


def load_general_data():
    with open("generalInfo.json", "r") as json_file:
        return json.load(json_file)


def load_food_data():
    with open("food.json", "r") as json_file:
        return json.load(json_file)


@app.route('/v1/courses/index/faculties', methods=['GET'])
def get_all_faculties():
    return jsonify(general["faculties_info"]), 200


@app.route('/v1/courses/index/<faculty>', methods=['GET'])
def get_courses_by_faculty(faculty):
    faculty_data = course["faculties"].get(faculty)

    if faculty_data:
        return jsonify(faculty_data), 200

    return jsonify({"error": "Faculty not found."}), 404


@app.route('/v1/courses/index/<faculty>/<subject>/courses', methods=['GET'])
def get_courses_by_faculty_subject(faculty, subject):
    courses_subject = course["faculties"][faculty][subject]

    if courses_subject:
        return jsonify(courses_subject["courses"]), 200
    return jsonify({"error": "Not a valid faulty or subject."}), 404


@app.route('/v1/food-areas/locations', methods=['GET'])
def get_food_areas():
    return general["food_areas"], 200


@app.route('/v1/food-areas/food/all', methods=['GET'])
def get_food_all():
    return food, 200


@app.route('/v1/food-areas/<location>', methods=['GET'])
def get_food_by_location(location):
    food_by_location = food[location]

    if food_by_location:
        return jsonify(food_by_location), 200
    return jsonify({"error": "Not a food location"})


if __name__ == '__main__':
    course = load_course_data()
    food = load_food_data()
    general = load_general_data()
    app.run(debug=True)
