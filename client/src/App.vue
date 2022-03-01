<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/game">Game</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/login">Login</router-link> |
    </div>
    <router-view/>
  </div>
</template>

<style>
/* CSS part */

@import './assets/styles/style.css';
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300&display=swap');

#app {
  font-size: 20px; /* px means "pixels": the base font size is now 10 pixels high  */
  font-family: 'Oswald', sans-serif; 

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: black;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>