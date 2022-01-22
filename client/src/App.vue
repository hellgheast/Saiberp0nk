<template>
  <div id="app">
    <!--All the application is inside here ?-->
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <!-- <basic-page flavour="Vue version" /> -->

  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import BasicPage  from './components/BasicPage.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    BasicPage
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
