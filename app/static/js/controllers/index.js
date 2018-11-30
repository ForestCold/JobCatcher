Vue.config.devtools = true;

var app = new Vue({
    el: '#app',
    data: function() {
    },
    ready: function() {
      $('.sidenav').sideNav();
      $('.collapsible').collapsible();
    },
    methods: {
    }
})
