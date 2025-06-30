## this project builds a simple internal web app for a construction company to verify whether workers in site photos are wearing helmets. The company wants a lightweight, prototype-quality solution that includes image upload, processing, visualization, and a simple API + frontend.

1- frontend

  - Drag-and-drop image upload.
  - Preview of the uploaded image.
  - Display of processed results: overlaid boxes/masks and list of detected persons with/without helmets.
  - Basic loading and error handling.

2- Backend (Node.js + Express)
  ● Accept image uploads via REST API.
  ● Pass image to a Python service/script for processing.
  ● Return:
    ○ Annotated image (with helmets shown).
    ○ JSON metadata: bounding boxes, confidence scores, helmet .

3- Image Analysis (Python + OpenCV + AI)
   
● Detect people and helmet use using:
  ○ Pretrained models YOLOv8

4. DevOps (Docker + Setup)
● Containerize the app using Docker.
● Use docker-compose to run:
  ○ Frontend.
  ○ Backend.
  ○ Python processor.
  

## Project Setup
1- open terminal in image analysis and run python imageAnalysis.py
2- open terminal in backend and run node server.js
3- open terminal in fromtend and run npm start 

or

### Prerequisites
- Docker
- Docker Compose

### Run the Project
```bash
docker-compose up --build


Then access:

Frontend: http://localhost:3000

Backend: http://localhost:5000

Processor: http://localhost:8000


