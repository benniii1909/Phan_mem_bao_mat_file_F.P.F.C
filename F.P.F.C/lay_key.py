import winreg
def key_giai_ma():
    # Hàm lấy key từ Registry
    registry_path = r"SOFTWARE\\F.P.F.C"  # Đường dẫn Registry
    key_name = "EncryptionKey"          # Tên giá trị lưu key
    try:
            # Mở Registry và lấy giá trị key
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_READ)
        stored_key, _ = winreg.QueryValueEx(reg_key, key_name)
        winreg.CloseKey(reg_key)
        #print("Key đã lấy từ Registry:")
        #print(stored_key)
    except FileNotFoundError:
        print("Không tìm thấy key trong Registry. Đảm bảo key đã được tạo trước đó.")
    except Exception as e:
        print(f"Lỗi khi lấy key từ Registry: {e}")
    return stored_key

# Sử dụng hàm để lấy key từ Registry
key_giai_maa = key_giai_ma()

