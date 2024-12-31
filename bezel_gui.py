from flask import Flask, render_template, request, jsonify, send_file
import os
from PIL import Image, ImageDraw
import io

# Initialize Flask app
app = Flask(__name__)

# Directory for bezels
BEZEL_DIR = "bezels"

# Dictionary to define bezels and their transparent area dimensions and offsets
bezels = {
    "desktop": {
        "path": os.path.join(BEZEL_DIR, "desktop.png"),
        "resize": (2560, 1448),
        "offset": (130, 120),
        "apply_round_corners": False
    },
    "ipad_landscape": {
        "path": os.path.join(BEZEL_DIR, "ipad_landscape.png"),
        "resize": (1388, 1048),
        "offset": (50, 50),
        "apply_round_corners": True
    },
    "ipad_portrait": {
        "path": os.path.join(BEZEL_DIR, "ipad_portrait.png"),
        "resize": (1048, 1388),
        "offset": (50, 50),
        "apply_round_corners": True
    },
    "iphone_15": {
        "path": os.path.join(BEZEL_DIR, "iphone_15.png"),
        "resize": (440, 844),
        "offset": (35, 90),
        "apply_round_corners": True
    },
    "minimal": {
        "path": os.path.join(BEZEL_DIR, "minimal.png"),
        "resize": (3910, 2210),
        "offset": (95, 95),
        "apply_round_corners": False
    },
}

def embed_screenshot(bezel_path, screenshot_path, resize_dims, offset, apply_round_corners=False):
    """
    Embed a screenshot into a bezel image, positioning it within the transparent region.
    """
    # Open bezel and screenshot
    bezel = Image.open(bezel_path).convert("RGBA")
    screenshot = Image.open(screenshot_path).convert("RGBA")

    # Resize the screenshot to the specified dimensions
    screenshot = screenshot.resize(resize_dims, Image.Resampling.LANCZOS)

    # Create a blank canvas with the same size as the bezel
    output_image = Image.new("RGBA", bezel.size)

    # Position the screenshot at the specified offset
    x_offset, y_offset = offset
    output_image.paste(screenshot, (x_offset, y_offset), mask=screenshot)

    # Overlay the bezel on top
    output_image.paste(bezel, (0, 0), mask=bezel)

    return output_image

@app.route("/")
def index():
    """
    Home route to render the index page.
    """
    return render_template("index.html", bezels=list(bezels.keys()))

@app.route("/process", methods=["POST"])
def process_images():
    """
    Route to process images based on the selected bezel and user input.
    """
    try:
        bezel_name = request.form.get("bezel")
        files = request.files.getlist("files")

        if not bezel_name or bezel_name not in bezels:
            return jsonify({"error": "Invalid bezel selected."}), 400

        if not files:
            return jsonify({"error": "No files uploaded."}), 400

        bezel_data = bezels[bezel_name]
        bezel_path = bezel_data["path"]
        resize_dims = bezel_data["resize"]
        offset = bezel_data["offset"]

        processed_files = []

        for file in files:
            screenshot_path = file.stream
            output_image = embed_screenshot(
                bezel_path=bezel_path,
                screenshot_path=screenshot_path,
                resize_dims=resize_dims,
                offset=offset,
                apply_round_corners=bezel_data.get("apply_round_corners", False),
            )

            # Save output image to a BytesIO object
            output_io = io.BytesIO()
            output_image.save(output_io, "PNG")
            output_io.seek(0)

            # Append processed file for download
            processed_files.append(output_io)

        return jsonify({"message": "Images processed successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    """
    Route to download a processed file.
    """
    filepath = os.path.join("output", filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({"error": "File not found."}), 404

if __name__ == "__main__":
    # Create the required directories if they don't exist
    os.makedirs("output", exist_ok=True)

    # Run the app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
