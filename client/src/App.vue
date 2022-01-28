<template>
  <div id="app">
    <!--All the application is inside here ?-->
    <basic-page flavour="Vue version on WSL" />
    <chat-box/>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <script-page flavour="Script"/> 

  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import BasicPage  from './components/BasicPage.vue'
import ScriptPage from './components/ScriptPage.vue'
import ChatBox from './components/ChatBox.vue'
import SocketService from './scripts/socketio.service.js'

export default {
  
  name: 'App',
  components: {
    HelloWorld,
    ChatBox,
    BasicPage,
    ScriptPage
  },
  created() {
    console.log("Tried connection");
    SocketService.setupSocketConnection();
    SocketService.addListener();
  },
  beforeUnmount() {
    SocketService.disconnect();
  }
}
</script>

<style>

/* CSS part */

@import './assets/styles/style.css';

@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300&display=swap');

#app {
  font-size: 20px; /* px means "pixels": the base font size is now 10 pixels high  */
  font-family: 'Oswald', sans-serif; 

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: black;
}
</style>
