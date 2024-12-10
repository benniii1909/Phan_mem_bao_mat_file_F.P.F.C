from nhan_dien_mat import nhan_dien_mat
from theo_doi_luu_file import theo_doi_luu_file
from theo_doi_file_dang_chay import theo_doi_file_dang_chay
from chong_sao_chep import chong_sao_chep
import threading
import time

def chay_file():
    # Tạo một cờ dừng dùng chung
    stop_event = threading.Event()

    # Tạo các thread, truyền cờ dừng vào từng hàm
    thread_theo_doi_file_dang_chay = threading.Thread(target=theo_doi_file_dang_chay, args=(stop_event,))
    thread_nhan_dien_mat = threading.Thread(target=nhan_dien_mat, args=(stop_event,))
    thread_theo_doi_luu_file = threading.Thread(target=theo_doi_luu_file, args=(stop_event,))
    thread_chong_sao_chep = threading.Thread(target=chong_sao_chep, args=(stop_event,))

    # Khởi chạy các thread
    thread_theo_doi_file_dang_chay.start()
    thread_nhan_dien_mat.start()
    thread_theo_doi_luu_file.start()
    thread_chong_sao_chep.start()

    try:
        # Giám sát và giữ chương trình chính hoạt động
        while True:
            if (not thread_theo_doi_file_dang_chay.is_alive()) or (not thread_nhan_dien_mat.is_alive()) or (not thread_theo_doi_luu_file.is_alive()) or (not thread_chong_sao_chep.is_alive()):
                print("Một thread đã dừng, gửi tín hiệu dừng cho tất cả.")
                stop_event.set()  # Gửi tín hiệu dừng
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("Người dùng dừng chương trình.")
        stop_event.set()  # Gửi tín hiệu dừng cho tất cả

    # Đợi tất cả các thread hoàn thành
    thread_theo_doi_file_dang_chay.join()
    thread_nhan_dien_mat.join()
    thread_theo_doi_luu_file.join()
    thread_chong_sao_chep.join()
    print("Tất cả các thread đã dừng.")