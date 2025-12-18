(function () {
    console.log('[auto-toggle-sidebar]: Auto-toggle sidebar script started');

    const isHomepage = window.location.pathname === '/' ||
        window.location.pathname === '' ||
        window.location.pathname.endsWith('index.html');

    function toggleIfNeeded() {
        const btn = document.querySelector('.sidebar-toggle');
        if (btn && !isHomepage) {
            console.log('[auto-toggle-sidebar]: Non-homepage detected, hiding sidebar');
            btn.click();
            return true;
        }
        return false;
    }

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        toggleIfNeeded();
    } else {
        document.addEventListener('DOMContentLoaded', toggleIfNeeded);
    }
})();
