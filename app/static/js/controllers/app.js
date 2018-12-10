Vue.config.devtools = true;

var app = new Vue({
    el: '#app',
    store,
    components: {
      'head-nav' : headNav,
      'side-nav' : sideNav,
      'upload-area' : uploadArea,
      'analysis-area' : analysisArea,
      'recommendation-area' : recommendationArea
    },
    template: `
      <side-nav></side-nav>
      <head-nav></head-nav>
      <upload-area v-if="selectedModule=='upload'"></upload-area>
      <analysis-area v-if="selectedModule=='analysis'"></analysis-area>
      <recommendation-area v-if="selectedModule=='recommendation'"></recommendation-area>
    `,
    data: function() {
    },
    ready: function() {
      
    },
    methods: {

    },
    computed: {
      selectedModule () {
        return store.state.selectedModule;
      }
    }
})
