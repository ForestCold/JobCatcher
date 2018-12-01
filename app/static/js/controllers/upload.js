Vue.config.devtools = true;

var app = new Vue({
    el: '#upload',
    data: function() {
    },
    ready: function() {

      $('.sidenav').sideNav();
      $('.collapsible').collapsible();

      var uppy = Uppy.Core()
          .use(Uppy.Dashboard, {
              inline: true,
              width: '100%',
              height: '100%',
              target: '#upload-drag'
          })
          .use(Uppy.XHRUpload, {
            endpoint: '/upload',
            fieldName: 'file'
      });

      this.renderUppy(uppy);

    },
    methods: {
      renderUppy: function(uppy) {
        uppy.on('complete', (result) => {
            console.log(result)
        }).on('upload-success', (file, response) => {
          this.renderPDF(response);
          this.showKeyWords(response);
        })
      },
      renderPDF: function(url) {
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
      },
      showKeyWords: function(url) {
        $.ajax({
            method: 'GET',
            url: 'analysis/' + url.replace("uploaded_files/", ""),
            success: function(resp) {
                if (!resp || resp.status !== "success") {
                    resp = $.parseJSON(resp)
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
    }
})
