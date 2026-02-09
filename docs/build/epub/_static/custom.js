// Custom JavaScript for 5D Interpolator Documentation

(function() {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        createDownloadMenu();
    });

    function createDownloadMenu() {
        // Create download menu HTML
        const menuHTML = `
            <div class="download-menu">
                <button class="download-toggle" id="download-toggle" aria-label="Download Documentation">
                    📥
                </button>
                <div class="download-panel" id="download-panel">
                    <div class="download-panel-header">
                        <h3>📚 Download Documentation</h3>
                    </div>
                    <div class="download-panel-body">
                        <div class="download-section">
                            <div class="download-section-title">Formats</div>
                            <a href="downloads/5D-Interpolator-Documentation.pdf"
                               class="download-item"
                               download
                               title="Download PDF version">
                                <div class="download-item-icon">📄</div>
                                <div class="download-item-info">
                                    <div class="download-item-title">PDF</div>
                                    <div class="download-item-meta">~423 KB • Printable</div>
                                </div>
                            </a>
                            <a href="downloads/5D-Interpolator-Documentation.epub"
                               class="download-item"
                               download
                               title="Download EPUB version">
                                <div class="download-item-icon">📖</div>
                                <div class="download-item-info">
                                    <div class="download-item-title">EPUB</div>
                                    <div class="download-item-meta">~83 KB • E-reader format</div>
                                </div>
                            </a>
                            <a href="downloads/5D-Interpolator-Documentation-HTML.zip"
                               class="download-item"
                               download
                               title="Download HTML archive">
                                <div class="download-item-icon">🗂️</div>
                                <div class="download-item-info">
                                    <div class="download-item-title">HTML Archive</div>
                                    <div class="download-item-meta">~8.2 MB • Offline browsing</div>
                                </div>
                            </a>
                        </div>

                        <div class="download-divider"></div>

                        <div class="download-section">
                            <div class="download-section-title">Version</div>
                            <div class="download-item" style="cursor: default; border: 1px solid #28a745;">
                                <div class="download-item-icon">✅</div>
                                <div class="download-item-info">
                                    <div class="download-item-title">
                                        v0.1.0 <span class="version-badge">Stable</span>
                                    </div>
                                    <div class="download-item-meta">Current version</div>
                                </div>
                            </div>
                            <div class="download-item" style="cursor: default;">
                                <div class="download-item-icon">🚀</div>
                                <div class="download-item-info">
                                    <div class="download-item-title">
                                        v0.1.0 <span class="version-badge latest">Latest</span>
                                    </div>
                                    <div class="download-item-meta">Last updated: ${new Date().toLocaleDateString()}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Insert menu into page
        document.body.insertAdjacentHTML('beforeend', menuHTML);

        // Add event listeners
        const toggle = document.getElementById('download-toggle');
        const panel = document.getElementById('download-panel');

        if (toggle && panel) {
            // Toggle panel on button click
            toggle.addEventListener('click', function(e) {
                e.stopPropagation();
                panel.classList.toggle('active');
            });

            // Close panel when clicking outside
            document.addEventListener('click', function(e) {
                if (!panel.contains(e.target) && !toggle.contains(e.target)) {
                    panel.classList.remove('active');
                }
            });

            // Prevent panel from closing when clicking inside it
            panel.addEventListener('click', function(e) {
                e.stopPropagation();
            });

            // Close panel on Escape key
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && panel.classList.contains('active')) {
                    panel.classList.remove('active');
                }
            });

            // Track downloads (optional analytics)
            const downloadLinks = panel.querySelectorAll('a.download-item');
            downloadLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    const format = this.querySelector('.download-item-title').textContent.trim();
                    console.log('Download started:', format);

                    // Close panel after download starts
                    setTimeout(function() {
                        panel.classList.remove('active');
                    }, 300);
                });
            });
        }
    }

    // Add keyboard shortcut (Ctrl/Cmd + D)
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            const toggle = document.getElementById('download-toggle');
            if (toggle) {
                toggle.click();
            }
        }
    });
})();
