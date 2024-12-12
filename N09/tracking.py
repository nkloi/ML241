import tkinter as tk
from tkinter import filedialog, Label, Button
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
import os
import sys
import math

class VideoApp:
    def __init__(self, root, model_path):
        self.root = root
        self.root.title("Person Tracking")
        self.root.geometry("1100x500")
        self.root.resizable(True, True)
        self.xoa = 0
        self.yoa = 0
        self.model = YOLO(model_path)

        self.control_frame = tk.Frame(self.root, width=300, height=500, bg="lightgray")
        self.control_frame.grid(row=0, column=0, sticky="ns")
        self.control_frame.grid_propagate(False)

        self.btn_choose = Button(self.control_frame, text="Chọn Video", command=self.select_video, width=15)
        self.btn_choose.grid(row=0, column=0, pady=10)

        self.btn_camera = Button(self.control_frame, text="Camera", command=self.use_camera, width=15)
        self.btn_camera.grid(row=1, column=0, pady=10)

        self.btn_stop = Button(self.control_frame, text="Dừng", command=self.stop_video, width=15)
        self.btn_stop.grid(row=2, column=0, pady=10)

        self.btn_start = Button(self.control_frame, text="Chạy", command=self.start_video, width=15)
        self.btn_start.grid(row=3, column=0, pady=10)

        self.btn_reset = Button(self.control_frame, text="Reset", command=self.reset_app, width=15)
        self.btn_reset.grid(row=4, column=0, pady=10)

        self.btn_quit = Button(self.control_frame, text="Thoát", command=self.quit_app, width=15, bg="red", fg="white")
        self.btn_quit.grid(row=5, column=0, pady=20)

        self.delay_slider = tk.Scale(self.control_frame, from_=10, to=50, orient="horizontal", label="Delay (ms)")
        self.delay_slider.set(20)
        self.delay_slider.grid(row=6, column=0, pady=10)

        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.grid(row=0, column=1, sticky="nsew")
        self.video_frame.grid_propagate(False)

        self.video_label = Label(self.video_frame)
        self.video_label.pack(fill="both", expand=True)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.mouse_position_label = Label(self.control_frame, text="Tọạ độ chuột: (x, y)", bg="lightgray")
        self.mouse_position_label.grid(row=7, column=0, pady=10)

        self.click_position = None

        self.video_label.bind("<Motion>", self.show_mouse_position)
        self.video_label.bind("<Button-1>", self.show_click_position)

        self.running = False
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        self.vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.update_video()

    def select_video(self):
        file_path = filedialog.askopenfilename(
            title="Chọn Video",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")]
        )
        if file_path:
            self.video_source = file_path
            self.vid.release()
            self.vid = cv2.VideoCapture(self.video_source)
            self.running = True

    def use_camera(self):
        self.video_source = 0
        self.vid.release()
        self.vid = cv2.VideoCapture(self.video_source)
        self.running = True

    def start_video(self):
        self.running = True

    def stop_video(self):
        self.running = False

    def reset_app(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def quit_app(self):
        self.root.destroy()

    def update_video(self):
        if self.running:
            ret, frame = self.vid.read()
            if ret:
                label_width = self.video_label.winfo_width()
                label_height = self.video_label.winfo_height()

                frame = cv2.resize(frame, (label_width, label_height))
                results = self.model(frame, stream=True)

                annotated_frame = frame.copy()
                boxes = []

                for result in results:
                    boxes.extend(result.boxes.xyxy.cpu().numpy())

                nearest_box = None
                min_distance = float('inf')

                if self.click_position:
                    click_x, click_y = self.click_position

                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box)
                        x_avg = (x1 + x2) / 2
                        y_avg = (y1 + y2) / 2
                        distance = math.sqrt((x_avg - click_x) ** 2 + (y_avg - click_y) ** 2)

                        if distance < min_distance:
                            min_distance = distance
                            nearest_box = (x1, y1, x2, y2, x_avg, y_avg)

                for box in boxes:
                    x1, y1, x2, y2 = map(int, box)
                    if nearest_box and (x1, y1, x2, y2) == nearest_box[:4]:
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2) 
                        cv2.circle(annotated_frame, (int(nearest_box[4]), int(nearest_box[5])), 5, (0, 255, 0), -1)
                    else:
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  

                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                annotated_frame = Image.fromarray(annotated_frame)
                annotated_frame = ImageTk.PhotoImage(image=annotated_frame)

                self.video_label.configure(image=annotated_frame)
                self.video_label.image = annotated_frame

        delay = self.delay_slider.get()
        self.root.after(delay, self.update_video)

    def show_mouse_position(self, event):
        x, y = event.x, event.y
        self.mouse_position_label.config(text=f"Tọạ độ chuột: ({x}, {y})")

    def show_click_position(self, event):
        x, y = event.x, event.y
        self.click_position = (x, y)
        self.mouse_position_label.config(text=f"Vị trí click: ({x}, {y})")

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    root = tk.Tk()
    model_path = "best.pt"
    app = VideoApp(root, model_path)
    root.mainloop()