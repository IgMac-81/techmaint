"""Extensões do Flask criadas aqui e ligadas à aplicação em app/__init__.py.

Por que separado? Se importássemos o `db` direto de dentro do __init__.py,
teríamos import circular (A importa B que importa A). Este arquivo quebra o ciclo.
"""

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar esta página."
login_manager.login_message_category = "aviso"
