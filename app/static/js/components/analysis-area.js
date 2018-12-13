Vue.config.devtools = true;

var analysisArea = Vue.component('analysis-area', {
    components: {
      'preview' : preview,
      'keywords' : keywords
    },
    template: `
      <div class="row" style="margin-left:240px">
        <preview></preview>
        <keywords></keywords>
      </div>
    `
})
