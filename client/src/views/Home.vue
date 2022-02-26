<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <basic-page flavour="Vue version on WSL" />
    <chat-box/>
    <hello-world msg="Welcome to Your Vue.js 3 App"/>
    <script-page flavour="Script"/> 

  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import BasicPage  from '@/components/BasicPage.vue'
import ScriptPage from '@/components/ScriptPage.vue'
import ChatBox from '@/components/ChatBox.vue'
import SocketService from '@/scripts/socketio.service.js'

export default {
  name: 'Home',
  components: {
    HelloWorld,
    ChatBox,
    BasicPage,
    ScriptPage
  },
  created() {
    if(SocketService.connected()){
      console.log("Already connected");
    }
    else {
      SocketService.setupSocketConnection();
      SocketService.addListener();
    }
  },
  beforeUnmount() {
    SocketService.disconnect();
  }
}
</script>
