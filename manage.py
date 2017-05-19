# coding=utf-8
import os
from oslo_config import cfg
from oslo_log import log as logging

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_script.commands import ShowUrls, Clean
from flask_assets import ManageAssets

from fe import create_app
from fe.database.sqlalchemy import models
from fe.extensions import assets_env
from fe.i18n import _LI

CONF = cfg.CONF

LOG = logging.getLogger(__name__)

# Get the ENV from os_environ
env = os.environ.get('BLOG_ENV', 'dev')
# Create thr app instance via Factory Method
app = create_app('fe.conf.config.%sConfig' % env.capitalize())

# Init manager object via app object
manager = Manager(app)

# Init migrate object via app and db object
migrate = Migrate(app, models.db)

# Create the new application manage commands as below
# Start the flask web server
manager.add_command("server", Server(host=CONF.host, port=CONF.server_port))
# Manage database migrate
manager.add_command("db", MigrateCommand)
# Show all mapper of route url
manager.add_command("show-urls", ShowUrls())
# Clean alll the file of .pyc and .pyo
manager.add_command("clean", Clean())
# Pack the static file
manager.add_command('assets', ManageAssets(assets_env))


# 创建表
# db.create_all()

@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag,
                Role=models.Role,
                BrowseVolume=models.BrowseVolume,
                Reminder=models.Reminder,
                Server=Server)


if __name__ == '__main__':
    LOG.info(_LI('Running jack blog manager.'))
    manager.run()
