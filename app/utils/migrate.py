import sqlite3

conn = sqlite3.connect("cnpj_insight.db")

cursor = conn.cursor()

cursor.execute("""
ALTER TABLE consulta
ADD COLUMN favorito INTEGER NOT NULL DEFAULT 0
""")

conn.commit()
conn.close()

print("Migração concluída.")