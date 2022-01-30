<template>
  <div id="event-handling" class="demo" border="border">
      
      <ul>
        <li v-for="msg in rxmessages" :key="msg.id">{{msg}}</li>
      </ul>
      
      <p @click="changeTitle">{{ message }}</p>
      <input v-model="message" placeholder="Enter your message">
      <button v-on:click="sendServer">Send to server</button>
  </div>
</template>

<script>
import SocketService from '../scripts/socketio.service.js'

export default {
    name: "ChatBox",
    props: {

    },
    data: function() {
        return {
            message: "",
            rxmessages: []
        }
    },
    // state functions
    created() {
        console.log('created : message is ' + this.message)
    },
    mounted(){
        SocketService.socket.on("chatmsg",(data) => {
            console.log(`${data}`);
            var today = new Date();
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            let timemsg = time + " " +data;
            this.rxmessages.push(timemsg);
        });
    },
    unmounted() {
        console.log('unmounted component');
    },
    // internal methods of the component
    methods: {
        sendServer() {
            SocketService.sendMessage(this.message);
        },
        changeTitle() {
            this.message = "ChatBox clicked message";
            console.log("Clicked title");
        }
    }


}
</script>


<style>
.demo {
    user-select: none;
    border: 2px solid greenyellow;
    width: fit-content;
    border-style: dashed;
}
</style>