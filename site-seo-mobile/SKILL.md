---
name: site-seo-mobile
description: Padrões obrigatórios para qualquer site, landing page ou página web criada ou alterada. Use SEMPRE que o usuário pedir para criar, refazer ou editar site, landing page, página de vendas, blog, loja ou qualquer HTML/front-end. Garante SEO técnico e on-page, mobile-first, performance (Core Web Vitals), acessibilidade, dados estruturados, compartilhamento social e rastreamento básico. Roda a auditoria automática antes de entregar.
---

# Site com SEO + Mobile + Performance (padrão obrigatório)

Todo site/página criado ou editado deve sair já atendendo a este padrão. Não é opcional nem "fase 2".

## Fluxo

1. **Levante os dados** (peça só o que faltar, no máximo 3 perguntas curtas): nome do negócio, o que vende/oferece, público e cidade/região (SEO local), palavra-chave principal, URL final do site, WhatsApp/telefone, ação principal (CTA) e IDs de rastreamento (GA4, Meta Pixel), se houver.
2. **Construa** seguindo as regras abaixo, partindo de `references/head-template.html`.
3. **Audite**: `python3 site-seo-mobile/scripts/audit_html.py <arquivo.html ou pasta>`. Corrija tudo que aparecer como ERRO e avalie os AVISOS.
4. **Entregue** com um resumo curto: o que foi aplicado, o resultado da auditoria e o que depende do usuário (domínio, imagens reais, IDs de rastreamento, Search Console).

Nunca invente dados do cliente (telefone, endereço, avaliações, CNPJ). Se faltar, deixe um placeholder visível `[PREENCHER: ...]` e avise.

## 1. Mobile-first (prioridade máxima)

- `<meta name="viewport" content="width=device-width, initial-scale=1">` (nunca bloquear zoom: sem `user-scalable=no`).
- CSS escrito primeiro para celular; `min-width` em media queries para telas maiores.
- Sem rolagem horizontal em 360px de largura. Testar 360, 390, 768 e 1280px.
- Alvos de toque ≥ 44×44px, com espaçamento entre eles. Botão de CTA/WhatsApp sempre acessível (fixo no rodapé ou no topo no mobile, sem cobrir conteúdo).
- Texto base ≥ 16px (evita zoom automático no iOS em inputs), `line-height` ≥ 1.5.
- Inputs com `type`, `inputmode` e `autocomplete` corretos (`tel`, `email`, `name`).
- Links `tel:` e `https://wa.me/55DDDNUMERO?text=...` para contato.
- Evite pop-ups que cobrem a tela inteira no mobile (penalizados pelo Google).

## 2. SEO técnico

- `<html lang="pt-BR">`, `<meta charset="utf-8">`.
- `<title>` único por página, 50–60 caracteres, palavra-chave principal no início + marca.
- `<meta name="description">` único, 120–160 caracteres, com benefício e CTA.
- `<link rel="canonical" href="URL absoluta">` em toda página.
- `robots.txt` (apontando para o sitemap) e `sitemap.xml` na raiz, com URLs absolutas.
- URLs curtas, minúsculas, sem acento, com hífens (`/consultoria-financeira-sp`).
- HTTPS obrigatório; sem conteúdo misto (http dentro de https).
- Página 404 própria. Redirecionar versões duplicadas (www/sem www, http/https).
- Páginas que não devem indexar (obrigado, admin, testes): `<meta name="robots" content="noindex">`.
- Sites com mais de um idioma: `hreflang`.

## 3. SEO on-page e conteúdo

- **Um único `<h1>`** com a palavra-chave principal e a promessa da página. Depois `h2`/`h3` em ordem lógica, sem pular níveis.
- Estrutura semântica: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`. Apenas um `<main>`.
- A palavra-chave aparece naturalmente no h1, no primeiro parágrafo, em ao menos um h2 e no `alt` de uma imagem. Sem keyword stuffing.
- Texto real e útil acima da dobra; nada de conteúdo essencial só em imagem ou só carregado por JavaScript.
- Seção de FAQ com perguntas reais do público (também alimenta dados estruturados).
- Links internos com texto âncora descritivo (nunca "clique aqui"). Links externos de confiança com `rel="noopener"`.
- SEO local (quando houver cidade/endereço): NAP (nome, endereço, telefone) idêntico em todo o site, cidade no título/h1/descrição e mapa incorporado com `loading="lazy"`.
- Sinais de confiança (E-E-A-T): quem somos, prova social real, política de privacidade, contato visível.

## 4. Dados estruturados (JSON-LD)

Incluir em `<script type="application/ld+json">` e validar sintaxe:
- `Organization` ou `LocalBusiness` (conforme o caso) em toda home.
- `WebSite` na home.
- `FAQPage` se houver FAQ visível na página (o conteúdo do JSON-LD deve bater com o texto visível).
- `BreadcrumbList` em páginas internas.
- `Article`/`BlogPosting` em posts; `Product`/`Offer` em páginas de produto; `Service` para serviços.
Só marque o que existe de verdade na página. Dados falsos ou invisíveis geram penalização.

## 5. Compartilhamento social

Open Graph e Twitter Card em toda página: `og:type`, `og:title`, `og:description`, `og:url`, `og:image` (1200×630, URL absoluta), `og:locale` (`pt_BR`), `twitter:card` (`summary_large_image`). Importante para links enviados por WhatsApp e para anúncios.

## 6. Performance (Core Web Vitals)

Metas: LCP < 2,5s, INP < 200ms, CLS < 0,1, no mobile em 4G.
- Imagens: WebP/AVIF, dimensionadas para o uso real, com `width` e `height` (evita CLS), `loading="lazy"` (exceto a imagem principal acima da dobra, que usa `fetchpriority="high"` e **sem** lazy), `decoding="async"` e `srcset`/`sizes` quando houver várias larguras.
- Fontes: no máximo 2 famílias e 2–3 pesos; `font-display: swap`; `preconnect` para o domínio de fontes; preferir fontes do sistema quando a marca permitir.
- CSS crítico inline ou arquivo único pequeno; JS com `defer`; nada de bibliotecas pesadas para algo que CSS resolve. Sem jQuery novo.
- Scripts de terceiros (GA4, Pixel, chat) carregados com `async`/`defer`, e só os necessários.
- Reservar espaço para banners, embeds e imagens (sem "pulos" de layout).
- Vídeos: `preload="none"` ou facade (miniatura que carrega o player ao clicar); nunca autoplay com som.
- Habilitar compressão (gzip/brotli) e cache longo para assets estáticos, quando o hosting permitir.
- Total de página no mobile idealmente < 1,5 MB.

## 7. Acessibilidade (também ajuda no SEO)

- Todo `<img>` com `alt` descritivo (decorativas: `alt=""`).
- Contraste mínimo 4.5:1 para texto normal.
- Foco visível em links e botões; navegação completa por teclado.
- Botões e links com texto claro; ícones sozinhos com `aria-label`.
- Formulários com `<label>` associado a cada campo e mensagens de erro legíveis.
- Respeitar `prefers-reduced-motion`.

## 8. Rastreamento e conversão (quando for página de captação/anúncio)

- Placeholders para GA4 e Meta Pixel com os IDs informados pelo usuário; nunca inventar IDs.
- Evento de conversão no CTA principal (clique no WhatsApp, envio de formulário) e página de obrigado com `noindex`.
- Suporte a parâmetros UTM (não bloquear nem quebrar URLs com `?utm_...`); canonical sempre sem parâmetros.
- Um objetivo por landing page: um CTA principal repetido, sem menu de saída que disperse o visitante.
- LGPD: aviso de cookies quando houver pixel/analytics, link para Política de Privacidade e checkbox de consentimento em formulários que coletam dados pessoais.

## 9. Segurança e higiene

- Sem chaves/segredos no front-end.
- Links externos com `rel="noopener"` (`nofollow`/`sponsored` para links pagos/afiliados).
- Favicon (`.ico` ou `.svg`) e `apple-touch-icon`; `theme-color`.
- Sem `console.log`, `lorem ipsum`, "TODO" ou textos de exemplo na entrega.

## Checklist final (confira antes de entregar)

- [ ] Auditoria `audit_html.py` sem ERROS
- [ ] viewport correto, sem scroll horizontal em 360px
- [ ] title, description, canonical, 1 h1
- [ ] Open Graph + Twitter Card com imagem 1200×630
- [ ] JSON-LD válido e coerente com o conteúdo visível
- [ ] Imagens com alt, width/height, lazy (exceto a principal)
- [ ] robots.txt + sitemap.xml + favicon
- [ ] CTA visível e funcional no mobile (tel:/wa.me/formulário)
- [ ] Placeholders `[PREENCHER: ...]` listados para o usuário
- [ ] Próximos passos informados: publicar em HTTPS, enviar sitemap no Google Search Console, criar/atualizar Google Meu Negócio (se local), medir no PageSpeed Insights

## Arquivos desta skill

- `references/head-template.html`: `<head>` completo (SEO, social, JSON-LD, performance) para copiar e preencher.
- `references/robots-sitemap.md`: modelos de `robots.txt` e `sitemap.xml`.
- `scripts/audit_html.py`: auditoria automática de HTML (sem dependências externas).
