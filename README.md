# FS_auth_middleware

Pacote Python para autenticação JWT e permissões reutilizáveis com Django Rest Framework.

## Instalação

```bash
pip install git+https://github.com/Cassio-de-Paula/FS_auth_middleware.git@{VERSION}
```

No `requirements.txt`:

```
git+https://github.com/Cassio-de-Paula/FS_auth_middleware.git@{VERSION}#egg=fs-auth-middleware
```

Este middleware foi desenvolvido para intergar de forma eficiente e segura, diversos projetos django, vinculados a um sistema base que fornece a autenticação de usuários, utilizando o sistema de grupos e permissões nativo do Framework Django.

## Configuração

### Configurações no `settings.py`

As variáveis abaixo devem ser adicionadas ao `settings.py` do projeto Django:

- `FS_AUTH_SYSTEM_MODEL`: caminho do model de sistema (ex.: `systems.System`).
- `FS_AUTH_ACCESS_TOKEN`: nome do cookie que armazena o token JWT de autenticação.
- `FS_AUTH_REFRESH_TOKEN`: nome do cookie que armazena o token JWT de refresh.

Exemplo:

```python
FS_AUTH_SYSTEM_MODEL = "systems.System"
FS_AUTH_ACCESS_TOKEN = "access_token"
FS_AUTH_REFRESH_TOKEN = "refresh_token"
```

### Requisitos do System model

O model configurado em `FS_AUTH_SYSTEM_MODEL` precisa ser compatível com os seguintes campos:

- `id`, `name`, `system_url`, `is_active`, `api_key`, `current_state`, `secret_key`, `dev_team`.

## Uso

`@has_permissions()` recebe uma lista de permissões, extrai o cookie configurado em `FS_AUTH_ACCESS_TOKEN` recebido na request, decodifica com a `SECRET_KEY` do projeto, verifica se as permissões obtidas do token incluem as permissões recebidas como argumento. O middleware valida também se o usuário está ativo no banco de dados através do atributo `is_active (boolean)`, e caso não esteja, remove os cookies configurados em `FS_AUTH_ACCESS_TOKEN` e `FS_AUTH_REFRESH_TOKEN` do cliente, impedindo-o de autenticar-se novamente até que sua conta seja reativada.

Ex:
@has_permissions(['add_model', 'view_model', 'change_model', 'delete_model'])
