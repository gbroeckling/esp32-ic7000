import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID
from . import IcomCIV, icom_civ_ns

CONF_ICOM_CIV_ID = "icom_civ_id"
CONF_MODE = "mode"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ICOM_CIV_ID): cv.use_id(IcomCIV),
        cv.Optional(CONF_MODE): text_sensor.text_sensor_schema(),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_ICOM_CIV_ID])

    if CONF_MODE in config:
        s = await text_sensor.new_text_sensor(config[CONF_MODE])
        cg.add(parent.set_mode_sensor(s))
