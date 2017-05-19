# coding=utf-8
from fe import create_app
from fe.conf.config import DevConfig

app = create_app(DevConfig)
app.run(host=app.config["HOST"], port=app.config["PORT"])
