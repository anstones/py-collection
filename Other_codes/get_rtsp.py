import cv2

def get_img_from_camera_net(folder_path):
    cap = cv2.VideoCapture("rtsp://admin:admin@10.80.11.11/ch1/stream1")#获取网络摄像机
    
    i = 1
    while i<3:
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        print (str(i))
        cv2.imwrite(folder_path + str(i) + '.jpg', frame)# 存储为图像
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    folder_path = 'D:\\Anacon\\'
    get_img_from_camera_net(folder_path)

    '''
    opencv 连接caram 取流
    '''
    # url = 'rtsp://admin:password@192.168.1.104:554/11'
    url = "rtsp://admin:oeasy123@192.168.1.106:554/LiveMedia/ch1/Media1"
    cap = cv2.VideoCapture(url)
    while cap.isOpened():
        # Capture frame-by-frame  
        ret, frame=cap.read()
        # Display the resulting frame  
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture  
    cap.release()
    cv2.destroyAllWindows()