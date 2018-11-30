Vue.config.devtools = true;

Vue.component('side-nav', {
    template: `
    <ul id="slide-out" class="side-nav fixed">
        <li><div class="user-view">
          <div class="background" style="background-color: #3d5165">
          </div>
          <a href="#!user"><img class="rect" src="images/icon-img.png"></a>
          <a href="#!name"><span class="white-text name">Job Catcher</span></a>
          <a href="#!email"><span class="white-text email">Description</span></a>
        </div></li>
        <li><a href="upload.html"><i class="material-icons">person_pin</i>Resume Analysis</a></li>
        <li><a href="#!"><i class="material-icons">search</i>Job Recommendation</a></li>
        <li><div class="divider"></div></li>
        <li><a class="subheader">Profile</a></li>
        <li><a class="waves-effect" href="#!">Uploaded Resume</a></li>
        <li><a class="waves-effect" href="#!">Search History</a></li>
      </ul>
      <a href="#" data-activates="slide-out" class="button-collapse"><i class="material-icons">menu</i></a>
    `
})
