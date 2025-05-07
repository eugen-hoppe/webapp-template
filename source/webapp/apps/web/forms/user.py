from starlette_wtf import StarletteForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired, Email, Length


class UserForm(StarletteForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])

    location_search = StringField("Ort", validators=[Length(min=2)])
    location_id = HiddenField()
