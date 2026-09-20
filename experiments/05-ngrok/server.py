from http.server import BaseHTTPRequestHandler, HTTPServer

# การทดลองนี้จะใช้ Flask app ที่ทำงานบน localhost:5000
# ดังนั้นเราจะไม่สร้างเว็บเซิร์ฟเวอร์แยกต่างหาก แต่ให้ใช้ ngrok เชื่อมกับ Flask ได้เลย


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # ข้อความนี้ใช้เฉพาะกรณีที่นักเรียนต้องการเห็นข้อความสั้น ๆ ก่อนเปิด ngrok
        message = "โปรดรัน Flask app ก่อน แล้วจึงรัน ngrok http 5000\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def log_message(self, format, *args):
        # ซ่อน log เพื่อให้เห็นผลลัพธ์ที่สำคัญชัดเจนขึ้น
        pass


if __name__ == "__main__":
    port = 5000
    server = HTTPServer(("0.0.0.0", port), DemoHandler)
    print(f"เซิร์ฟเวอร์นี้กำลังรอที่ http://localhost:{port}")
    print("แต่สำหรับการทดลองจริง ให้รัน Flask app ในโฟลเดอร์ 01-flask ก่อน")
    print("แล้วรัน: ngrok http 5000")
    server.serve_forever()
