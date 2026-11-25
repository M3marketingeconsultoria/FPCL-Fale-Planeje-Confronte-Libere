# Framework FPCL — Fale, Planeje, Confronte, Libere

O jeito certo de conversar com a IA. Vale para tudo: agent, skill, sistema, app.

| Passo | O que fazer |
|---|---|
| **F**ale | Converse de forma humanizada, como falaria com uma pessoa. |
| **P**laneje | Peça para a IA montar o plano **antes** de executar. |
| **C**onfronte | Questione, ajuste e desafie cada passo do plano. |
| **L**ibere | Só então aprove para a IA executar. |

## O que é este repositório

Um skill do Claude (`SKILL.md`) que faz a IA seguir o FPCL automaticamente:

1. Conversa em linguagem natural e tira dúvidas essenciais.
2. Apresenta um plano (objetivo, passos, riscos, como verificar) sem executar nada.
3. Aceita questionamentos e revisa o plano quantas vezes for preciso.
4. Só executa depois de uma aprovação explícita ("libera", "aprovado").

Perguntas simples e leituras sem efeito colateral são respondidas direto.

## Como instalar

**Claude Code:** copie o `SKILL.md` para uma pasta `fpcl` dentro de `~/.claude/skills/`:

```bash
mkdir -p ~/.claude/skills/fpcl
cp SKILL.md ~/.claude/skills/fpcl/SKILL.md
```

**Claude (interface):** compacte uma pasta `fpcl/` contendo o `SKILL.md` em um `.zip` e envie em Settings → Skills.

**Outras IAs (ChatGPT etc.):** copie o texto do `SKILL.md`, sem o bloco `---` do topo, para as instruções personalizadas.

## Como usar

O skill é acionado pela descrição em pedidos de criar, alterar ou executar algo. Para chamar manualmente, digite `/fpcl`.
