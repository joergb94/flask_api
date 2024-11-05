from app.config import create_app
from app.controllers.bmi_level_controller import bmi_level_bp
from app.controllers.user_bmi_controller import calculatorBmi

app = create_app()
app.register_blueprint(bmi_level_bp)
app.register_blueprint(calculatorBmi)
