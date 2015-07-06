import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://lmalhoit:7Lauren10@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://lmalhoit:7Lauren10@localhost:5432/blogful-test"
    DEBUG = True
    SECRET_KEY = "Not secret"