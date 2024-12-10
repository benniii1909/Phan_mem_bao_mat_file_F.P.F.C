import psutil
import time

kt=False
def theo_doi_file_dang_chay(stop_flag):

    def get_new_process(initial_processes):
        """So sánh danh sách tiến trình hiện tại với danh sách ban đầu để tìm tiến trình mới."""
        current_processes = {p.pid: p.info for p in psutil.process_iter(['pid', 'name', 'exe', 'username', 'status'])}
        new_processes = {pid: info for pid, info in current_processes.items() if pid not in initial_processes}
        return new_processes

    def is_user_application(process_info):
        """Kiểm tra xem tiến trình có phải là ứng dụng giao diện người dùng."""
        exe_path = process_info.get('exe', '')
        username = process_info.get('username', None)
        process_name = process_info.get('name', '').lower()
        status = process_info.get('status', '')

        # Loại trừ các tiến trình hệ thống phổ biến
        system_processes = [
            'svchost.exe', 'sppsvc.exe', 'services.exe', 'explorer.exe', 
            'taskhost.exe', 'csrss.exe', 'winlogon.exe', 'dwm.exe'
        ]

        # Loại bỏ các tiến trình nền không giao diện người dùng
        background_processes = [
            'chrome.exe',  # Trình duyệt nền
            'opera.exe',
            'edge.exe',
            'msedgewebview2.exe'  # WebView runtime
        ]

        # Tiến trình phải có đường dẫn thực thi hợp lệ và không thuộc thư mục hệ thống
        is_valid_exe = exe_path and not exe_path.lower().startswith("c:\\windows\\")

        # Tiến trình phải có người dùng (không phải hệ thống) và không nằm trong danh sách loại trừ
        is_not_system = username is not None and process_name not in system_processes

        # Tiến trình không phải là ứng dụng nền không cần thiết
        is_not_background = process_name not in background_processes

        # Tiến trình phải ở trạng thái đang chạy
        is_active = status in [psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING]

        return is_valid_exe and is_not_system and is_not_background and is_active

    def monitor_process(process_pid):
        global kt

        """Theo dõi tiến trình cho đến khi nó kết thúc."""
        try:
            process = psutil.Process(process_pid)
            print(f"Đang theo dõi tiến trình: {process.name()} (PID: {process_pid})")
            while process.is_running() and process.status() != psutil.STATUS_ZOMBIE and not stop_flag.is_set():
                #print(f"Tiến trình {process_pid} đang chạy...")
                time.sleep(0.1)
            print(f"Tiến trình {process_pid} đã kết thúc. Kết thúc chương trình.")
            kt=True

            exit(0)  # Thoát chương trình khi tiến trình kết thúc
        except psutil.NoSuchProcess:
            print(f"Không tìm thấy tiến trình với PID: {process_pid}. Kết thúc chương trình.")
            kt=True
            exit(0)  # Thoát chương trình nếu tiến trình không tồn tại

    def main():
        global kt
        print("Đang lấy danh sách tiến trình hiện tại...")
        initial_processes = {p.pid: p.info for p in psutil.process_iter(['pid', 'name', 'exe', 'username', 'status'])}

        # Khởi động tiến trình mục tiêu ngay sau khi script bắt đầu
        time.sleep(3)  # Cho phép tiến trình mục tiêu khởi động

        # Tìm tiến trình mới
        new_processes = get_new_process(initial_processes)

        # Lọc chỉ các tiến trình là ứng dụng giao diện người dùng
        user_applications = {pid: info for pid, info in new_processes.items() if is_user_application(info)}

        if not user_applications:
            kt=True
            print("Không có ứng dụng mới nào được mở.")
        else:
            for pid, info in user_applications.items():
                print(f"Phát hiện ứng dụng mới: {info['name']} (PID: {pid})")
                monitor_process(pid)
    main()

