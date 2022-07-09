from cv2 import copyTo
from cvzone.HandTrackingModule import HandDetector
import cv2
import asyncio,websockets
import threading

class VideoCap():
    #initialize function
    
    def __init__(self,cap,dectector):
        self.cap = cap
        self.detector = dectector
    
    async def set_hand_frame(self):
        url = "ws://gesture-control-server.herokuapp.com"
        async with websockets.connect(url) as websocket:
            while True:
                success, img = cap.read()
                hands, img = detector.findHands(img)
                self.hands = hands
                self.image = img
                #perfrom sending data to server
                cv2.imshow("Frame", img)
                k = cv2.waitKey(1)
                try:
                    if hands:
                        fingers = self.detector.fingersUp(hands[0])
                        #code to sum of all 1's in fingers
                        s = 0
                        for i in fingers:
                            if i == 1:
                                s+=1
                        await websocket.send(str(s))
                        
                        print(s)
                except:
                    print("No Hands")
                
                
                if k == 1:
                    break
                else:
                    continue
                
            
    
    def get_fingers(self):
        return self.hands
        
    def show_frame(self):
        asyncio.run(self.set_hand_frame())
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
    def destroy_frame(self):
        self.cap.release()
        cv2.destroyAllWindows()
        

async def handler(websocket):
    message = await websocket.recv()
    print(message)
        
    
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    videoCap = VideoCap(cap,detector)
    videoCap.show_frame()
    
    