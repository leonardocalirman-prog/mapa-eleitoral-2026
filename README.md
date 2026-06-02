# Mapa Eleitoral 2026 — Nowcasting por UF

Um experimento de nowcasting eleitoral para o Brasil, visualizando a temperatura política por estado com metodologia simples, transparente e replicável.

> **Aviso:** Este é um exercício analítico de portfólio. Não é uma previsão eleitoral — o objetivo é organizar sinais disponíveis em uma leitura visual de risco político, não cravar um resultado.

---

## O que é

Um mapa interativo do Brasil por UF que classifica cada estado em cinco categorias:

| Cor | Categoria | Critério |
|-----|-----------|----------|
| 🔵 Azul escuro | Sólido esquerda | Margem estimada > +20 pp |
| 🔵 Azul claro | Provável esquerda | +5 a +20 pp |
| ⚫ Cinza | Competitivo | ±5 pp |
| 🔴 Coral claro | Provável direita | -5 a -20 pp |
| 🔴 Coral escuro | Sólido direita | < -20 pp |

---

## Metodologia

### Fórmula V1

```
margem_estimada(UF) = margem_2022(UF) + swing_nacional + ajuste_estadual
```

- **margem_2022**: diferença Lula% − Bolsonaro% no 1º turno de 2022, por UF (fonte: TSE)
- **swing_nacional**: variação uniforme aplicada a todas as UFs, calibrável via parâmetro
- **ajuste_estadual**: correção local opcional, quando há pesquisas estaduais disponíveis

### O que o modelo não faz (ainda)

- Não modela o 2º turno
- Não pesa pesquisas por recência
- Não usa pesquisas estaduais individualmente
- Não estima bandas de incerteza

Essas são as evoluções naturais da V2 — veja o roadmap abaixo.

---

## Instalação

```bash
git clone https://github.com/leonardocalirman-prog/mapa-eleitoral-2026.git
cd mapa-eleitoral-2026
pip install -r requirements.txt
```

Para o **dashboard interativo** instale também o Quarto CLI:
https://quarto.org/docs/get-started/ (instalador nativo Windows/Mac/Linux).

---

## Uso

### Dashboard interativo (Quarto + Observable JS)

```bash
# Gera dados de apoio (JSON + GeoJSON)
python prep_data.py

# Renderiza o dashboard (saída em docs/)
quarto render

# Preview em modo dev (recarrega ao salvar)
quarto preview
```

O dashboard tem:
- Slider de **swing nacional**
- Sliders de **ajuste por região** (N, NE, CO, SE, S)
- Sliders por UF (em painel colapsável)
- Cards no header com totais por classificação
- Composição nacional simulada (% esquerda × % direita, ponderada por votos válidos)
- Mapa choropleth interativo
- Tabela ordenada por margem estimada

Default = resultado de 2022.

### CLI estático (script Python original)

```bash
# Gera mapa com swing padrão de -5pp e abre no browser
python main.py

# Swing customizado
python main.py --swing -8

# Com ajustes estaduais específicos (quando há pesquisas locais)
python main.py --swing -5 --ajustes "SP=-3,MG=2,BA=1"

# Imprime tabela de margens no terminal
python main.py --swing -5 --tabela --no-open
```

### Scraper de pesquisas (Wikipedia)

```bash
python -m src.pesquisas
```

Baixa a tabela de pesquisas presidenciais 2026 da Wikipedia, agrupa
candidatos por bloco (esquerda × direita), calcula mediana das últimas
30 dias e imprime no terminal.

### Exemplo de output no terminal

```
── Mapa Eleitoral 2026 ──────────────────
  Swing nacional : -5.0 pp

  Prováveis esquerda : 14 UFs  (sólido: 10, provável: 4)
  Competitivos       :  3 UFs
  Prováveis direita  : 10 UFs  (provável: 3, sólido: 7)

Mapa exportado: output/mapa_eleitoral.html
```

---

## Estrutura do projeto

```
mapa-eleitoral-2026/
├── index.qmd                  # Dashboard Quarto (output principal)
├── _quarto.yml                # Configuração do site Quarto
├── prep_data.py               # Gera JSON/GeoJSON consumidos pelo dashboard
├── main.py                    # CLI estática original
├── requirements.txt
├── data/
│   ├── resultados_2022.py     # Resultados TSE 2022 por UF (fonte de verdade)
│   ├── resultados_2022.json   # Gerado por prep_data.py (input do dashboard)
│   └── br_states.geojson      # Malha estadual IBGE (cacheado em disco)
├── src/
│   ├── modelo.py              # Lógica do nowcasting (CLI)
│   ├── mapa.py                # Choropleth Plotly (CLI)
│   └── pesquisas.py           # Scraper de pesquisas presidenciais
├── .github/workflows/
│   └── publish.yml            # Renderiza Quarto e publica no GitHub Pages
├── docs/                      # Saída do `quarto render` (servido pelo Pages)
└── output/
    └── mapa_eleitoral.html    # Saída do CLI estático
```

---

## Fontes de dados

| Dado | Fonte |
|------|-------|
| Resultados eleitorais 2022 | [TSE — Repositório de dados eleitorais](https://dadosabertos.tse.jus.br/) |
| Malha estadual | [IBGE API de malhas geográficas](https://servicodados.ibge.gov.br/api/v3/malhas/estados) |
| Pesquisas eleitorais | [TSE — Pesquisas eleitorais registradas](https://www.tse.jus.br/eleicoes/pesquisa-eleitoral-2) |

---

## Roadmap

### V1 (atual)
- [x] Resultado 2022 por UF
- [x] Swing nacional parametrizável
- [x] Mapa interativo HTML (Plotly)
- [x] Classificação em 5 categorias
- [x] Tooltip com detalhes por estado

### V2 (em curso)
- [x] Dashboard interativo (Quarto + Observable JS)
- [x] Sliders de swing nacional + ajuste por região + por UF
- [x] Composição nacional ponderada por votos válidos
- [x] Build automático via GitHub Actions
- [x] Scraper de pesquisas da Wikipedia
- [ ] Plugar mediana das pesquisas como swing sugerido no dashboard
- [ ] Bandas de incerteza por UF
- [ ] Cenários de 2º turno

### V3
- [ ] Leitura macro acoplada: câmbio, juros, CDS por cenário eleitoral
- [ ] Backtests com swing histórico (2018 → 2022)
- [ ] API pública dos dados normalizados

---

## Contexto macro

Eleições presidenciais afetam diretamente variáveis de mercado: nível da taxa neutra de juros, prêmio de risco fiscal (CDS), dinâmica do câmbio e rotação setorial de ativos. Este mapa funciona como camada visual para acompanhar assimetrias regionais e simular cenários de risco político — complementando análises de renda fixa e câmbio.

---

## Autor

**Leonardo Wandersman** · Economista
[GitHub](https://github.com/leonardocalirman-prog)

---

*Metodologia transparente, replicável e não-partidária.*  
*Contribuições e correções são bem-vindas via PR.*
