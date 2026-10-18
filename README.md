# chimera-skills

Catálogo curado de skills (formato `SKILL.md`) para o [Chimera](https://github.com/brcampidelli/chimera-agent)
e para qualquer agente que leia o padrão aberto de skills. *English below.*

## O que tem aqui

34 skills: **15 escritas por nós** (Apache-2.0) e **19 cópias de terceiros** com licença permissiva,
cada uma com o próprio LICENSE, fixada num commit e revisada.

| Área | Skills |
|---|---|
| Bancos de dados e segurança | `supabase`, `supabase-postgres-best-practices`, `supabase-rls-audit`*, `lgpd-checklist`*, `security-threat-model`, `security-best-practices` |
| Sites e código | `nextjs-app-router`*, `mobile-native`, `frontend-design`, `codebase-design`, `improve-codebase-architecture` |
| Testes e revisão | `systematic-debugging`, `verification-before-completion`, `break-ui`, `code-review`, `gh-fix-ci` |
| Pagamentos e finanças | `stripe-best-practices`, `pix-e-nfe`*, `trading-risk-rules`* |
| Mensagens e marketing | `whatsapp-cloud-api`*, `meta-ads-basics`*, `resend`, `email-best-practices` |
| Documentos e escrita | `redacao-pt-br`*, `docx-builder`*, `xlsx-builder`*, `pptx-builder`*, `pdf` |
| Educação | `banco-de-questoes-fsrs`* |
| Agentes e infraestrutura | `eval-design`*, `chimera-skill-authoring`*, `mcp-builder`, `vercel-deploy-seguro`* |
| Produto | `grill-me` |

\* escrita por nós.

## Regras do catálogo

- **Licença lida no arquivo**, nunca no README. Aceitas: MIT, Apache-2.0, BSD-2/3-Clause, ISC, MPL-2.0, CC0-1.0.
- **Fonte fixada** por commit em [`upstream.lock`](upstream.lock), com o hash de cada arquivo copiado.
- **Só texto.** Nenhuma skill traz script executável; exemplos de código ficam no markdown.
- **Revisão por item** em [`reviews/`](reviews/), com o hash exato do conteúdo revisado.
- **Checagem de segurança** automática: instalação por pipe para shell, instalação global sem versão,
  privilégio de administrador, frases dirigidas ao agente ou ao revisor, gatilhos que tentam valer
  para todo turno.
- **Sem número inventado:** popularidade só como estrelas do GitHub com a data da leitura; nenhuma
  contagem de instalação.
- **Curadoria não é aprovação.** O Chimera importa toda skill daqui como **pendente e não confiável**;
  quem liga é você.

Categorias: as 26 de [`categories.yaml`](categories.yaml), compartilhadas com `chimera-plugins` e
`chimera-connectors`. Metadados de vitrine em [`catalog/`](catalog/).

## Validar

```bash
pip install "pyyaml==6.0.3" "chimera-agent==0.68.1"
python scripts/check.py --require-chimera
```

Para contribuir, leia [CONTRIBUTING.md](CONTRIBUTING.md). Atribuições em [NOTICE](NOTICE).

---

## English

A curated catalogue of `SKILL.md` skills for [Chimera](https://github.com/brcampidelli/chimera-agent)
and any agent that reads the open skills format: 15 original skills (Apache-2.0, several focused on
Brazil: Portuguese writing, LGPD, Pix and tax invoices, WhatsApp Cloud API) and 19 permissively
licensed third-party skills, each with its own licence file, pinned to a commit and reviewed.

Rules: licences are read from the licence file; sources are pinned in `upstream.lock` with a hash per
copied file; skills ship text only, no executables; every item has a review recording the exact
content hash; CI scans for pipe-to-shell installs, unpinned global installs, privilege escalation,
reader-directed instructions and triggers that try to own every turn; popularity is GitHub stars with
the read date, never install counts. Curation is not approval: Chimera imports every skill from here
pending and untrusted.

Run `python scripts/check.py --require-chimera` to validate. See CONTRIBUTING.md and NOTICE.

## License

Original content: Apache-2.0 (see [LICENSE](LICENSE)). Third-party skills: the licence in each
skill's folder, summarised in [NOTICE](NOTICE).
