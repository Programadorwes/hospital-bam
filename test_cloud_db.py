# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extensions

conn_str = "postgresql://postgress:e8qtpfgZGKGhWc81IjxVlDYBC7l8zH3B@dpg-d5tno4p4tr6s73f5n74g-a/hospitalmp"

try:
    conn = psycopg2.connect(conn_str, client_encoding='LATIN1')
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM bam;")
    count = cur.fetchone()[0]
    print("Total BAM:", count)
    
    cur.execute("SELECT COUNT(*) FROM bam WHERE paciente_nome ILIKE '%elson%';")
    elson_count = cur.fetchone()[0]
    print("Com ELSON:", elson_count)
    
    cur.close()
    conn.close()
    print("OK!")
    
except Exception as e:
    print("ERRO:", str(e))
