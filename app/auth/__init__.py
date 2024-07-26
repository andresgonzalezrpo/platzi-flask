from flask import Blueprint
auth = Blueprint('auth', __name__,url_prefix='/auth') #all routes /auth will be redirect to this Blueprint

from . import views