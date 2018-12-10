Vue.config.devtools = true;

var analysisArea = Vue.component('analysis-area', {
    components: {
      'preview' : preview,
      'keywords' : keywords
    },
    template: `
      <preview></preview>
      <keywords></keywords>
    `
})
