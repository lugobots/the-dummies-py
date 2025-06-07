#!/usr/bin/env bash
set -e

# 1) Verifica se existe python3 no PATH
if ! command -v python3 &> /dev/null; then
  echo "Python não encontrado. Instale o Python ≥ 3.9 e garanta que 'python3' esteja no PATH."
  exit 1
fi

# 2) Verifica versão mínima (3.9)
MIN_VERSION="3.9"
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(printf '%s\n%s' "$MIN_VERSION" "$PY_VER" | sort -V | head -n1) != "$MIN_VERSION" ]]; then
  echo "Versão do Python é $PY_VER; é necessário Python ≥ $MIN_VERSION."
  exit 1
fi

VENV_DIR="venv"

# 3) Cria virtualenv se não existir
if [[ ! -d "$VENV_DIR" ]]; then
  echo "Criando virtualenv em ./$VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
else
  echo "Virtualenv já existe em ./$VENV_DIR"
fi

# 4) Ativa a virtualenv
echo "Ativando virtualenv..."
source "$VENV_DIR/bin/activate"

# 5) Atualiza pip e instala dependências
echo "Atualizando pip e instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# 6) Pull das imagens Docker (opcional)
read -rp "Deseja fazer pull das imagens Docker recomendadas? [S/n] " RESP
if [[ "$RESP" =~ ^[sS] ]]; then
  echo "Fazendo pull das imagens Docker necessárias..."
  docker pull lugobots/server
  docker pull lugobots/the-dummies-go:latest
  docker pull python:3.9-slim-buster
  echo "Pull concluído."
else
  echo "Pulando pull das imagens Docker."
fi

cat <<EOF

=================================================================
  Ambiente configurado com sucesso!
  Para ativar em outra sessão, use:
    source ./$VENV_DIR/bin/activate
=================================================================

EOF
