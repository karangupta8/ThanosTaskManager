# Infinity Snap (Thanos Task Manager)

A fun computer vision + systems project inspired by Thanos and the Infinity Gauntlet. Perform a finger snap gesture in front of your webcam, and the program will randomly select half of your running processes to "disappear".

By default, it runs in **dry run mode** (only prints processes), so your system is safe until you explicitly disable it.

> "Perfectly balanced, as all things should be..."

---

## Features

*   **Visual Snap Detection**: Uses OpenCV for real-time webcam processing.
*   **Process Management**: Uses `psutil` to handle system processes.
    *   Randomly selects exactly half of eligible processes.
    *   Maintains a `DO_NOT_KILL` list for critical system apps.
    *   Configurable dry run mode to avoid accidental termination.
*   **Sound Effects**: Plays the iconic snap sound when triggered.
*   **Dynamic GUI**: Built with Tkinter, featuring:
    *   Webcam feed for detection.
    *   A list of "snapped" processes that fade away like ashes.
    *   Final purple quote display.

---

## Requirements

*   Python 3.6+
*   Webcam
*   Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Configuration

Inside `ThanosTaskManager.py`, you can configure:

*   `DRY_RUN = True` → Set to `False` to actually terminate processes.
*   `DO_NOT_KILL` → List of process names to ignore (e.g., `explorer.exe`).
*   `SNAP_SOUND_PATH` → Path to your snap sound file (`snap.mp3`).

---

## Usage

1.  Ensure `snap.mp3` is in the project folder.
2.  Run the script:
    ```bash
    python ThanosTaskManager.py
    ```
3.  Hold your hand in front of the camera and perform a finger snap gesture.
4.  Watch as half your tasks turn to dust.

---

## Safety Notes

*   **Dry run mode is enabled by default.** No processes will be killed unless you change the config.
*   Use the `DO_NOT_KILL` list to protect important work!
*   This project is for educational/entertainment purposes only. Use with caution.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
