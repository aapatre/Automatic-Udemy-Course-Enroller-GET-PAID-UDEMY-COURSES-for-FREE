Requisitos
- Python 3.9–3.12
- Windows PowerShell (ou Bash em Linux/macOS)

Instalação (Windows)
1. Abra PowerShell no diretório do projeto
2. Crie/ative venv e instale dependências:
   - `.\scripts\setup.ps1`
3. (Opcional) Instale ferramentas de dev:
   - `pip install -r requirements-dev.txt`

Instalação (Linux/macOS)
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -e .`
4. (Opcional) `pip install -r requirements-dev.txt`

Build do pacote
- Windows: `.\scripts\build.ps1`
- Linux/macOS: `python -m build`

Resolução de problemas
- Se `udemy_enroller` não for reconhecido, use `python -m udemy_enroller.cli`
- Se o Chrome não abrir, verifique instalação local do navegador
- Logs: `~/.udemy_enroller/app.log`
