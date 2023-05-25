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
    const obj = await quizApiService.getQuizInfo();
    this.registeredScores = obj.data.scores;
  }
};
</script>

<style>
.home-page {
  text-align: center;
  margin-top: 100px;
  /* Ajout d'une marge supérieure */
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

/* Ajout des styles pour le header */
.header {
  position: fixed;
  top: 0;
  width: 100%;
  background-color: #f8f8f8;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0;
}
</style>