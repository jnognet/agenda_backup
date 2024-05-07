from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import locale

locale.setlocale(locale.LC_TIME, "pt_BR")

# data de inicio inclusive e de fim do backup exclusive
data_inicio = datetime.fromisoformat('2024-01-01')
 # >= 1 ano
data_fim = data_inicio + relativedelta(years=+5)

print(data_inicio)
print(data_fim)

# interstício entre data de início e de fim do backup
dias_intersticio = (data_fim - data_inicio).days 

agenda_intersticio = []
# todos os dias do interstício entre início e fim do backup
for delta_dia in range(dias_intersticio):
    dia = data_inicio + relativedelta(days=+delta_dia)
    agenda_intersticio.append(dia)

# agenda de backups anual dentro do interstício 
agenda_ano = [agenda_intersticio[0]]
for delta_ano in range(1, relativedelta(data_fim, data_inicio).years):
    data_proximo_backup_ano = data_inicio + relativedelta(years=+delta_ano)
    for delta_dia in range(7):
        data_proximo_backup_dia = data_proximo_backup_ano + relativedelta(days=+delta_dia)
        if data_proximo_backup_dia.weekday() == 5:
            agenda_ano.append(data_proximo_backup_dia)
            break

# agenda de backups semestral dentro do interstício 
agenda_semestre = []
semestres = ((data_fim.year - data_inicio.year) * 12 + (data_fim.month - data_inicio.month)) // 6
for delta_semestre in range(0, semestres):
    data_proximo_backup_semestre = data_inicio + relativedelta(months=+2) + relativedelta(months=+(delta_semestre * 6)) 
    for delta_dia in range(7):
        data_proximo_backup_dia = data_proximo_backup_semestre + relativedelta(days=+delta_dia)
        if data_proximo_backup_dia.weekday() == 5:
            agenda_semestre.append(data_proximo_backup_dia)
            break

# agenda de backups mensal dentro do interstício 
agenda_mes = []
meses = ((data_fim.year - data_inicio.year) * 12 + (data_fim.month - data_inicio.month))
for delta_mes in range(0, meses):
    data_proximo_backup_mes = data_inicio + relativedelta(months=+delta_mes)
    for delta_dia in range(7):
        data_proximo_backup_dia = data_proximo_backup_mes + relativedelta(days=+delta_dia)
        if data_proximo_backup_dia.weekday() == 5:
            agenda_mes.append(data_proximo_backup_dia)
            break

# agenda de backups semanal dentro do interstício 
agenda_semana = []
semanas = (data_fim - data_inicio).days // 7
for delta_semana in range(1, semanas + 1):
    data_proximo_backup_semana = data_inicio + relativedelta(days=+(delta_semana * 7)) 
    for delta_dia in range(7):
        data_proximo_backup_dia = data_proximo_backup_semana + relativedelta(days=-delta_dia)
        if data_proximo_backup_dia.weekday() == 5:
            agenda_semana.append(data_proximo_backup_dia)
            break

backups = []
last_full = datetime.min
last_diferencial = datetime.min
last_incremental = datetime.min

for dia in agenda_intersticio:
    try:
        idxano = agenda_ano.index(dia)
    except:
        idxano = None
    
    try:
        idxsemestre = agenda_semestre.index(dia)
    except:
        idxsemestre = None

    try:
        idxmes = agenda_mes.index(dia)
    except:
        idxmes = None

    try:
        idxsemana = agenda_semana.index(dia)
    except:
        idxsemana = None

    if idxano != None:
        backup = { "data_backup": dia, "dia_backup": dia.strftime("%A"), "frequencia_backup": "anual", "tipo_backup": "full", "expiracao_backup": dia + relativedelta(years=+5), "referencia_tipo": "-", "referencia_backup": "-" }
        backups.append(backup)
        last_full = dia
    elif idxsemestre != None:
        backup = { "data_backup": dia, "dia_backup": dia.strftime("%A"), "frequencia_backup": "semestral", "tipo_backup": "full", "expiracao_backup": dia + relativedelta(months=+18), "referencia_tipo": "-", "referencia_backup": "-" }
        backups.append(backup)
        last_full = dia
    elif idxmes != None:
        backup = { "data_backup": dia, "dia_backup": dia.strftime("%A"), "frequencia_backup": "mensal", "tipo_backup": "diferencial", "expiracao_backup": dia + relativedelta(months=+7), "referencia_tipo": "full", "referencia_backup": last_full }
        backups.append(backup)
        last_diferencial = dia
    elif idxsemana != None:
        backup = { "data_backup": dia, "dia_backup": dia.strftime("%A"), "frequencia_backup": "semanal", "tipo_backup": "diferencial", "expiracao_backup": dia + relativedelta(days=+(8 * 7)), "referencia_tipo": "full", "referencia_backup": last_full }
        backups.append(backup)
        last_diferencial = dia
    else:
        if last_full > last_diferencial and last_full > last_incremental:
            backup = { "data_backup": dia, "dia_backup": dia.strftime("%A"), "frequencia_backup": "diario", "tipo_backup": "incremental", "expiracao_backup": dia + relativedelta(days=+15), "referencia_tipo": "full", "referencia_backup": last_full }
        elif last_diferencial > last_incremental:
            backup = { "data_backup": dia, "dia_backup": dia.strftime("%A"), "frequencia_backup": "diario", "tipo_backup": "incremental", "expiracao_backup": dia + relativedelta(days=+15), "referencia_tipo": "diferencial", "referencia_backup": last_diferencial }
        else:
            backup = { "data_backup": dia, "dia_backup": dia.strftime("%A"), "frequencia_backup": "diario", "tipo_backup": "incremental", "expiracao_backup": dia + relativedelta(days=+15), "referencia_tipo": "incremental", "referencia_backup": last_incremental }
        backups.append(backup)
        last_incremental = dia

with open('agendas.json', 'w', encoding="utf-8") as fout:
    json.dump(agenda_ano, fout, indent=4, default=str, ensure_ascii=False)
    json.dump(agenda_semestre, fout, indent=4, default=str, ensure_ascii=False)
    json.dump(agenda_mes, fout, indent=4, default=str, ensure_ascii=False)
    json.dump(agenda_semana, fout, indent=4, default=str, ensure_ascii=False)
    json.dump(agenda_intersticio, fout, indent=4, default=str, ensure_ascii=False)

with open('backups.json', 'w', encoding="utf-8") as fout:
    json.dump(backups, fout, indent=4, default=str, ensure_ascii=False)
