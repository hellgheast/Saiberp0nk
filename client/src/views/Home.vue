<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <basic-page flavour="Vue version on WSL" />
    <hello-world msg="Welcome to Your Vue.js 3 App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import BasicPage  from '@/components/BasicPage.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld,
    BasicPage,
  }
}
</script>
