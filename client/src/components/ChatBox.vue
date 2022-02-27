<template>
  <div id="event-handling" class="demo" border="border">
      
      <ul>
        <li v-for="msg in state.rxmessages" :key="msg.id">{{msg}}</li>
      </ul>
      
      <p @click="changeTitle">{{ state.message }}</p>
      <input v-model="state.message" placeholder="Enter your message">
      <button v-on:click="sendServer">Send to server</button>
  </div>
</template>

<script setup>
import { reactive,onBeforeMount,onMounted, onUnmounted, inject} from 'vue'
//import { useChatMessageStore }from '@/stores/chatmessage.js'

        const ssocket = inject("ssocket")

        const state = reactive({
            message: "",
            rxmessages: []
        })

        function sendServer() {
            // Check the content of the message
            switch(state.message) {
                case "right":
                case "left":
                case "up":
                case "down":
                    ssocket.sendMove(state.message);
                    break;
                default:
                    ssocket.sendMessage(state.message);
            }
        }

        function changeTitle() {
            state.message = "ChatBox clicked message";
            console.log("Clicked title");
        }

        onMounted(() => {
            console.log("ChatBox Mounted");
            try {
                ssocket.socket.on("chatmsg",(data) => {
                    console.log(`${data}`);
                    let today = new Date();
                    let time = today.getHours() + ":" + String(today.getMinutes()).padStart(2, "0") + ":" + today.getSeconds();
                    let timemsg = time + " " + data;
                    state.rxmessages.push(timemsg);
                });
                console.log("ChatBox connected"); 
            } catch(err){
                alert(err.message);
            }
            
        })

        onBeforeMount(() => {
            console.log('onBeforeMount : message is ' + state.message)
        })
        
        onUnmounted(() => {
            console.log('onUnmounted: Chatbox unmounted');
        })
        
</script>


<style>
.demo {
    user-select: none;
    border: 2px solid greenyellow;
    width: fit-content;
    border-style: dashed;
}
</style>