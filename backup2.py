from datetime import datetime
from dateutil.relativedelta import relativedelta

# data de inicio e de fim do backup
data_inicio = datetime.fromisoformat('2024-01-01')
data_fim = data_inicio + relativedelta(years=+2)

print(data_inicio)
print(data_fim)

# primeiro sábado antes da data de início do backup
# onde se faz o backup full de referência
primeiro_sabado_antes = None
for delta_dia in range(7):
    dia_x = data_inicio + relativedelta(days=-delta_dia)
    if dia_x.weekday() == 5:
        primeiro_sabado_antes = dia_x
        break

agenda_intersticio = [primeiro_sabado_antes]

# interstício entre data de início e de fim do backup
dias_intersticio = (data_fim - data_inicio).days + 1

# todos os dias do interstício entre início e fim do backup
# mais o primeiro sábado anterior com marcações dos dias
# indicados para o backup full
for delta_dia in range(dias_intersticio):
    dia_x = data_inicio + relativedelta(days=+delta_dia)
    if dia_x != primeiro_sabado_antes:
        agenda_intersticio.append(dia_x)

# agenda de backups anual dentro do interstício mais o
# primeiro sábado anterior
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
for delta_semestre in range(semestres):
    data_proximo_backup_semestre = data_inicio + relativedelta(months=+((delta_semestre + 1) * 6)) 
    for delta_dia in range(7):
        data_proximo_backup_dia = data_proximo_backup_semestre + relativedelta(days=-delta_dia)
        if data_proximo_backup_dia.weekday() == 5:
            agenda_semestre.append(data_proximo_backup_dia)
            break

# agenda de backups mensal dentro do interstício 
agenda_mes = []
meses = ((data_fim.year - data_inicio.year) * 12 + (data_fim.month - data_inicio.month))
for delta_mes in range(meses):
    data_proximo_backup_mes = data_inicio + relativedelta(months=+(delta_mes + 1)) 
    for delta_dia in range(7):
        data_proximo_backup_dia = data_proximo_backup_mes + relativedelta(days=-delta_dia)
        if data_proximo_backup_dia.weekday() == 5:
            agenda_mes.append(data_proximo_backup_dia)
            break

# agenda de backups semanal dentro do interstício 
agenda_semana = []
semanas = (data_fim - data_inicio).days // 7
for delta_semana in range(semanas):
    data_proximo_backup_semana = data_inicio + relativedelta(days=+((delta_semana + 1) * 7)) 
    for delta_dia in range(7):
        data_proximo_backup_dia = data_proximo_backup_semana + relativedelta(days=-delta_dia)
        if data_proximo_backup_dia.weekday() == 5:
            agenda_semana.append(data_proximo_backup_dia)
            break

# print(agenda_intersticio)
# print(agenda_ano)
# print(agenda_semestre)
# print(agenda_mes)
# print(agenda_semana)

backups = []
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
        backup = { "data_backup": dia, "frequencia_backup": "anual", "tipo_ backup": "full" }
        backups.append(backup)
    elif idxsemestre != None:
        backup = { "data_backup": dia, "frequencia_backup": "semestral", "tipo_ backup": "full" }
        backups.append(backup)
    elif idxmes != None:
        backup = { "data_backup": dia, "frequencia_backup": "mensal", "tipo_ backup": "diferencial" }
        backups.append(backup)
    elif idxsemana != None:
        backup = { "data_backup": dia, "frequencia_backup": "semanal", "tipo_ backup": "diferencial" }
        backups.append(backup)
    else:
        backup = { "data_backup": dia, "frequencia_backup": "diario", "tipo_ backup": "incremental" }
        backups.append(backup)

for backup in backups:
    print(backup)