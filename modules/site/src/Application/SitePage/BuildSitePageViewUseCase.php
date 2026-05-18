<?php

declare(strict_types=1);

namespace App\Context\Site\Application\SitePage;

use App\Context\Site\Application\SitePage\Dto\SitePageView;
use Symfony\Contracts\Translation\TranslatorInterface;

final class BuildSitePageViewUseCase
{
    public function __construct(
        private readonly SitePageRegistry $sitePageRegistry,
        private readonly TranslatorInterface $translator,
    ) {
    }

    public function execute(string $page): SitePageView
    {
        $definition = $this->sitePageRegistry->get($page);
        $isEn = $this->translator->getLocale() === 'en';

        return new SitePageView(
            $definition['template'],
            $this->translator->trans($definition['meta_title_key'], [], 'site'),
            $this->translator->trans($definition['meta_description_key'], [], 'site'),
            $isEn ? $definition['canonical_en'] : $definition['canonical_ru'],
        );
    }
}
