from marshmallow import Schema, fields, validate, ValidationError

def validate_id(value):
    if value is not None and (not isinstance(value, int) or value <= 0):
        raise ValidationError("ID must be a positive integer.")


class CalculatorBmiValidate(Schema):
    id = fields.Int(required=False, validate=validate_id)
    name = fields.Str(required=True, allow_none=False)
    email = fields.Str(required=True, allow_none=False)
    phone = fields.Str(required=True, allow_none=False)
    weight = fields.Float(required=True, validate=validate.Range(min=1))
    height = fields.Float(required=True, validate=validate.Range(min=0.1))
