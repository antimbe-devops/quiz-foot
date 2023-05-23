<template>
  <div class="home-page">
    <h1>Home page</h1>

    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date" class="score-entry">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>

    <router-link to="/start-new-quiz-page" class="start-quiz-button">Démarrer le quiz !</router-link>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: []
    };
  },
  async created() {
    console.log("Composant Home page 'created'");
    this.registeredScores = await quizApiService.getRegisteredScores();
  }
};
</script>

<style>
.home-page {
  text-align: center;
}

.score-entry {
  margin-bottom: 10px;
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
