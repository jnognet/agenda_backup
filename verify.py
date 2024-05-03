from datetime import datetime
import json
import locale

locale.setlocale(locale.LC_TIME, "pt_BR")

data_verificacao = datetime.fromisoformat('2024-12-28')

with open('backups.json', 'r', encoding="utf-8") as fout:
    backups = json.load(fout)

verify = []
for backup in backups:
    if datetime.strptime(backup['data_backup'], '%Y-%m-%d %H:%M:%S') < data_verificacao and datetime.strptime(backup['expiracao_backup'], '%Y-%m-%d %H:%M:%S') > data_verificacao:
        verify.append(backup)

with open('verify.json', 'w', encoding="utf-8") as fout:
    json.dump(verify, fout, indent=4, default=str, ensure_ascii=False)