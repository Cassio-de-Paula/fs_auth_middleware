# FS_auth_middleware

Pacote Python para autenticação JWT e permissões reutilizáveis com Django Rest Framework.

## Instalação

```bash
pip install git+https://github.com/Cassio-de-Paula/FS_auth_middleware.git
```

Este middleware foi desenvolvido para intergar de forma eficiente e segura, diversos projetos django, vinculados a um sistema base que fornece a autenticação de usuários, utilizando o sistema de grupos e permissões nativo do Framework Django

@is_athenticated()
Verifica se o token do usuário é decodificável através de uma SECRET_KEY registrada no banco de dados do sistema principal

@has_every_permission(['add_entity', 'view_entity', 'change_entity', 'delete_entity'])
Recebe como argumento, codenames de permissões no padrão gerado pelo Framework Django para cada uma das entidades do projeto, e verifica se o parâmetro permissions possui todas

@has_any_permission(['add_entity', 'view_entity', 'change_entity', 'delete_entity'])
Recebe como argumento, codenames de permissões no padrão gerado pelo Framework Django para cada uma das entidades do projeto, e verifica se o parâmetro permissions possui ao menos uma
