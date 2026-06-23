<?php

declare(strict_types=1);

namespace App\Context\Site\Application\SitePage;

final class SitePageRegistry
{
    public const HOME = 'home';
    public const ABOUT = 'about';
    public const CONTACTS = 'contacts';
    public const BLOG = 'blog';
    public const BLOG_POST_MONITORING = 'blog_post_monitoring';
    public const BLOG_POST_KPI_METRICS = 'blog_post_kpi_metrics';
    public const BLOG_POST_LLM_PARSING = 'blog_post_llm_parsing';
    public const NEWS = 'news';

    /**
     * @return array<string, array{
     *   template:string,
     *   meta_title_key:string,
     *   meta_description_key:string,
     *   canonical_ru:string,
     *   canonical_en:string,
     *   sitemap_priority:string,
     *   sitemap_lastmod:string
     * }>
     */
    public function all(): array
    {
        return [
            self::HOME => [
                'template' => 'site/index.html.twig',
                'meta_title_key' => 'meta.home.title',
                'meta_description_key' => 'meta.home.description',
                'canonical_ru' => '/',
                'canonical_en' => '/en',
                'sitemap_priority' => '1.0',
                'sitemap_lastmod' => '2026-06-01',
            ],
            self::ABOUT => [
                'template' => 'site/about.html.twig',
                'meta_title_key' => 'meta.about.title',
                'meta_description_key' => 'meta.about.description',
                'canonical_ru' => '/about',
                'canonical_en' => '/en/about',
                'sitemap_priority' => '0.8',
                'sitemap_lastmod' => '2026-05-15',
            ],
            self::CONTACTS => [
                'template' => 'site/contacts.html.twig',
                'meta_title_key' => 'meta.contacts.title',
                'meta_description_key' => 'meta.contacts.description',
                'canonical_ru' => '/contacts',
                'canonical_en' => '/en/contacts',
                'sitemap_priority' => '0.7',
                'sitemap_lastmod' => '2026-05-10',
            ],
            self::BLOG => [
                'template' => 'site/blog.html.twig',
                'meta_title_key' => 'meta.blog.title',
                'meta_description_key' => 'meta.blog.description',
                'canonical_ru' => '/blog',
                'canonical_en' => '/en/blog',
                'sitemap_priority' => '0.9',
                'sitemap_lastmod' => '2026-06-20',
            ],
            self::BLOG_POST_MONITORING => [
                'template' => 'site/blog_post_monitoring.html.twig',
                'meta_title_key' => 'meta.blog_post_monitoring.title',
                'meta_description_key' => 'meta.blog_post_monitoring.description',
                'canonical_ru' => '/blog/monitoring-cen-konkurentov',
                'canonical_en' => '/en/blog/competitor-price-monitoring-guide',
                'sitemap_priority' => '0.85',
                'sitemap_lastmod' => '2026-06-10',
            ],
            self::BLOG_POST_KPI_METRICS => [
                'template' => 'site/blog_post_kpi_metrics.html.twig',
                'meta_title_key' => 'meta.blog_post_kpi.title',
                'meta_description_key' => 'meta.blog_post_kpi.description',
                'canonical_ru' => '/blog/7-metric-dlya-analiza-cenovoy-strategii',
                'canonical_en' => '/en/blog/seven-metrics-pricing-strategy-kpi',
                'sitemap_priority' => '0.84',
                'sitemap_lastmod' => '2026-06-05',
            ],
            self::BLOG_POST_LLM_PARSING => [
                'template' => 'site/blog_post_llm_parsing.html.twig',
                'meta_title_key' => 'meta.blog_post_llm.title',
                'meta_description_key' => 'meta.blog_post_llm.description',
                'canonical_ru' => '/blog/llm-i-parsing-v-cenovom-monitoringe',
                'canonical_en' => '/en/blog/llm-parsing-in-price-monitoring',
                'sitemap_priority' => '0.83',
                'sitemap_lastmod' => '2026-06-23',
            ],
            self::NEWS => [
                'template' => 'site/news.html.twig',
                'meta_title_key' => 'meta.news.title',
                'meta_description_key' => 'meta.news.description',
                'canonical_ru' => '/news',
                'canonical_en' => '/en/news',
                'sitemap_priority' => '0.8',
                'sitemap_lastmod' => '2026-05-01',
            ],
        ];
    }

    /**
     * @return array{
     *   template:string,
     *   meta_title_key:string,
     *   meta_description_key:string,
     *   canonical_ru:string,
     *   canonical_en:string,
     *   sitemap_priority:string,
     *   sitemap_lastmod:string
     * }
     */
    public function get(string $page): array
    {
        $pages = $this->all();
        if (!isset($pages[$page])) {
            throw new \InvalidArgumentException(sprintf('Unknown site page: %s', $page));
        }

        return $pages[$page];
    }
}
