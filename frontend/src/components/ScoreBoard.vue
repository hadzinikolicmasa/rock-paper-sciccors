<template>
  <div class="scoreboard">
        <h3 v-if = "username && !message">Last 10 Games</h3>
        <table v-if="results.length">
            <thead>
                <tr>
                    <th>Opponent</th>
                    <th>Your Choice</th>
                    <th>Opponent's Choice</th>
                    <th>Result</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(r, index) in results" :key="index">
                  <td>{{ r.opponent }}</td>
                  <td>{{ r.your_choice }}</td>
                  <td>{{ r.opponent_choice }}</td>
                  <td :class="r.result">{{ r.result }}</td>
                </tr>
            </tbody>
        </table>

    <p style="color:red;" v-else-if="message">{{message}}</p>
    <p v-else>No games played yet.</p>
  </div>
</template>


<script>
export default {
  name: "ScoreBoard",
  props: {
    username: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      results: [],
      message: ""
    };
  },
  mounted() {
    this.fetchResults();
  },
  methods: {
    async fetchResults() {
      try {
          const res = await fetch("results", {
               method: "POST",
                headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ username: this.username })
          });

          const data = await res.json();

          if (data.error) this.message = `${data.error}`;
          else this.results = data;
      } catch (err) {
          console.error("Failed to fetch results:", err);
      }
    }
  }
};
</script>

<style scoped>

.scoreboard {
  margin-top: 20px;
  font-size: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background-color: white;
}

th, td {
  border: 1px solid #ccc;
  padding: 0.5rem;
  text-align: center;
}

th {
  background-color: #f2f2f2;
}

.win {
  color: green;
  font-weight: bold;
}

.lose {
  color: red;
  font-weight: bold;
}

.tie {
  color: gray;
  font-weight: bold;
}
</style>
