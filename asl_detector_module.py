import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

#creating class for ASL detector
class ASLDetector:
  #initialize each variable
  def __init__(self, model, labels):
      #turn of camera and detect hands, label each hand position with letters within label variable
      self.cap = cv2.VideoCapture(0)
      self.detector = HandDetector(maxHands=1)
      self.classifier = Classifier(model, labels)
      self.offset = 20
      self.imgSize = 300
      self.labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
      self.detected_letter = None  # Initialize detected_letter attribute to None
#function to create frame for data training
  def get_letter(self):
      success, img = self.cap.read()
      imgOutput = img.copy()

      try:
          hands, img = self.detector.findHands(img)

          if hands:
              hand = hands[0]
              x, y, w, h = hand['bbox']
              imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
              imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]
              imgCropShape = imgCrop.shape
              aspectRatio = h / w

              if aspectRatio > 1:
                  k = self.imgSize / h
                  wCal = math.ceil(k * w)
                  imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                  imgResizeShape = imgResize.shape
                  wGap = math.ceil((self.imgSize - wCal) / 2)
                  imgWhite[:, wGap:wCal + wGap] = imgResize
                  prediction, index = self.classifier.getPrediction(imgWhite, draw=False)
                  self.detected_letter = self.labels[index]
                  print(f"Letter: {self.detected_letter}")

              else:
                  k = self.imgSize / w
                  hCal = math.ceil(k * h)
                  imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                  imgResizeShape = imgResize.shape
                  hGap = math.ceil((self.imgSize - hCal) / 2)
                  imgWhite[hGap:hCal + hGap, :] = imgResize
                  prediction, index = self.classifier.getPrediction(imgWhite, draw=False)
                  self.detected_letter = self.labels[index]

              # draw rectangles and text around hand for labelling
              cv2.rectangle(imgOutput, (x - self.offset, y - self.offset - 50),
                          (x - self.offset + 90, y - self.offset - 50 + 50), (255, 0, 255), cv2.FILLED)
              cv2.putText(imgOutput, self.labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
              cv2.rectangle(imgOutput, (x - self.offset, y - self.offset),
                          (x + w + self.offset, y + h + self.offset), (255, 0, 255), 4)

          cv2.imshow("Image", imgOutput)
            #q for quitting program
          key = cv2.waitKey(1)
          if key == ord("q"):
              return False
        #error prevention when hand becomes too big or too small for camera to detect or when hand leaves detected area
      except Exception as e:
          print(f"Error: {e}")

      return str(self.detected_letter) if self.detected_letter else None

  def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
    #return detected letter for hangman
#   def get_letter(self):
#         return self.detected_letter
#taking trained data from external files
if __name__ == "__main__":
    model = "C:\\Users\\almir\\Desktop\\final project algopro\\1\\Model\\keras_model.h5"
    labels = "C:\\Users\\almir\\Desktop\\final project algopro\\1\\Model\\labels.txt"

    asl_detection = ASLDetector(model, labels)

    while asl_detection.get_letter():
        detected_letter = asl_detection.get_letter()
        if detected_letter:
            print(f"Letter is: {detected_letter}")

    asl_detection.release()
