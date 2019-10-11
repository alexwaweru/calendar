import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        SECRET_KEY = os.getenv('SECRET_KEY', cfg['SECRET_KEY'])
        DEBUG = False

class DevelopmentConfig(Config):
    with open("dev_config.yml", 'r') as ymlfile:
        dev_cfg = yaml.load(ymlfile)
        DEBUG = dev_cfg["DEBUG"]
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, dev_cfg['DATABASE_URI'])
        SQLALCHEMY_TRACK_MODIFICATIONS = dev_cfg["SQLALCHEMY_TRACK_MODIFICATIONS"]


class TestingConfig(Config):
    with open("test_config.yml", 'r') as ymlfile:
        test_cfg = yaml.load(ymlfile)
        DEBUG = test_cfg["DEBUG"]
        TESTING = test_cfg["TESTING"]
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, test_cfg["SQLALCHEMY_DATABASE_URI"])
        PRESERVE_CONTEXT_ON_EXCEPTION = test_cfg["PRESERVE_CONTEXT_ON_EXCEPTION"]
        SQLALCHEMY_TRACK_MODIFICATIONS = test_cfg["SQLALCHEMY_TRACK_MODIFICATIONS"]


class ProductionConfig(Config):
    with open("prod_config.yml", 'r') as ymlfile:
        prod_cfg = yaml.load(ymlfile)
        DEBUG = prod_cfg["DEBUG"]
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, prod_cfg["SQLALCHEMY_DATABASE_URI"])


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY