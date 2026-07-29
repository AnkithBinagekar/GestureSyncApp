@echo off
echo 🛠 Building GUI with MediaPipe...

pyinstaller --noconsole --onefile ^
--add-data "assets\\expression_pointer.tflite;assets" ^
--add-data "C:\\Python310\\Lib\\site-packages\\mediapipe\\python\\_framework_bindings.cp310-win_amd64.pyd;mediapipe\\python" ^
--add-data "C:\\Python310\\Lib\\site-packages\\mediapipe\\modules;mediapipe\\modules" ^
gui_app.py

pause
