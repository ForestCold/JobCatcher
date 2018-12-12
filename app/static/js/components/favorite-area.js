Vue.config.devtools = true;

var favoriteArea = Vue.component('favorite-area', {
    template: `
      <div class="area">
        </br><ul class="collapsible popout" data-collapsible="expandable" style="margin-top: 20px">
          <li v-for="job in jobList">
            <div class="collapsible-header" style="font-weight: 600; display: block">
              <div style="display: block; color: #3d5165">
              <i class="material-icons" style="color: #3d5165">{{job.icon}}</i>
                <span style="font-weight: 600; vertical-align: top">{{job.Company}}</span>
                <span style="font-weight: 400; color: #89c3b0; display: block; float: right"> {{job.Location}}</span>
              </div>
              <span style="font-weight: 300; display: block"> {{job.Position}}</span>
            </div>
            <div class="collapsible-body">
              <span>Description</span>
              <span>{{job.Description}}</span>
              </br></br><a class="waves-effect waves-light btn" href={{job.Url}} target="_blank">Apply</a>
            </div>
          </li>
        </ul>
      </div>
    `,
    ready : function() {
      $('.collapsible').collapsible();
      this.favorite(this.selectedResume);
    },
    data: function(){
      return {
        selectedResume : '',
        jobList : [],
        favoriteJobs : {}
      }
    },
    methods : {
      favorite(resume) {
        this.jobList = this.favoriteJobs[resume];
      }
    },
    computed: {
      selectedResume() {
        return store.state.selectedResume;
      },
      favoriteJobs() {
        return store.state.favoriteJobs;
      }
    },
    watch: {
      selectedResume: function(newResume, oldResume) {
        if (newResume != oldResume) {
          this.favorite(newResume);
        }
      }
    }
})
