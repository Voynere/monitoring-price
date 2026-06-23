<?php

declare(strict_types=1);

namespace App\Tests\Context\Site\Application\Seo;

use App\Context\Site\Application\Seo\SitemapBuilder;
use App\Context\Site\Application\SitePage\SitePageRegistry;
use PHPUnit\Framework\TestCase;

final class SitemapBuilderTest extends TestCase
{
    public function testBuildIncludesLastmodAndHreflang(): void
    {
        $builder = new SitemapBuilder(new SitePageRegistry());
        $xml = $builder->build('https://price.smyalichi.ru');

        self::assertStringContainsString('<lastmod>2026-06-23</lastmod>', $xml);
        self::assertStringContainsString('/blog/llm-i-parsing-v-cenovom-monitoringe', $xml);
        self::assertStringContainsString('hreflang="ru"', $xml);
        self::assertStringContainsString('hreflang="en"', $xml);
    }
}
