from flask import Flask, request, jsonify
import os

app = Flask(__name__)

def calculate_match_percentage(file1_path, file2_path):
    total_lines = 0
    matching_lines = 0

    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        while True:
            line1 = file1.readline()
            line2 = file2.readline()

            if not line1 and not line2:
                break

            total_lines += 1

            if line1.strip() == line2.strip():
                matching_lines += 1

        total_lines += sum(1 for _ in file1) + sum(1 for _ in file2)

    return (matching_lines / total_lines * 100) if total_lines > 0 else 100.0

@app.route("/compare", methods=["POST"])
def compare_files():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "Both files must be uploaded"}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    file1_path = os.path.join("uploads", "file1.txt")
    file2_path = os.path.join("uploads", "file2.txt")

    os.makedirs("uploads", exist_ok=True)
    file1.save(file1_path)
    file2.save(file2_path)

    match_percentage = calculate_match_percentage(file1_path, file2_path)

    return jsonify({"matchPercentage": match_percentage})

if __name__ == "__main__":
    app.run(debug=True)
