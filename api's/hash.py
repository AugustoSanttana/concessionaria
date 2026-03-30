from werkzeug.security import generate_password_hash

hash_senha = generate_password_hash("senha_super_secreta", method="pbkdf2:sha256:260000")
print(hash_senha)
