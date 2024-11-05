from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.bmi_level_model import BmiLevelModel
from app.models.user_model import UserModel
from app.models.user_bmi_model import UserBmiModel
from app.validator.calculator_bmi_validate import CalculatorBmiValidate
from app.service.chatbotOpenai import get_chatbot_response
from marshmallow import ValidationError

calculatorBmi = Blueprint('calculatorbmi', __name__, url_prefix='/calculatorbmi')

@calculatorBmi.route('/')
def index():
    bmi_levels = BmiLevelModel.get_all_bmi_levels()
    return bmi_levels

@calculatorBmi.route('/create', methods=['POST'])
def creta_user_bmi():
    schema = CalculatorBmiValidate()
    try:
        validated_data = schema.load(request.get_json())
        description = ""
        bmi_level_id = 0
        weight = validated_data['weight']
        height = validated_data['height']

        ibm = weight/height**2

        if ibm > 30:
            bmi_level_id = 1
        elif ibm >= 25 and ibm <= 30:
            bmi_level_id = 2
        elif ibm >= 18.5 and ibm < 25:
            bmi_level_id = 3
        else:
            bmi_level_id = 4
            
        dataUser = UserModel.get_user_by_email(validated_data['email'])
        if dataUser:
            update_user = UserModel.update_user(dataUser['user_id'],validated_data['name'], validated_data['email'],validated_data['phone'])
            bmi_level= BmiLevelModel.get_bmi_level_by_id(bmi_level_id)
            description = get_chatbot_response(bmi_level['name'])
            user_bmi=UserBmiModel.update_user_bmi(dataUser['user_bmi_id'],dataUser['user_id'],bmi_level['id'],weight,height,description)
            user_bmi['status']="updated"
        else:
            new_user = UserModel.create_user(validated_data['name'], validated_data['email'],validated_data['phone'])
            bmi_level= BmiLevelModel.get_bmi_level_by_id(bmi_level_id)
            description = get_chatbot_response(bmi_level['name'])
            user_bmi=UserBmiModel.create_user_bmi(new_user['id'],bmi_level['id'],weight,height,description)
            user_bmi['status']="created"
        return jsonify(user_bmi), 200 
    except ValidationError as err:
        return jsonify(err.messages), 422

