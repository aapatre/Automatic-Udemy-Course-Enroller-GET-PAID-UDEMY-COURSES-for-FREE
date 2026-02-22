Modos de execução
- REST (sem navegador):
  - `udemy_enroller`
  - `python -m udemy_enroller.cli`
- UI (com navegador via Selenium):
  - `udemy_enroller --browser chrome`
  - `python -m udemy_enroller.cli --browser chrome`

Flags principais
- `--idownloadcoupon --freebiesglobal --tutorialbar --discudemy --coursevania`
- `--max-pages N`
- `--experimental-fuzz --fuzz-seed 123 --max-concurrency 10`
- `--delete-settings --delete-cookie`
- `--debug`

Ambiente CI/headless
- Defina `UDEMY_EMAIL` e `UDEMY_PASSWORD`
- UI headless: `--browser chrome` e `CI_TEST=True`

Logs
- Em tempo real no terminal (stream)
- Arquivo: `~/.udemy_enroller/app.log`
