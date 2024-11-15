import spidev
import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import numpy as np


class ADNS_3080:
    # Initialize SPI
    def __init__(self) -> None:
        # Sensor Registers
        self.PRODUCT_ID = 0x00
        self.MOTION = 0x02
        self.DELTA_X = 0x03
        self.DELTA_Y = 0x04
        self.CONFIG_BITS = 0x0A
        self.SQUAL=0x05

        self.FRAME_CAPTURE = 0x12  # Frame Capture register address
        self.PIXELS_X = 30
        self.PIXELS_Y = 30


        RESET_PIN = 17  # Replace with the actual GPIO pin number

        # Set up the GPIO
        GPIO.setmode(GPIO.BCM)  # Use BCM numbering
        GPIO.setup(RESET_PIN, GPIO.OUT)
        GPIO.output(RESET_PIN, GPIO.HIGH)
        time.sleep(0.01)  # Hold high for at least 10 ms

        # Lower the reset pin
        GPIO.output(RESET_PIN, GPIO.LOW)
        
        time.sleep(0.01) 
        GPIO.cleanup()
        
        
    

    

    def read_register(self,register):
        """Read a single byte from a register."""

        time.sleep(0.01)  # Short delay to stabilize
        data=self.spi.xfer2([register,0x00])[1]  # MSB=0 for read
          # Read data

        return data

    def write_register(self,register, value):
        """Write a single byte to a register."""
    
        time.sleep(0.01)  # Short delay to stabilize
        self.spi.xfer2([register | 0x80, value])  # MSB=1 for write

    def set_up_spi(self,SPI_BUS,CS_PIN):
        self.SPI_BUS=SPI_BUS
        self.CS_PIN=CS_PIN
        self.spi = spidev.SpiDev()
        self.spi.open(self.SPI_BUS, self.CS_PIN)  # Open SPI bus 0, device 0
        self.spi.max_speed_hz = 100000 # 1 MHz max for ADNS-3080
        self.spi.mode = 0  # SPI mode 3    

        product_id = self.read_register(self.PRODUCT_ID)
        if product_id == 0x17: 
            self.read_register(self.MOTION)
            self.set_resolution(1600)
        else:
            print("product id: ",hex(product_id))
            self.spi.close()
            raise RuntimeError("Spi is not working: check connections")

    
    def set_resolution(self,resolution_cpi):
        """Set sensor resolution to 400 or 1600 CPI."""
        if resolution_cpi == 400:
            self.write_register(self.CONFIG_BITS, 0x00)  # Clear bit 0 for 400 CPI
        elif resolution_cpi == 1600:
            new_value=0x09|0x01<<6|0x01<<4
            print(new_value)
            self.write_register(self.CONFIG_BITS, new_value)  # Set bit 0 for 1600 CPI
        else:
            print("Invalid resolution. Use 400 or 1600 CPI.")
        time.sleep(0.001)  # Allow the sensor to update configuration
        print(f"Resolution set to {resolution_cpi} CPI.")

    def get_squal(self,):
        print(self.read_register(self.SQUAL))

    def read_motion(self):
        """Read motion data (dx, dy) from the sensor."""
        motion = self.read_register(self.MOTION)
        print(f"Motion register: {motion:#04x}")  # Print the motion register value
        
        if motion & 0x80:  # Check if motion bit is set (bit 7)
            print("Motion detected!")
            dx = self.read_register(self.DELTA_X)
            dy = self.read_register(self.DELTA_Y)
            
            # Convert from 2's complement if necessary
            dx = dx - 256 if dx > 127 else dx
            dy = dy - 256 if dy > 127 else dy
        else:
            print("No motion detected.")
            dx, dy = 0, 0  # No motion detected
        
        return dx, dy
    def capture_image(self,):
        # Start image capture by reading the Frame Capture register
        self.spi.xfer2([self.FRAME_CAPTURE])  # Start frame capture
        
        # Create an empty image array
        image = np.zeros((self.PIXELS_Y, self.PIXELS_X), dtype=np.uint8)
        
        # Loop over each pixel in the 30x30 array
        for y in range(self.PIXELS_Y):
            for x in range(self.PIXELS_X):
                # Read the pixel value (1-byte response)
                pixel_value = self.spi.xfer2([0x00])[0]
                image[y, x] = pixel_value
        
        return image

# Main Program
if __name__=="__main__":
    flow_sensor=ADNS_3080()
    spibus=1
    cs_pin=0
    try:
        
        flow_sensor.set_up_spi(spibus,cs_pin)
        # while True:
                # dx, dy = flow_sensor.read_motion()
                # dx_mm = (dx / 1600) * 25.4  # Convert to mm (assuming 1600 CPI)
                # dy_mm = (dy / 1600) * 25.4
                # print(f"dx_mm={dx_mm:.3f} mm, dy_mm={dy_mm:.3f} mm")
                #flow_sensor.get_squal()
        print(flow_sensor.read_register(0x02))

        # image = flow_sensor.capture_image()
        # plt.imshow(image, cmap='gray')
        # plt.title("ADNS-3080 Captured Image")
        # plt.savefig("plot.png")
                
    except RuntimeError as R:
        flow_sensor.spi.close()
        print(R)


