Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    'module' : 'index',
    'pdfUrl' : 'none'
  },
  mutations: {
    updateModule(state, moduleName) {
      state.module = moduleName;
    },
    updatePdfUrl(state, pdfUrl) {
      state.pdfUrl = pdfUrl;
    }
  },
  actions: {
    setModule (state, moduleName) {
      this.commit("updateModule", moduleName);
    },
    setPdfUrl (state, pdfUrl) {
      this.commit("updatePdfUrl", pdfUrl);
    }
  }
})
