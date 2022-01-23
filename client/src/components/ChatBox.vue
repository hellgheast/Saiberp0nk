<template>
  <div id="event-handling" class="demo" border="border">
      <p @click="changeTitle">{{ message }}</p>
      <input v-model="message">
      <button v-on:click="sendServer">Send to server</button>
  </div>
</template>

<script>
export default {
    name: "ChatBox",
    props: {

    },
    data: function() {
        return {
            message: "Welcome to Chatbox"
        }
    },
    // state functions
    created() {
        console.log('mounted : message is ' + this.message)
    },
    unmounted() {
        console.log('unmounted component');
    },
    // internal methos of the component
    methods: {
        sendServer() {
            this.message = this.message
                                .split('')
                                .reverse()
                                .join('');
        },
        changeTitle() {
            this.message = "ChatBox clicked message";
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