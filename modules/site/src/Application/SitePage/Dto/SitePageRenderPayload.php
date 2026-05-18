<?php

declare(strict_types=1);

namespace App\Context\Site\Application\SitePage\Dto;

/**
 * @phpstan-type SitePageTwigContext array{
 *   page_title: string,
 *   meta_description: string,
 *   canonical_path: string
 * }
 */
final readonly class SitePageRenderPayload
{
    /**
     * @param SitePageTwigContext $twigContext
     */
    public function __construct(
        public string $template,
        public array $twigContext,
    ) {
    }
}
