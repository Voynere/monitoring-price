<?php

declare(strict_types=1);

namespace App\Context\Site\Controller;

use App\Context\Site\Application\SitePage\BuildSitePageRenderPayloadUseCase;
use App\Context\Site\Application\SitePage\SitePageRegistry;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class SiteController extends AbstractController
{
    #[Route(path: ['ru' => '/', 'en' => '/en'], name: 'site_home', methods: ['GET'])]
    public function home(BuildSitePageRenderPayloadUseCase $buildSitePageRenderPayloadUseCase): Response
    {
        return $this->renderPage($buildSitePageRenderPayloadUseCase, SitePageRegistry::HOME);
    }

    #[Route(path: ['ru' => '/about', 'en' => '/en/about'], name: 'site_about', methods: ['GET'])]
    public function about(BuildSitePageRenderPayloadUseCase $buildSitePageRenderPayloadUseCase): Response
    {
        return $this->renderPage($buildSitePageRenderPayloadUseCase, SitePageRegistry::ABOUT);
    }

    #[Route(path: ['ru' => '/contacts', 'en' => '/en/contacts'], name: 'site_contacts', methods: ['GET'])]
    public function contacts(BuildSitePageRenderPayloadUseCase $buildSitePageRenderPayloadUseCase): Response
    {
        return $this->renderPage($buildSitePageRenderPayloadUseCase, SitePageRegistry::CONTACTS);
    }

    #[Route(path: ['ru' => '/blog', 'en' => '/en/blog'], name: 'site_blog', methods: ['GET'])]
    public function blog(BuildSitePageRenderPayloadUseCase $buildSitePageRenderPayloadUseCase): Response
    {
        return $this->renderPage($buildSitePageRenderPayloadUseCase, SitePageRegistry::BLOG);
    }

    #[Route(path: ['ru' => '/blog/monitoring-cen-konkurentov', 'en' => '/en/blog/competitor-price-monitoring-guide'], name: 'site_blog_post_monitoring', methods: ['GET'])]
    public function blogPostMonitoring(BuildSitePageRenderPayloadUseCase $buildSitePageRenderPayloadUseCase): Response
    {
        return $this->renderPage($buildSitePageRenderPayloadUseCase, SitePageRegistry::BLOG_POST_MONITORING);
    }

    #[Route(path: ['ru' => '/blog/7-metric-dlya-analiza-cenovoy-strategii', 'en' => '/en/blog/seven-metrics-pricing-strategy-kpi'], name: 'site_blog_post_kpi_metrics', methods: ['GET'])]
    public function blogPostKpiMetrics(BuildSitePageRenderPayloadUseCase $buildSitePageRenderPayloadUseCase): Response
    {
        return $this->renderPage($buildSitePageRenderPayloadUseCase, SitePageRegistry::BLOG_POST_KPI_METRICS);
    }

    #[Route(path: ['ru' => '/news', 'en' => '/en/news'], name: 'site_news', methods: ['GET'])]
    public function news(BuildSitePageRenderPayloadUseCase $buildSitePageRenderPayloadUseCase): Response
    {
        return $this->renderPage($buildSitePageRenderPayloadUseCase, SitePageRegistry::NEWS);
    }

    private function renderPage(BuildSitePageRenderPayloadUseCase $buildSitePageRenderPayloadUseCase, string $page): Response
    {
        $payload = $buildSitePageRenderPayloadUseCase->execute($page);

        return $this->render($payload->template, $payload->twigContext);
    }
}
