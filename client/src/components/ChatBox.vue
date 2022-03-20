<template>
  <div id="event-handling" class="demo" border="border">
    <div class="chatText">
      <ul class="chatListStyle">
        <li v-for="msg in state.rxmessages" :key="msg.id">{{msg}}</li>
      </ul>
    </div>
    <textarea v-model="state.message" v-on:keypress.enter.prevent="sendServer" rows="4" cols="50" placeholder="Enter your message"></textarea>
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
    border: 2px solid rgb(47, 189, 255);
    width: fit-content;
    height: fit-content;
    border-style: solid;
}

.chatText {
    height: 350px;
    min-width: 200px;
    border:1px solid grey;
    overflow-y: scroll;
}

.chatListStyle {
    list-style-type:none;
}

</style>