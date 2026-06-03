# Nowcast Eleitoral 2026 — Metodologia

*Documento técnico-metodológico do projeto `mapa-eleitoral-2026`.*
*Autor: Leonardo Wandersman. Versão 0.2 — Maio/2026.*

---

## Sumário executivo

O Nowcast Eleitoral 2026 é um exercício de risco político por unidade da federação, construído sobre três pilares: (i) o resultado do primeiro turno presidencial de 2022 como linha de base; (ii) uma hipótese de *swing* — nacional uniforme ou regional observado — calibrada pelo backtest e por pesquisas agregadas; (iii) ajustes regionais e estaduais calibráveis pelo usuário. O dashboard interativo permite simular cenários e observar como a recomposição das margens muda a classificação das UFs em cinco categorias (sólido esquerda, provável esquerda, competitivo, provável direita, sólido direita).

A validação do modelo é feita por um *backtest 2018 → 2022* com duas premissas alternativas. Premissa A — swing nacional uniforme — produz **MAE de 10,0 pontos percentuais**. Premissa B — swing por região observado — reduz o erro para **MAE 6,9 pp (−31%)**. O ganho prova empiricamente que a heterogeneidade regional é informação real, não ruído. O dashboard oferece um toggle que aplica essa heterogeneidade como baseline.

A calibração contemporânea usa pesquisas presidenciais maio/2026 de 12 institutos (Datafolha, Quaest/Genial, AtlasIntel, PoderData, Indexa, Vox, Verità, etc). A leitura metodologicamente compatível com a margem de 2022 (Lula vs Bolsonaro direto) é **Lula vs Flávio direto**, dando mediana **+7,1 pp** e swing implícito **+1,9 pp vs 2022** — quase idêntico ao quadro base de 2022. Os terceiros (Caiado, Zema, Renan) ficam no "outros" e são redistribuídos no 2º turno via parâmetro.

O projeto é open-source, escrito em Python e Observable JavaScript, renderizado via Quarto Dashboard, publicado em GitHub Pages, e atualizável com pesquisas agregadas via edição de um arquivo JSON simples.

---

## 1. Objetivo

Construir uma camada visual de **acompanhamento de risco político eleitoral** em granularidade estadual, com três propriedades:

1. **Transparência metodológica:** toda decisão de modelagem é explícita e auditável.
2. **Reatividade:** o usuário pode simular cenários movendo parâmetros e observar o resultado em tempo real.
3. **Honestidade sobre incerteza:** o backtest mostra o erro real da abordagem, sem mascarar limitações.

O público-alvo são profissionais de mercado financeiro (renda fixa, câmbio, equities, macro) que precisam mapear assimetrias regionais e calibrar prêmios de risco político em ativos brasileiros.

---

## 2. Arquitetura

O projeto separa três camadas:

**Camada de dados** (`data/`): fontes oficiais e dados intermediários em formato consumível.
- `resultados_2022.py` — TSE 1º turno, margem Lula − Bolsonaro por UF.
- `resultados_2018.py` — TSE 1º turno, margem Haddad − Bolsonaro por UF.
- `pesquisas_manual.json` — agregador manual de pesquisas presidenciais (Datafolha, Quaest, Atlas, etc).
- `br_states.geojson` — malha estadual do IBGE.
- `resultados_2022.json`, `backtest_2018_2022.json`, `pesquisas_mediana.json` — JSONs derivados consumidos pelo dashboard.

**Camada de transformação** (`src/`): lógica de modelo e ETL em Python.
- `modelo.py` — fórmula central de classificação por margem.
- `mapa.py` — geração estática do choropleth (Plotly).
- `backtest.py` — validação 2018 → 2022.
- `pesquisas.py` — scraper (deprecated em favor de input manual; preservado pra trabalho futuro).

**Camada de apresentação** (`index.qmd` + `_quarto.yml`): dashboard interativo em Quarto + Observable JS. Renderização estática publicada via GitHub Actions no GitHub Pages.

Um único ponto de entrada (`prep_data.py`) regenera todos os JSONs intermediários a partir das fontes em `data/`.

---

## 3. Modelo

### 3.1. Premissa central

A hipótese fundamental é o **swing nacional uniforme**: a variação na margem entre dois pleitos consecutivos se distribui de forma homogênea pelas unidades federativas. Formalmente, se `m_uf(t)` denota a margem (em pontos percentuais) da esquerda sobre a direita em uma UF em determinado pleito,

> `m_uf(t+1) = m_uf(t) + Δ_nacional`

onde `Δ_nacional` é o swing nacional observado ou hipotetizado.

A premissa é uma simplificação herdada da literatura britânica de análise eleitoral (Butler-Stokes, 1969) e tem como contraponto principal a abordagem de *uniform partisan swing* aplicada distrito a distrito. Vantagem: parametrização com um único número. Limitação: ignora heterogeneidade estrutural entre regiões.

### 3.2. Notação

Para cada UF `i`, denotamos:

- `m^{2022}_i` — margem real Lula − Bolsonaro em 2022, em pontos percentuais. Exemplo: `m^{2022}_BA = +56`, `m^{2022}_SP = −12`.
- `l^{2022}_i`, `b^{2022}_i` — percentuais Lula e Bolsonaro em 2022. Exemplo: `l^{2022}_BA = 73%`, `b^{2022}_BA = 17%`.
- `o_i = 100 − l^{2022}_i − b^{2022}_i` — eleitorado em terceira via, brancos e nulos em 2022 (mantido constante na simulação).
- `v_i` — votos válidos em 2022 (peso de cada UF na agregação nacional). Exemplo: `v_SP ≈ 22,4 milhões`.
- `s` — swing nacional, parâmetro do modelo.
- `a^R_i` — ajuste regional aplicado a cada UF segundo sua macrorregião (Norte, Nordeste, Centro-Oeste, Sudeste, Sul).
- `m̂_i` — margem estimada para 2026 na UF `i`.

### 3.3. Equação central

> `m̂_i = m^{2022}_i + s + a^R_i`

Exemplo numérico, São Paulo com `s = −3` e `a^SE = +1`:
`m̂_SP = −12 + (−3) + 1 = −14 pp`

### 3.4. Classificação por faixa

A margem estimada é mapeada em cinco classes via limiares fixos:

| Faixa de `m̂_i` | Classe |
|---|---|
| `> +20` | Sólido esquerda |
| `+5` a `+20` | Provável esquerda |
| `−5` a `+5` | Competitivo |
| `−20` a `−5` | Provável direita |
| `< −20` | Sólido direita |

Os limiares são convencionais e podem ser parametrizados; valores escolhidos refletem o uso comum em análise eleitoral norte-americana (Cook PVI usa janelas similares).

---

## 4. Agregação nacional e projeção de 2º turno

### 4.1. Primeiro turno nacional ponderado

Dada uma margem estimada por UF, recuperamos os percentuais individuais de Lula e Bolsonaro mantendo a participação de "outros" constante em relação a 2022:

> `l̂_i = (100 − o_i + m̂_i) / 2`
> `b̂_i = (100 − o_i − m̂_i) / 2`

A intuição é: o eleitorado "Outros" `o_i` em uma UF segue o mesmo que em 2022, e o restante (`100 − o_i`) se divide entre os dois polos de forma que `l̂_i − b̂_i = m̂_i`. A agregação nacional é uma média ponderada pelo eleitorado:

> `L̂_nac = (Σ_i l̂_i · v_i) / Σ_i v_i`
> `B̂_nac = (Σ_i b̂_i · v_i) / Σ_i v_i`
> `M̂_nac = L̂_nac − B̂_nac`

No caso default (`s = 0`, todos os `a^R_i = 0`), o modelo reproduz `M̂_nac ≈ +5,3 pp`, próximo da margem real de 2022 de `+5,2 pp`. A pequena divergência vem do arredondamento das margens por UF para inteiros.

### 4.2. Segundo turno

A projeção de segundo turno parte do primeiro turno simulado e redistribui o eleitorado "Outros" entre os dois finalistas segundo um único parâmetro `f` (slider `% Outros → Esquerda (2T)`, default `0,60`):

> `e^{2T}_i = l̂_i + f · o_i`
> `d^{2T}_i = b̂_i + (1 − f) · o_i`

Agregando nacionalmente e calculando `Ê^{2T} − D̂^{2T}` obtemos a margem do segundo turno. A premissa de divisão constante é grosseira — na prática, a redistribuição varia por UF e por candidato terceiro. É um placeholder calibrável.

---

## 5. Decomposição regional

Para cada uma das cinco macrorregiões `R` (Norte, Nordeste, Centro-Oeste, Sudeste, Sul), calculamos:

> `peso_R = Σ_{i ∈ R} v_i`
> `m̂_R = (Σ_{i ∈ R} m̂_i · v_i) / peso_R`
> `c_R = m̂_R · (peso_R / Σ_i v_i)`

`c_R` é a *contribuição em pontos percentuais da região R para a margem nacional*. Por construção, `Σ_R c_R = M̂_nac`. O dashboard exibe essa decomposição como barras horizontais — visualização que isola onde está concentrada a vantagem (ou desvantagem) de cada bloco no cenário simulado.

---

## 6. Calibração: pesquisas e ajustes

### 6.1. Swing implícito das pesquisas

Pesquisas presidenciais agregadas fornecem uma estimativa contemporânea da margem nacional. Definimos:

> `Δ_pesquisas = M_pesquisas − m^{2022}_nac`

Quando o usuário ativa o toggle "Usar swing das pesquisas", o modelo substitui `s` por `Δ_pesquisas`. O insumo `M_pesquisas` é a mediana das margens das pesquisas no recorte temporal padrão de 30 dias, lida do arquivo `pesquisas_manual.json`.

**Escolha metodológica — Leitura A vs Leitura B.** Há duas formas defensáveis de calcular a margem em cada pesquisa:

- **Leitura A — Lula vs candidato principal direita (Flávio Bolsonaro).** Mantém comparabilidade com a margem 2022 do modelo (que é Lula 48,4 − Bolsonaro 43,2 = +5,2 pp, sem somar Tebet/Ciro). Os terceiros (Caiado, Zema, Renan, Marçal) ficam no "outros" (~25% das pesquisas atuais) e são redistribuídos via slider `migOutros` no cálculo do 2º turno.

- **Leitura B — Soma bloco esquerda vs soma bloco direita.** Captura o cenário de unificação da direita no 2T. Resultado: mediana negativa (−5,5 pp), porque a direita fragmentada soma mais que Lula. Mas se aplicada como swing 1T e combinada com `migOutros` no 2T, gera **dupla contagem dos terceiros** — eles entram no swing e são redistribuídos de novo.

**Adotamos Leitura A** por consistência interna do modelo. A unificação da direita emerge da combinação `swing implícito + migOutros baixo` (terceiros migrando majoritariamente para a direita no 2T).

Mediana atual (maio/2026, 12 institutos): **M_pesquisas = +7,1 pp**, swing implícito **+1,9 pp**.

A mediana é preferida à média por robustez a outliers.

### 6.2. Ajustes regionais

Os sliders por região permitem ao usuário incorporar informação local não capturada pelo swing nacional — tipicamente, pesquisas estaduais e regionais específicas. O ajuste `a^R_i` se aplica a todas as UFs da região `R`, e se acumula linearmente sobre o swing nacional.

Importante: os ajustes regionais não pretendem ser um modelo causal de variação política regional. São um parâmetro de calibração que reflete a *crença subjetiva do analista* sobre dinâmicas locais.

---

## 7. Backtest 2018 → 2022

### 7.1. Setup

Aplicamos a equação central usando 2018 como linha de base, com duas premissas alternativas para o swing:

**Modelo A — Swing nacional uniforme:**
> `m̂^{A}_i = m^{2018}_i + Δ^{obs}_nac`,&nbsp; `Δ^{obs}_nac = +21,9 pp`

**Modelo B — Swing regional observado** (ponderado por votos válidos):
> `m̂^{B}_i = m^{2018}_i + Δ^{obs}_R(i)`

onde `Δ^{obs}_R` é o swing observado da macrorregião R entre 2018 e 2022:

| Região | Margem 2018 (pp) | Margem 2022 (pp) | Swing observado | Desvio vs nacional |
|---|---|---|---|---|
| Norte | −18,5 | +13,7 | **+32,2** | +10,3 |
| Nordeste | +17,8 | +46,9 | **+29,1** | +7,2 |
| Sudeste | −32,6 | −6,6 | **+26,0** | +4,1 |
| Sul | −37,6 | −22,0 | **+15,6** | −6,3 |
| Centro-Oeste | −38,3 | −28,1 | **+10,3** | −11,6 |

Comparamos `m̂_i` com `m^{2022}_i` observado em cada modelo. Métricas de erro:

> `MAE = (1/N) · Σ_i |m^{2022}_i − m̂_i|`
> `RMSE = √[(1/N) · Σ_i (m^{2022}_i − m̂_i)²]`

### 7.2. Resultados

| Métrica | Modelo A (nacional) | Modelo B (regional) | Ganho de B |
|---|---|---|---|
| Erro médio absoluto (MAE) | **10,0 pp** | **6,9 pp** | **−3,1 pp (−31%)** |
| Raiz do erro quadrático médio (RMSE) | 11,9 pp | 9,4 pp | −2,5 pp |
| Erro máximo | 26,1 pp (Acre) | 24,2 pp (Roraima) | −1,9 pp |
| UFs com swing acima do nacional | 15 | — | — |
| UFs com swing abaixo do nacional | 12 | — | — |

Os cinco maiores erros absolutos do Modelo A (e como o Modelo B se sai):

| UF | 2018 | 2022 real | A est. | A erro | B est. | B erro |
|---|---|---|---|---|---|---|
| AC | −49 | −1 | −27,1 | +26,1 | −16,8 | **+15,8** |
| AM | −23 | +20 | −1,1 | +21,1 | +9,2 | **+10,8** |
| AP | −37 | +3 | −15,1 | +18,1 | −4,8 | **+7,8** |
| RJ | −39 | +1 | −17,1 | +18,1 | −13,0 | +14,0 |
| AL | −3 | +35 | +18,9 | +16,1 | +26,1 | **+8,9** |

### 7.3. Discussão

Três padrões emergem:

**(i) Norte virou pró-Lula muito além do nacional.** Acre, Amazonas, Amapá e Pará tiveram swings 12 a 26 pp superiores ao nacional. Hipóteses razoáveis: peso de transferências federais (Bolsa Família, Auxílio Brasil), efeito de candidatos locais aliados ao governo federal, dinâmicas evangélicas regionais menos densas que no Sudeste.

**(ii) Nordeste consolidou pra esquerda.** Estados que já haviam votado Lula em 2018 (BA, AL, MA, CE) ampliaram a margem em 2022. Padrão consistente com a teoria do "voto retrospectivo" (Fiorina, 1981): eleitores nordestinos recompensam o legado dos programas sociais petistas mesmo após anos fora do governo.

**(iii) Sudeste-Sul próximos da estimativa.** São Paulo (erro −1,9 pp) e Minas Gerais (+5,1 pp) ficaram bem ajustados pelo swing uniforme. A leitura é que essas regiões respondem aos vetores nacionais sem dinâmicas regionais fortes.

A implicação operacional é clara: usar swing nacional uniforme produz um *baseline honesto* mas insuficiente. Os sliders de ajuste regional do dashboard existem como ferramenta para o analista incorporar a heterogeneidade estrutural que o backtest revela.

---

## 8. Limitações

**Limitações de premissa do modelo:**

- Swing uniforme não captura swings regionais.
- A divisão constante de "outros" no 2T é heurística.
- Não há tratamento de incerteza (intervalos de confiança ausentes).
- O modelo é estático: não incorpora dinâmica temporal (efeito convenção, debates, eventos de cauda).

**Limitações dos dados:**

- Resultados 2018 estão aproximados a inteiros — refinar com dados do TSE em granularidade decimal.
- Pesquisas dependem de input manual semanal — automação via API de agregadores seria preferível.
- Eleitorado por UF está aproximado — usar TSE em vez de estimativas.

**Limitações analíticas:**

- O backtest 2018 → 2022 é apenas um ciclo. Validação robusta requer 2010 → 2014 e 2014 → 2018 também.
- O modelo é puramente reduzido — não há features explicativas (PIB per capita, transferências, demografia).
- A classificação em cinco faixas é convencional. Limiares alternativos mudariam interpretações.

---

## 9. Roadmap

**V2 (concluída):**
- [x] Dashboard interativo Quarto + Observable.
- [x] Backtest 2018 → 2022 com decomposição por UF.
- [x] **Modelo B (swing regional)** — MAE 6,9 pp, ganho de 31% sobre Modelo A.
- [x] Toggle "Aplicar heterogeneidade regional" no Simulador.
- [x] Projeção de 2º turno parametrizada (slider migOutros).
- [x] Decomposição regional da margem nacional.
- [x] Card de pesquisas alimentado por JSON manual (12 institutos, mediana +7,1 pp).
- [x] Convenção visual brasileira: vermelho = esquerda, azul = direita.
- [x] Publicação automatizada via GitHub Actions + Pages.

**V3 (próximos blocos):**
- [ ] Multi-backtest: incluir 2010 → 2014 e 2014 → 2018 para validar robustez do ganho de B.
- [ ] Bandas de incerteza por UF (bootstrap sobre erros do backtest).
- [ ] Cards de cenários pré-definidos (cenário base, downside, upside).
- [ ] Modelagem de migração 2T por UF (em vez de uniforme nacional).

**V4 (modelo sério):**
- [ ] Regressão de margem estimada como função de margem prévia + variação macroeconômica por UF (PIB, desemprego, transferências federais, programas sociais).
- [ ] Modelo bayesiano combinando prior do swing uniforme com likelihood de pesquisas estaduais.
- [ ] Camada de impacto macro: tradução de cenários eleitorais em prêmio de risco fiscal (CDS), curva de juros DI e câmbio.

---

## Apêndice A — Glossário de variáveis

| Nome no código | Notação | Tipo | Significado | Exemplo |
|---|---|---|---|---|
| `resultados[i].margem_2022` | `m^{2022}_i` | constante | Margem real Lula − Bolso por UF em 2022 (pp) | BA: +56, SP: −12 |
| `resultados[i].lula_2022` | `l^{2022}_i` | constante | % Lula por UF em 2022 | BA: 73, SP: 36 |
| `resultados[i].bolso_2022` | `b^{2022}_i` | constante | % Bolsonaro por UF em 2022 | BA: 17, SP: 48 |
| `resultados[i].votos_validos` | `v_i` | constante | Votos válidos por UF em 2022 (peso) | SP: 22,4 mi |
| `margem_2022_nacional` | `m^{2022}_nac` | constante | Margem nacional 1T 2022 | +5,2 pp |
| `swingNac` | `s` (slider) | parâmetro | Swing nacional do usuário | default: 0 |
| `usarPesquisa` | (toggle) | parâmetro | Substituir slider por swing das pesquisas | default: falso |
| `migOutros` | `f` (slider) | parâmetro | Fração dos "Outros" pra esquerda no 2T | default: 0,60 |
| `ajN, ajNE, ajCO, ajSE, ajS` | `a^R_i` | parâmetro | Ajuste extra por macrorregião | default: 0 cada |
| `swingEfetivo` | — | derivada | Swing efetivamente aplicado | calculada |
| `margens[i].margem_estimada` | `m̂_i` | derivada | Margem estimada por UF | calculada |
| `margens[i].classe` | — | derivada | Classe de competitividade (5 faixas) | "competitivo" |
| `counts` | — | derivada | Contagem de UFs por classe | `{solido_esq: 10, ...}` |
| `resumo_nacional.lula` | `L̂_nac` | derivada | % Lula nacional estimado | 46,2% |
| `resumo_nacional.margem_nacional` | `M̂_nac` | derivada | Margem nacional estimada | +5,3 pp |
| `projecao_2t.margem` | `M̂^{2T}` | derivada | Margem nacional do 2T | +7,9 pp |
| `decomposicao_regional[R].contribuicao_pp` | `c_R` | derivada | Contribuição da região para `M̂_nac` | varia |
| `pesquisas.margem` | `M_pesquisas` | externa | Mediana das pesquisas | varia |
| `backtest.mae_pp` | MAE | externa | Erro absoluto médio do backtest | 10,0 pp |

---

## Apêndice B — Fluxo de dados

```
                           ┌─────────────────────────┐
                           │  data/resultados_2022.py│
                           │  data/resultados_2018.py│
                           │  data/pesquisas_manual.json
                           └────────────┬────────────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │  prep_data.py    │
                              │  (orquestrador)  │
                              └────────┬─────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              ▼                        ▼                        ▼
   ┌──────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
   │ resultados_2022  │  │ backtest_2018_2022   │  │ pesquisas_mediana    │
   │      .json       │  │      .json           │  │      .json           │
   └────────┬─────────┘  └────────┬─────────────┘  └────────┬─────────────┘
            │                     │                         │
            └─────────────────────┼─────────────────────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │      index.qmd       │
                       │ (Quarto + ObservableJS)
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │   docs/  (HTML)      │
                       │   GitHub Pages       │
                       └──────────────────────┘
```

---

## Apêndice C — Reprodutibilidade

Para reproduzir o dashboard a partir de uma cópia limpa do repositório:

```
pip install -r requirements.txt
python prep_data.py          # regenera todos os JSONs
quarto preview               # subir dashboard local (com auto-reload)
quarto render                # render estático em docs/
```

Atualização semanal:
1. Editar `data/pesquisas_manual.json` adicionando pesquisas novas.
2. Rodar `python prep_data.py`.
3. Verificar localmente com `quarto preview`.
4. Commit + push. GitHub Actions republica em ~3 minutos.

---

## Referências

- Butler, D. & Stokes, D. (1969). *Political Change in Britain.*
- Fiorina, M. (1981). *Retrospective Voting in American National Elections.*
- Gelman, A. & Hill, J. (2007). *Data Analysis Using Regression and Multilevel/Hierarchical Models.*
- TSE — Repositório de dados eleitorais: https://dadosabertos.tse.jus.br/
- IBGE — API de malhas geográficas: https://servicodados.ibge.gov.br/api/v3/malhas/

---

*Este documento é versionado junto com o código. Última atualização: `git log -1 METODOLOGIA.md`.*
