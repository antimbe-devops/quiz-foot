<template>
  <div class="score">
    <h2>Résultats du quiz</h2>
    <p>Nom du joueur : {{ this.username }}</p>
    <p>Score : {{ this.userScore }}</p>
  </div>
</template>

<script>
import QuizApiService from '../services/QuizApiService';
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  data() {
    return {
      username: '',
      userScore: 0
    };
  },
  created() {
    this.launchScore();
  },
  methods: {
    async launchScore() {
      this.username = participationStorageService.getPlayerName();
      const response = await QuizApiService.getScore(this.username)
      this.userScore = response.data.scores
      console.log(this.userScore)


    }
  },
  name: 'Score',
};
</script>


<style>
.score {
  margin-bottom: 20px;
}

.score h2 {
  font-size: 24px;
  font-weight: bold;
}

.score p {
  font-size: 18px;
  margin-bottom: 10px;
}
</style>

