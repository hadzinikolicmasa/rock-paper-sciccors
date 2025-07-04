<template>
  <div class="register_form">
    <input v-model="username" placeholder="Enter username" />
    <button @click="register">Register to play</button>

    <p v-if="message" :class="{'success': !isError, 'error': isError}">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: "RegisterForm",
  data() {
    return {
      username: "",
      message: "",
      isError : false
    };
  },
  methods: {
    async register() {

      try {
            const res = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: this.username })
            });
            const data = await res.json();

            if (res.ok) {
                this.message = data.message;
                this.isError = false;
            } else {
                this.message = data.error;
                this.isError = true;
            }
      } catch (err) {
            this.message = "Error connecting with the server.";
            this.isError = true;
      }
    }
  }
};
</script>

<style scoped>
input {
  margin-right: 10px;
}

.success{
  color:darkgreen;
}

.error{
  color:darkred;
}
</style>