from sqlalchemy import create_engine, text

# Função para inserir dados na tabela Wallet
def inserir_dados_wallet(totalInvested, active, investorId, conn_string):
    # Criar engine de conexão usando a connection string fornecida
    engine = create_engine(conn_string)

    # Conectar ao banco de dados com um contexto de transação que faz commit automaticamente
    with engine.begin() as conn:  # Usando begin para garantir o commit
        # Criar a query de inserção com nomes de colunas entre aspas duplas
        query = text("""
            INSERT INTO "Wallet" ("totalInvested", "active", "investorId")
            VALUES (:totalInvested, :active, :investorId)
        """)

        # Executar a query passando os parâmetros
        conn.execute(query, {"totalInvested": totalInvested, "active": active, "investorId": investorId})

        print(f"Dados inseridos na tabela Wallet para o investorId {investorId}.")

# Função principal para calcular e inserir os dados
def main():
    # Connection string fornecida para conectar ao banco de dados
    conn_string = "postgresql://finance-api_owner:s6wc1tNPBDJS@ep-red-lab-a4y556ty.us-east-1.aws.neon.tech/finance-api?sslmode=require"

    # Definindo os valores que serão inseridos na tabela Wallet
    totalInvested = 0.00  # Valor total investido
    active = True  # Definindo a carteira como ativa
    investorId = 4  # ID do investidor (chave estrangeira para a tabela Investor)

    # Inserir os dados na tabela Wallet
    inserir_dados_wallet(totalInvested, active, investorId, conn_string)

# Executar a função principal
if __name__ == "__main__":
    main()