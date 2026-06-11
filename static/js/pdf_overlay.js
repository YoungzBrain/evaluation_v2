// PDF Overlay System using PDF.js
// Renders a PDF with form inputs positioned as an overlay

(function() {
  'use strict';

  // Initialize PDF.js worker
  if (typeof pdfjsLib !== 'undefined') {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }

  window.PDFOverlay = {
    pdfUrl: null,
    pdfDoc: null,
    currentPage: 1,
    scale: 1.5,
    containerSelector: '#pdf-overlay-container',
    questions: [],
    canvasHeight: 0,
    pageHeight: 0,

    /**
     * Initialize the PDF overlay system
     * @param {string} pdfUrl - URL to the PDF
     * @param {Array} questions - Question data with position info
     */
    init: function(pdfUrl, questions) {
      this.pdfUrl = pdfUrl;
      this.questions = questions || [];
      this.renderPDF();
    },

    /**
     * Load and render the PDF
     */
    renderPDF: function() {
      const self = this;
      if (!window.pdfjsLib) {
        console.error('PDF.js not loaded');
        return;
      }

      pdfjsLib.getDocument(this.pdfUrl).promise.then(function(pdf) {
        self.pdfDoc = pdf;
        self.renderPage(1);
      }).catch(function(err) {
        console.error('PDF loading failed:', err);
      });
    },

    /**
     * Render a specific page
     * @param {number} pageNum - Page number to render
     */
    renderPage: function(pageNum) {
      const self = this;
      this.pdfDoc.getPage(pageNum).then(function(page) {
        const viewport = page.getViewport({ scale: self.scale });
        const canvas = document.getElementById('pdf-canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = viewport.width;
        canvas.height = viewport.height;
        self.canvasHeight = viewport.height;
        self.pageHeight = viewport.height;

        const renderContext = {
          canvasContext: ctx,
          viewport: viewport,
        };

        page.render(renderContext).promise.then(function() {
          // After rendering the PDF, position the form inputs
          self.positionFormInputs();
        }).catch(function(err) {
          console.error('Page rendering failed:', err);
        });
      });
    },

    /**
     * Position form inputs on the PDF overlay
     */
    positionFormInputs: function() {
      const container = document.querySelector(this.containerSelector);
      if (!container) return;

      // Get all question blocks
      const questionBlocks = container.querySelectorAll('.question-block');
      const totalQuestions = this.questions.length;

      if (totalQuestions === 0) {
        console.warn('No questions provided for positioning');
        return;
      }

      // Calculate vertical spacing: distribute questions across page height
      const margin = 40; // Top/bottom margin in pixels
      const usableHeight = this.pageHeight - (2 * margin);
      const spacingPerQuestion = usableHeight / Math.max(totalQuestions, 1);

      // Position each question block
      questionBlocks.forEach((block, index) => {
        const yPosition = margin + (index * spacingPerQuestion);

        // Position the block absolutely on the canvas
        block.style.position = 'absolute';
        block.style.top = yPosition + 'px';
        block.style.left = '40px';
        block.style.width = (this.canvasHeight - 80) + 'px'; // Account for margins
        block.style.zIndex = 10 + index;

        // Slightly transparent background for visibility
        block.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        block.style.padding = '12px';
        block.style.borderRadius = '6px';
        block.style.border = '1px solid #cbd5e1';
        block.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
      });

      // Adjust container height to accommodate all elements
      container.style.height = (this.canvasHeight + 50) + 'px';
    },

    /**
     * Recalculate positions on window resize
     */
    handleResize: function() {
      if (this.pdfDoc) {
        this.positionFormInputs();
      }
    }
  };

  // Initialize on DOM ready
  document.addEventListener('DOMContentLoaded', function() {
    // Check if overlay should be initialized
    const container = document.querySelector('#pdf-overlay-container');
    if (container && container.dataset.pdfUrl) {
      const pdfUrl = container.dataset.pdfUrl;
      const questionsJson = container.dataset.questions || '[]';
      const questions = JSON.parse(questionsJson);

      window.PDFOverlay.init(pdfUrl, questions);
    }
  });

  // Handle window resize
  window.addEventListener('resize', function() {
    window.PDFOverlay.handleResize();
  });
})();
