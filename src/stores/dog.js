import { defineStore } from 'pinia'

export const useDogStore = defineStore('dog', {
  state: () => ({
    breeds: [],
  }),
  actions: {
    setBreeds(breeds) {
      this.breeds = breeds
    },
  },
})
