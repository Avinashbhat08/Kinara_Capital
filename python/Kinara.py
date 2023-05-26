from flash import Flask, request, jsonify
import csv

app = Flask(__name__)

# Load student details from a CSV file
def load_student_details():
    student_details = []
    with open('student_details.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_details.append(row)
    return student_details

# Paginate the student details
def paginate_student_details(student_details, page_number, page_size):
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    paginated_data = student_details[start_index:end_index]
    return paginated_data

# Apply server-side filtering to student details
def filter_student_details(student_details, filter_criteria):
    filtered_data = []
    for student in student_details:
        include_student = True
        for key, value in filter_criteria.items():
            if student.get(key) != value:
                include_student = False
                break
        if include_student:
            filtered_data.append(student)
    return filtered_data

# API endpoint for loading student details with pagination
@app.route('/students', methods=['GET'])
def get_students():
    page_number = int(request.args.get('page_number', 1))
    page_size = int(request.args.get('page_size', 10))
    
    student_details = load_student_details()
    paginated_data = paginate_student_details(student_details, page_number, page_size)
    
    return jsonify(paginated_data)

# API endpoint for server-side filtering
@app.route('/students/filter', methods=['POST'])
def filter_students():
    filter_criteria = request.get_json()
    
    student_details = load_student_details()
    filtered_data = filter_student_details(student_details, filter_criteria)
    
    return jsonify(filtered_data)

# Run the Flask application
if __name__ == '__main__':
    app.run()

