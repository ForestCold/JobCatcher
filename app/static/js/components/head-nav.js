Vue.config.devtools = true;

var headNav = Vue.component('head-nav', {
    template: `
    <div class="navbar-fixed">
      <nav>
  			<div class="nav-wrapper grey lighten-5">
  				<a href="#" class="brand-logo">Logo</a>
          <ul id="nav-mobile" class="right hide-on-med-and-down">
            <li v-for="module in modules" v-on:click="moduleActive(module.name)" v-bind:class="{'active':(module.name === curModule)}">
              <a href="#!"><i class="material-icons" style="color:#495a6e">{{module.icon}}</i>
            </li>
          </ul>
  			</div>
  		</nav>
    </div>
    `,
    data: function(){
      return {
        'modules' : [{
          'name' : 'home',
          'text' : 'Home',
          'icon' : 'home'
        },{
          'name' : 'analysis',
          'text' : 'Analysis',
          'icon' : 'pageview'
        },{
          'name' : 'recommendation',
          'text' : 'Recommendation',
          'icon' : 'sort'
        },{
          'name' : 'favorite',
          'text' : 'Favorite',
          'icon' : 'favorite'
        }],
        curModule : 'analysis'
      }
    },
    methods: {
      moduleActive : function(name) {
        if (name == "home") {
          window.location.href="index.html";  
        } else {
          this.curModule = name;
          store.dispatch('setSelectedModule', name);
        }
      }
    }
})
