# Fluxos de deploy na Vercel

Confira as flags na ajuda da versão fixada (`npx vercel --help`); a CLI muda entre versões.

## Variáveis de ambiente

- Defina pelo painel ou por `npx vercel env add NOME preview|production` (o valor é digitado pelo dono,
  não pelo agente).
- Puxe para desenvolvimento local com `npx vercel env pull .env.local`; `.env*.local` fica no `.gitignore`.
- Variável usada no build do Next.js exige **novo build** depois de mudar.

## GitHub Actions (quando o build é na sua CI)

```yaml
name: deploy-preview
on:
  pull_request:
permissions:
  contents: read
jobs:
  preview:
    runs-on: ubuntu-latest
    # Segredos não chegam a PRs de forks; prefira a integração Git da Vercel para PRs externos.
    if: github.event.pull_request.head.repo.full_name == github.repository
    env:
      VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
      VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
      VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
    steps:
      - uses: actions/checkout@<sha-de-40-caracteres>   # fixe por SHA, não por tag
      - uses: actions/setup-node@<sha-de-40-caracteres>
        with: { node-version-file: .nvmrc }
      - run: npm ci
      - run: npx vercel pull --yes --environment=preview
      - run: npx vercel build
      - run: npx vercel deploy --prebuilt
```

Produção em workflow separado, disparado manualmente (`workflow_dispatch`) ou por push na branch de
produção, com ambiente protegido (aprovação obrigatória no GitHub Environments). Nunca use
`pull_request_target` para isso.

## Rollback

1. Liste os deploys: `npx vercel ls` (ou painel → Deployments).
2. Volte para o último deploy bom: `npx vercel rollback <url-ou-id>` ou "Promote" no painel.
3. Rollback de código não desfaz migração de banco: confira compatibilidade antes.
4. Registre o motivo e abra tarefa para a correção.

## O que nunca fazer

- Empacotar o projeto e enviar por HTTP para um domínio que não seja da própria Vercel.
- Usar um token de outra pessoa ou de um serviço "grátis, sem login".
- Publicar em produção sem preview e sem aprovação.
- Commitar `.vercel/` com IDs junto de segredos, ou `.env` com valores reais.
