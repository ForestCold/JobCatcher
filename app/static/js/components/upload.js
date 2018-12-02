Vue.config.devtools = true;

var upload = Vue.component('upload', {
    template: `
      <div id="upload-area"></div>
    `,
    ready: function() {
      var uppy = Uppy.Core()
          .use(Uppy.Dashboard, {
              inline: true,
              width: '100%',
              height: '100%',
              target: '#upload-area'
          })
          .use(Uppy.XHRUpload, {
              endpoint: '/upload',
              fieldName: 'file'
      });
      this.renderUppy(uppy);
    },
    methods: {
      renderUppy(uppy) {
        uppy.on('complete', (result) => {
            console.log(result)
        }).on('upload-success', (file, response) => {
          store.dispatch('setPdfUrl', response);
        })
      }
    }
})
