import psycopg2

conn = psycopg2.connect(host='localhost', database='hospitalmp', user='postgres', password='653886', port='5432')
cur = conn.cursor()
cur.execute('''
    SELECT p.nome, b.idbam, b.receita, p.prontuario
    FROM bam b
    JOIN pacientes p ON b.paciente_idpaciente = p.idpaciente
    WHERE b.receita IS NOT NULL AND b.receita <> ''
    LIMIT 20;
''')
resultados_receita = cur.fetchall()

cur.execute('''
    SELECT DISTINCT p.nome, b.idbam, p.prontuario
    FROM bam b
    JOIN pacientes p ON b.paciente_idpaciente = p.idpaciente
    WHERE p.prontuario IN (
        SELECT prontuario FROM examescomplementares WHERE prontuario IS NOT NULL AND prontuario <> ''
    )
    LIMIT 20;
''')
resultados_exame = cur.fetchall()

print('Pacientes com receita:')
for nome, idbam, receita, prontuario in resultados_receita:
    print(f'{nome} (idbam={idbam}, prontuario={prontuario})')

print('\nPacientes com exame:')
for nome, idbam, prontuario in resultados_exame:
    print(f'{nome} (idbam={idbam}, prontuario={prontuario})')

cur.close()
conn.close()
