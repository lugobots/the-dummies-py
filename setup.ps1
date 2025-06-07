# setup.ps1

if (-not (Get-Command python.exe -ErrorAction SilentlyContinue)) {
    Write-Error "Python nao encontrado. Instale o Python 3.9 e garanta que python.exe esteja no PATH."
    exit 1
}

$venvDir = "venv"
if (-not (Test-Path $venvDir)) {
    Write-Host "Criando virtualenv em .\$venvDir ..."
    python.exe -m venv $venvDir
} else {
    Write-Host "Virtualenv ja existe em .\$venvDir"
}

Write-Host "Ativando virtualenv..."
& "$venvDir\Scripts\Activate.ps1"

Write-Host "Atualizando pip e instalando dependencias..."
& "$venvDir\Scripts\python.exe" -m pip install --upgrade pip
& "$venvDir\Scripts\python.exe" -m pip install -r requirements.txt

$resp = Read-Host "Deseja fazer pull das imagens Docker recomendadas? [S/n]"
if ($resp -match "^[sS]") {
    Write-Host "Fazendo pull das imagens Docker necessarias..."
    docker pull lugobots/server
    docker pull lugobots/the-dummies-go:latest
    docker pull python:3.9-slim-buster
    Write-Host "Pull concluido."
} else {
    Write-Host "Pulando pull das imagens Docker."
}

Write-Host "================================================================="
Write-Host " Ambiente configurado com sucesso! "
Write-Host " Para abrir em outra sessao, use: .\\venv\\Scripts\\Activate.ps1"
Write-Host "================================================================="
