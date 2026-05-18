<?php

declare(strict_types=1);

namespace App\Context\Site\Application\Seo;

final class JsonLdGraphBuilder
{
    /**
     * @return array<string, mixed>
     */
    public function buildWebPageGraph(
        string $siteOrigin,
        string $pageUrl,
        string $locale,
        string $orgName,
        string $logoUrl,
        string $pageTitle,
        string $pageDescription,
    ): array {
        $inLang = $locale === 'en' ? 'en' : 'ru';
        $webpageNode = [
            '@type' => 'WebPage',
            '@id' => $pageUrl.'#webpage',
            'url' => $pageUrl,
            'name' => $pageTitle,
            'description' => $pageDescription,
            'isPartOf' => ['@id' => $siteOrigin.'/#website'],
            'inLanguage' => $inLang,
        ];

        return $this->graph($this->organizationWebsiteNodes($siteOrigin, $locale, $orgName, $logoUrl), [$webpageNode]);
    }

    /**
     * @param list<array<string, mixed>> $items
     * @return array<string, mixed>
     */
    public function buildCollectionPageGraph(
        string $siteOrigin,
        string $pageUrl,
        string $locale,
        string $orgName,
        string $logoUrl,
        string $pageTitle,
        string $pageDescription,
        array $items,
    ): array {
        $inLang = $locale === 'en' ? 'en' : 'ru';
        $collectionNode = [
            '@type' => 'CollectionPage',
            '@id' => $pageUrl.'#webpage',
            'url' => $pageUrl,
            'name' => $pageTitle,
            'description' => $pageDescription,
            'isPartOf' => ['@id' => $siteOrigin.'/#website'],
            'inLanguage' => $inLang,
            'mainEntity' => [
                '@type' => 'ItemList',
                'numberOfItems' => count($items),
                'itemListElement' => $items,
            ],
        ];

        return $this->graph($this->organizationWebsiteNodes($siteOrigin, $locale, $orgName, $logoUrl), [$collectionNode]);
    }

    /**
     * @param array<string, mixed> $articleNode
     * @return array<string, mixed>
     */
    public function buildArticleGraph(
        string $siteOrigin,
        string $locale,
        string $orgName,
        string $logoUrl,
        array $articleNode,
    ): array {
        return $this->graph($this->organizationWebsiteNodes($siteOrigin, $locale, $orgName, $logoUrl), [$articleNode]);
    }

    /**
     * @return list<array<string, mixed>>
     */
    public function organizationWebsiteNodes(string $siteOrigin, string $locale, string $orgName, string $logoUrl): array
    {
        $inLang = $locale === 'en' ? 'en' : 'ru';

        return [
            [
                '@type' => 'Organization',
                '@id' => $siteOrigin.'/#organization',
                'name' => $orgName,
                'url' => $siteOrigin.'/',
                'logo' => [
                    '@type' => 'ImageObject',
                    'url' => $logoUrl,
                ],
                'contactPoint' => [
                    '@type' => 'ContactPoint',
                    'telephone' => '+7-908-449-92-92',
                    'email' => 'info@smyalichi.ru',
                    'contactType' => 'customer support',
                    'areaServed' => 'RU',
                    'availableLanguage' => ['ru', 'en'],
                ],
            ],
            [
                '@type' => 'WebSite',
                '@id' => $siteOrigin.'/#website',
                'url' => $siteOrigin.'/',
                'name' => $orgName,
                'publisher' => ['@id' => $siteOrigin.'/#organization'],
                'inLanguage' => [$inLang],
            ],
        ];
    }

    /**
     * @param list<array<string, mixed>> $baseNodes
     * @param list<array<string, mixed>> $extraNodes
     * @return array<string, mixed>
     */
    private function graph(array $baseNodes, array $extraNodes): array
    {
        return [
            '@context' => 'https://schema.org',
            '@graph' => array_merge($baseNodes, $extraNodes),
        ];
    }
}
