import numpy as np
import cv2
import mediapipe as mp
import time
import pyautogui  # Để chụp ảnh toàn màn hình
import win32gui
import win32con
import win32api

def nhan_dien_mat(stop_flag):

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(color=(128, 0, 128), thickness=2, circle_radius=1)

    cap = cv2.VideoCapture(0)

    # Biến trạng thái để theo dõi cửa sổ làm mờ
    blurred_screen_active = False

    def check_face_occlusion(face_landmarks, img_w, img_h):
        # Kiểm tra sự tồn tại của các điểm mốc cần thiết
        if len(face_landmarks) < 263:  # Kiểm tra xem có đủ điểm không
            return False

        # Kiểm tra xem có điểm mũi và mắt nào bị lệch quá nhiều không (để phát hiện che khuất)
        left_eye = (face_landmarks[33][0], face_landmarks[33][1])  # Điểm mắt trái
        right_eye = (face_landmarks[263][0], face_landmarks[263][1])  # Điểm mắt phải
        nose = (face_landmarks[1][0], face_landmarks[1][1])  # Mũi
        
        # Tính khoảng cách giữa hai mắt và giữa mắt và mũi
        eye_distance = np.linalg.norm(np.array(left_eye) - np.array(right_eye))
        nose_to_eye_distance = np.linalg.norm(np.array(nose) - np.array(left_eye))
        
        # Nếu khoảng cách giữa hai mắt hoặc mắt và mũi quá nhỏ, có thể mặt bị che khuất
        if eye_distance < 40 or nose_to_eye_distance < 40:
            return True  # Mặt bị che khuất
        return False  # Mặt không bị che khuất

    while cap.isOpened() and not stop_flag.is_set():
        success, image = cap.read()
        if not success:
            break

        start = time.time()

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_2d = []
        face_3d = []
        text = ""
        face_occluded = False

        if results.multi_face_landmarks:
            # Kiểm tra số lượng gương mặt trong khung hình
            if len(results.multi_face_landmarks) > 1:
                text = "Nhiều gương mặt phát hiện, làm mờ màn hình"
                # Nếu có nhiều hơn một người trong khung hình, làm mờ màn hình
                screenshot = pyautogui.screenshot()
                screen = np.array(screenshot)
                screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

                # Làm mờ màn hình
                blurred_screen = cv2.GaussianBlur(screen, (55, 55), 30)

                # Hiển thị toàn màn hình
                cv2.namedWindow("Blurred Screen", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Blurred Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow("Blurred Screen", blurred_screen)

                # Lấy handle của cửa sổ "Blurred Screen"
                hwnd = win32gui.FindWindow(None, "Blurred Screen")
                if hwnd:
                    # Đặt cửa sổ luôn nằm trên cùng
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

                blurred_screen_active = True
                continue  # Bỏ qua phần xử lý tiếp theo nếu có nhiều gương mặt

            for face_landmarks in results.multi_face_landmarks:
                face_2d.clear()
                face_3d.clear()
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx in [33, 263, 1, 61, 291, 199]:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)
                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])

                # Kiểm tra xem mặt có bị che khuất không
                if check_face_occlusion(face_2d, img_w, img_h):
                    face_occluded = True

                # Get 2D and 3D coordinates
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                focal_length = 1 * img_w
                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                    [0, focal_length, img_w / 2],
                                    [0, 0, 1]])
                distortion_matrix = np.zeros((4, 1), dtype=np.float64)

                success, rotation_vec, translation_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, distortion_matrix)

                # Get rotational angles
                rmat, jac = cv2.Rodrigues(rotation_vec)
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                # Determine the orientation text
                if y < -11 or y > 11 or x < -7 or x > 11:
                    text = "quay di"

                # Project the nose point
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rotation_vec, translation_vec, cam_matrix,
                                                                distortion_matrix)

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

                cv2.line(image, p1, p2, (255, 0, 0), 3)

                cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                cv2.putText(image, "x: " + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "y: " + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(image, "z: " + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Nếu không có gương mặt, làm mờ màn hình
        if not results.multi_face_landmarks:
            text = "Không phát hiện gương mặt"

        # Nếu `text` có giá trị, hiển thị màn hình mờ
        if text:
            # Chụp ảnh màn hình
            screenshot = pyautogui.screenshot()
            screen = np.array(screenshot)
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

            # Làm mờ màn hình
            blurred_screen = cv2.GaussianBlur(screen, (55, 55), 30)

            # Hiển thị toàn màn hình
            cv2.namedWindow("Blurred Screen", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Blurred Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Blurred Screen", blurred_screen)

            # Lấy handle của cửa sổ "Blurred Screen"
# Tạo cửa sổ làm mờ với thuộc tính không bị ảnh hưởng bởi Windows + D
            hwnd = win32gui.FindWindow(None, "Blurred Screen")
            if hwnd:
                # Đặt cửa sổ luôn nằm trên cùng và không bị ảnh hưởng bởi Windows + D
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                    win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOPMOST | win32con.WS_EX_TOOLWINDOW)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW | win32con.SWP_NOACTIVATE)

            blurred_screen_active = True
        else:
            # Nếu cửa sổ làm mờ đang mở, đóng nó
            if blurred_screen_active:
                cv2.destroyWindow("Blurred Screen")
                blurred_screen_active = False

            # Hiển thị khung hình webcam bình thường
            cv2.imshow('nhan_dien', image)

        # Bỏ qua phím ESC trong vòng lặp
        key = cv2.waitKey(5)
        if key == 27 and not blurred_screen_active:  # Cho phép ESC chỉ khi không có màn hình mờ
            break

    cap.release()
    cv2.destroyAllWindows()