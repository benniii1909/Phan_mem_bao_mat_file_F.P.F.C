from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os
import base64
import winreg
from tkinter import messagebox

# Hàm tạo và lưu key vào Registry
def generate_and_store_key():
    registry_path = r"SOFTWARE\\F.P.F.C"  # Đường dẫn Registry
    key_name = "EncryptionKey"          # Tên giá trị lưu key

    # Kiểm tra xem key đã tồn tại trong Registry hay chưa
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ)
        stored_key, _ = winreg.QueryValueEx(reg_key, key_name)
        winreg.CloseKey(reg_key)
        print("Key đã tồn tại trong Registry:")
        print(stored_key)
        return stored_key
    except FileNotFoundError:
        pass  # Nếu không tìm thấy, tiếp tục tạo key mới

    # Tạo key ngẫu nhiên
    key = os.urandom(32)  # 32 bytes tương đương 256-bit key
    key_b64 = base64.b64encode(key).decode('utf-8')

    # Lưu key vào Registry
    try:
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path)
        winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, key_b64)
        winreg.CloseKey(reg_key)
        print("Key đã được tạo và lưu vào Registry:")
        print(key_b64)
    except Exception as e:
        print(f"Lỗi khi lưu key vào Registry: {e}")
        return None

    return key_b64

# Gọi hàm tạo và lưu key
if __name__ == "__main__":
    generate_and_store_key()
    messagebox.showinfo("F.P.F.C","Đã tạo một key và lưu vào thiết bị")
