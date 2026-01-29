import psycopg2

conn = psycopg2.connect(host='localhost', database='hospitalmp', user='postgres', password='653886', port='5432')
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'examescomplementares'")
colunas = cur.fetchall()
print('Colunas da tabela examescomplementares:')
for col in colunas:
    print(col[0])
cur.close()
conn.close()