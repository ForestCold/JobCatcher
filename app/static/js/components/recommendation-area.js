Vue.config.devtools = true;

var recommendationArea = Vue.component('recommendation-area', {
    template: `
    <div class="area">

      <div class="row" style="margin-left:20px; margin-right:20px">
        <div class="input-field col s3">
          <select>
            <option value="" disabled>Experience</option>
            <option>Entry Level</option>
            <option>Less Than Two Years</option>
            <option>Two To Five Years</option>
            <option>More Than Five Years</option>
          </select>
        </div>
        <div class="input-field col s3">
          <input type="text" class="validate" v-model="location">
          <label for="location">Location</label>
        </div>
        <div class="input-field col s3">
          <form action="#">
             <p class="range-field">
               <input type="range" id="test5" min="0" max="100" v-model="number"/>
             </p>
          </form>
          <span style="color:#495a6e">Show Top {{number}} Jobs</span>
        </div>
        <div class="input-field col s3">
          <a class="waves-effect waves-light btn" style="background-color:#78c5af; float:right" v-on:click="searchActive()">
          <i class="material-icons left">search</i>Search</a>
        </div>

      </div>
      <ul class="collapsible popout" data-collapsible="expandable" style="margin-top: 20px">
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
            <span>{{job.Description}}</span>
            </br></br><a class="waves-effect waves-light btn" href={{job.Url}} target="_blank">Apply</a>
            <a href="#!" class="secondary-content" v-on:click="favorite(job)" v-if="!job.favorite"><i class="material-icons" style="color:#ff7961">favorite_border</i></a>
            <a href="#!" class="secondary-content" v-on:click="favorite(job)" v-if="job.favorite"><i class="material-icons" style="color:#ff7961">favorite</i></a>
          </div>
        </li>
      </ul>
    </div>
    `,
    data: function(){
      return {
        selectedResume : '',
        jobList : [],
        location : "",
        number : 10
      }
    },
    ready : function() {
      $('.collapsible').collapsible();
      $('select').material_select();
      this.recommend(this.selectedResume);
    },
    methods : {
      recommend : function(resume) {
        var _this = this;
        if (this.selectedResume in store.state.allJobs) {
          var allJobs = store.state.allJobs[this.selectedResume];
          for (index in allJobs) {
            Vue.set(this.jobList, parseInt(allJobs[index].id), allJobs[index]);
          }
          return;
        }
        $.ajax({
            method: 'GET',
            url: 'recommend/' + resume.replace("uploaded_files/", ""),
            success: function(resp) {
                if (!resp || resp.status !== "success") {
                    resp = JSON.parse(resp);
                    _this.jobList = {};
                    for (job in resp) {
                      resp[job]['icon'] = 'vpn_key';
                      resp[job]['id'] = job;
                      resp[job]['favorite'] = false;
                      Vue.set(_this.jobList, parseInt(job), resp[job]);
                    }
                    store.dispatch('setAllJobs', {
                      'job' : resp,
                      'resume' : _this.selectedResume
                    });
                    return;
                }
            },error: function() {

            }
        });
      },
      favorite : function(job) {
        job['favorite'] = !job['favorite'];
        store.dispatch('setFavoriteJobs', {
          'job' : job,
          'resume' : this.selectedResume
        });
      },
      searchActive : function() {
        var experience = "All levels";
        if ($('li.active.selected')[0]) {
          experience = $('li.active.selected')[0].children[0].innerHTML;
        }
        var _this = this;
        var searchData = {
          "location" : _this.location,
          "number" : _this.number,
          "experience" : experience,
          'resume' : _this.selectedResume
        }

        console.log(searchData)

        $.ajax({
            method: 'GET',
            url: 'update_recommendation/' + JSON.stringify(searchData),
            processData: false,
            contentType: false,
            success: function(resp) {
                if (!resp || resp.status !== "success") {
                    console.log(resp);
                    return;
                }
            },error: function() {

            }
        });
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
          this.recommend(newResume);
        }
      }
    }
})
