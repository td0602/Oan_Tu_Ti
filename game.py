# đọc webcam, lấy hình nhận diện bàn tay, lấy hình ngón tay và nhận diện: đấm, kéo, lá
# Máy random 1 g trị, và so sánh ai thắng
# Chú ý: bài này chỉ hđ với tay phải

import mediapipe
import cv2
import hand_detection_lib as handlib
import os
import random

# Bổ sung những thứ cần thiết cho detect hand
# khoửi tạo lớp hand detector
detector = handlib.handDetector()

# biến Wevcam
cam = cv2.VideoCapture(0)

def draw_results(frame, user_draw):
    # Máy lựa chọn ngẫu nhiên
    com_draw = random.randint(0, 2)

    # Vẽ hình, viết chữ theo user_draw: ra 0 thì load ảnh o.png, ra 1 thì load ảnh 1.png
    frame = cv2.putText(frame, 'You', (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
    # đè ảnh kéo, búa, lá lên khung hình
    s_img = cv2.imread(os.path.join("pix", str(user_draw) + ".png"))
    x_offset = 50
    y_offset = 100
    frame[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

    # Vẽ hình, viết chữ theo com_draw (tương tự trên)
    frame = cv2.putText(frame, 'Computer', (400, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
    s_img = cv2.imread(os.path.join("pix", str(com_draw) + ".png"))
    x_offset = 400
    y_offset = 100
    frame[y_offset:y_offset + s_img.shape[0], x_offset:x_offset + s_img.shape[1]] = s_img

    # Kiểm tra và hiển thị kết quá
    if user_draw == com_draw:
        result = "DRAW!"
    elif (user_draw == 0) and (com_draw == 1):
        result = "YOU WIN!"
    elif (user_draw == 1) and (com_draw == 2):
        result = "YOU WIN!"
    elif (user_draw == 2) and (com_draw == 0):
        result = "YOU WIN!"
    else:
        result = "YOU LOSE!"
    # vẽ dòng chữ result lên frame
    frame = cv2.putText(frame, result, (50, 450), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 255), 2, cv2.LINE_AA)


while True:
    # mở webcam
    ret, frame = cam.read()
    # lật lại frame cho nó phẳng
    # do sử dụng camera trc laptop nên lật lại cho đúng chiều
    frame = cv2.flip(frame, 1) # 1 là lật theo chiều ngang

    # Đưa hình ảnh vào Detector
    frame, hand_lms = detector.findHands(frame)
    # đếm số finger
    n_fingers = detector.count_finger(hand_lms)

    # để lưu giá trị người dùng ra: đấm, kéo, lá
    user_draw = -1 # 0: lá, 1: đấm, 2: kéo
    if n_fingers == 0:
        user_draw = 1
    elif n_fingers == 2:
        user_draw = 2
    elif n_fingers == 5:
        user_draw =0
    elif n_fingers != -1: #
        print(("Chỉ chấp nhận: Đấm, Lá và Kéo!"))
    else:
        print("Không có bàn tay trong hình!")


    key = cv2.waitKey(1)


    # show lên
    cv2.imshow("game", frame)
    if key == ord("q"):
        break
    elif key == ord(" "): # Nếu bấm dấu cách
        draw_results(frame, user_draw)
        # Sau khi vẽ xong ta lại hiển thị lên
        cv2.imshow("game", frame)
        # Bấm phím bất kỳ để người dùng nhìn thấy kết quả
        cv2.waitKey()
cam.release()
cv2.destroyAllWindows()