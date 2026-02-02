from flask import Flask, render_template, request, send_file
from process import transpose_blocks
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static"
INPUT_IMG = os.path.join(UPLOAD_FOLDER, "input.jpg")
OUTPUT_IMG = os.path.join(UPLOAD_FOLDER, "output.jpg")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        block_w = int(request.form["block_w"])
        block_h = int(request.form["block_h"])

        file.save(INPUT_IMG)

        transpose_blocks(
            INPUT_IMG,
            OUTPUT_IMG,
            block_w,
            block_h
        )

        return render_template(
            "index.html",
            output_image="static/output.jpg"
        )

    return render_template("index.html", output_image=None)

@app.route("/download")
def download():
    return send_file(OUTPUT_IMG, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

