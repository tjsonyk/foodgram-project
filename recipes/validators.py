from django import forms

def validate_not_negative(value):
    if value < 0:
        raise forms.ValidationError(
            'Отрицательно значение? Реально?!',
            params={'value': value},
        )