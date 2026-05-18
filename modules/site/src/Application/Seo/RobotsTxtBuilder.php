<?php

declare(strict_types=1);

namespace App\Context\Site\Application\Seo;

final class RobotsTxtBuilder
{
    public function build(string $schemeAndHost): string
    {
        $sitemapUrl = rtrim($schemeAndHost, '/').'/sitemap.xml';

        return <<<TXT
User-agent: *
Allow: /

Sitemap: {$sitemapUrl}
TXT;
    }
}
