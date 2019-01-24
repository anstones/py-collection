from flask import Blueprint
from config import *

admin = Blueprint('admin',__name__,
                template_folder=TEMPLATES_DIR,
                static_folder=STATICFILES_DIR
                )

from APP.Admin import views