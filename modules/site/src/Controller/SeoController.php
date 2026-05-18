<?php

declare(strict_types=1);

namespace App\Context\Site\Controller;

use App\Context\Site\Application\Seo\RobotsTxtBuilder;
use App\Context\Site\Application\Seo\SitemapBuilder;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class SeoController
{
    #[Route('/robots.txt', name: 'site_robots', methods: ['GET'])]
    public function robots(Request $request, RobotsTxtBuilder $robotsTxtBuilder): Response
    {
        $content = $robotsTxtBuilder->build($request->getSchemeAndHttpHost());

        return new Response($content, 200, ['Content-Type' => 'text/plain; charset=UTF-8']);
    }

    #[Route('/sitemap.xml', name: 'site_sitemap', methods: ['GET'])]
    public function sitemap(Request $request, SitemapBuilder $sitemapBuilder): Response
    {
        $xml = $sitemapBuilder->build($request->getSchemeAndHttpHost());

        return new Response($xml, 200, ['Content-Type' => 'application/xml; charset=UTF-8']);
    }
}
