import cv2
import numpy as np
import psutil, random, os, signal, time
from tkinter import Tk, Label
from threading import Thread
from playsound import playsound


DRY_RUN = True   # If True, just print selected processes, else kill them
DO_NOT_KILL = ["python.exe", "System", "explorer.exe", "systemd"]  # extend as needed
SNAP_SOUND_PATH = "snap.mp3"


def thanos_snap():
    processes = [p.info for p in psutil.process_iter(['pid', 'name'])]
    safe_processes = [p for p in processes if p['name'] not in DO_NOT_KILL]

    if not safe_processes:
        print("No eligible processes to snap.")
        return []

    random.shuffle(safe_processes)
    half = len(safe_processes) // 2
    chosen = safe_processes[:half]

    for proc in chosen:
        if DRY_RUN:
            print(f"[DRY RUN] 💀 Would snap: {proc['name']} (PID: {proc['pid']})")
        else:
            try:
                os.kill(proc['pid'], signal.SIGKILL)
                print(f"💀 Snapped: {proc['name']} (PID: {proc['pid']})")
            except Exception as e:
                print(f"Could not snap {proc['name']}: {e}")

    return [p['name'] for p in chosen]


def ashes_gui(process_list):
    root = Tk()
    root.title("Infinity Snap")
    root.configure(bg="white")
    root.geometry("500x500")

    labels = []
    for i, proc in enumerate(process_list):
        lbl = Label(root, text=proc, fg="white", bg="black", font=("Helvetica", 12))
        lbl.pack()
        labels.append(lbl)

    root.update()

    # Simulate ashes fade-out
    for alpha in range(100, 0, -5):
        gray = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
        for lbl in labels:
            lbl.config(fg=gray)
        root.update()
        time.sleep(0.1)

    # Final quote
    final_lbl = Label(root, text='"Perfectly balanced, as all things should be..."',
                      fg="purple", bg="black", font=("Helvetica", 14, "italic"))
    final_lbl.pack()
    root.update()

    root.mainloop()


def detect_snap():
    cap = cv2.VideoCapture(0)
    detected = False
    snap_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # crude skin color range
        lower = np.array([0, 30, 60], dtype=np.uint8)
        upper = np.array([20, 150, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower, upper)

        # contour detection
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(max_contour)
            if 3000 < area < 7000:  # arbitrary threshold for "snap-like" size
                snap_counter += 1
            else:
                snap_counter = 0

            if snap_counter > 15:  # ~0.5 sec of holding gesture
                detected = True
                break

        cv2.imshow("Snap Detector", mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected


if __name__ == "__main__":
    print("Show your hand and perform a SNAP gesture in front of webcam...")
    if detect_snap():
        print("Snap detected!")
        Thread(target=playsound, args=(SNAP_SOUND_PATH,)).start()
        processes_to_kill = thanos_snap()
        if processes_to_kill:
            ashes_gui(processes_to_kill)
    else:
        print("No snap detected.")
