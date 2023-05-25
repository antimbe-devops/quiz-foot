<template>
  <div class="new-quiz-page">
    <h1>New Quiz Page</h1>

    <label for="username">Username:</label>
    <input type="text" v-model="username" />
    <p>{{ username }}</p>

    <button class="start-quiz-button" @click="launchNewQuiz">Démarrer le quiz !</button>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";


export default {
  name: "NewQuizPage",
  data() {
    return {
      username: ""
    };
  },
  methods: {
    launchNewQuiz() {
      const playerName = this.username;
      participationStorageService.savePlayerName(playerName);
      console.log("Launch new quiz with", playerName);
      // Redirection vers la première question du quiz
      this.$router.push('/questions');
    }
  }

};
</script>

<style>
.new-quiz-page {
  text-align: center;
}

.start-quiz-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
}
</style>
