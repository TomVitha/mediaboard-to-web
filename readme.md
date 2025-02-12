
# Mediaboard to Web


Tento script přebírá HTML export z Mediaboard a generuje HTML řádky do tabulky pro web.

## Požadavky


### Python

Lze stáhnout z  [oficiálních stránek](https://www.python.org/downloads/windows/), z [Microsoft Store](https://apps.microsoft.com/detail/9pnrbtzxmb4z) nebo přes příkaz winget:
    
```cmd
winget install -i -e --id Python.Python.3.13
```

Ve všech případech je doporučeno si přidat Python do PATH. Společně s tím se nám také nainstaluje `pip`.


### Python balíky:

Script pracuje s Python balíky, které je potřeba nainstalovat následujícími příkazy:

```sh
pip install beautifulsoup4
```
```sh
pip install jinja2
```

## Používání

### Vytvoření vstupního souboru

1) V Mediaboard vyber všechny požadované články, 

2) Klikni "Stáhnout" a změň "Formát souboru" na HTML. Všechny ostatní možnosti exportu ponechat beze změny. 

3) Klikni "Stánout".

### Spuštění skriptu

1. **Konzole:**
   - Skript spusť pomocí `script.py` nebo `run.bat`.
   - Do okna konzole přetáhni vstupní soubor, nebo zadej cestu k němu.

2. **Správce souborů:**
   - Vstupní soubor přetáhněte na skript ve správci souborů.

### Výstup

Výstupní soubor se vygeneruje ve stejném umístění, kde se nachází vstupní soubor a rovnou se otevře ve VS Code.