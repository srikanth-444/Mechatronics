import time
import math

from communication import Publisher
import icm20948


class ICM20948Handler:
    def __init__(self, spi_device="/dev/spidev0.0", spi_speed=1000000):
        self.spi_device = spi_device
        self.spi_speed = spi_speed
        self.icm = None
        self.Publisher = Publisher(host='tcp://*:5556',topic="theta")

    def setup(self):
        print("Initializing ICM-20948...")
        time.sleep(0.1)

        self.icm = icm20948.ICM_20948_SPI()

        while True:
            if self.icm.begin(self.spi_device, self.spi_speed) == icm20948.ICM_20948_Stat_Ok:
                print("Device connected!")
                break
            else:
                print("Initialization failed. Retrying...")
                time.sleep(0.5)

        if self.icm.initializeDMP() != icm20948.ICM_20948_Stat_Ok:
            print("DMP initialization failed!")
            exit(1)

        self.icm.enableDMPSensor(icm20948.INV_ICM20948_SENSOR_GAME_ROTATION_VECTOR, True)
        self.icm.setDMPODRrate(icm20948.DMP_ODR_Reg_Quat6, 0)
        self.icm.enableFIFO(True)
        self.icm.enableDMP(True)
        self.icm.resetDMP()
        self.icm.resetFIFO()

        print("DMP initialization complete!")

    def process_data(self):
        header, q1, q2, q3 = self.icm.readDMPdataFromFIFO()
        q1 /= 1073741824.0
        q2 /= 1073741824.0
        q3 /= 1073741824.0

        if (self.icm.status in [icm20948.ICM_20948_Stat_Ok, icm20948.ICM_20948_Stat_FIFOMoreDataAvail]):
            if (header & int(icm20948.Quat6)) > 0:
                q0 = math.sqrt(1.0 - (q1 ** 2 + q2 ** 2 + q3 ** 2))
                qw, qx, qy, qz = q0, q2, q1, -q3

                roll = math.degrees(math.atan2(2.0 * (qw * qx + qy * qz), 1.0 - 2.0 * (qx ** 2 + qy ** 2)))
                pitch = math.degrees(math.asin(max(-1.0, min(1.0, 2.0 * (qw * qy - qx * qz)))))
                yaw = math.degrees(math.atan2(2.0 * (qw * qz + qx * qy), 1.0 - 2.0 * (qy ** 2 + qz ** 2)))

                data = [yaw] 
                self.Publisher.publish_data(data)

            time.sleep(0.01)

    def run(self):
        try:
            while True:
                self.process_data()
        except KeyboardInterrupt:
            self.Publisher.close()
            print("Exiting...")

if __name__ == "__main__":
    handler = ICM20948Handler()
    handler.setup()
    handler.run()