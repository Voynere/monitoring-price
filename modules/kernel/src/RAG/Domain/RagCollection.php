<?php

declare(strict_types=1);

namespace App\Context\Kernel\RAG\Domain;

final class RagCollection
{
    public const PRICE_RULES = 'price_rules';
    public const PURCHASE_HISTORY = 'purchase_history';
    public const SEO_COMPETITORS = 'seo_competitors';
    public const DATA_METRICS = 'data_metrics';
    public const SITE_CONTENT = 'site_content';

    /**
     * @return list<string>
     */
    public static function all(): array
    {
        return [
            self::PRICE_RULES,
            self::PURCHASE_HISTORY,
            self::SEO_COMPETITORS,
            self::DATA_METRICS,
            self::SITE_CONTENT,
        ];
    }
}
