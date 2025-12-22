Ambientes

Desenvolvimento
- `.\scripts\setup.ps1` para preparar venv
- Execução local com `scripts/run-ui.ps1` ou `scripts/run-rest.ps1`

Teste
- `pytest` (Windows: `.\scripts\test.ps1`)
- Métricas fuzz: ver `fuzz_summary` em logs

Produção
- Instalação via `pip install .` ou artefato `wheel` (ver `scripts/build.ps1`)
- Use REST por padrão; UI requer navegador instalado

Variáveis de Ambiente
- `UDEMY_EMAIL`, `UDEMY_PASSWORD`: login automatizado em CI
- `CI_TEST`: se `True`, fluxo CI com encerramento precoce após tentativa
