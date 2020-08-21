# Must import all models here so that alembic can detect them
from app.models import User, CeleryTaskmeta, CeleryTasksetmeta # noqa
from app.models.form_models import * # noqa
from app.db.base_class import Base # noqa