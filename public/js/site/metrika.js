(function () {
    var counterId = 109066328;

    function injectTag() {
        (function (m, e, t, r, i, k, a) {
            m[i] = m[i] || function () {
                (m[i].a = m[i].a || []).push(arguments);
            };
            m[i].l = 1 * new Date();
            for (var j = 0; j < document.scripts.length; j++) {
                if (document.scripts[j].src === r) {
                    return;
                }
            }
            k = e.createElement(t);
            a = e.getElementsByTagName(t)[0];
            k.async = 1;
            k.src = r;
            a.parentNode.insertBefore(k, a);
        })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=' + counterId, 'ym');
    }

    function initCounterOnce() {
        if (window.__smyalichiYmCounterInited) {
            return;
        }
        window.__smyalichiYmCounterInited = true;
        injectTag();
        ym(counterId, 'init', {
            ssr: true,
            webvisor: true,
            trackHash: true,
            clickmap: true,
            ecommerce: 'dataLayer',
            referrer: document.referrer,
            url: location.href,
            accurateTrackBounce: true,
            trackLinks: true,
        });
    }

    function hitCurrentPage() {
        if (typeof ym !== 'function') {
            return;
        }
        ym(counterId, 'hit', window.location.pathname + window.location.search, {
            referer: document.referrer,
            url: window.location.href,
        });
    }

    function scheduleMetrikaIdle() {
        if ('requestIdleCallback' in window) {
            window.requestIdleCallback(
                function () { initCounterOnce(); },
                { timeout: 5000 }
            );
        } else {
            window.setTimeout(initCounterOnce, 200);
        }
    }

    function bootstrapFirstPaint() {
        if (document.readyState === 'complete') {
            scheduleMetrikaIdle();
        } else {
            window.addEventListener('load', scheduleMetrikaIdle, { once: true });
        }
    }

    bootstrapFirstPaint();

    var skipFirstTurboLoad = true;
    document.addEventListener('turbo:load', function () {
        if (skipFirstTurboLoad) {
            skipFirstTurboLoad = false;
            return;
        }
        if (window.__smyalichiYmCounterInited) {
            hitCurrentPage();
        }
    });
})();
