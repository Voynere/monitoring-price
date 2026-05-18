<?php

declare(strict_types=1);

namespace App\Context\Site\Application\SitePage;

use App\Context\Site\Application\SitePage\Dto\SitePageRenderPayload;

final class BuildSitePageRenderPayloadUseCase
{
    public function __construct(
        private readonly BuildSitePageViewUseCase $buildSitePageViewUseCase,
    ) {
    }

    public function execute(string $page): SitePageRenderPayload
    {
        $view = $this->buildSitePageViewUseCase->execute($page);

        return new SitePageRenderPayload(
            $view->template,
            [
                'page_title' => $view->pageTitle,
                'meta_description' => $view->metaDescription,
                'canonical_path' => $view->canonicalPath,
            ],
        );
    }
}
