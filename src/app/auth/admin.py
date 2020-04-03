import sqlalchemy as sa
from starlette_admin import ModelAdmin
from starlette_auth.tables import scope, user
from starlette_auth.utils.crypto import hash_password
from starlette_core.database import database
from wtforms import form

from app.auth.forms import ScopeForm, UserCreateForm, UserUpdateForm


class ScopeAdmin(ModelAdmin):
    section_name = "Authentication"
    collection_name = "Scopes"
    model_class = scope
    object_str_function = lambda self: self["code"]
    list_field_names = ["code", "description"]
    create_form = ScopeForm
    update_form = ScopeForm
    delete_form = form.Form

    @classmethod
    def get_default_ordering(cls, qs):
        return qs.order_by("code")


class UserAdmin(ModelAdmin):
    section_name = "Authentication"
    collection_name = "Users"
    model_class = user
    object_str_function = lambda self: self["email"]
    list_field_names = ["email", "first_name", "last_name"]
    paginate_by = 10
    order_enabled = True
    search_enabled = True
    create_form = UserCreateForm
    update_form = UserUpdateForm
    delete_form = form.Form

    @classmethod
    def get_default_ordering(cls, qs):
        return qs.order_by("email")

    @classmethod
    def get_search_results(cls, qs, term):
        return qs.where(
            sa.or_(
                user.c.email.ilike(f"%{term}%"),
                user.c.first_name.ilike(f"%{term}%"),
                user.c.last_name.ilike(f"%{term}%"),
            )
        )

    @classmethod
    async def do_create(cls, form, request):
        data = form.data.copy()
        password = hash_password(form.password.data)
        data.update({"password": password, "is_active": True})
        del data["confirm_password"]
        qs = cls.model_class.insert().values(**data)
        return await database.execute(qs)
