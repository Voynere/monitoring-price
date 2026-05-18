(function () {
    var bootstrapReady;

    function loadBootstrapBundle() {
        if (window.bootstrap) {
            return Promise.resolve();
        }
        if (bootstrapReady) {
            return bootstrapReady;
        }
        if (window.__smyalichiBootstrapBundleLoading) {
            return window.__smyalichiBootstrapBundleLoading;
        }

        bootstrapReady = window.__smyalichiBootstrapBundleLoading = new Promise(function (resolve, reject) {
            var existing = document.querySelector('script[data-smyalichi-bootstrap-bundle]');
            if (existing) {
                existing.addEventListener('load', function () { resolve(); }, { once: true });
                existing.addEventListener('error', reject, { once: true });
                return;
            }

            var script = document.createElement('script');
            script.dataset.smyalichiBootstrapBundle = '1';
            script.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js';
            script.crossOrigin = 'anonymous';
            script.integrity = 'sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });

        return bootstrapReady;
    }

    function initNav() {
        var panel = document.getElementById('siteNav');
        var buttons = document.querySelectorAll('.site-menu-button[data-bs-target="#siteNav"]');
        if (!panel || !buttons.length) {
            return;
        }

        var ariaMenuOpen = panel.getAttribute('data-aria-open') || 'Open menu';
        var ariaMenuClose = panel.getAttribute('data-aria-close') || 'Close menu';

        function setExpanded(expanded) {
            buttons.forEach(function (btn) {
                btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
            });
        }

        function initOffcanvasHandlers() {
            if (panel.dataset.bsInitDone === '1') {
                return;
            }
            panel.dataset.bsInitDone = '1';

            panel.addEventListener('shown.bs.offcanvas', function () {
                setExpanded(true);
                buttons.forEach(function (btn) {
                    btn.setAttribute('aria-label', ariaMenuClose);
                });
            });

            panel.addEventListener('hidden.bs.offcanvas', function () {
                setExpanded(false);
                buttons.forEach(function (btn) {
                    btn.setAttribute('aria-label', ariaMenuOpen);
                });
            });

            if (window.bootstrap && window.bootstrap.Offcanvas) {
                window.bootstrap.Offcanvas.getOrCreateInstance(panel);
            }
        }

        function ensureBootstrapAndInit() {
            loadBootstrapBundle().then(initOffcanvasHandlers).catch(function () {});
        }

        if ('requestIdleCallback' in window) {
            window.requestIdleCallback(ensureBootstrapAndInit, { timeout: 1800 });
        } else {
            window.setTimeout(ensureBootstrapAndInit, 1000);
        }

        buttons.forEach(function (btn) {
            btn.addEventListener('pointerdown', ensureBootstrapAndInit, { once: true, passive: true });
            btn.addEventListener('touchstart', ensureBootstrapAndInit, { once: true, passive: true });
            btn.addEventListener('click', ensureBootstrapAndInit, { once: true, passive: true });
        });
    }

    function beforeCacheNav() {
        var panel = document.getElementById('siteNav');
        if (panel && window.bootstrap && window.bootstrap.Offcanvas) {
            var instance = window.bootstrap.Offcanvas.getInstance(panel);
            if (instance) {
                instance.hide();
            }
        }
    }

    document.addEventListener('turbo:load', initNav);
    document.addEventListener('turbo:before-cache', beforeCacheNav);

    if (!window.Turbo) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initNav);
        } else {
            initNav();
        }
    }
})();
