<template>
  <div class="game">
    <img alt="Vue logo" src="../assets/logo.png">
    <h1>Testing game page</h1>
    <chat-box/>
    <canvas
        ref="game_map"
        width="400"
        height="400"
        style="border: 1px solid greenyellow">
    </canvas>
    <script-page flavour="Script"/> 

  </div>
</template>

<script setup>

import SocketService from '@/scripts/socketio.service.js'

// Importing components makes them availables in the template side
// @ is an alias to /src
import ChatBox from '@/components/ChatBox.vue'
import ScriptPage from '@/components/ScriptPage.vue'

import { provide,ref,reactive,onMounted, onBeforeUnmount} from 'vue'


    const state = reactive({
        context:{},
        players:[],
    })
    // retrieving a DOM element in the javascript part
    const game_map = ref(null);

    console.log("Setup socket in Game");
    SocketService.setupSocketConnection();
    
    provide("ssocket",SocketService);


    function drawPlayers() {
        console.log(state.players);
        state.context.clearRect(0,0,game_map.value.width,game_map.value.height);
        Array.from(state.players).forEach(function({x, y, size, c}) {
            state.context.beginPath();
            state.context.rect(x, y, size, size);
            state.context.fillStyle = c;
            state.context.fillRect(x,y,size,size);
            state.context.fill();
        });
    }

    onMounted(() => {
        console.log("onMounted Game");
        if(SocketService.connected()){
            console.log("Already connected");
            state.context = game_map.value.getContext("2d");
        }
        else {
            console.log("Game component init");
            SocketService.addListener();
            state.context = game_map.value.getContext("2d");
            SocketService.socket.on("players_list",(data) =>{
                state.players = data;
                drawPlayers();
            });
            SocketService.requestPosition();
        }
     })

    onBeforeUnmount(() => {
        SocketService.disconnect();
    })

</script>
