# Mapa Eleitoral 2026: Nowcasting por UF

Um experimento de nowcasting eleitoral para o Brasil. O projeto transforma resultados estaduais de 2022 em um mapa interativo que permite simular swings nacionais e ajustes locais por UF.

> Este é um exercício analítico de portfólio. Não é previsão eleitoral. O objetivo é organizar sinais disponíveis em uma leitura visual de risco político, com metodologia simples, transparente e replicável.

## O que o projeto faz

O mapa classifica cada estado em cinco categorias, de acordo com a margem estimada entre esquerda e direita.

| Cor | Categoria | Critério |
|---|---|---|
| Vermelho escuro | Sólido esquerda | Margem estimada > +20 pp |
| Vermelho claro | Provável esquerda | +5 a +20 pp |
| Cinza | Competitivo | entre -5 e +5 pp |
| Azul claro | Provável direita | -5 a -20 pp |
| Azul escuro | Sólido direita | < -20 pp |

Convenção usada na V1: margem positiva favorece Lula/esquerda. Margem negativa favorece Bolsonaro/direita.

## Metodologia

A V1 usa uma regra de swing uniforme com possibilidade de ajuste estadual:

```text
margem_estimada(UF) = margem_2022(UF) + swing_nacional + ajuste_estadual(UF)
```

Onde:

* `margem_2022`: diferença entre Lula% e Bolsonaro% no primeiro turno de 2022, por UF.
* `swing_nacional`: deslocamento uniforme aplicado a todas as UFs, em pontos percentuais.
* `ajuste_estadual`: correção local opcional, útil quando houver pesquisa estadual ou julgamento específico sobre a UF.

Exemplo: se uma UF teve Lula +10 pp em 2022, um swing nacional de -5 pp e ajuste local de +2 pp, a margem estimada fica em +7 pp.

## O que a V1 ainda não faz

* Não modela segundo turno.
* Não incorpora pesquisas estaduais automaticamente.
* Não pesa pesquisas por recência, instituto ou tamanho amostral.
* Não estima intervalos de confiança.
* Não estima turnout, migração de votos entre candidatos ou voto útil.

Esses pontos entram naturalmente em versões futuras.

## Como rodar

```bash
git clone https://github.com/SEU-USUARIO/mapa-eleitoral-2026.git
cd mapa-eleitoral-2026
pip install -r requirements.txt
python main.py
```

### Com swing nacional customizado

```bash
python main.py --swing -8
```

### Com ajustes estaduais específicos

```bash
python main.py --swing -5 --ajustes "SP=-3,MG=2,BA=1"
```

### Imprimindo a tabela no terminal

```bash
python main.py --swing -5 --tabela --no-open
```

## Exemplo de output

```text
── Mapa Eleitoral 2026 ──────────────────
  Swing nacional : -5.0 pp

  Prováveis esquerda : 14 UFs  (sólido: 10, provável: 4)
  Competitivos       :  3 UFs
  Prováveis direita  : 10 UFs  (provável: 3, sólido: 7)

Mapa exportado: output/mapa_eleitoral.html
```

## Estrutura

```text
mapa-eleitoral-2026/
├── main.py
├── requirements.txt
├── data/
│   ├── resultados_2022.py
│   └── br_states.geojson
├── src/
│   ├── modelo.py
│   └── mapa.py
├── docs/
│   └── index.html
└── output/
    └── mapa_eleitoral.html
```

## Fontes de dados

| Dado | Fonte |
|---|---|
| Resultados eleitorais de 2022 | TSE, Portal de Dados Abertos, dataset Resultados 2022 |
| Malha estadual | IBGE, API de malhas geográficas |

A base eleitoral usada nesta V1 foi consolidada por UF a partir dos resultados oficiais do primeiro turno presidencial de 2022.

## Roadmap

### V1

* Resultado presidencial de 2022 por UF.
* Swing nacional parametrizável.
* Ajustes estaduais opcionais.
* Mapa interativo em HTML com Plotly.
* Tooltip por estado com margem de 2022, swing, ajuste local e margem estimada.

### V2

* Ingestão de pesquisas estaduais registradas.
* Peso por recência e qualidade da fonte.
* Bandas de incerteza por UF.
* Comparação visual entre 2022 e cenário estimado.

### V3

* Dashboard em Streamlit ou Dash.
* Atualização automatizada via GitHub Actions.
* Camada macro para conectar cenário eleitoral com câmbio, juros, risco fiscal e rotação setorial.

## Contexto macro

Eleições presidenciais afetam variáveis relevantes para o mercado: prêmio de risco fiscal, câmbio, curva de juros e percepção de estabilidade institucional. Este mapa funciona como uma camada visual para acompanhar assimetrias regionais e simular cenários políticos de maneira transparente.

## Autor

Leonardo Wandersman, economista.

