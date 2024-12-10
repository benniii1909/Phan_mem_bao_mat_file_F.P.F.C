from tkinter.filedialog import askopenfilename
import os
from tkinterdnd2 import TkinterDnD, DND_FILES
import customtkinter as ctk
from PIL import Image, ImageTk
from ma_hoa import *
import pyperclip
from lay_key import *
from tkinter import messagebox
from ma_hoa import *
from giai_ma import *
import threading
from chay_file import*

def giao_dien():
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


    def copy_text():
        text_to_copy = key_giai_maa  # Đoạn văn bản cần sao chép
        pyperclip.copy(text_to_copy)
        print(f"Đã sao chép: {text_to_copy}")

    def load_resized_image(path, size=(150, 150)):
        """Tải và chỉnh kích thước ảnh PNG."""
        image = Image.open(path)
        image = image.resize(size, Image.Resampling.LANCZOS)  # Thay đổi kích thước ảnh
        return ImageTk.PhotoImage(image)

    # Hàm chọn file
    def browse_file():
        """Mở cửa sổ chọn file và xử lý file đã chọn."""
        global current_file, image_label
        file_path = askopenfilename()
        if not file_path:
            return  # Nếu người dùng hủy chọn file
        
        current_file = file_path
        drop_label.configure(text=f"Tệp: {os.path.basename(file_path)}",font=("Arial",14,"bold"))

        
        # Hiển thị hình ảnh tương ứng với loại file
        if not image_label:
            image_label = ctk.CTkLabel(right_frame, text="")
            image_label.place(relx=0.5, rely=0.5, anchor="center")
        
        if file_path.endswith('.bin'):
            image_label.configure(image=bin_image)  # Hiển thị ảnh cho file .bin
            open_button.configure(state="normal")
            encrypt_button.configure(state="disabled")
        else:
            image_label.configure(image=default_image)  # Hiển thị ảnh mặc định
            open_button.configure(state="disabled")
            encrypt_button.configure(state="normal")

    # Hàm xử lý kéo file vào
    def on_file_drop(event):
        """Xử lý khi file được kéo vào."""
        global current_file, image_label
        file_path = event.data.strip()
        current_file = file_path

        drop_label.configure(text=f"Tệp: {os.path.basename(file_path)}",font=("Arial",14,"bold"))
        if not image_label:
            image_label = ctk.CTkLabel(right_frame, text="")
            image_label.place(relx=0.5, rely=0.5, anchor="center")
        
        if file_path.endswith('.bin'):
            image_label.configure(image=bin_image)
            open_button.configure(state="normal")
            encrypt_button.configure(state="disabled")
        else:
            image_label.configure(image=default_image)
            open_button.configure(state="disabled")
            encrypt_button.configure(state="normal")

    # Hàm xử lý nút "X"
    def clear_file():
        global current_file, image_label
        current_file = None
        drop_label.configure(text="Kéo hoặc nhấn để chọn tệp",font=("Arial", 20, 'bold'))

        open_button.configure(state="disabled")
        encrypt_button.configure(state="disabled")
        if image_label:
            image_label.destroy()
            image_label = None

    def open_file():
        if current_file and selected_format:
            lmao=giai_ma(current_file,selected_format)
            chay_file()
            xoa_file(lmao)

        if selected_format=="":
            messagebox.showerror("Lỗi", "Vui lòng chọn định file")
    def encrypt_file():
        if current_file:
            key = key_entry.get()
            try:
                test = base64.b64decode(key)
                kt=True
            except:
                kt=False
            if key:
                if kt:
                    ma_hoa(key, current_file)
                    messagebox.showinfo("Thông báo", f"Đã mã hóa tệp: {os.path.basename(current_file)} với khóa: {key}")
                else:
                    messagebox.showerror("Lỗi", "Key không hợp lệ!")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập Key trước khi mã hóa!")

    def update_suggestions(event):
        # Lấy nội dung hiện tại trong entry của select_box
        user_input = select_box.get().lower()
        # Lọc danh sách định dạng phù hợp với nội dung nhập
        filtered_formats = [fmt for fmt in file_formats if fmt.startswith(user_input)]
        # Cập nhật giá trị trong combobox
        select_box.configure(values=filtered_formats)
        if filtered_formats:
            select_box.set(user_input)  # Giữ nguyên phần đã nhập
        else:
            select_box.set("")  # Xóa nếu không có gợi ý phù hợp


    selected_format = ""
    # Hàm xử lý khi chọn định dạng từ menu
    def on_combobox_select(choice):
        global selected_format
        selected_format = choice  # Lưu kết quả vào biến toàn cục
        print(f"Đã chọn định dạng tệp: {selected_format}")


    # Biến toàn cục
    current_file = None
    image_label = None

    # Giao diện
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = TkinterDnD.Tk()
    root.title("F.P.F.C")
    root.geometry("600x400")
    root.configure(bg="#5c5b5b")

    left_frame = ctk.CTkFrame(root, width=200, height=400, corner_radius=10, fg_color="#2e2e2e")
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    open_button = ctk.CTkButton(left_frame, text="Mở", state="disabled", command=open_file, font=("Arial", 25,"bold"), width=150, height=50)
    open_button.pack(pady=20, padx=10)

    encrypt_button = ctk.CTkButton(left_frame, text="Mã Hoá", state="disabled", command=encrypt_file, font=("Arial", 25,"bold"), width=150, height=50)
    encrypt_button.pack(pady=20, padx=10)

    key_entry = ctk.CTkEntry(left_frame, placeholder_text="Nhập Key tại đây", font=("Arial", 14),
        height=35)
    key_entry.pack(pady=20, padx=10)

    right_frame = ctk.CTkFrame(root, width=400, height=400, corner_radius=10, fg_color="#2e2e2e")
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Nút "ẩn" cho toàn bộ vùng kéo file
    browse_button = ctk.CTkButton(
        right_frame,
        text="",
        width=400,
        height=400,
        fg_color="#2e2e2e",
        hover_color="#4e4e4e",hover=False,  
        command=browse_file,
        corner_radius=10
    )
    browse_button.place(relx=0.5, rely=0.5, anchor="center")

    copy_button = ctk.CTkButton(
        left_frame,
        text="C",  # Nội dung nút (chữ "C" đại diện cho "Copy")
        width=20,  # Chiều rộng nút
        height=20,  # Chiều cao nút
        font=("Arial", 16, "bold"),  # Font chữ của nội dung
        corner_radius=30,  # Góc bo tròn (giúp nút tròn)# Màu nền của nút
        text_color="white",  # Màu chữ  # Màu khi di chuột qua
        command=copy_text  # Gắn chức năng sao chép
    )

    # Định vị nút ở góc dưới bên trái
    copy_button.place(relx=0.02, rely=0.95, anchor="sw")
    drop_label = ctk.CTkLabel(left_frame, text="Sao chép key thiết bị", font=("Arial", 12, 'bold'))
    drop_label.place(relx=0.25, rely=0.95, anchor="sw")

    drop_label = ctk.CTkLabel(right_frame, text="Kéo hoặc nhấn để chọn tệp", font=("Arial", 20, 'bold'))
    drop_label.place(relx=0.5, rely=0.2, anchor="center")

    clear_button = ctk.CTkButton(right_frame, text="X", width=30, height=30, font=("Arial", 12), fg_color="#5c5b5b", text_color="white", corner_radius=30, command=clear_file)
    clear_button.place(relx=0.95, rely=0.05, anchor="center")

    # Tải ảnh
    default_image = load_resized_image("F.P.F.C/icon.png", size=(150, 150))
    bin_image = load_resized_image("F.P.F.C/bin.png", size=(150, 150))

    select_label = ctk.CTkLabel(left_frame, text="Chọn định dạng tệp:", font=("Arial", 14))
    select_label.pack(pady=(7, 5), padx=10)

    file_formats = [
        "doc", "docx","xls", "xlsx","ppt", "pptx","pdf",
        "png", "jpg", "jpeg", "gif", "bmp", "svg", "tiff", "webp","mp4", "mp3", # Hình ảnh
        "txt",   "odt", "rtf", "md", "tex",  # Văn bản
        "csv", "ods",  # Bảng tính
        "mkv", "mov", "avi", "flv", "wmv", "webm",  # Video
        "wav", "aac", "flac", "ogg", "m4a",  # Âm thanh
        "zip", "rar", "7z", "tar", "gz", "iso",  # File nén
        "bin", "exe", "dll", "apk", "deb", "dmg", "pkg", "msi"  # Khác
    ]

    # Tạo select box
    select_box = ctk.CTkComboBox(
        left_frame,
        values=file_formats,  # Sử dụng danh sách định dạng file
        font=("Arial", 14),
        command=on_combobox_select  # Hàm xử lý khi chọn
    )
    select_box.pack(pady=5, padx=10)

    # Cài đặt giá trị mặc định cho combo box
    select_box.set("...")  # Giá trị mặc định là "txt"

    # Ràng buộc sự kiện nhập dữ liệu vào hộp chọn để gợi ý tự động
    select_box.bind("<KeyRelease>", update_suggestions)

    # **Cho phép nhập liệu khi danh sách mở rộng**
    # Ràng buộc sự kiện nhấn phím lên/ xuống để giữ lại khả năng nhập liệu
    def prevent_dropdown_interruption(event):
        select_box.event_generate("<KeyRelease>", when="tail")

    # Hàm xử lý khi nhấn nút "X" để xóa nội dung trong ô nhập key
    def clear_key_entry():
        key_entry.delete(0, 'end')  # Xóa hết nội dung trong ô nhập

    # Thêm nút "X" vào ô nhập key, với nền trong suốt và không có hiệu ứng hover
    clear_key_button = ctk.CTkButton(
        left_frame,
        text="x",  # Nội dung nút là chữ "X"
        width=5,
        height=5,
        font=("Arial", 16, "bold"),
        corner_radius=100,
        fg_color="transparent",  # Nền trong suốt
        text_color="black",  # Màu chữ là đen hoặc bạn có thể thay đổi màu chữ
        command=clear_key_entry,  # Gắn hàm xóa nội dung khi nhấn nút
    )

    # Đặt nút "X" ở bên phải của ô nhập key, sao cho nó không che khuất nội dung
    clear_key_button.place(relx=0.9, rely=0.57, anchor="e")

    root.resizable(False, False)  # Ngừng thay đổi kích thước cửa sổ
    # Ẩn nút maximize
    root.overrideredirect(False)  
    # Gắn sự kiện nhấn mở menu, giữ danh sách hoạt động song song nhập liệu
    select_box.bind("<Button-1>", prevent_dropdown_interruption)
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_file_drop)
    root.mainloop()