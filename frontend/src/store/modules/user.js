import { login, register } from '@/api/api'

const state = {
  token: localStorage.getItem('token') || '',
  userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null')
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
  },
  SET_USER_INFO(state, userInfo) {
    state.userInfo = userInfo
    localStorage.setItem('userInfo', JSON.stringify(userInfo))
  },
  CLEAR_TOKEN(state) {
    state.token = ''
    state.userInfo = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }
}

const actions = {
  login({ commit }, userInfo) {
    return new Promise((resolve, reject) => {
      login(userInfo).then(response => {
        commit('SET_TOKEN', response.data.token)
        commit('SET_USER_INFO', response.data.user)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },
  register({ commit }, userInfo) {
    return new Promise((resolve, reject) => {
      register(userInfo).then(response => {
        commit('SET_TOKEN', response.data.token)
        commit('SET_USER_INFO', response.data.user)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },
  logout({ commit }) {
    commit('CLEAR_TOKEN')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

