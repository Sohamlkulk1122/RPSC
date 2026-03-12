import cv2
import pytesseract
import numpy as np
import customtkinter as ctk
from PIL import Image
import datetime
import os
import csv
import traceback
from tkinter import filedialog, messagebox
from fpdf import FPDF

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# CONFIGURATION
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class ToastNotification(ctk.CTkToplevel):
    def __init__(self, message, color="green"):
        super().__init__()
        self.overrideredirect(True)
        self.geometry(f"300x50+{self.winfo_screenwidth()//2 - 150}+50")
        self.configure(fg_color=color)
        label = ctk.CTkLabel(self, text=message, text_color="white", font=ctk.CTkFont(size=14, weight="bold"))
        label.pack(expand=True)
        self.after(2000, self.destroy)

class ANPRApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Smart Plate Recognition")
        self.geometry("1150x850")
        self.db_path = "database.csv"
        
        if not os.path.exists("detections"): os.makedirs("detections")
        if not os.path.exists(self.db_path) or os.stat(self.db_path).st_size == 0:
            with open(self.db_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Plate Number"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.logo_label = ctk.CTkLabel(self.sidebar, text="ANPR SYSTEM", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=(20, 10))

        self.search_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Search Plate...")
        self.search_entry.pack(pady=5, padx=20)
        
        btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        btn_frame.pack(pady=5)
        ctk.CTkButton(btn_frame, text="🔍", width=40, command=self.search_plate).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="↺", width=40, fg_color="gray", command=self.load_all_logs).grid(row=0, column=1, padx=5)

        ctk.CTkButton(self.sidebar, text="Upload Photo", command=self.upload_image).pack(pady=10, padx=20)
        self.btn_snap = ctk.CTkButton(self.sidebar, text="Live Scan", fg_color="#2ecc71", hover_color="#27ae60", command=self.process_webcam)
        self.btn_snap.pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="Export PDF Report", fg_color="#3498db", hover_color="#2980b9", command=self.export_to_pdf).pack(pady=10, padx=20)

        ctk.CTkLabel(self.sidebar, text="Database Logs:", font=ctk.CTkFont(size=12)).pack(pady=(20, 0))
        self.log_box = ctk.CTkTextbox(self.sidebar, width=200, height=300, font=("Consolas", 11))
        self.log_box.pack(pady=10, padx=10)
        self.load_all_logs()

        # Viewport
        self.main_view = ctk.CTkFrame(self)
        self.main_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.img_label = ctk.CTkLabel(self.main_view, text="Awaiting Input...")
        self.img_label.pack(expand=True, fill="both")

        self.cap = None
        self.is_camera_on = False

    def search_plate(self):
        query = self.search_entry.get().strip().upper()
        if not query: return
        self.log_box.delete("0.0", "end")
        with open(self.db_path, "r") as f:
            reader = csv.reader(f); next(reader)
            for row in reader:
                if len(row) >= 2 and query in row[1].upper():
                    self.log_box.insert("end", f"[{row[0].split()[1]}] {row[1]}\n")

    def load_all_logs(self):
        self.search_entry.delete(0, 'end')
        self.log_box.delete("0.0", "end")
        if os.path.exists(self.db_path) and os.stat(self.db_path).st_size > 0:
            with open(self.db_path, "r") as f:
                reader = csv.reader(f)
                try:
                    next(reader)
                    data = [row for row in reader if len(row) >= 2]
                    for row in reversed(data[-25:]):
                        self.log_box.insert("end", f"[{row[0].split()[1]}] {row[1]}\n")
                except StopIteration: pass

    def export_to_pdf(self):
        pdf = FPDF()
        pdf.add_page(); pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="ANPR System Report", ln=True, align='C')
        pdf.ln(10); pdf.set_fill_color(200, 220, 255)
        pdf.cell(95, 10, "Timestamp", 1, 0, 'C', 1)
        pdf.cell(95, 10, "Plate Number", 1, 1, 'C', 1)
        with open(self.db_path, "r") as f:
            reader = csv.reader(f); next(reader)
            for row in reader:
                if len(row) >= 2:
                    pdf.cell(95, 10, row[0], 1)
                    pdf.cell(95, 10, row[1], 1, 1)
        fn = f"Report_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
        pdf.output(fn); messagebox.showinfo("Success", f"Saved: {fn}")

    def apply_scan_effect(self, img, x, y, w, h):
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return img

    def extract_plate(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # DIP: Bilateral Filter to smooth textures (like phone screen lines) while keeping edges
        blurred = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(blurred, 30, 200)

        cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w)/h
                
                if 2.0 <= aspect_ratio <= 5.5:
                    self.apply_scan_effect(img, x, y, w, h)
                    
                    # ROI PREPROCESSING
                    roi = gray[y:y+h, x:x+w]
                    # Resize to 2x for better OCR
                    roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    # Use Otsu's Thresholding to isolate black text
                    _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    # Strict Whitelist to stop gibberish
                    config = '--psm 7 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                    text = pytesseract.image_to_string(thresh, config=config)
                    clean = "".join(e for e in text if e.isalnum()).upper()
                    
                    # Only log if it looks like a valid plate length
                    if 6 <= len(clean) <= 10:
                        self.save_data(clean, img)
                        ToastNotification(f"DETECTED: {clean}")
                        self.load_all_logs()
                        break
        return img

    def save_data(self, text, frame):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.db_path, "a", newline="") as f:
            csv.writer(f).writerow([ts, text])
        cv2.imwrite(f"detections/{text}.jpg", frame)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_tk = ctk.CTkImage(light_image=Image.fromarray(img_rgb), dark_image=Image.fromarray(img_rgb), size=(800, 500))
        self.img_label.configure(image=img_tk, text="")

    def upload_image(self):
        fp = filedialog.askopenfilename()
        if fp:
            img = cv2.imread(fp)
            if img is not None: self.display_image(self.extract_plate(img))

    def process_webcam(self):
        if not self.is_camera_on:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened(): return
            self.is_camera_on = True
            self.btn_snap.configure(text="STOP SCAN", fg_color="#e74c3c")
            self.update_webcam()
        else:
            self.is_camera_on = False
            if self.cap: self.cap.release()
            self.btn_snap.configure(text="LIVE SCAN", fg_color="#2ecc71")

    def update_webcam(self):
        if self.is_camera_on:
            ret, frame = self.cap.read()
            if ret:
                self.display_image(self.extract_plate(frame))
                self.after(20, self.update_webcam)

if __name__ == "__main__":
    try:
        app = ANPRApp()
        app.mainloop()
    except Exception:
        traceback.print_exc()
        input("Press Enter to exit...")