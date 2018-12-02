Vue.config.devtools = true;

var sideNav = Vue.component('side-nav', {
    template: `
    <ul id="slide-out" class="side-nav fixed">
        <li><div class="user-view">
          <div class="background" style="background-color: #3d5165">
          </div>
          <a href="#!user"><img class="rect" src="images/icon-img.png"></a>
          <a href="#!name"><span class="white-text name">Job Catcher</span></a>
          <a href="#!email"><span class="white-text email">Description</span></a>
        </div></li>
        <li v-for="module in modules" v-on:click="moduleActive(module.name)">
          <a href="#!"><i class="material-icons">{{module.icon}}</i>{{module.text}}
        </li>
        <li><div class="divider"></div></li>
        <li><a class="subheader">Profile</a></li>
        <li><a class="waves-effect" href="#!">Uploaded Resume</a></li>
        <li><a class="waves-effect" href="#!">Search History</a></li>
      </ul>
      <a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
    `,
    data: function(){
      return {
        'modules' : [{
          'name' : 'resumeAnalysis',
          'text' : 'Resume Analysis',
          'icon' : 'person_pin'
        },{
          'name' : 'jobRecommendation',
          'text' : 'Job Recommendation',
          'icon' : 'search'
        }]
      }
    },
    methods: {
      moduleActive : function(name) {
        store.dispatch('setModule', name);
      }
    }
})
