(function () {
    var onScroll = null;
    var boundBtn = null;
    var boundClick = null;

    function pauseHeroVideos() {
        document.querySelectorAll('.sl-hero__video').forEach(function (video) {
            video.pause();
        });
    }

    function playHeroVideos() {
        document.querySelectorAll('.sl-hero__video').forEach(function (video) {
            var playPromise = video.play();
            if (playPromise && typeof playPromise.catch === 'function') {
                playPromise.catch(function () {});
            }
        });
    }

    function dispose() {
        if (onScroll) {
            window.removeEventListener('scroll', onScroll);
            onScroll = null;
        }
        if (boundBtn && boundClick) {
            boundBtn.removeEventListener('click', boundClick);
        }
        boundBtn = null;
        boundClick = null;
        pauseHeroVideos();
    }

    function init() {
        dispose();

        var btn = document.getElementById('site-scroll-top');
        var header = document.querySelector('.site-header--wp');
        if (!btn) {
            return;
        }

        var ticking = false;
        var prevHideBtn;
        var prevCompact;

        function applyScrollState() {
            var y = window.scrollY || window.pageYOffset;
            var hideBtn = y < 360;
            var compact = header ? y > 56 : false;

            if (prevHideBtn !== hideBtn) {
                prevHideBtn = hideBtn;
                btn.hidden = hideBtn;
            }

            if (header && prevCompact !== compact) {
                prevCompact = compact;
                header.classList.toggle('site-header--wp-scrolled', compact);
            }

            ticking = false;
        }

        onScroll = function () {
            if (!ticking) {
                ticking = true;
                requestAnimationFrame(applyScrollState);
            }
        };

        boundClick = function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };
        boundBtn = btn;

        window.addEventListener('scroll', onScroll, { passive: true });
        btn.addEventListener('click', boundClick);

        requestAnimationFrame(function () {
            requestAnimationFrame(applyScrollState);
        });

        playHeroVideos();
    }

    document.addEventListener('turbo:load', init);
    document.addEventListener('turbo:before-cache', dispose);

    if (!window.Turbo) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    }
})();
