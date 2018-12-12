Vue.config.devtools = true;

var app = new Vue({
    el: '#app',
    store,
    components: {
      'head-nav' : headNav,
      'side-nav' : sideNav,
      'analysis-area' : analysisArea,
      'recommendation-area' : recommendationArea,
      'favorite-area' : favoriteArea
    },
    template: `
      <side-nav></side-nav>
      <head-nav></head-nav>
      <analysis-area v-if="selectedModule=='analysis'"></analysis-area>
      <recommendation-area v-if="selectedModule=='recommendation'"></recommendation-area>
      <favorite-area v-if="selectedModule=='favorite'"></favorite-area>
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
