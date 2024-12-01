import hid
import time
from communication import Publisher

class Opticalflow:

    def __init__(self,):
        self.MOUSE_DPI = 800  # Dots per inch
        self.device = hid.device()
        self.vendor_id=1133
        self.product_id=49271
        self.Publisher = Publisher(topic="XandY") 
        
        self.x=0
        self.y=0

    def counts_to_cm(self,counts):
        return counts*2.54 / self.MOUSE_DPI
    def read(self,):
        try:
            self.device.open(self.vendor_id, self.product_id)
            self.device.set_nonblocking(True)
            while True:
                start_time=time.time()
                data = self.device.read(4)  # Read 8 bytes, modify based on your mouse's report descriptor
                dt=time.time()-start_time
                if data:
                    dx = data[1]  # X-axis movement, modify based on your mouse's data structure
                    dy = data[2]  # Y-axis movement
                    
                    # Convert to signed values (for example, if 2's complement is used)
                    dx = dx - 256 if dx > 127 else dx
                    dy = dy - 256 if dy > 127 else dy

                    # Convert to inches
                    dx_cm = self.counts_to_cm(dx)
                    dy_cm = self.counts_to_cm(dy)


                    self.x=self.x+dx_cm
                    self.y=self.y+dy_cm
                else:
                    pass
                
                data = [self.x, self.y] 
                self.Publisher.publish_data(data)
                
                  
        except KeyboardInterrupt:
            print("Stopped mouse tracking.")
            self.device.close()
        except Exception as e:
            print(f"Error: {e}")
    

if __name__ == "__main__":
    opticalflow=Opticalflow()
    
    opticalflow.read()

