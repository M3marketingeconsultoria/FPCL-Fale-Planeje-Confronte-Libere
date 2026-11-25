# robots.txt e sitemap.xml

## robots.txt (raiz do site)

```
User-agent: *
Allow: /
Disallow: /obrigado
Disallow: /admin

Sitemap: https://[DOMINIO]/sitemap.xml
```

## sitemap.xml (raiz do site)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://[DOMINIO]/</loc>
    <lastmod>AAAA-MM-DD</lastmod>
  </url>
</urlset>
```

Regras: só URLs indexáveis (200, canonical para si mesmas, sem noindex), sempre absolutas, e enviar no Google Search Console.
