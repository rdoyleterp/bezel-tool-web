from flask import Flask, render_template, request, send_file
import os
from PIL import Image

app = Flask(
    __name__,
    static_folder="static",  # Folder for static files (CSS/JS)
    template_folder="templates"  # Folder for HTML templates
)

# Bezel configurations
BEZELS = {
    "desktop": {"path": "app/bezels/desktop.png", "resize": (2560, 1448)},
    "ipad_landscape": {"path": "app/bezels/ipad_landscape.png", "resize": (1388, 1048)},
    "ipad_portrait": {"path": "app/bezels/ipad_portrait.png", "resize": (1048, 1388)},
    "iphone_15": {"path": "app/bezels/iphone_15.png", "resize": (440, 844)},
    "minimal": {"path": "app/bezels/minimal.png", "resize": (3910, 2210)},
}

@app.route("/")
def index():
    return render_template("index.html", bezels=list(BEZELS.keys()))

@app.route("/upload", methods=["POST"])
def upload_file():
    # Handle file uploads
    uploaded_files = request.files.getlist("files")
    selected_bezel = request.form.get("bezel")
    output_dir = "app/output"
    os.makedirs(output_dir, exist_ok=True)

    processed_files = []
    for uploaded_file in uploaded_files:
        if uploaded_file.filename != "":
            file_path = os.path.join(output_dir, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Apply bezel if selected
            if selected_bezel in BEZELS:
                bezel = BEZELS[selected_bezel]
                processed_path = apply_bezel(file_path, bezel["path"], bezel["resize"])
                processed_files.append(processed_path)

    return {"processed_files": processed_files}

def apply_bezel(image_path, bezel_path, resize_dims):
    """Applies a bezel to an image."""
    output_dir = "app/output"
    os.makedirs(output_dir, exist_ok=True)

    image = Image.open(image_path)
    bezel = Image.open(bezel_path)

    # Resize the image to fit the bezel
    image = image.resize(resize_dims, Image.Resampling.LANCZOS)

    # Create a new image with the bezel overlay
    output_image = Image.new("RGBA", bezel.size)
    output_image.paste(image, (0, 0))
    output_image.paste(bezel, (0, 0), mask=bezel)

    output_path = os.path.join(output_dir, f"processed_{os.path.basename(image_path)}")
    output_image.save(output_path)

    return output_path

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join("app/output", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
