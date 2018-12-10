Vue.config.devtools = true;

var uploadArea = Vue.component('upload', {
    template: `
    <div class="area">
      <div class="row">
        <div id="upload-resume-area" class="col s12"></div>
      </div>

      <div id="modal1" class="modal modal-fixed-footer">
        <div class="modal-content">
          <div class="row">
            <form class="col s12">
            <span style="color:#a8a8a8">Add more information...</span>
              <div class="row">
                <div class="input-field col s6">
                  <input id="resume_name" type="text" class="validate" v-model="curResume.name">
                  <label for="resume_name">Resume Name</label>
                </div>
                <div class="input-field col s6">
                  <input id="domain" type="text" class="validate" v-model="curResume.domain">
                  <label for="domain">Domain</label>
                </div>
                <div class="input-field col s6">
                  <input id="work_experience" type="text" class="validate" v-model="curResume.experience">
                  <label for="work_experience">Work Experience</label>
                </div>
                <div class="input-field col s6">
                  <input id="job_type" type="text" class="validate" v-model="curResume.type">
                  <label for="job_type">Job Type</label>
                </div>
              </div>
            </form>
          </div>
        </div>
        <div class="modal-footer">
          <a href="#!" class="modal-action modal-close waves-effect waves-green btn-flat " v-on:click="resumeSubmit()">Submit</a>
        </div>
      </div>

    </div>
    `,
    data : function() {
      return {
        'curResume' : {
          'name' : "",
          'domain' : "",
          'experience' : "",
          'type' : ""
        },
        'selectedResume' : '',
        'resumeCompleteStatus' : true
      }
    },
    ready: function() {

      $('.modal').modal();

      var uppy = Uppy.Core();
      uppy.use(Uppy.Dashboard, {
              inline: true,
              width: '100%',
              height: '100%',
              target: '#upload-resume-area',
              allowMultipleUploads: false,
              hideCancelButton: false
          }).use(Uppy.XHRUpload, {
              endpoint: '/upload',
              fieldName: 'file'
          })

      this.renderUppy(uppy);

    },
    methods: {
      renderUppy(uppy) {
        var _this = this;
        uppy.on('file-added', (file) => {
          this.resumeCompleteStatus = false;
        }).on('complete', (result) => {
          var id = "uppy_" + result.successful[0].id;
          var name = result.successful[0].name;
          document.getElementById(id).onclick = function() {
            _this.selectedResume = "uploaded_files/" + name;
            store.dispatch('setSelectedResume', _this.selectedResume);
          };
          this.resumeCompleteStatus = true;
        }).on('upload-success', (file, response) => {
          this.selectedResume = response;
          $('#modal1').modal('open');
        })
      },
      resumeSubmit() {
        store.dispatch('setSelectedResume', this.selectedResume);
        store.dispatch('setUploadedResume', this.selectedResume);
        store.dispatch('addResumeInfo', this.curResume);
      }
    }
})
