#include "icom_civ.h"
#include "esphome/core/log.h"

namespace esphome {
namespace icom_civ {

static const char *TAG = "icom_civ";

void IcomCIV::setup() {
  ESP_LOGD(TAG, "Setting up Icom CI-V interface, address: 0x%02X", this->civ_address_);
  this->rx_pos_ = 0;
  this->in_frame_ = false;
}

void IcomCIV::dump_config() {
  ESP_LOGCONFIG(TAG, "Icom CI-V:");
  ESP_LOGCONFIG(TAG, "  CI-V Address: 0x%02X", this->civ_address_);
}

void IcomCIV::loop() {
  // Read incoming CI-V data
  while (this->available()) {
    uint8_t byte;
    this->read_byte(&byte);

    if (byte == CIV_PREAMBLE) {
      if (this->rx_pos_ > 0 && this->rx_buf_[0] == CIV_PREAMBLE) {
        // Second preamble byte — start of frame
        this->rx_pos_ = 0;
        this->rx_buf_[this->rx_pos_++] = CIV_PREAMBLE;
        this->rx_buf_[this->rx_pos_++] = CIV_PREAMBLE;
        this->in_frame_ = true;
        continue;
      }
      this->rx_buf_[0] = CIV_PREAMBLE;
      this->rx_pos_ = 1;
      continue;
    }

    if (this->in_frame_) {
      if (this->rx_pos_ < sizeof(this->rx_buf_)) {
        this->rx_buf_[this->rx_pos_++] = byte;
      }

      if (byte == CIV_EOM) {
        // Complete frame received
        this->process_response(this->rx_buf_, this->rx_pos_);
        this->rx_pos_ = 0;
        this->in_frame_ = false;
      }
    }
  }
}

void IcomCIV::update() {
  // Poll radio state periodically
  this->request_frequency();
  this->request_mode();
  this->request_smeter();
  this->request_ptt();
}

void IcomCIV::send_command(uint8_t cmd, const uint8_t *data, uint8_t len) {
  this->write_byte(CIV_PREAMBLE);
  this->write_byte(CIV_PREAMBLE);
  this->write_byte(this->civ_address_);  // to radio
  this->write_byte(CIV_CONTROLLER);       // from controller
  this->write_byte(cmd);
  for (uint8_t i = 0; i < len; i++) {
    this->write_byte(data[i]);
  }
  this->write_byte(CIV_EOM);
  this->flush();
}

void IcomCIV::send_command(uint8_t cmd, uint8_t sub, const uint8_t *data, uint8_t len) {
  this->write_byte(CIV_PREAMBLE);
  this->write_byte(CIV_PREAMBLE);
  this->write_byte(this->civ_address_);
  this->write_byte(CIV_CONTROLLER);
  this->write_byte(cmd);
  this->write_byte(sub);
  for (uint8_t i = 0; i < len; i++) {
    this->write_byte(data[i]);
  }
  this->write_byte(CIV_EOM);
  this->flush();
}

void IcomCIV::process_response(const uint8_t *data, uint8_t len) {
  // Minimum frame: FE FE <to> <from> <cmd> <data...> FD
  if (len < 6) return;

  // Check if this is addressed to us
  if (data[2] != CIV_CONTROLLER) return;

  uint8_t cmd = data[4];

  switch (cmd) {
    case CMD_READ_FREQ:
    case CMD_SET_FREQ: {
      // Frequency: 5 BCD bytes, LSB first
      if (len >= 10) {
        this->current_freq_ = this->bcd_to_freq(&data[5], 5);
        if (this->frequency_sensor_ != nullptr) {
          this->frequency_sensor_->publish_state(this->current_freq_);
        }
        ESP_LOGD(TAG, "Frequency: %u Hz", this->current_freq_);
      }
      break;
    }
    case CMD_READ_MODE:
    case CMD_SET_MODE: {
      if (len >= 7) {
        this->current_mode_ = data[5];
        if (this->mode_sensor_ != nullptr && this->current_mode_ < 9) {
          this->mode_sensor_->publish_state(MODE_NAMES[this->current_mode_]);
        }
        ESP_LOGD(TAG, "Mode: %s", this->current_mode_ < 9 ? MODE_NAMES[this->current_mode_] : "Unknown");
      }
      break;
    }
    case CMD_READ_SMETER: {
      if (len >= 7 && data[5] == 0x02) {
        // S-meter reading
        uint8_t level = data[6];
        if (this->smeter_sensor_ != nullptr) {
          this->smeter_sensor_->publish_state(level);
        }
      }
      break;
    }
    case CMD_READ_PTT: {
      if (len >= 7 && data[5] == 0x00) {
        this->current_ptt_ = (data[6] != 0x00);
        if (this->ptt_sensor_ != nullptr) {
          this->ptt_sensor_->publish_state(this->current_ptt_ ? 1.0f : 0.0f);
        }
      }
      break;
    }
    default:
      break;
  }
}

void IcomCIV::request_frequency() {
  this->send_command(CMD_READ_FREQ, nullptr, 0);
}

void IcomCIV::request_mode() {
  this->send_command(CMD_READ_MODE, nullptr, 0);
}

void IcomCIV::request_smeter() {
  uint8_t sub = 0x02;  // S-meter
  this->send_command(CMD_READ_SMETER, sub, nullptr, 0);
}

void IcomCIV::request_ptt() {
  uint8_t sub = 0x00;  // TX status
  this->send_command(CMD_READ_PTT, sub, nullptr, 0);
}

void IcomCIV::set_frequency(uint32_t freq_hz) {
  uint8_t bcd[5];
  this->freq_to_bcd(freq_hz, bcd);
  this->send_command(CMD_SET_FREQ, bcd, 5);
  ESP_LOGD(TAG, "Set frequency: %u Hz", freq_hz);
}

void IcomCIV::set_mode(uint8_t mode) {
  uint8_t data[2] = {mode, 0x01};  // mode + filter
  this->send_command(CMD_SET_MODE, data, 2);
  ESP_LOGD(TAG, "Set mode: %d", mode);
}

void IcomCIV::set_ptt(bool on) {
  uint8_t sub = 0x00;
  uint8_t data = on ? 0x01 : 0x00;
  this->send_command(CMD_SET_PTT, sub, &data, 1);
  ESP_LOGD(TAG, "Set PTT: %s", on ? "ON" : "OFF");
}

// BCD conversion — CI-V uses 5 bytes BCD, LSB first
// e.g. 14.250.000 Hz = 00 00 25 41 00 (reversed)
uint32_t IcomCIV::bcd_to_freq(const uint8_t *bcd, uint8_t len) {
  uint32_t freq = 0;
  uint32_t mult = 1;
  for (uint8_t i = 0; i < len; i++) {
    freq += (bcd[i] & 0x0F) * mult;
    mult *= 10;
    freq += ((bcd[i] >> 4) & 0x0F) * mult;
    mult *= 10;
  }
  return freq;
}

void IcomCIV::freq_to_bcd(uint32_t freq, uint8_t *bcd) {
  for (uint8_t i = 0; i < 5; i++) {
    bcd[i] = (freq % 10);
    freq /= 10;
    bcd[i] |= (freq % 10) << 4;
    freq /= 10;
  }
}

}  // namespace icom_civ
}  // namespace esphome
