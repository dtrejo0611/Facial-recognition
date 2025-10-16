# Face Recognition Project (DeepFace + OpenCV + pyttsx3)

This repository contains a small face-recognition demo that captures frames from a webcam, attempts to identify people using DeepFace, logs recognized names with timestamps in a local SQLite database, and optionally greets newly recognized people with speech synthesis.

## Overview

The application opens a video capture (webcam), processes each frame through DeepFace to find matches against a local face database, stores recognition events (name + timestamp) in an SQLite database, and uses a text-to-speech engine to greet newly detected persons. It is implemented with minimal dependencies so it can be extended for production use.

## Features

- Live webcam capture (cv2.VideoCapture).
- Face recognition using DeepFace (VGG-Face model in current code).
- Logging of recognition events into an SQLite database.
- Voice greeting using pyttsx3 when a new person is detected.
- Simple, modular code: recognition logic (proyecto.py) and DB management (dbManager.py).

## Repository structure

- proyecto.py
  - Main application loop. Captures frames, runs recognition, logs events, and speaks greetings.
- dbManager.py
  - Simple SQLite wrapper class `baseDatos` for creating the DB and inserting records.
- (Expect a folder named `db` containing images used by DeepFace for recognition; see "Database and face database" below.)

## Requirements

The core Python packages used:

- Python 3.8+
- deepface
- opencv-python (cv2)
- pyttsx3
- numpy (pulled in by deepface / opencv)
- sqlite3 (standard library)
- (optionally) other DeepFace backends like tensorflow/keras if not already installed by `deepface` installation

## Usage

1. Prepare a `db` folder as the face database (see below).
2. Run the script:
   ```bash
   python proyecto.py
   ```
3. The window titled "Proyecto" will open and show the camera feed.
   - The script reads frames, tries to recognize faces and shows the recognized name on the frame.
   - When a recognized name changes (a different person is detected), the code writes the name and current timestamp to the SQLite DB and attempts to greet them using the computer voice.
   - Press the `q` key in the OpenCV window to quit.

## Database and face database (db) layout

- SQLite DB:
  - Created by `dbManager.baseDatos` as `./miBD.sqlite3` by default.
  - Table: `reconocimientos(persona TEXT, tiempo TIMESTAMP)`
  - Every time a new (different from last) face is detected, `agregarRegistro()` inserts a row with (name, timestamp).
  - You can change path/name by creating `baseDatos(ruta, bd)` with custom parameters.

- DeepFace face database:
  - The script calls DeepFace.find(..., db_path="db", model_name="VGG-Face").
  - Create a `db` directory in the project root. Place one or more reference images for each person to be recognized. DeepFace commonly expects a flat directory of images or subfolders—placing clear face images named to identify the person (or in subfolders) works best.
  - Example layout:
    ```
    project_root/
      db/
        Bill Gates/
          photo1.jpg
          ...
        Elon Musk/
          photo1.jpg
          ...        
    ```
  - DeepFace will return identity paths which the current code parses to extract a person name using string splitting; ensure your `db` structure matches that parsing or adapt the parsing logic.
