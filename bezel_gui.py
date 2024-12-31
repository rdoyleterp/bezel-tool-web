from flask import Flask, render_template, request, send_from_directory
import os
from PIL import Image

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEZELS_DIR = os.path.join(BASE_DIR, "bezels")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/")
def index():
    bezels = [f for f in os.listdir(BEZELS_DIR) if os.path.isfile(os.path.join(BEZELS_DIR, f))]
    return render_template("index.html", bezels=bezels)

@app.route("/process", methods=["POST"])
def process_images():
    try:
        # Get selected bezel and uploaded files
        selected_bezel = request.form["bezel"]
        bezel_path = os.path.join(BEZELS_DIR, selected_bezel)
        files = request.files.getlist("images")
        
        processed_files = []

        for uploaded_file in files:
            if uploaded_file.filename == "":
                continue

            # Save uploaded file temporarily
            temp_path = os.path.join(OUTPUT_DIR, uploaded_file.filename)
            uploaded_file.save(temp_path)

            # Open and process the image
            screenshot = Image.open(temp_path)
            bezel = Image.open(bezel_path).convert("RGBA")
            screenshot = screenshot.resize((800, 600))  # Resize screenshot (example dimensions)
            bezel.paste(screenshot, (50, 50), mask=screenshot)  # Example placement
            
            # Save processed image
            output_filename = f"processed_{uploaded_file.filename}"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            bezel.save(output_path, "PNG")
            processed_files.append(output_filename)

        return {"message": "Images processed successfully!", "files": processed_files}
    except Exception as e:
        return {"error": str(e)}

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)