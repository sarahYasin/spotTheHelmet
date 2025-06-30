from flask import Flask, request, jsonify
from inference_sdk import InferenceHTTPClient
import cv2
import numpy as np
import base64
import json
import os
import tempfile

app = Flask(__name__)

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="gXCGYwYqkVJoKqZfPjFQ"
)

# def iou(boxA, boxB):
#     ax1, ay1, ax2, ay2 = boxA
#     bx1, by1, bx2, by2 = boxB

#     inter_x1 = max(ax1, bx1)
#     inter_y1 = max(ay1, by1)
#     inter_x2 = min(ax2, bx2)
#     inter_y2 = min(ay2, by2)

#     inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
#     areaA = (ax2 - ax1) * (ay2 - ay1)
#     areaB = (bx2 - bx1) * (by2 - by1)

#     union_area = areaA + areaB - inter_area
#     return inter_area / union_area if union_area else 0

@app.route("/process", methods=["POST"])
def process():
    # 1. Check upload field name 'image'
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    # 2. Save upload to a temp file
    file = request.files['image']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        temp_path = tmp.name
        file.save(temp_path)

    # 3. Read image into OpenCV
    img = cv2.imread(temp_path)
    if img is None:
        # Clean up before returning
        os.remove(temp_path)
        return jsonify({"error": "Failed to read image"}), 400

    # 4. Run inference on the temp file, then delete temp file
    try:
        # result = CLIENT.infer(temp_path, model_id="ppe-detection-yfmym/1")
        result = CLIENT.infer(temp_path, model_id="ppe-detection-qlq3d/1")
    except Exception as e:
        # Clean up
        os.remove(temp_path)
        # Log e if desired
        return jsonify({"error": "Inference failed", "details": str(e)}), 500
    finally:
        # Remove the temp file after inference
        if os.path.exists(temp_path):
            os.remove(temp_path)

    preds = result.get("predictions", [])
    metadata = []
    for pred in preds:
        # cls = pred.get("class", "")
        cls = pred["class"]
        if cls!="helmet" :
            continue
        conf = pred["confidence"]
        # conf = pred.get("confidence", 0)
        # Roboflow returns x,y as center coordinates, and width,height (in pixels)
        x, y, w, h = pred["x"], pred["y"], pred["width"], pred["height"]
        # Convert to top-left / bottom-right
        x1 = int(x - w/2)
        y1 = int(y - h/2)
        x2 = int(x + w/2)
        y2 = int(y + h/2)
        # Choose a color per class or a default color
        # For debugging, you might map class names to colors, e.g.:
        color = (0, 255, 255)
        # Draw rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        # Label text = e.g. "class (xx%)"
        label = f"{cls} ({int(round(conf*100))}%)"
        # Choose text position
        text_y = y1 - 10 if y1 - 10 > 10 else y1 + 20
        cv2.putText(img, label, (x1, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        metadata.append({
                "class": cls,
                "confidence": conf,
                "bbox": [x1,y1,x2,y2]
                
            })
    

    # (Optional) Save annotated image to disk for debugging
    try:
        debug_path = "annotated_output.jpg"
        cv2.imwrite(debug_path, img)
        # print("Annotated image saved to", debug_path)
    except Exception:
        pass

    #  Encode annotated image as base64
    _, img_encoded = cv2.imencode('.jpg', img)
    b64_img = base64.b64encode(img_encoded).decode()

    # Return JSON with base64 image and metadata
    return jsonify({
        "image": b64_img,
        "metadata": metadata
    })

if __name__ == "__main__":
    # Run Flask app on port 8000
    app.run(host="0.0.0.0", port=8000)

