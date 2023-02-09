import abc

from django.db import transaction
from typing import List

from zero_migrations.constants import MIGRATION_TABLE_BACKUP_DIR_NAME, MIGRATION_TABLE_BACKUP_FILE_NAME
from zero_migrations.utils import BackupFile, Migration


class BaseRestore(abc.ABC):

    @abc.abstractmethod
    def restore(self):
        raise NotImplementedError


class MigrationRestore(BaseRestore):

    def __init__(self):
        self.file_handler = BackupFile(
            dir_name=MIGRATION_TABLE_BACKUP_DIR_NAME,
            file_name=MIGRATION_TABLE_BACKUP_FILE_NAME
        )

    @transaction.atomic
    def restore(self):
        backup_migrations = self.get_migrations_data_from_backup()
        Migration.objects.all().delete()
        Migration.objects.bulk_create(backup_migrations)

    def get_migrations_data_from_backup(self) -> List[Migration]:
        migrations_data = self.file_handler.read()
        backup_migrations = []
        for migration in migrations_data:
            backup_migrations.append(
                Migration(**migration)
            )

        return backup_migrations
