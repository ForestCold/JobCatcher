Vue.config.devtools = true;

var sideNav = Vue.component('side-nav', {
    template: `
    <ul id="slide-out" class="side-nav fixed">
        <li><div class="user-view">
          <div class="background" style="background-color: #3d5165">
          </div>
          <a href="#!user"><img class="rect" src="images/icon-img.png"></a>
          <a href="#!name"><span class="white-text name">Job Catcher</span></a>
          <a href="#!email"><span class="white-text email">About Us</span></a>
        </div></li>
        <li v-for="resume in resumeShowList" v-on:click="resumeSelected(resume)" v-bind:class="{'active':(resume === curResume)}">
          <a href="#!" style="color:#3d5165">
            <i class="material-icons" style="color:#495a6e">description</i>
          {{resumeList[resume].name}}</a>
        </li>
      </ul>
    `,
    data: function(){
      return {
        resumeShowList : [],
        curResume : 'none'
      }
    },
    methods: {
      resumeSelected : function(name) {
        store.dispatch('setSelectedResume', name);
        this.curResume = name;
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
        if (newResume != oldResume) {
          for (resume in store.state.resumeList) {
            this.resumeShowList.push(resume);
          }
        }
      }
    }
})
