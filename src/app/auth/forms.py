from starlette_admin.forms import widgets
from wtforms import fields, form, validators


class ScopeForm(form.Form):
    code = fields.StringField()
    description = fields.StringField()


class UserBaseForm(form.Form):
    first_name = fields.StringField()
    last_name = fields.StringField()
    email = fields.StringField()


class UserCreateForm(UserBaseForm):
    password = fields.PasswordField(
        validators=[validators.InputRequired()], widget=widgets.PasswordInput()
    )
    confirm_password = fields.PasswordField(
        validators=[
            validators.InputRequired(),
            validators.EqualTo("password", message="The passwords do not match."),
        ],
        widget=widgets.PasswordInput(),
    )


class UserUpdateForm(UserBaseForm):
    is_active = fields.BooleanField(widget=widgets.CheckboxInput())
