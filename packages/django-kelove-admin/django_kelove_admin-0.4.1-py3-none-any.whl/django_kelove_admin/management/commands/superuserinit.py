# ==================================================================
#       文 件 名: superuserinit.py
#       概    要: 初始化超级用户
#       作    者: IT小强 
#       创建时间: 8/10/20 3:32 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================


import os
import uuid
from hashlib import md5

from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.management import get_system_username

from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, IntegrityError


class Command(BaseCommand):
    """
    初始化超级用户
    """

    help = 'Used to create a superuser.'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.UserModel = get_user_model()
        self.username_field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)

    def add_arguments(self, parser):
        parser.add_argument(
            '--database',
            default=DEFAULT_DB_ALIAS,
            help='Specifies the database to use. Default is "default".',
        )

    def handle(self, *args, **options):
        """
        初始化超级用户
        :param args:
        :param options:
        :return:
        """
        username = get_system_username()
        if not username:
            username = 'admin'

        password = md5(str(uuid.uuid4()).encode()).hexdigest()

        database = options['database']

        try:
            self.UserModel._default_manager.db_manager(database).create_superuser(
                username=username,
                password=password
            )

            save_path = os.path.join(settings.BASE_DIR, 'storage')

            if not os.path.isdir(save_path):
                os.mkdir(save_path)

            file_path = os.path.join(save_path, 'admin_password')

            with open(file_path, 'w') as f:
                f.writelines([username, '\n', password])
            if options['verbosity'] >= 1:
                msgs = [
                    'Superuser created successfully.',
                    'username:{username}'.format(username=username),
                    'password:{password}'.format(password=password),
                    'path:{path}'.format(path=file_path)
                ]
                for msg in msgs:
                    self.stdout.write(msg)
        except IntegrityError:
            msg = 'Superuser "{username}" already exists'.format(username=username)
            if options['verbosity'] >= 1:
                self.stdout.write(msg)
