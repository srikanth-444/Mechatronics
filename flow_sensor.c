#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>

int main() {
    int spi_fd; // File descriptor for the SPI device
    uint8_t tx_buf[1] = {0x00}; // Address to read (ADNS-3080 Product ID register)
    uint8_t rx_buff[1];        // Buffer to store the received data
    uint8_t mode=SPI_MODE_2;
    struct spi_ioc_transfer tr_cmd = {
    .tx_buf = (unsigned long)&tx_buf,  // Command to send
    .rx_buf = (unsigned long)&rx_buff,                   // No need to read response yet
    .len = 1,
    .delay_usecs=50,
    .bits_per_word=8                        // Length of command (1 byte)
    };
    uint8_t tx_dummy = 0x00;           // Dummy byte to clock out data
    uint8_t rx_response = 0;           // Buffer to store Product ID
    struct spi_ioc_transfer tr_response = {
    .tx_buf = (unsigned long)&tx_dummy,  // Send dummy byte
    .rx_buf = (unsigned long)&rx_response,  // Read Product ID
    .len = 1,  
    .delay_usecs=50,
    .bits_per_word=8                            // Length of transfer (1 byte)
    };

    // Open the SPI device
    spi_fd = open("/dev/spidev1.0", O_RDWR);
    if (spi_fd < 0) {
        perror("Failed to open SPI device");
        return -1;
    }

    if (ioctl(spi_fd,SPI_IOC_WR_MODE,&mode)<0){
        perror("spi modeset failed");
        close(spi_fd);
        return -1;
    }
    // Perform the SPI transfer
    if (ioctl(spi_fd, SPI_IOC_MESSAGE(1), &tr_cmd) < 0) {
        perror("SPI transfer failed");
        close(spi_fd);
        return -1;
    }
    if (ioctl(spi_fd, SPI_IOC_MESSAGE(1), &tr_response) < 0) {
        perror("SPI transfer failed");
        close(spi_fd);
        return -1;
    }
    printf("Received data: 0x%02X\n", rx_buff[0]);
    printf("Received data: 0x%02X\n", rx_response);
    
    // printf("Received data: 0x%02X\n", rx_buf[2]);
    // printf("Received data: 0x%02X\n", rx_buf[3]);
    // printf("Received data: 0x%02X\n", rx_buf[4]);


    // Close the SPI device
    close(spi_fd);
    return 0;
}