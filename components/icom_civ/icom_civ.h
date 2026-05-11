#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/number/number.h"

namespace esphome {
namespace icom_civ {

// CI-V command codes
static const uint8_t CIV_PREAMBLE = 0xFE;
static const uint8_t CIV_EOM = 0xFD;
static const uint8_t CIV_CONTROLLER = 0xE0;  // PC/controller address

// Commands
static const uint8_t CMD_SET_FREQ = 0x05;
static const uint8_t CMD_READ_FREQ = 0x03;
static const uint8_t CMD_SET_MODE = 0x06;
static const uint8_t CMD_READ_MODE = 0x04;
static const uint8_t CMD_READ_SMETER = 0x15;
static const uint8_t CMD_SET_PTT = 0x1C;
static const uint8_t CMD_READ_PTT = 0x1C;
static const uint8_t CMD_SET_VFO = 0x07;
static const uint8_t CMD_SET_POWER = 0x14;

// Mode codes
static const char* MODE_NAMES[] = {
  "LSB", "USB", "AM", "CW", "RTTY", "FM", "WFM", "CW-R", "RTTY-R"
};

class IcomCIV : public PollingComponent, public uart::UARTDevice {
 public:
  void setup() override;
  void loop() override;
  void update() override;
  void dump_config() override;

  void set_civ_address(uint8_t addr) { this->civ_address_ = addr; }

  // Sensors
  void set_frequency_sensor(sensor::Sensor *s) { this->frequency_sensor_ = s; }
  void set_smeter_sensor(sensor::Sensor *s) { this->smeter_sensor_ = s; }
  void set_mode_sensor(text_sensor::TextSensor *s) { this->mode_sensor_ = s; }
  void set_ptt_sensor(sensor::Sensor *s) { this->ptt_sensor_ = s; }

  // Actions
  void set_frequency(uint32_t freq_hz);
  void set_mode(uint8_t mode);
  void set_ptt(bool on);
  void power_on();
  void power_off();

 protected:
  uint8_t civ_address_{0x70};

  // Sensors
  sensor::Sensor *frequency_sensor_{nullptr};
  sensor::Sensor *smeter_sensor_{nullptr};
  text_sensor::TextSensor *mode_sensor_{nullptr};
  sensor::Sensor *ptt_sensor_{nullptr};

  // State
  uint32_t current_freq_{0};
  uint8_t current_mode_{0};
  bool current_ptt_{false};

  // RX buffer
  uint8_t rx_buf_[64];
  uint8_t rx_pos_{0};
  bool in_frame_{false};

  // CI-V protocol
  void send_command(uint8_t cmd, const uint8_t *data, uint8_t len);
  void send_command(uint8_t cmd, uint8_t sub, const uint8_t *data, uint8_t len);
  void process_response(const uint8_t *data, uint8_t len);
  void request_frequency();
  void request_mode();
  void request_smeter();
  void request_ptt();

  // Helpers
  uint32_t bcd_to_freq(const uint8_t *bcd, uint8_t len);
  void freq_to_bcd(uint32_t freq, uint8_t *bcd);
};

// PTT Switch
class IcomPTTSwitch : public switch_::Switch, public Parented<IcomCIV> {
 public:
  void write_state(bool state) override {
    this->parent_->set_ptt(state);
    this->publish_state(state);
  }
};

// Power Switch
class IcomPowerSwitch : public switch_::Switch, public Parented<IcomCIV> {
 public:
  void set_power_pin(GPIOPin *pin) { this->power_pin_ = pin; }
  void write_state(bool state) override {
    if (this->power_pin_ != nullptr) {
      // Momentary pulse to ground PWRK
      this->power_pin_->digital_write(false);
      delay(200);
      this->power_pin_->digital_write(true);
    }
    this->publish_state(state);
  }
 protected:
  GPIOPin *power_pin_{nullptr};
};

// Frequency Number
class IcomFrequencyNumber : public number::Number, public Parented<IcomCIV> {
 public:
  void control(float value) override {
    this->parent_->set_frequency(static_cast<uint32_t>(value));
    this->publish_state(value);
  }
};

}  // namespace icom_civ
}  // namespace esphome
