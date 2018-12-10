Vue.config.devtools = true;

var jobRanks = Vue.component('job-ranks', {
    template: `
    <div class="area">
    <span style="color:#a8a8a8">We find some exciting opportunities for you!</span>
    <ul class="collapsible popout" data-collapsible="expandable">
      <li>
        <div class="collapsible-header active"><i class="material-icons">filter_drama</i>First</div>
        <div class="collapsible-body"><span>Lorem ipsum dolor sit amet.</span></div>
      </li>
      <li>
        <div class="collapsible-header active"><i class="material-icons">place</i>Second</div>
        <div class="collapsible-body"><span>Lorem ipsum dolor sit amet.</span></div>
      </li>
    </ul>
    </div>
    `,
    ready : function() {
      $('.collapsible').collapsible();
    }
})
