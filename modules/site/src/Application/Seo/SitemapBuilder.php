<?php

declare(strict_types=1);

namespace App\Context\Site\Application\Seo;

use App\Context\Site\Application\SitePage\SitePageRegistry;

final class SitemapBuilder
{
    public function __construct(
        private readonly SitePageRegistry $sitePageRegistry,
    ) {
    }

    public function build(string $schemeAndHost): string
    {
        $baseUrl = rtrim($schemeAndHost, '/');
        $xmlItems = '';

        foreach ($this->sitePageRegistry->all() as $page) {
            $ruLoc = $baseUrl.$page['canonical_ru'];
            $enLoc = $baseUrl.$page['canonical_en'];
            $priority = $page['sitemap_priority'];
            $lastmod = $page['sitemap_lastmod'];
            $alts = self::sitemapAlternateLinksXml($ruLoc, $enLoc);

            $xmlItems .= sprintf(
                "<url><loc>%s</loc>\n%s<lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>\n",
                htmlspecialchars($ruLoc, ENT_XML1),
                $alts,
                $lastmod,
                $priority
            );
            $xmlItems .= sprintf(
                "<url><loc>%s</loc>\n%s<lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority></url>\n",
                htmlspecialchars($enLoc, ENT_XML1),
                $alts,
                $lastmod,
                $priority
            );
        }

        return <<<XML
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{$xmlItems}</urlset>
XML;
    }

    private static function sitemapAlternateLinksXml(string $ruUrl, string $enUrl): string
    {
        $h = static fn (string $u): string => htmlspecialchars($u, ENT_XML1);

        return sprintf(
            "<xhtml:link rel=\"alternate\" hreflang=\"ru\" href=\"%s\" />\n<xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"%s\" />\n<xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"%s\" />\n",
            $h($ruUrl),
            $h($enUrl),
            $h($ruUrl)
        );
    }
}
