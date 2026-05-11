import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID
from . import IcomCIV, icom_civ_ns

CONF_ICOM_CIV_ID = "icom_civ_id"
CONF_PTT = "ptt"
CONF_POWER = "power"
CONF_POWER_PIN = "power_pin"

IcomPTTSwitch = icom_civ_ns.class_("IcomPTTSwitch", switch.Switch, cg.Parented.template(IcomCIV))
IcomPowerSwitch = icom_civ_ns.class_("IcomPowerSwitch", switch.Switch, cg.Parented.template(IcomCIV))

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ICOM_CIV_ID): cv.use_id(IcomCIV),
        cv.Optional(CONF_PTT): switch.switch_schema(IcomPTTSwitch),
        cv.Optional(CONF_POWER): switch.switch_schema(IcomPowerSwitch).extend(
            {
                cv.Optional(CONF_POWER_PIN): cv.int_,
            }
        ),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_ICOM_CIV_ID])

    if CONF_PTT in config:
        s = await switch.new_switch(config[CONF_PTT])
        await cg.register_parented(s, config[CONF_ICOM_CIV_ID])

    if CONF_POWER in config:
        s = await switch.new_switch(config[CONF_POWER])
        await cg.register_parented(s, config[CONF_ICOM_CIV_ID])
