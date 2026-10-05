
// ISM330DLC IMU Reader — Jetson (I2C)
// Reads raw accelerometer and gyroscope data and prints to terminal.



#include <iostream>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <iomanip>
#include <cstdint>
#include <stdexcept>
#include <cstring>

// Configuration Constants
const char* I2C_DEVICE = "/dev/i2c-7";
const int IMU_ADDR = 0x6A;

// Register Map
const uint8_t WHO_AM_I   = 0x0F;
const uint8_t CTRL1_XL   = 0x10;
const uint8_t CTRL2_G    = 0x11;
const uint8_t CTRL3_C    = 0x12;
const uint8_t OUTX_L_G   = 0x22;
const uint8_t OUTX_L_XL  = 0x28;

class ISM330DLC {
private:
    int file_descriptor;

    void write_reg(uint8_t reg, uint8_t value) {
        uint8_t buffer[2] = {reg, value};
        if (write(file_descriptor, buffer, 2) != 2) {
            throw std::runtime_error("Failed to write to I2C register");
        }
    }

    uint8_t read_reg(uint8_t reg) {
        if (write(file_descriptor, &reg, 1) != 1) {
            throw std::runtime_error("Failed to set register pointer");
        }
        uint8_t value;
        if (read(file_descriptor, &value, 1) != 1) {
            throw std::runtime_error("Failed to read register value");
        }
        return value;
    }

public:
    ISM330DLC() {
        // Open I2C Bus
        if ((file_descriptor = open(I2C_DEVICE, O_RDWR)) < 0) {
            throw std::runtime_error("Failed to open I2C bus. Try sudo.");
        }

        // Set I2C Address
        if (ioctl(file_descriptor, I2C_SLAVE, IMU_ADDR) < 0) {
            throw std::runtime_error("Failed to acquire bus access/talk to slave");
        }

        verify_who_am_i();
        configure();
    }

    void verify_who_am_i() {
        uint8_t chip_id = read_reg(WHO_AM_I);
        if (chip_id != 0x6B) {
            throw std::runtime_error("WHO_AM_I mismatch! Expected 0x6B.");
        }
        std::cout << "IMU detected (WHO_AM_I = 0x6B)" << std::endl;
    }

    void configure() {
        uint8_t ctrl3 = read_reg(CTRL3_C);
        write_reg(CTRL3_C, ctrl3 | 0x44); // Block Data Update & IF_INC
        write_reg(CTRL1_XL, 0x40);        // 104 Hz, +/- 2g
        write_reg(CTRL2_G, 0x40);         // 104 Hz, 250 dps
        usleep(100000); // 100ms
        std::cout << "IMU configured: 104 Hz | Accel ±2g | Gyro ±250 dps" << std::endl;
    }

    void read_raw_data(uint8_t start_reg, int16_t out[3]) {
        uint8_t reg = start_reg;
        uint8_t data[6];

        if (write(file_descriptor, &reg, 1) != 1) return;
        if (read(file_descriptor, data, 6) != 6) return;

        // Combine bytes (Little Endian)
        out[0] = (int16_t)(data[0] | (data[1] << 8));
        out[1] = (int16_t)(data[2] | (data[3] << 8));
        out[2] = (int16_t)(data[4] | (data[5] << 8));
    }

    ~ISM330DLC() {
        if (file_descriptor >= 0) close(file_descriptor);
    }
};

int main() {
    try {
        ISM330DLC imu;
        int16_t accel[3], gyro[3];

        std::cout << std::setw(30) << "ACCEL (raw)" << " | " << std::setw(30) << "GYRO (raw)" << std::endl;
        std::cout << std::string(70, '-') << std::endl;

        while (true) {
            imu.read_raw_data(OUTX_L_XL, accel);
            imu.read_raw_data(OUTX_L_G, gyro);

            std::cout << "\r" 
                      << std::setw(8) << accel[0] << std::setw(8) << accel[1] << std::setw(8) << accel[2] 
                      << "  |  " 
                      << std::setw(8) << gyro[0] << std::setw(8) << gyro[1] << std::setw(8) << gyro[2] 
                      << std::flush;

            usleep(50000); // 50ms
        }
    } catch (const std::exception& e) {
        std::cerr << "\nError: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}