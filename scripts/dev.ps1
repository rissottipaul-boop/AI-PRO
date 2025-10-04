param(
    [switch]$Install,
    [switch]$Lint,
    [switch]$Test,
    [switch]$All
)

if ($Install) {
    python -m pip install --upgrade pip
    pip install .[dev]
}

if ($Lint) {
    ruff check .
    ruff format --check .
    mypy src/autonomous_dev
}

if ($Test) {
    pytest -q
}

if ($All) {
    ruff check .; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    ruff format --check .; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    mypy src/autonomous_dev; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    pytest -q
}
