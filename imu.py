import spidev
import time


class Imu:

    def __init__(self,) -> None:
        

        # Constants
        self.WHO_AM_I = 0x00       # WHO_AM_I register for ICM-20948
        self.Pwr_Mangment_1=0x06   # powermangment
        self.Pwr_Mangment_2=0x07   # for disabling gyro and accel
        self.USR_CTRL=0x03         # USR_CTRL
        self.USR_BANK=0x7F
        self.GYRO_SMPLRT_DIV=0x00
        self.GYRO_CONFIG_1=0X01
        self.ACCE_SMPLRT_DIV_1=0x10
        self.ACCE_SMPLRT_DIV_2=0x11
        self.ACCE_CONFIG_1=0x14
        self.ACCEL_XOUT_H=0x2D
        self.ACCEL_XOUT_L=0x2E
        self.ACCEL_YOUT_H=0x2F
        self.ACCEL_YOUT_L=0x30
        self.ACCEL_ZOUT_H=0x31
        self.ACCEL_ZOUT_L=0x32
        self.GYRO_XOUT_H=0x33
        self.GYRO_XOUT_L=0x34
        self.GYRO_YOUT_H=0x35
        self.GYRO_YOUT_L=0x36
        self.GYRO_ZOUT_H=0x37
        self.GYRO_ZOUT_L=0x38
        self.INT_PIN_CFG=0x0f
        self.INT_ENABLE_1=0x11
        self.INT_STATUS_1=0x1A
        

    def read_register(self,register):
        time.sleep(0.01)  # Short delay for stabilization
        response = self.spi.xfer2([register | 0x80, 0x00])  # Read bit set
        return response[1]

    def write_register(self,register,value):
        time.sleep(0.01)  # Short delay for stabilization
        response = self.spi.xfer2([register, value])  # write bit
        return response[1]
    
    def divide_into_8_bit_numbers(self,number):
        # Ensure the number fits within 16 bits (0 to 65535)
        if number < 0 or number > 0xFFFF:
            raise ValueError("Number must be between 0 and 65535 (inclusive).")

        # Extract lower 8 bits (the rightmost 8 bits)
        lower_8_bits = number & 0xFF
        
        # Extract upper 8 bits (the leftmost 8 bits)
        upper_8_bits = (number >> 8) & 0xFF

        return lower_8_bits, upper_8_bits
    
    def into_16_bit(self,msb,lsb):
        value=(msb<<8)|lsb
        if value<32768:
            return value
        else:
            return value-65536
    
    def set_up_spi(self,SPI_BUS,CS_PIN):
        
        self.SPI_BUS=SPI_BUS
        self.CS_PIN=CS_PIN

        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(self.SPI_BUS, self.CS_PIN)
        self.spi.max_speed_hz = 500000  # Reduced speed to 500 kHz
        self.spi.mode = 3               # Set SPI mode to 3

        # Attempt to read WHO_AM_I register
        who_am_i_value = self.read_register(self.WHO_AM_I)

        if (who_am_i_value==0xea):
            #wake the chip from sleep
            self.write_register(self.Pwr_Mangment_1,0x00)
            #enable the accelrometer and gyroscope
            self.write_register(self.Pwr_Mangment_2,0x00)
            #setting into spi mode
            current_value=self.read_register(self.USR_CTRL)
            new_value=current_value|0x10
            self.write_register(self.USR_CTRL,new_value)
            return True
        else:
            print("who am i value: ",hex(who_am_i_value))
            print("user ctrl: ",hex(self.read_register(self.USR_CTRL)))
            print("power managment: ",hex(self.read_register(self.Pwr_Mangment_1)))
            self.spi.close()
            raise RuntimeError("Spi is not working: check connections")

    
    def switch_register_bank(self,register):
        current_bank=self.read_register(self.USR_BANK)
        value=register<<4
        new=current_bank|value
        self.write_register(self.USR_BANK,new)

    def set_gyroconfig(self,dps,low_pass,sample_rate,):
        self.switch_register_bank(2)
        self.write_register(self.GYRO_SMPLRT_DIV,sample_rate)

        current_config=self.read_register(self.GYRO_CONFIG_1)

        low_pass=low_pass<<3
        enable_filter=0x01
        dps=dps<<1

        new_config=current_config|low_pass|enable_filter|dps
        self.write_register(self.GYRO_CONFIG_1,new_config)
        self.write_register(self.USR_BANK,0x00)

        return True
    
    def set_Acce_config(self,scale,low_pass,sample_rate,):
        self.switch_register_bank(2)
        lsb,msb=self.divide_into_8_bit_numbers(sample_rate)
        self.write_register(self.ACCE_SMPLRT_DIV_1,msb)
        self.write_register(self.ACCE_SMPLRT_DIV_2,lsb)

        current_config=self.read_register(self.ACCE_CONFIG_1)

        low_pass=low_pass<<3
        enable_filter=0x01
        scale=scale<<1

        new_config=current_config|low_pass|enable_filter|scale
        self.write_register(self.ACCE_CONFIG_1,new_config)
        self.write_register(self.USR_BANK,0x00)
        return True

    def set_int_config(self,):
        ACTL=0x01<<7
        OPEN=0x00
        LATCH=0x01<<5

        current_value=self.read_register(self.INT_PIN_CFG)
        new_value=current_value|ACTL|OPEN|LATCH
        self.write_register(self.INT_PIN_CFG,new_value)
        return True

    def get_acelaration_data(self,):
        X_H=self.read_register(self.ACCEL_XOUT_H)
        X_L=self.read_register(self.ACCEL_XOUT_L)
        Y_H=self.read_register(self.ACCEL_YOUT_H)
        Y_L=self.read_register(self.ACCEL_YOUT_L)
        Z_H=self.read_register(self.ACCEL_ZOUT_H)
        Z_L=self.read_register(self.ACCEL_ZOUT_L)
        
        return{"a_x":self.into_16_bit(X_H,X_L)/16384,"a_y":self.into_16_bit(Y_H,Y_L)/16384,"a_z":self.into_16_bit(Z_H,Z_L)/16384}
    
    def get_gyroscope_data(self,):
        X_H=self.read_register(self.GYRO_XOUT_H)
        X_L=self.read_register(self.GYRO_XOUT_L)
        Y_H=self.read_register(self.GYRO_YOUT_H)
        Y_L=self.read_register(self.GYRO_YOUT_L)
        Z_H=self.read_register(self.GYRO_ZOUT_H)
        Z_L=self.read_register(self.GYRO_ZOUT_L)
        return{"g_x":self.into_16_bit(X_H,X_L)*0.007,"g_y":self.into_16_bit(Y_H,Y_L)*0.007,"g_z":self.into_16_bit(Z_H,Z_L)*0.007}
    
    def int_enable_(self,):
        current_value=self.read_register(self.INT_ENABLE_1)
        new_value=current_value|0x01
        self.write_register(self.INT_ENABLE_1,new_value)
        return True
    
    def get_int_status_1(self,):
        value=self.read_register(self.INT_STATUS_1)
        if value&0x01:
            return True
        else:
            return False

        
    
    def get_magnetometer_data():
        pass


    def get_data(self,):
        a=self.get_acelaration_data()
        g=self.get_gyroscope_data()
        return {**a,**g}



if __name__=="__main__":
    imu=Imu()
    spibus=0
    cs_pin=0

    #gyro config
    gyro_scale=0x00 #+/-250 dps
    gyro_low_pass=0x03 #51.2HZ
    gyro_sample_rate=0x07 #140.HZ

    #accelerometer config
    accel_scale=0x00 #+/-2g
    accel_low_pass=0x03 #50.4
    accel_sample_rate=7 #140 HZ



    imu.set_up_spi(SPI_BUS=spibus,CS_PIN=cs_pin)
    imu.set_gyroconfig(dps=gyro_scale,low_pass=gyro_low_pass,sample_rate=gyro_sample_rate)
    imu.set_Acce_config(scale=accel_scale,low_pass=accel_low_pass,sample_rate=gyro_sample_rate)
    imu.set_int_config()
    imu.int_enable_()

    starting_time=time.time()
    counter=0
    while (time.time()-starting_time)<30:
        if(imu.get_int_status_1):
            imu.get_data()
            counter+=1
            print(counter)      
