from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import os

# Initialize the app
app = Flask(__name__)

# Configure paths
UPLOAD_FOLDER = "app/uploads"
PROCESSED_FOLDER = "app/processed"
BEZEL_FOLDER = "app/bezels"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Bezel configurations
BEZELS = {
    "desktop": {"path": os.path.join(BEZEL_FOLDER, "desktop.png"), "resize": (2560, 1448), "offset": (130, 120)},
    "ipad_landscape": {"path": os.path.join(BEZEL_FOLDER, "ipad_landscape.png"), "resize": (1388, 1048), "offset": (50, 50)},
    "ipad_portrait": {"path": os.path.join(BEZEL_FOLDER, "ipad_portrait.png"), "resize": (1048, 1388), "offset": (50, 50)},
    "iphone_15": {"path": os.path.join(BEZEL_FOLDER, "iphone_15.png"), "resize": (440, 844), "offset": (35, 90)},
    "minimal": {"path": os.path.join(BEZEL_FOLDER, "minimal.png"), "resize": (3910, 2210), "offset": (95, 95)},
}

# Home route
@app.route("/")
def index():
    return render_template("index.html", bezels=BEZELS)

# Image upload route
@app.route("/upload", methods=["POST"])
def upload_image():
    uploaded_files = request.files.getlist("images")
    uploaded_paths = []

    for uploaded_file in uploaded_files:
        if uploaded_file.filename:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)
            uploaded_paths.append(file_path)

    return jsonify({"uploaded": uploaded_paths})

# Image processing route
@app.route("/process", methods=["POST"])
def process_images():
    images = request.form.getlist("images[]")
    bezel_name = request.form.get("bezel")
    group_name = request.form.get("group_name", "")
    bezel_config = BEZELS.get(bezel_name)

    if not images or not bezel_config:
        return jsonify({"error": "Invalid image selection or bezel configuration."}), 400

    processed_paths = []

    for image_path in images:
        try:
            # Open bezel and image
            bezel = Image.open(bezel_config["path"]).convert("RGBA")
            image = Image.open(image_path).convert("RGBA")

            # Resize and embed image
            image = image.resize(bezel_config["resize"], Image.LANCZOS)
            output_image = Image.new("RGBA", bezel.size)
            output_image.paste(image, bezel_config["offset"])
            output_image.paste(bezel, (0, 0), mask=bezel)

            # Save processed image
            output_filename = f"{group_name}_{os.path.basename(image_path)}"
            output_path = os.path.join(PROCESSED_FOLDER, output_filename)
            output_image.save(output_path)
            processed_paths.append(output_path)
        except Exception as e:
            return jsonify({"error": f"Failed to process image {image_path}: {str(e)}"}), 500

    return jsonify({"processed": processed_paths})

# Serve processed files
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
