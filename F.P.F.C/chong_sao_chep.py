import win32clipboard as clipboard
import time

def chong_sao_chep(stop_flag):
    def xoa():
        try:
            clipboard.OpenClipboard()
            clipboard.EmptyClipboard()
        except Exception as e:
            print(f"Lỗi khi mở clipboard: {e}")
        finally:
            try:
                clipboard.CloseClipboard()
            except:
                pass

    def xoa_het(interval=0.1):
        try:
            while not stop_flag.is_set():
                xoa()
                time.sleep(interval)
        except KeyboardInterrupt:
            pass

    xoa_het(interval=0.1)
