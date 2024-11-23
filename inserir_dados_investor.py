from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Função para criar e inserir um novo investidor no banco de dados
def criar_investidor(email, name, password, tax_id, conn_string):
    engine = create_engine(conn_string)

    with engine.begin() as conn:  # Usando begin para garantir o commit
        try:
            query_insert_investor = text("""
                INSERT INTO "Investor" ("email", "name", "password", "tax_id")
                VALUES (:email, :name, :password, :tax_id)
            """)
            conn.execute(query_insert_investor, {
                "email": email,
                "name": name,
                "password": password,
                "tax_id": tax_id
            })
            print(f"Investidor com email {email} inserido na tabela Investor.")
        except SQLAlchemyError as e:
            print("Erro ao inserir investidor:", str(e))

# Exemplo de uso para inserir
if __name__ == "__main__":
    conn_string = "postgresql://finance-api_owner:s6wc1tNPBDJS@ep-red-lab-a4y556ty.us-east-1.aws.neon.tech/finance-api?sslmode=require"
    email = "10334750@mackenzista.com.br"
    name = "Marcelo Kodaira"
    password = "12345678"
    tax_id = "10334750"

    criar_investidor(email, name, password, tax_id, conn_string)

