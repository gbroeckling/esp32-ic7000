import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID, UNIT_HERTZ, UNIT_EMPTY, STATE_CLASS_MEASUREMENT
from . import IcomCIV, icom_civ_ns

CONF_ICOM_CIV_ID = "icom_civ_id"
CONF_FREQUENCY = "frequency"
CONF_SMETER = "s_meter"
CONF_PTT_STATE = "ptt_state"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ICOM_CIV_ID): cv.use_id(IcomCIV),
        cv.Optional(CONF_FREQUENCY): sensor.sensor_schema(
            unit_of_measurement=UNIT_HERTZ,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_SMETER): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_PTT_STATE): sensor.sensor_schema(
            accuracy_decimals=0,
        ),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_ICOM_CIV_ID])

    if CONF_FREQUENCY in config:
        s = await sensor.new_sensor(config[CONF_FREQUENCY])
        cg.add(parent.set_frequency_sensor(s))

    if CONF_SMETER in config:
        s = await sensor.new_sensor(config[CONF_SMETER])
        cg.add(parent.set_smeter_sensor(s))

    if CONF_PTT_STATE in config:
        s = await sensor.new_sensor(config[CONF_PTT_STATE])
        cg.add(parent.set_ptt_sensor(s))
