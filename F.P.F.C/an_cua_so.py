from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QGraphicsBlurEffect
from PyQt5.QtGui import QPixmap, QScreen
from PyQt5.QtCore import QTimer, Qt

class FullScreenBlurOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Loại bỏ viền cửa sổ
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)

        # Lấy ảnh chụp màn hình
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)  # Chụp toàn bộ màn hình

        # Tạo label hiển thị ảnh
        label = QLabel(self)
        pixmap = QPixmap(screenshot)

        # Áp dụng hiệu ứng làm mờ
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(15)  # Điều chỉnh độ mờ (15 là mức trung bình)
        label.setPixmap(pixmap)
        label.setGraphicsEffect(blur_effect)

        # Mở rộng label để phủ toàn màn hình
        label.setGeometry(self.rect())

        # Đặt bộ hẹn giờ để tự động đóng sau 3 giây

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Tạo và hiển thị cửa sổ overlay với hiệu ứng blur
    overlay = FullScreenBlurOverlay()
    overlay.show()

    # Chạy ứng dụng
    sys.exit(app.exec_())
