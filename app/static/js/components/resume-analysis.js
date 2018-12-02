Vue.config.devtools = true;

var resumeAnalysis = Vue.component('resume-analysis', {
    components: {
      'preview' : preview,
      'keywords' : keywords
    },
    template: `
      <preview></preview>
      <keywords></keywords>
    `
})
