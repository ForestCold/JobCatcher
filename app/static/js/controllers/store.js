Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    'selectedModule' : 'upload',
    'selectedResume' : 'none',
    'resumeList' : {},
    'uploadedResume' : 'none'
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
    updateResumeList (state, resumeInfo) {
      var selectedResumeInfo = resumeInfo;
      state.resumeList[state.selectedResume] = {
        'name' : resumeInfo.name,
        'domain' : resumeInfo.domain,
        'experience' : resumeInfo.experience,
        'type' : resumeInfo.type
      };
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
    addResumeInfo (state, resumeInfo) {
      this.commit("updateResumeList", resumeInfo);
    }
  }
})
