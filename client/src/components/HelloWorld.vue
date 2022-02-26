<template>
  <div class="hello">
    <h1>{{ msg }}</h1>

    <p>The main goal of this prototype is</p>

    <ul>
        <li>To experiment with web technologies</li>
        <li>Understand the interaction of back-end and front-end</li>
        <li>Have some fun building a game for my habibis</li>
    </ul>

    <h2>Logos</h2>
    <p>Short logo</p>
    <img src="../assets/logo.png" alt="My glorious logo">
    <p>Extended logo</p>
    <img src="../assets/Sponk.png" alt="My glorious logo">
  </div>
</template>

<script setup>
import {defineProps} from 'vue'
defineProps(['msg'])
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
