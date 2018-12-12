Vue.config.devtools = true;

var sideNav = Vue.component('side-nav', {
    template: `
    <ul id="slide-out" class="side-nav fixed">
        <li><div class="user-view">
          <div class="background" style="background:#495a6e">
          </div>
          <a href="#!user"><img class="rect" src="images/icon.png" style="width: 80px; height: 80px"></a>
          <a href="#!name"><span class="white-text name">Job Catcher</span></a>
          <a href="#!email"><span class="white-text email">About Us</span></a>
        </div></li>
        <li><div style="height: 45px"><a class="subheader" style="float:left; margin-left: 20px">Upload Resumes</a>
          <div class="UppyForm" style="float:right; margin-right: 10px"></div></div></li>
        <li><div class="divider"></div></li>
        <li v-for="resume in resumeShowList" v-on:click="resumeSelected(resume)" v-bind:class="{'active':(resume === selectedResume)}">
          <a href="#!" style="color:#3d5165">
            <i class="material-icons" style="color:#495a6e; margin-right: 10px !important">attach_file</i>
          {{resume}}</a>
        </li>
      </ul>
    `,
    data: function(){
      return {
        resumeShowList : ["example.pdf"],
        selectedResume : 'example.pdf',
        resumeCompleteStatus : true
      }
    },
    ready : function() {

      var uppy = new Uppy.Core({
        debug: true,
        autoProceed: true,
        restrictions: {
          allowedFileTypes: [".pdf"]
        }
      });

      uppy.use(Uppy.FileInput, { target: '.UppyForm', replaceTargetContent: false })
          .use(Uppy.XHRUpload, {
              endpoint: '/upload',
              fieldName: 'file'
          });

      $(".uppy-FileInput-btn").append("<i class='material-icons' style='color:#495a6e'>add</i>");

      uppy.use(Uppy.ProgressBar, {
        target: 'body',
        fixed: true,
        hideAfterFinish: false
      });

      this.renderUppy(uppy);
    },
    methods: {
      resumeSelected : function(name) {
        store.dispatch('setSelectedResume', name);
        this.selectedResume = name;
      },
      renderUppy(uppy) {
        uppy.on('upload-success', (file, response) => {
          this.selectedResume = file.name;
          store.dispatch('setSelectedResume', this.selectedResume);
          store.dispatch('setUploadedResume', this.selectedResume);
        })
      }
    },
    computed: {
      uploadedResume() {
        return store.state.uploadedResume;
      },
      resumeList() {
        return store.state.resumeList;
      }
    },
    watch: {
      uploadedResume: function(newResume, oldResume) {
        this.resumeShowList.push(newResume);
      }
    }
})
