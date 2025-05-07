from starlette_wtf import StarletteForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


class UserForm(StarletteForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(max=50)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)],
    )
