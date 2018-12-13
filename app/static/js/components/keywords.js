Vue.config.devtools = true;

var keywords = Vue.component('keywords', {
    template: `
      <div class="col s6">
        <div class="col s12" style="padding-top:50px; height:300px"><canvas id="chart"></canvas></div>
        <div class="chips chips-initial col s12"></div>
      </div>
    `,
    data: {
      selectedResume : ''
    },
    ready: function() {
      this.reload(this.selectedResume);
    },
    methods: {
      reload : function(selectedResume) {
        var _this = this;
        $.ajax({
            method: 'GET',
            url: 'analysis/' + selectedResume,
            success: function(resp) {
                if (!resp || resp.status !== "success") {
                    resp = $.parseJSON(resp)
                    _this.renderChart(resp);
                    return;
                }
            },error: function() {

            }
        });
      },
      renderChart : function(resp) {
        var _this = this;
        var data = {
          "datasets" : [{"data" : [], "backgroundColor" : []}],
          "labels" : [],
        }
        for (index in Object.keys(resp)) {
          var position = Object.keys(resp)[index];
          data.datasets[0].data.push(resp[position].percentage.toFixed(2));
          data.labels.push(position);
          data.datasets[0].backgroundColor.push(colorbrewer.self[1][index]);
        }
        console.log(data)

        var myNewChart = new Chart("chart", {
            type: 'doughnut',
            data: data
        });

        $("#chart").click(
          function(evt){
            var activePoints = myNewChart.getElementsAtEvent(evt);
            var chartData = activePoints[0]['_chart'].config.data;
            var idx = activePoints[0]['_index'];
            var label = chartData.labels[idx];
            _this.renderWords(resp[label].words)
          });
        },
        renderWords : function(words) {
          var data = [];
          for (r in words) {
            word = {'tag' : words[r]}
            data.push(word)
          }
          console.log(data)
          $('.chips-initial').material_chip({
            data: data
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
