Vue.config.devtools = true;

var recommendationArea = Vue.component('recommendation-area', {
    components: {
      'job-ranks' : jobRanks
    },
    template: `
      <job-ranks></job-ranks>
    `
})
