Vue.config.devtools = true;

var keywords = Vue.component('keywords', {
    template: `
      <div id = "keyword-area"></div>
    `,
    data: {
      pdfUrl : ''
    },
    ready: function() {
      this.reload(this.pdfUrl);
    },
    methods: {
      reload : function(url) {
        $.ajax({
            method: 'GET',
            url: 'analysis/' + url.replace("uploaded_files/", ""),
            success: function(resp) {
                if (!resp || resp.status !== "success") {
                    resp = $.parseJSON(resp)
                    $(".cloud-tags").remove();
                    $("#keyword-area").append("<ul class=\"cloud-tags\">");
                    for (keyword in resp) {
                      $(".cloud-tags").append("<li> <a href=\"#tag_lin\">" + resp[keyword] + "</a> </li>");
                    }
                    $(".cloud-tags").prettyTag({
                      randomColor: false
                    });
                    return;
                }
            },error: function() {

            }
        });
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
          this.reload(newUrl);
        }
      }
    }
})
