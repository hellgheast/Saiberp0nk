<template>
  <div class="game">
    <img alt="Vue logo" src="../assets/logo.png">
    <h1>Testing game page</h1>
    <chat-box/>
    <script-page flavour="Script"/> 

  </div>
</template>

<script>
// @ is an alias to /src
import ChatBox from '@/components/ChatBox.vue'
import ScriptPage from '@/components/ScriptPage.vue'
import SocketService from '@/scripts/socketio.service.js'

export default {
  name: 'Game',
  components: {
    ChatBox,
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
