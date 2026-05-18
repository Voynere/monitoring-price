<?php

declare(strict_types=1);

namespace App\Context\Site\Application\SitePage\Dto;

final readonly class SitePageView
{
    public function __construct(
        public string $template,
        public string $pageTitle,
        public string $metaDescription,
        public string $canonicalPath,
    ) {
    }
}
