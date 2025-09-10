# FS_auth_middleware

Pacote Python para autenticação JWT e permissões reutilizáveis com Django Rest Framework.

## Instalação

```bash
pip install git+https://github.com/Cassio-de-Paula/FS_auth_middleware.git
```

Este middleware foi desenvolvido para intergar de forma eficiente e segura, diversos projetos django, vinculados a um sistema base que fornece a autenticação de usuários, utilizando o sistema de grupos e permissões nativo do Framework Django

@has_permissions()
recebe uma lista de permissões, extrai o cookie "access_token" recebido na request, decodifica com a SECRET_KEY do projeto, verifica se as permissões obtidas do token incluem as permissões recebidas como argumento. 

Ex:
@has_permissions(['add_model', 'view_model', 'change_model', 'delete_model'])
