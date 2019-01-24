from APP.Admin import admin
from APP.Admin.models import *

@admin.route('/rx')
def reaix():
    return 'everyone reaix'