<template>
   <div>
      <div>
          <h2>MULTI PLAYER</h2>
          <p><b>Enter your username & match id you want to join </b> </p>
          <p>(if you don't, you will create a new match)</p>
          <input v-model="username"  type="text" placeholder="Enter your username"  :disabled="user_selected"/><br>
          <input v-model="match_id"  type="number" placeholder="Enter match id"  /><br>
      </div>

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
  name: "MultiPlayer",
  components : {ScoreBoard},

  data() {
    return {
      choices: [],
      username: "",
      choice_id : -1,
      message : "",
      user_selected: false,
      showScoreBoard :false,
      score_error : "",
      scoreboardKey : 0,
      match_id : null
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
          const payload = {
              username: this.username,
              choice_id: this.choice_id
          };
        if (this.match_id != null) payload.match_id = this.match_id;

        const res = await fetch("/multi/play", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (data.error) {
            this.message = `${data.error}`;
            return;
        }

        if (data.message && data.message.includes("Match created")) {
            this.message = `Match created! Share this match ID: ${data.match_id}`;
            this.match_id = data.match_id;
            this.user_selected = true;

            this.startPolling(this.match_id);
            return;
        }

        if (data.message && data.message.includes("Match completed")) {
            this.message =
                `Match completed!\n` +
                `Player 1: ${data.player_one.username} chose ${data.player_one.choice}\n` +
                `Player 2: ${data.player_two.username} chose ${data.player_two.choice}\n` +
                `Winner: ${data.winner}`;
            this.user_selected = true;
        }
      } catch (err) {
          console.error("Fetch error:", err);
          this.message = "Server error. Please try again.";
      }
    },
      selectChoice(choice_id){
          this.choice_id = choice_id
      },
      show_score(){
          this.message = ""
          this.showScoreBoard = true
          this.scoreboardKey += 1
      },
      hide_score(){
      this.message = ""
      this.showScoreBoard = false
    },
    async delete_score(){
      this.message = ""
      try {
            await fetch("/results/reset", {
                  method: "DELETE",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ username: this.username })
             });

            this.scoreboardKey += 1

      } catch (err) {
            console.error("Failed to delete scores:", err);
            this.message = "Failed to connect to server.";
      }
    },
    startPolling(match_id) {
        this.pollInterval = setInterval(async () => {
              const res = await fetch(`/multi/status?match_id=${match_id}`);
              const data = await res.json();

        if (data.status === "done") {
              clearInterval(this.pollInterval);
              this.message =
                    `Match completed!\n` +
                    `Player 1: ${data.player_one.username} chose ${data.player_one.choice}\n` +
                    `Player 2: ${data.player_two.username} chose ${data.player_two.choice}\n` +
                    `Winner: ${data.winner}`;
        }else if (data.status === "expired"){
                    clearInterval(this.pollInterval)
                    this.message = "Match expired. Opponent didn’t join in time.";

        }

       }, 2000);
}
  }
};
</script>


<style scoped>
button {
  margin-top: 1rem;
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
