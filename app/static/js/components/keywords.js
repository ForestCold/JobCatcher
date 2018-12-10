Vue.config.devtools = true;

var keywords = Vue.component('keywords', {
    template: `
      <div class="chips chips-initial"></div>
    `,
    data: {
      selectedResume : ''
    },
    ready: function() {
      this.reload(this.selectedResume);
    },
    methods: {
      reload : function(selectedResume) {
        $.ajax({
            method: 'GET',
            url: 'analysis/' + selectedResume.replace("uploaded_files/", ""),
            success: function(resp) {
                if (!resp || resp.status !== "success") {
                    resp = $.parseJSON(resp)
                    var data = [];
                    for (r in resp) {
                      word = {'tag' : resp[r]}
                      data.push(word)
                    }
                    $('.chips-initial').material_chip({
                      data: data
                    });
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
          this.reload(newResume);
        }
      }
    }
})
