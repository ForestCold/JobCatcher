Vue.config.devtools = true;

var preview = Vue.component('preview', {
    template: `
      <div id="preview-area" class="col s6"></div>
    `,
    ready: function() {
      this.renderPDF(this.selectedResume);
    },
    methods: {
      renderPDF(url) {
        url = "uploaded_files/" + url;
        var options = {
          height: "600px",
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
      selectedResume() {
        return store.state.selectedResume;
      }
    },
    watch: {
      selectedResume: function(newResume, oldResume) {
        if (newResume != oldResume) {
          this.renderPDF(newResume);
        }
      }
    }
})
