import cv2
import numpy as np

class HSVColorJitter:
    def __init__(self, fraction=0.5):
        """ randomly change hue, saturation, value
        :param fractiobaohedu n: ramdom factor
        """
        self.fraction = fraction

    def __call__(self, image):
        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        H, S, V = img_hsv[:, :, 0], img_hsv[:, :, 1], img_hsv[:, :, 2]

        r = np.random.uniform(-1, 1, 3) * self.fraction + 1
        H = ((H * r[0]) % 180).astype(img_hsv.dtype)
        S = np.clip(S * r[1], a_min=0, a_max=255, out=S)
        V = np.clip(V * r[2], a_min=0, a_max=255, out=V)

        img_hsv[:, :, 0] = H.astype(np.uint8)
        img_hsv[:, :, 1] = S.astype(np.uint8)
        img_hsv[:, :, 2] = V.astype(np.uint8)
        image = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        return image

if __name__ == "__main__":
    random_hsv = HSVColorJitter()
    while True:
        img = cv2.imread("/home/liam/deepblue/datasets/VOC2007/train/image/000005.jpg")
        img2 = random_hsv(img)
        res = cv2.hconcat([img, img2])
        cv2.imshow("res", res)
        cv2.waitKey(0)
