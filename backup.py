from datetime import datetime
from dateutil.relativedelta import relativedelta
from enum import Enum

class Backup_Type(Enum):
    INCREMENTAL = 1
    DIFERENCIAL = 2
    FULL = 3

class Backup:
    def __init__(self, data_backup: datetime, tipo_backup: Backup_Type, data_referencia_backup: datetime, 
                 tipo_referencia_backup: Backup_Type, expiracao_backup: datetime) -> None:
        self.data_backup = data_backup
        self.tipo_backup = tipo_backup
        self.data_referencia_backup = data_referencia_backup
        self.tipo_referencia_backup = tipo_referencia_backup
        self.expiracao_backup = expiracao_backup

def backups_anuais(data_backup: datetime, versoes: int, tipo: Backup_Type):
    for x in range(versoes):
        print(data_backup + relativedelta(years=+x))

backups_anuais('2024/01/01', 5, Backup_Type.FULL)