from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os
from lay_key import * 

 # Giả sử key_giai_maa đã được định nghĩa trong module này
def giai_ma(file_giai_ma,dinh_dang_file):
    # Khóa Base64 đã được mã hóa (cung cấp từ trước)
    key_base64 = key_giai_maa  # Khóa Base64

    # Giải mã Base64 thành byte
    key = base64.b64decode(key_base64)

    # Hàm kiểm tra tính hợp lệ của khóa (có thể giải mã thử một phần của file)
    def check_key(input_file_path, key):
        try:
            # Đọc file mã hóa
            with open(input_file_path, 'rb') as input_file:
                iv = input_file.read(16)  # Lấy IV từ đầu file
                encrypted_data = input_file.read()  # Đọc phần dữ liệu đã mã hóa

            # Khởi tạo Cipher AES với chế độ CBC
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            # Thực hiện giải mã thử một phần dữ liệu (ví dụ, 32 byte đầu tiên)
            decrypted_data = decryptor.update(encrypted_data[:32]) + decryptor.finalize()

            # Kiểm tra xem dữ liệu đã giải mã có hợp lệ không
            # Bạn có thể thực hiện kiểm tra hợp lệ ở đây, ví dụ, kiểm tra nếu dữ liệu giải mã có thể đọc được.
            # Ví dụ đơn giản: kiểm tra nếu có dữ liệu không rỗng
            if len(decrypted_data) == 0:
                print("Dữ liệu giải mã không hợp lệ.")
                return False

            # Nếu giải mã thành công và hợp lệ
            return True

        except Exception as e:
            # Nếu có lỗi trong quá trình giải mã, nghĩa là khóa sai
            print(f"Lỗi khi giải mã thử: {e}")
            return False

    # Hàm giải mã file (thực hiện kiểm tra tính hợp lệ trước khi giải mã)
    def decrypt_file(input_file_path, output_file_path):
        # Kiểm tra tính hợp lệ của khóa
        if not check_key(input_file_path, key):
            print("Khóa không chính xác! Không thể giải mã.")
            return

        # Kiểm tra xem file đầu vào có tồn tại không
        if not os.path.exists(input_file_path):
            print(f"File {input_file_path} không tồn tại.")
            return

        # Đọc file đã mã hóa
        with open(input_file_path, 'rb') as input_file:
            iv = input_file.read(16)  # Lấy IV từ đầu file
            encrypted_data = input_file.read()  # Đọc phần dữ liệu đã mã hóa

        # Khởi tạo Cipher AES với chế độ CBC
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Thực hiện giải mã
        try:
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            # Loại bỏ padding (Padding byte luôn là giá trị của số byte đã được thêm vào)
            padding_length = decrypted_data[-1]
            decrypted_data = decrypted_data[:-padding_length]

            # Ghi dữ liệu giải mã vào file output
            with open(output_file_path, 'wb') as output_file:
                output_file.write(decrypted_data)

            print(f"File đã được giải mã và lưu tại {output_file_path}")

        except Exception as e:
            print(f"Lỗi khi giải mã: {e}")
            return
        
    def lay_sau_dau_slash(input_str):

        last_slash_index = input_str.rfind('/')
        if last_slash_index == -1:
            return ""  # Trả về chuỗi rỗng nếu không có dấu '/'
        return input_str[last_slash_index + 1:]
    
    def kq(input_str):
        last_slash_index = input_str.rfind('.')
        if last_slash_index == -1:
            return input_str  # Trả về chuỗi gốc nếu không có dấu '/'
        return input_str[:last_slash_index]
    
    def mo_file(file_path):
        os.startfile(file_path)

    print(lay_sau_dau_slash(file_giai_ma))
    input_file = file_giai_ma # Đường dẫn đến file mã hóa
    output_file = kq(lay_sau_dau_slash(file_giai_ma))+"."+dinh_dang_file  # Đường dẫn lưu file đã giải mã
    # Gọi hàm giải mã file
    decrypt_file(input_file, output_file)
    mo_file(output_file)
    return output_file
