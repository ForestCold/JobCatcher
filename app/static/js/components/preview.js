Vue.config.devtools = true;

var preview = Vue.component('preview', {
    template: `
      <div id="preview-area"></div>
    `,
    data: {
      pdfUrl : ''
    },
    ready: function() {
      this.renderPDF(this.pdfUrl);
    },
    methods: {
      renderPDF(url) {
        var options = {
          height: "400px",
          page: '2',
          pdfOpenParams: {
            view: 'FitV',
            pagemode: 'thumbs',
            search: 'lorem ipsum'
          }
        };
        PDFObject.embed(url, "#preview-area", options);
      }
    },
    computed: {
      pdfUrl() {
        return store.state.pdfUrl;
      }
    },
    watch: {
      pdfUrl: function(newUrl, oldUrl) {
        if (newUrl != oldUrl) {
          this.renderPDF(newUrl);
        }
      }
    }
})
