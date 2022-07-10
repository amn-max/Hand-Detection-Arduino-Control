from time import time
from cvzone.HandTrackingModule import HandDetector
import cv2
import asyncio,websockets
import threading
import time

class VideoCap():
    #initialize function
    
    def __init__(self,cap,dectector):
        self.cap = cap
        self.detector = dectector
    
    async def set_hand_frame(self):
        url = "ws://gesture-control-server.herokuapp.com"
        async with websockets.connect(url) as websocket:
            
            while True:
                await asyncio.sleep(0.0001)
                success, img = cap.read()
                hands, img = detector.findHands(img)
                self.hands = hands
                self.image = img
                #perfrom sending data to server
                cv2.imshow("Frame", img)
                k = cv2.waitKey(1)
                if hands:
                    fingers = self.detector.fingersUp(hands[0])
                    print(fingers)
                    s=0
                    for f in fingers:
                        if f == 1:
                            s+= 1
                    await send(websocket,str(s))
                    
                    
            
                
            
    
    def get_fingers(self):
        return self.hands
        
    def show_frame(self):
        asyncio.get_event_loop().run_until_complete(self.set_hand_frame())
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
    def destroy_frame(self):
        self.cap.release()
        cv2.destroyAllWindows()
        

async def send(client,data):
    await client.send(data)

async def handler(websocket):
    message = await websocket.recv()
    print(message)
        
    
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    videoCap = VideoCap(cap,detector)
    videoCap.show_frame()
    
    