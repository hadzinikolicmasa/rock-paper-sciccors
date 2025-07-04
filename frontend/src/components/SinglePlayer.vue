<template>
      <div>
          <h2>SINGLE PLAYER</h2>
          <p><b>Enter your username : </b> </p>
          <p>(if you don't, your result will not be saved)</p>
          <input v-model="username"  type="text" placeholder="Enter your username"  :disabled="user_selected"/><br>

     <div v-if="choices.length">
          <h3>Choose your move:</h3>

          <ul>
              <li @click = "selectChoice(choice.id)" v-for="choice in choices" :key="choice.id"  class="choice-item" :class="{ selected: choice.id === choice_id }">
              <img :src="`/assets/${choice.name}.png`" :alt="choice.name" class="choice-img"/><br>
                    {{ choice.name }}
              </li>
          </ul>

          <p v-if="message" class="msg">{{ message }}</p>

      <button @click="play">Play</button><br>
      <button @click="$emit('back')">Back</button>

     </div>
    </div>

    <hr>
    <div>
        <button @click="show_score">Show my scores</button>
        <button @click="hide_score">Hide scores</button><br>
        <button @click="delete_score">Delete scores</button><br>

        <p v-if="score_error" class="msg">{{ score_error }}</p>

        <ScoreBoard :username="username" v-if="showScoreBoard"  :key="scoreboardKey"/>
    </div>
</template>


<script>
import ScoreBoard from "./ScoreBoard.vue";

export default {
  name: "SinglePlayer",
  components : {ScoreBoard},
  data() {
    return {
      choices: [],
      username: "",
      choice_id : null,
      message : "",
      user_selected: false,
      showScoreBoard :false,
      score_error : "",
      scoreboardKey : 0
    };
  },
  mounted() {
    this.fetchChoices();
  },
  methods: {
    async fetchChoices() {
      try {
        const res = await fetch("/choices");
        const data = await res.json();
        this.choices = data;
      } catch (err) {
        console.error("Failed to fetch choices:", err);
      }
    },
    async play() {
        this.message = "";
        try {
            const res = await fetch("play", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                       username: this.username,
                       choice_id: this.choice_id,
            }),
          });

            const data = await res.json();

            if (data.error) {
                  this.message = `${data.error}`;
            } else {
                  if(this.username) this.user_selected = true;
                  this.message = `You chose ${data.player_choice.name}. Computer chose ${data.computer_choice.name}. Result: ${data.result.toUpperCase()}`;
            }

        } catch (err) {
              this.message = "Failed to connect to server.";
              console.error(err);
        }
    },
    selectChoice(choice_id){
      this.choice_id = choice_id
    },
    show_score(){

        this.showScoreBoard = true
        this.scoreboardKey += 1

    },
    hide_score(){
      this.showScoreBoard = false
    },
    async delete_score(){
      this.message = ""
      try {
             await fetch("results/reset", {
                  method: "DELETE",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ username: this.username })
             });

            this.scoreboardKey += 1

      }catch (err) {
          console.error("Failed to delete scores:", err);
          this.message = "Failed to connect to server.";
      }

    }
  }
};
</script>


<style scoped>

button {
  margin: 5px;
}

.choice-item {
  display: inline-block;
  margin: 0.5rem;
  padding: 30px 10px;
  cursor: pointer;
  transition: transform 0.2s , box-shadow 0.2s ease;
}

.choice-item:hover {
  transform: scale(1.6);
}

.msg{
  color:darkred;
}

.choice-item.selected {
  border-color: dodgerblue;
  background-color: #e6f0ff;
  font-weight: bold;
}

input:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.6;
}

.choice-img{
  width:100px;
}

</style>
