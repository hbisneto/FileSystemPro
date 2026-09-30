# Resumo das funções

| # | Função | Retorno principal | Observação |
|---|--------|-------------------|------------|
| 1 | `get_raw_object` | dict com timestamps `float` e size `int` | Resolve a limitação documentada |
| 2 | `get_permissions` | `mode`, `octal`, `readable/writable/executable` | Usa `os.stat` + `os.access` |
| 3 | `get_owner` | `uid`, `gid`, `user`, `group` | `pwd`/`grp` no Unix; fallback limpo no Windows |
| 4 | `get_mime_type` | `str` ou `None` | `mimetypes` (stdlib) |
| 5 | `get_checksum` | hex digest | Qualquer algoritmo do `hashlib` (padrão sha256) |
| 6 | `is_empty` | `bool` | Arquivo 0 bytes **ou** diretório vazio |
| 7 | `get_link_target` | `str` | `os.readlink` |
| 8 | `get_age` | `seconds` + `human` ("3 days") | Referência `created` ou `modified` |
| 9 | `compare` | `identical` + `differences` | Útil para sync/auditoria |
| 10 | `get_objects` | dict `{path: metadata}` | Suporte a `parallel=True` com `ThreadPoolExecutor` |