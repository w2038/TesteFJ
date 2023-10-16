import sqlite3
from datetime import datetime

class GerenciadorProducao:
    def __init__(self):
        # Inicializa a conexão e o cursor do banco de dados
        self.conn = sqlite3.connect('gerenciamento_producao.db')
        self.cursor = self.conn.cursor()
        # Cria as tabelas se elas não existirem
        self.criar_tabela_ordens_producao()
        self.criar_tabela_produtos()

    def __del__(self):
        # Fecha a conexão ao destruir a instância
        self.conn.close()

    def criar_tabela_ordens_producao(self):
        # Cria a tabela ordens_producao se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ordens_producao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT,
                quantidade INTEGER,
                data_entrega TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def criar_tabela_produtos(self):
        # Cria a tabela produtos se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                quantidade_inicial INTEGER
            )
        ''')
        self.conn.commit()

    def cadastrar_produto(self):
        # Solicita detalhes do produto ao usuário
        nome = input('Digite o nome do produto: ')
        quantidade_inicial = int(input('Digite a quantidade inicial de material: '))
        # Insere os detalhes do produto no banco de dados
        self.cursor.execute('INSERT INTO produtos (nome, quantidade_inicial) VALUES (?, ?)', (nome, quantidade_inicial))
        self.conn.commit()
        print(f'Produto "{nome}" cadastrado com sucesso!')

    def listar_produtos(self):
        # Lista todos os produtos no banco de dados
        self.cursor.execute('SELECT * FROM produtos')
        produtos = self.cursor.fetchall()

        if not produtos:
            print('Nenhum produto cadastrado.')
        else:
            print('### Produtos Cadastrados ###')
            for produto in produtos:
                print(f'ID: {produto[0]}, Nome: {produto[1]}, Quantidade Inicial: {produto[2]}')

    def cadastrar_ordem_producao(self, produto, quantidade, data_entrega):
        # Registra uma nova ordem de produção no banco de dados
        status = 'Em andamento'
        self.cursor.execute('''
            INSERT INTO ordens_producao (produto, quantidade, data_entrega, status)
            VALUES (?, ?, ?, ?)
        ''', (produto, quantidade, data_entrega, status))
        self.conn.commit()
        print('Ordem de produção registrada com sucesso!')

    def listar_ordens_producao(self):
        # Lista todas as ordens de produção no banco de dados
        self.cursor.execute('SELECT * FROM ordens_producao')
        ordens = self.cursor.fetchall()
        if not ordens:
            print('Nenhuma ordem de produção encontrada.')
        else:
            for ordem in ordens:
                print(f'ID: {ordem[0]}, Produto: {ordem[1]}, Quantidade: {ordem[2]}, Data de Entrega: {ordem[3]}, Status: {ordem[4]}')

    def verificar_disponibilidade_materiais(self, produto, quantidade_necessaria):
            # Verifica a quantidade inicial de materiais disponíveis para o produto
            self.cursor.execute('SELECT quantidade_inicial FROM produtos WHERE nome = ?', (produto,))
            resultado = self.cursor.fetchone()

            if resultado is not None:
                quantidade_inicial = resultado[0]

                # Verifica se há material suficiente para a produção
                if quantidade_inicial >= quantidade_necessaria:
                    print(f'Produção possível para o produto "{produto}".')
                else:
                    print(f'Produção não é possível para o produto "{produto}" devido à falta de materiais.')
            else:
                print(f'Produto "{produto}" não encontrado.')

    def atualizar_status_ordem_producao(self, ordem_id, status):
        # Atualiza o status de uma ordem de produção no banco de dados
        self.cursor.execute('UPDATE ordens_producao SET status = ? WHERE id = ?', (status, ordem_id))
        self.conn.commit()
        print('Status da ordem de produção atualizado com sucesso!')

    def relatorio_producao(self):
        # Gera um relatório de produção
        self.cursor.execute('SELECT * FROM ordens_producao WHERE status = "Em andamento"')
        ordens_andamento = self.cursor.fetchall()

        self.cursor.execute('SELECT * FROM ordens_producao WHERE status = "Concluída"')
        ordens_concluidas = self.cursor.fetchall()

        print('### Ordens em Andamento ###')
        for ordem in ordens_andamento:
            print(f'ID: {ordem[0]}, Produto: {ordem[1]}, Quantidade: {ordem[2]}, Data de Entrega: {ordem[3]}')

        print('\n### Ordens Concluídas ###')
        for ordem in ordens_concluidas:
            print(f'ID: {ordem[0]}, Produto: {ordem[1]}, Quantidade: {ordem[2]}, Data de Entrega: {ordem[3]}')

    def menu(self):
        while True:
            print('\n### Menu ###')
            print('1. Cadastrar Produto')
            print('2. Listar Produtos')
            print('3. Cadastrar Ordem de Produção')
            print('4. Listar Ordens de Produção')
            print('5. Verificar Disponibilidade de Materiais')
            print('6. Atualizar Status de Ordem de Produção')
            print('7. Relatório de Produção')
            print('8. Sair')

            escolha = input('Escolha uma opção: ')

            if escolha == '1':
                self.cadastrar_produto()
            elif escolha == '2':
                self.listar_produtos()
            elif escolha == '3':
                produto = input('Digite o nome do produto para a ordem de produção: ')
                quantidade = int(input('Digite a quantidade desejada: '))
                data_entrega = input('Digite a data de entrega (YYYY-MM-DD): ')
                self.cadastrar_ordem_producao(produto, quantidade, data_entrega)
            elif escolha == '4':
                self.listar_ordens_producao()
            elif escolha == '5':
                produto_verificar = input('Digite o nome do produto para verificar disponibilidade: ')
                quantidade_verificar = int(input('Digite a quantidade desejada: '))
                self.verificar_disponibilidade_materiais(produto_verificar, quantidade_verificar)
            elif escolha == '6':
                ordem_id = int(input('Digite o ID da ordem de produção a ser atualizada: '))
                status_novo = input('Digite o novo status (Em andamento/Concluída): ')
                self.atualizar_status_ordem_producao(ordem_id, status_novo)
            elif escolha == '7':
                self.relatorio_producao()
            elif escolha == '8':
                break
            else:
                print('Opção inválida. Tente novamente.')


gerenciador = GerenciadorProducao()
gerenciador.menu()
