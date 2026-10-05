#include <chrono>
#include <memory>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <cstdint>
#include <stdexcept>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"

using namespace std::chrono_literals;

// ─── IMU Driver (same as yours) ────────────────────────────────────────────

const char* I2C_DEVICE  = "/dev/i2c-7";
const int   IMU_ADDR    = 0x6A;

const uint8_t WHO_AM_I  = 0x0F;
const uint8_t CTRL1_XL  = 0x10;
const uint8_t CTRL2_G   = 0x11;
const uint8_t CTRL3_C   = 0x12;
const uint8_t OUTX_L_G  = 0x22;
const uint8_t OUTX_L_XL = 0x28;

// Scaling constants
const double ACCEL_SCALE = 0.000061;   // ±2g in g/LSB  → then × 9.81 for m/s²
const double GYRO_SCALE  = 0.00875;    // ±250 dps in dps/LSB → then × π/180 for rad/s

class ISM330DLC {
private:
    int fd;

    void write_reg(uint8_t reg, uint8_t value) {
        uint8_t buf[2] = {reg, value};
        if (write(fd, buf, 2) != 2)
            throw std::runtime_error("Failed to write I2C register");
    }

    uint8_t read_reg(uint8_t reg) {
        if (write(fd, &reg, 1) != 1)
            throw std::runtime_error("Failed to set register pointer");
        uint8_t value;
        if (read(fd, &value, 1) != 1)
            throw std::runtime_error("Failed to read register");
        return value;
    }

public:
    ISM330DLC() {
        if ((fd = open(I2C_DEVICE, O_RDWR)) < 0)
            throw std::runtime_error("Failed to open I2C bus");
        if (ioctl(fd, I2C_SLAVE, IMU_ADDR) < 0)
            throw std::runtime_error("Failed to set I2C slave address");

        uint8_t id = read_reg(WHO_AM_I);
        if (id != 0x6B)
            throw std::runtime_error("WHO_AM_I mismatch");

        uint8_t ctrl3 = read_reg(CTRL3_C);
        write_reg(CTRL3_C, ctrl3 | 0x44);
        write_reg(CTRL1_XL, 0x40);  // 104 Hz, ±2g
        write_reg(CTRL2_G,  0x40);  // 104 Hz, ±250 dps
        usleep(100000);
    }

    void read_raw(uint8_t start_reg, int16_t out[3]) {
        uint8_t data[6];
        if (write(fd, &start_reg, 1) != 1) return;
        if (read(fd, data, 6) != 6) return;
        out[0] = (int16_t)(data[0] | (data[1] << 8));
        out[1] = (int16_t)(data[2] | (data[3] << 8));
        out[2] = (int16_t)(data[4] | (data[5] << 8));
    }

    ~ISM330DLC() { if (fd >= 0) close(fd); }
};

// ─── ROS2 Publisher Node ────────────────────────────────────────────────────

class ImuPublisher : public rclcpp::Node
{
public:
    ImuPublisher()
    : Node("imu_publisher"), imu_()          // ← constructs ISM330DLC here
    {
        publisher_ = this->create_publisher<sensor_msgs::msg::Imu>("imu/data", 10);
        timer_ = this->create_wall_timer(
            50ms,                            // ← 20 Hz (matches your usleep(50000))
            std::bind(&ImuPublisher::timer_callback, this));

        RCLCPP_INFO(this->get_logger(), "IMU Publisher started");
    }

private:
    void timer_callback()
    {
        int16_t accel[3], gyro[3];
        imu_.read_raw(OUTX_L_XL, accel);    // ← read accelerometer
        imu_.read_raw(OUTX_L_G,  gyro);     // ← read gyroscope

        auto msg = sensor_msgs::msg::Imu();

        // Header
        msg.header.stamp    = this->now();
        msg.header.frame_id = "imu_link";

        // Accel: raw → m/s²  (LSB × 0.000061 g/LSB × 9.81 m/s²/g)
        msg.linear_acceleration.x = accel[0] * ACCEL_SCALE * 9.81;
        msg.linear_acceleration.y = accel[1] * ACCEL_SCALE * 9.81;
        msg.linear_acceleration.z = accel[2] * ACCEL_SCALE * 9.81;

        // Gyro: raw → rad/s  (LSB × 0.00875 dps/LSB × π/180)
        msg.angular_velocity.x = gyro[0] * GYRO_SCALE * (M_PI / 180.0);
        msg.angular_velocity.y = gyro[1] * GYRO_SCALE * (M_PI / 180.0);
        msg.angular_velocity.z = gyro[2] * GYRO_SCALE * (M_PI / 180.0);

        // No orientation estimate from raw data, mark covariance as unknown
        msg.orientation_covariance[0] = -1;

        publisher_->publish(msg);
    }

    ISM330DLC imu_;                          // ← IMU is a member of the node
    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

// ─── Main ───────────────────────────────────────────────────────────────────

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ImuPublisher>());
    rclcpp::shutdown();
    return 0;
}
