<?php

declare(strict_types=1);

namespace App\Context\Site\Twig;

use App\Context\Site\Application\Seo\JsonLdGraphBuilder;
use Twig\Extension\AbstractExtension;
use Twig\TwigFunction;

/**
 * Общие узлы JSON-LD для публичного сайта (переиспользование в шаблонах страниц).
 */
final class SiteSeoExtension extends AbstractExtension
{
    public function __construct(
        private readonly JsonLdGraphBuilder $jsonLdGraphBuilder,
    ) {
    }

    public function getFunctions(): array
    {
        return [
            new TwigFunction('site_ld_organization_website', $this->organizationWebsiteNodes(...)),
            new TwigFunction('site_ld_graph', $this->buildGraph(...)),
        ];
    }

    /**
     * @return list<array<string, mixed>>
     */
    public function organizationWebsiteNodes(string $siteOrigin, string $locale, string $orgName, string $logoUrl): array
    {
        return $this->jsonLdGraphBuilder->organizationWebsiteNodes($siteOrigin, $locale, $orgName, $logoUrl);
    }

    /**
     * @param array<string, mixed> $context
     * @return array<string, mixed>
     */
    public function buildGraph(
        string $pageType,
        string $siteOrigin,
        string $pageUrl,
        string $locale,
        string $orgName,
        string $logoUrl,
        string $pageTitle,
        string $pageDescription,
        array $context = [],
    ): array {
        return match ($pageType) {
            'collection' => $this->jsonLdGraphBuilder->buildCollectionPageGraph(
                $siteOrigin,
                $pageUrl,
                $locale,
                $orgName,
                $logoUrl,
                $pageTitle,
                $pageDescription,
                $context['items'] ?? [],
            ),
            'article' => $this->jsonLdGraphBuilder->buildArticleGraph(
                $siteOrigin,
                $locale,
                $orgName,
                $logoUrl,
                $context['articleNode'] ?? [],
            ),
            default => $this->jsonLdGraphBuilder->buildWebPageGraph(
                $siteOrigin,
                $pageUrl,
                $locale,
                $orgName,
                $logoUrl,
                $pageTitle,
                $pageDescription,
            ),
        };
    }
}
