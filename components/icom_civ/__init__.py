import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, sensor, switch, text_sensor, number
from esphome.const import CONF_ID

DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor", "text_sensor", "switch", "number"]

CONF_CIV_ADDRESS = "civ_address"
CONF_POLL_INTERVAL = "poll_interval"

icom_civ_ns = cg.esphome_ns.namespace("icom_civ")
IcomCIV = icom_civ_ns.class_("IcomCIV", cg.PollingComponent, uart.UARTDevice)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(IcomCIV),
            cv.Optional(CONF_CIV_ADDRESS, default=0x70): cv.hex_uint8_t,
            cv.Optional(CONF_POLL_INTERVAL, default="2s"): cv.update_interval,
        }
    )
    .extend(cv.polling_component_schema("2s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    cg.add(var.set_civ_address(config[CONF_CIV_ADDRESS]))
