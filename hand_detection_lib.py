# file này để sử dụng thư viện mediapipe để phát hiện ra bàn tay, đếm số lượng ngón tay
import cv2
import mediapipe as mp
# viết theo hướng đối tượng để dễ quản lý code sau này
class handDetector():
    def __init__(self):
        # Khởi tạo đối tượng hand bởi thư viện mp
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        # thuộc tính Draw dùng để vẽ những đốt ngón tay khi dêtct được hỗ trợ bởi mp
        # lệnh vẽ
        self.mpDraw = mp.solutions.drawing_utils


    # Hàm để tìm tay trong ảnh: đầu vào là ảnh bàn tay, và trả ra một ảnh vẽ các lendmark lên trên và danh sách các đốt ngón tay gồm các tọa độ
    def findHands(selfs, img):
        # chuyển ảnh từ BGR thành RGB: ảnh đọc từ camera bằng opencv là ở dạng BGR,
        # mà mp lại làm việc với RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Đưa vào thư viện mediapipe
        results = selfs.hands.process(imgRGB)
        # tạo một list lendmark rỗng để ta lấy những cái cần duyệt trong này ra để kiểm tra xem có mấy ngón tay xòe ra
        hand_lms = []

        # Kiểm tra results có tay trong ảnh không
        if results.multi_hand_landmarks:
            # vẽ landmark cho các bàn tay
            for handlm in results.multi_hand_landmarks:
                # vẽ đường nối với các đốt tay
                selfs.mpDraw.draw_landmarks(img, handlm, selfs.mpHands.HAND_CONNECTIONS)

            # Trích ra các toạ độ khớp của các ngón tay
            # Khi detect landmark thì tọa độ x, y trả ra không phải tọa độ thật mà là cái tỉ lệ so với cái ảnh. vd: 0.5 thì đốt ngón tay ở giữa ảnh, 0.6 lệch bên này, 0.3 lệch bên kia
            # nên mình nhân với kích thước ảnh để ra tọa ộ thực tế của đốt ngón tay đó
            firstHand = results.multi_hand_landmarks[0]  # tiện làm việc, vd có 2 tay thì chỉ lấy tay đầu tiên để xử lý
            # duyệt trong cái lendmark của bàn tay đầu tiên
            h, w, _ = img.shape # lấy chiều cao và chiều rộng ảnh
            # lấy ra tất cả các đốt ngón tay trong lendmark
            for id, lm in enumerate(firstHand.landmark):
                # nhân với kích thước ảnh ầu vào để ra tọa độ thật
                real_x, real_y = int(lm.x * w), int(lm.y * h)
                # thêm các đốt ngón tay vào list hand_lms với các thành phần: id, real_x ...
                hand_lms.append([id, real_x, real_y])

        return img, hand_lms

    # đếm ngón tay trong list hand_lms
    # mediapipe có 5 ngón tay tất cả: ngón đầu từ số 4, ngón 2 là số 8, ngón 3 là 12, ngón 4 16 ngón 5 là 20
    # do 1 ngón tay có 4 đốt, trên đỉnh ngón là 4, 8, 12, 16, 20
    # Lên gg: mediapipe hand để biết thêm
    def count_finger(self, hand_lms):
        # đánhđấu lại các điểm
        finger_start_index = [4, 8, 12, 16, 20]
        # bến đếm số lượng ngón tay
        n_fingers = 0
        #  nếu có hand_lms
        if len(hand_lms) > 0:
            # Kiểm tra ngón cái
            # Nếu tọa độ điểm ở đầu ngón cái nhỏ hơn tọa độ điểm ở cuối ngón thì tay đang mở
            # tọa độ x của điểm số 4 < điểm số 3 thì ngón cái đang mở
            if hand_lms[finger_start_index[0]][1] < hand_lms[finger_start_index[0] - 1][1]:
                n_fingers += 1

            # Kiểm tra 4 ngón còn lại
            # kiểm tra với tọa độ y qua [idx][2], 2 là lấy theo tọa dộ y
            for idx in range(1, 5): # chạy từ 1 - 4
                # nếu điểm 8 < 6, 12 < 10, 16 <14, 20< 18 thì ngón tay mở
                if hand_lms[finger_start_index[idx]][2] < hand_lms[finger_start_index[idx] - 2][2]:
                    n_fingers += 1

            return n_fingers
        else:
            # nếu k có bàn tay, nếu để 0 trùng với khi ta lắm tay lại: có bàn tay nhưng k có ngón
            return -1
