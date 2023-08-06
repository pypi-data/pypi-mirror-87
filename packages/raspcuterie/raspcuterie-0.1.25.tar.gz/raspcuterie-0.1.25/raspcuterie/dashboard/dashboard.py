from flask import render_template, Blueprint, current_app
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import YamlLexer

from raspcuterie.devices import OutputDevice, InputDevice
from raspcuterie.devices.input.am2302 import AM2302

bp = Blueprint("dashboard", __name__, template_folder="./templates")


@bp.route("/")
def dashboard():

    refrigerator = OutputDevice.registry["refrigerator"]
    heater = OutputDevice.registry["heater"]
    dehumidifier = OutputDevice.registry["dehumidifier"]
    humidifier = OutputDevice.registry["humidifier"]

    am2302: AM2302 = InputDevice.registry["temperature"]

    temperature_data = am2302.temperature_data()
    humidity_data = am2302.humidity_data()

    x = list(dict(temperature_data).values())
    if x:
        temperature_min = min(x)
        temperature_max = max(x)
    else:
        temperature_min = 0
        temperature_max = 0

    y = list(dict(humidity_data).values())
    if y:
        humidity_min = min(y)
        humidity_max = max(y)
    else:
        humidity_min = 0
        humidity_max = 0

    config = current_app.config["config"]
    formatter = HtmlFormatter(linenos=True, style="friendly", noclasses=True)
    config_text = highlight(config, YamlLexer(), formatter)

    return render_template(
        "dashboard.html",
        refrigerator=refrigerator.value(),
        heater=heater.value(),
        dehumidifier=dehumidifier.value(),
        humidifier=humidifier.value(),
        humidifier_data=humidifier.chart(),
        dehumidifier_data=dehumidifier.chart(),
        refrigerator_data=refrigerator.chart(),
        heater_data=heater.chart(),
        temperature_min=temperature_min,
        temperature_max=temperature_max,
        temperature_data=temperature_data,
        humidity_data=humidity_data,
        humidity_min=humidity_min,
        humidity_max=humidity_max,
        config_text=config_text,
    )
