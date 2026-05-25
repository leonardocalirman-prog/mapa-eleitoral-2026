# Como publicar no GitHub

## 1. Criar o repositório

No GitHub, crie um novo repositório chamado:

```text
mapa-eleitoral-2026
```

Descrição sugerida:

```text
Mapa interativo de nowcasting eleitoral por UF para o Brasil, com swing nacional parametrizável e metodologia transparente.
```

## 2. Subir o projeto pelo terminal

Dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "Initial version of electoral nowcasting map"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/mapa-eleitoral-2026.git
git push -u origin main
```

## 3. Ativar GitHub Pages

No repositório:

```text
Settings > Pages > Build and deployment > Deploy from a branch
```

Selecione:

```text
Branch: main
Folder: /docs
```

Depois disso, o mapa ficará disponível em uma URL parecida com:

```text
https://SEU-USUARIO.github.io/mapa-eleitoral-2026/
```

## 4. Antes de postar no LinkedIn

Troque no post:

```text
[INSERIR LINK]
```

pelo link do GitHub ou pelo link do GitHub Pages.
