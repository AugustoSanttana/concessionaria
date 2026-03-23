class UserDomain:
    def __init__(self, nome, email, senha, cpf, endereco):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.endereco = endereco

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "cpf": self.cpf,
            "endereco": self.endereco
        }