class ClienteDomain:
    def __init__(self, nome, email, senha, cpf, telefone, endereco, cep, data_nascimento, 
                 renda_mensal=None, cnh=None, categoria_cnh=None, profissao=None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.cep = cep
        self.data_nascimento = data_nascimento
        self.renda_mensal = renda_mensal  # Para análise de crédito
        self.cnh = cnh  # Número da CNH
        self.categoria_cnh = categoria_cnh  # A, B, C, D, E
        self.profissao = profissao

    def to_dict(self):
        return {
            "id": getattr(self, 'id', None),
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "cep": self.cep,
            "data_nascimento": self.data_nascimento,
            "renda_mensal": self.renda_mensal,
            "cnh": self.cnh,
            "categoria_cnh": self.categoria_cnh,
            "profissao": self.profissao
        }


class VendedorDomain:
    def __init__(self, nome, email, senha, cpf, telefone, endereco, cep, data_nascimento,
                 codigo_vendedor, comissao_percentual, meta_mensal=None, gerente_id=None):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.cep = cep
        self.data_nascimento = data_nascimento
        self.codigo_vendedor = codigo_vendedor
        self.comissao_percentual = comissao_percentual  # Percentual de comissão
        self.meta_mensal = meta_mensal  # Meta de vendas mensal
        self.gerente_id = gerente_id  # ID do gerente responsável

    def to_dict(self):
        return {
            "id": getattr(self, 'id', None),
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "cep": self.cep,
            "data_nascimento": self.data_nascimento,
            "codigo_vendedor": self.codigo_vendedor,
            "comissao_percentual": self.comissao_percentual,
            "meta_mensal": self.meta_mensal,
            "gerente_id": self.gerente_id
        }