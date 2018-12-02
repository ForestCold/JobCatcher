Vue.config.devtools = true;

var app = new Vue({
    el: '#app',
    store,
    components: {
      'side-nav' : sideNav,
      'upload' : upload,
      'resume-analysis' : resumeAnalysis
      // 'job-recommendation' : jobRecommendation
    },
    template: `
      <side-nav></side-nav>
      <upload></upload>
      <resume-analysis v-if="moduleName=='resumeAnalysis'"></resume-analysis>
    `,
    data: function() {
    },
    ready: function() {
    },
    methods: {

    },
    computed: {
        moduleName () {
          return store.state.module;
        }
    }
})
