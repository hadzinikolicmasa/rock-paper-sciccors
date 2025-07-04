<template>
  <div class="app-container">
    <div class="content-box">
      <h1 v-if="!showSinglePlayer && !showMultiPlayer">Welcome to RPSLS Game</h1>

      <RegisterForm v-if="!showSinglePlayer && !showMultiPlayer" />
      <SinglePlayer v-if="showSinglePlayer" @back="handleBack" />
      <MultiPlayer v-if="showMultiPlayer" @back="handleBack" />

      <button v-if="!showMultiPlayer && !showSinglePlayer" @click="startSinglePlayer" class="action-button">
        Start Single Player
      </button>

       <button v-if="!showMultiPlayer && !showSinglePlayer" class="action-button" @click="startMultiPlayer">
        Start Multi Player
      </button>
    </div>
  </div>
</template>

<script>
import RegisterForm from './components/Register.vue'
import SinglePlayer from "./components/SinglePlayer.vue";
import MultiPlayer from "./components/MultiPlayer.vue";

export default {
  name: 'App',
  components: {
    RegisterForm, SinglePlayer, MultiPlayer
  },
  data() {
    return {
      showSinglePlayer: false,
      showMultiPlayer: false
    };
  },
  methods: {
    startSinglePlayer() {
      this.showSinglePlayer = true;
    },
    startMultiPlayer() {
      this.showMultiPlayer = true;
    },
    handleBack() {
      this.showSinglePlayer = false;
      this.showMultiPlayer = false;
    }
  },
};
</script>

<style >

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

body {
  font-family:  sans-serif;
  background-image: url('../public/assets/background.png');
  background-size: cover;
  background-repeat: repeat;
  background-position: center;
  min-height: 150vh;
  width: 100vw;
  overflow-x: hidden;
}

.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.content-box {
  background: rgba(255, 255, 255, 0.85);
  padding: 40px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 90%;
}

h1 {
  margin-bottom: 2rem;
  font-size: 2rem;
  color: #333;
}

.action-button {
  padding: 0.75rem 2rem;
  font-size: 1.1rem;
  background-color: #794c4c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 10px;
  margin-top:50px;
}

.action-button:hover {
  background-color: #5c2d2d;
  transform: scale(1.05);
}

input, button {
  font-size: 14px;
  margin: 5px;
}


</style>
