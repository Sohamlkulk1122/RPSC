📷 Application Demo

(Add screenshots or GIF here after uploading images)

Example:

/screenshots/gui.png
/screenshots/detection.png
/screenshots/report.png
✨ Features

🚘 Automatic Number Plate Detection
📸 Upload vehicle images for scanning
🎥 Live webcam number plate recognition
🔎 Search number plates in database logs
📊 Export detection reports to PDF
💾 Automatic CSV database logging
🖼 Save detected vehicle images
🌙 Modern Dark Mode GUI using CustomTkinter
⚡ Fast real-time detection

🧠 How the System Works
1️⃣ Image Acquisition

Upload image

Or capture frames from webcam

2️⃣ Image Processing

The image is processed using Digital Image Processing techniques:

Convert to Grayscale

Apply Bilateral Filtering

Use Canny Edge Detection

3️⃣ Plate Detection

Contours are detected and filtered based on:

Shape

Size

Aspect Ratio

This isolates the license plate region.

4️⃣ OCR Extraction

The detected plate region is processed using Tesseract OCR:

ROI extraction

Image resizing

Otsu thresholding

Character whitelist filtering

5️⃣ Data Logging

The detected plate is stored with:

Timestamp

Plate number

Detection image

🖥️ GUI Interface

The application interface contains:

Section	Function
Upload Photo	Detect plate from image
Live Scan	Real-time detection using webcam
Search Plate	Find vehicle in database
Logs Panel	Display recent detections
Export PDF	Generate report
📁 Project Structure
RPSC/
│
├── main.py
├── database.csv
├── detections/
│   ├── plate_image1.jpg
│   ├── plate_image2.jpg
│
├── screenshots/
│   ├── gui.png
│   ├── detection.png
│
├── Report_XXXXXX.pdf
└── README.md
⚙️ Installation
1️⃣ Clone Repository
git clone https://github.com/Sohamlkulk1122/RPSC.git
cd RPSC
2️⃣ Install Dependencies
pip install opencv-python
pip install pytesseract
pip install numpy
pip install customtkinter
pip install pillow
pip install fpdf

Or install all at once:

pip install opencv-python pytesseract numpy customtkinter pillow fpdf
🔧 Install Tesseract OCR

Download Tesseract:

https://github.com/tesseract-ocr/tesseract

After installing, update the path inside main.py

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

For Linux:

sudo apt install tesseract-ocr
▶️ Running the Application
python main.py

The ANPR GUI application will launch.

📊 Database Example

The system stores data inside database.csv.

Timestamp,Plate Number
2026-03-12 14:20:11,MH12AB1234
2026-03-12 14:22:31,MH14CD5678
📄 PDF Report Example

The generated report contains:

Timestamp	Plate Number
2026-03-12 14:20:11	MH12AB1234
2026-03-12 14:22:31	MH14CD5678
🧪 Technologies Used
Technology	Purpose
Python	Programming Language
OpenCV	Computer Vision
Tesseract OCR	Text Recognition
NumPy	Image Processing
CustomTkinter	GUI Framework
Pillow	Image Handling
FPDF	Report Generation
🚀 Future Improvements

Possible enhancements for this project:

🤖 YOLOv8 Deep Learning plate detection
🌍 Country-specific plate recognition
☁ Cloud database integration
📡 Multiple CCTV camera support
📱 Mobile app dashboard
🧠 AI model training for better accuracy
📊 Detection analytics dashboard

👨‍💻 Author

Soham Kulkarni

GitHub
https://github.com/Sohamlkulk1122

⭐ Support the Project

If you found this project helpful:

⭐ Star the repository
🍴 Fork it
🐛 Report issues

📜 License

This project is released under the MIT License.

💡 Pro tip:
To make your repo look 10× more impressive, add:

screenshots/ folder

GUI images

GIF demo

Example:

screenshots/
  gui.png
  detection.png
  webcam.gif
