<template>
    <div>
    <h1>LOGIN</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="username" />
      <br />
      <br />
      <input v-model="password" placeholder="password" type="password" />
      <br />
      <br />
      <button @click="login" type="submit">Login</button>
    </form>
  </div>
</template>

<style>
</style>

<script setup>
import { ref } from 'vue';

const username = ref('');
const password = ref('');

function login() {
    fetch("http://localhost:3000/login",{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value
        })
    })
}


</script>