# app/controllers/user_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.bmi_level_model import BmiLevelModel

bmi_level_bp = Blueprint('bmilevels', __name__, url_prefix='/bmilevels')

@bmi_level_bp.route('/')
def index():
    bmi_levels = BmiLevelModel.get_all_bmi_levels()
    return  bmi_levels

@bmi_level_bp.route('/<bmi_level_id>', methods=['GET'])
def get_bmi_level_by_id(bmi_level_id):
    bmi_level = BmiLevelModel.get_bmi_level_by_id(bmi_level_id)
    return jsonify(bmi_level), 200 

