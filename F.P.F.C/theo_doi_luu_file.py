import os
import time
import psutil  
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def theo_doi_luu_file(stop_flag):
    def xoa_file(duong_dan):
        try:
            # Kiểm tra xem tệp có tồn tại không
            if os.path.exists(duong_dan):
                # Xóa tệp
                os.remove(duong_dan)
                print(f"Đã xóa tệp: {duong_dan}")
            else:
                print(f"Tệp không tồn tại: {duong_dan}")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi xóa tệp: {e}")
    # Các định dạng file ảnh hợp lệ
    DINH_DANG_ANH = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    # Hàm kiểm tra xem file có phải là file ảnh không
    def la_file_anh(path):
        _, extension = os.path.splitext(path)
        return extension.lower() in DINH_DANG_ANH

    # Hàm xử lý khi có file mới được tạo
    def xu_ly_file_moi(event):
        if not event.is_directory and la_file_anh(event.src_path):
            print(f"File ảnh mới được tạo: {event.src_path}")

    # Hàm lấy danh sách các ổ đĩa
    def lay_danh_sach_o_dia():
        o_dia = []
        for partition in psutil.disk_partitions():
            if os.name == 'nt':  # Windows
                o_dia.append(partition.device)
            else:  # Linux/macOS
                o_dia.append(partition.mountpoint)
        return o_dia

    # Theo dõi một thư mục cụ thể
    def theo_doi_thu_muc(thu_muc_goc):
        print(f"Theo dõi thư mục: {thu_muc_goc}")
        observer = Observer()

        # Tạo handler và gắn sự kiện
        event_handler = FileSystemEventHandler()
        event_handler.on_created = xu_ly_file_moi  # Gắn hàm xử lý sự kiện

        # Bắt đầu theo dõi
        observer.schedule(event_handler, thu_muc_goc, recursive=True)
        observer.start()
        return observer

    # Hàm chính

    try:
        danh_sach_o_dia = lay_danh_sach_o_dia()
        print(f"Phát hiện các ổ đĩa: {danh_sach_o_dia}")
        observers = []
        for o_dia in danh_sach_o_dia:
            print(f"Đang theo dõi: {o_dia}")
            xoa_file(o_dia)
            observer = theo_doi_thu_muc(o_dia)
            observers.append(observer)
        while not stop_flag.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nDừng theo dõi.")
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
