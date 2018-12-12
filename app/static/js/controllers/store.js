Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    'selectedModule' : 'analysis',
    'selectedResume' : 'example.pdf',
    'favoriteJobs' : {},
    'uploadedResume' : 'example.pdf',
    'allJobs' : {}
  },
  mutations: {
    updateSelectedModule (state, selectedModule) {
      state.selectedModule = selectedModule;
    },
    updateSelectedResume (state, selectedResume) {
      state.selectedResume = selectedResume;
    },
    updateUpdatedResume (state, uploadedResume) {
      state.uploadedResume = uploadedResume;
    },
    updateFavoriteJobs (state, data) {
      var resume = data.resume;
      var job = data.job;
      if (! (resume in state.favoriteJobs)) {
        state.favoriteJobs[resume] = {};
      }
      if (job.favorite) {
        state.favoriteJobs[resume][job.id] = job;
      } else {
        delete state.favoriteJobs[resume][job.id]
      }
    },
    updateAllJobs (state, data) {
      var resume = data.resume;
      var jobs = data.job;
      state.allJobs[resume] = {}
      for (index in jobs) {
        state.allJobs[resume][jobs[index].id] = jobs[index]
      }
    }
  },
  actions: {
    setSelectedModule (state, selectedModule) {
      this.commit("updateSelectedModule", selectedModule);
    },
    setSelectedResume (state, selectedResume) {
      this.commit("updateSelectedResume", selectedResume);
    },
    setUploadedResume (state, uploadedResume) {
      this.commit("updateUpdatedResume", uploadedResume);
    },
    setFavoriteJobs (state, data) {
      this.commit("updateFavoriteJobs", data);
    },
    setAllJobs (state, data) {
      this.commit("updateAllJobs", data);
    }
  }
})
