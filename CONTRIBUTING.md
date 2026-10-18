# Contribuindo / Contributing

## PT-BR

Toda skill entra por pull request e passa por `python scripts/check.py`. O CI roda o mesmo script com
o parser de skills do próprio Chimera.

### Skill própria (`mode: own`)

1. Crie `skills/<id>/SKILL.md` (veja a skill `chimera-skill-authoring`) e, se precisar,
   `skills/<id>/references/*.md`. Licença `Apache-2.0`. Sem arquivos executáveis.
2. Crie `catalog/<id>.json` (copie um existente; `source: null`).
3. Crie `reviews/<id>.md` com o checklist e o `Content sha256` de
   `python scripts/check.py --print-tree-hash skills/<id>`.

### Cópia de terceiro (`mode: include` ou `adapt`)

1. Licença lida **no arquivo** do repositório de origem, na pasta ou na raiz, e na lista aceita:
   MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, MPL-2.0, CC0-1.0. "MIT" só no README ou no
   frontmatter, sem arquivo, **não** conta.
2. Fixe o commit (sha de 40 caracteres). Copie o LICENSE de origem para a pasta da skill.
3. Copie só markdown. Deixe executáveis de fora e registre-os.
4. Reescreva só o frontmatter (`license` SPDX, `metadata`, `stage`, `topic`) e registre em
   `metadata.changes`. Mudou o corpo? `mode: adapt` e descreva cada mudança.
5. Atualize `upstream.lock` (hash de cada arquivo copiado), `NOTICE`, `catalog/<id>.json` (com
   estrelas e data da leitura) e `reviews/<id>.md`.

### Nunca entram

- ComposioHQ e VoltAgent/ClawHub, de nenhuma forma.
- As skills docx, pdf, pptx e xlsx da Anthropic (proprietárias) nem derivados delas.
- Conteúdo GPL/AGPL, sem licença, ou com termos de uso de fornecedor no lugar de licença.
- Instalação por pipe para shell, instalação global sem versão, pedido de privilégio de administrador,
  envio de código ou dados a terceiros, gatilho que tenta valer para todo turno, frase dirigida ao
  agente ou ao revisor.
- Contagem de instalações. Popularidade, quando houver, é só estrelas do GitHub com a data da leitura.

### Atualizar uma skill de terceiro

Novo sha → copiar de novo → rever o diff inteiro → atualizar lock, NOTICE, catálogo e revisão. O CI
recusa qualquer byte vendorizado que não bata com o `upstream.lock`, e qualquer revisão cujo hash não
bata com a pasta.

### Exceções de segurança

`security-exceptions.json` silencia um achado específico, com motivo verificável. Exceção que não casa
com mais nada reprova o CI: a lista só diminui ou é justificada de novo.

## EN

Every skill arrives by pull request and must pass `python scripts/check.py` (CI runs it with Chimera's
own SKILL.md parser). Own skills are Apache-2.0, markdown only, with a catalogue entry and a review
that records the content hash. Third-party copies need a licence **file** on the allowlist, a pinned
40-hex commit, the upstream LICENSE next to the skill, markdown only, frontmatter-only edits
(`mode: include`) or documented body edits (`mode: adapt`), plus `upstream.lock`, `NOTICE`, catalogue
and review entries. ComposioHQ, VoltAgent/ClawHub and Anthropic's proprietary document skills are
never accepted. No install counts, ever: popularity is GitHub stars with the date they were read.
