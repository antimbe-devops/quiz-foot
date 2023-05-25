<template>
  <div class="questions-manager">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerSelectedHandler" v-if="currentQuestion" />


  </div>
</template>

<script>
import { defineComponent } from 'vue';
import QuestionDisplay from '@/components/QuestionDisplay.vue';
import QuizApiService from '@/services/QuizApiService';
import Score from '@/components/Score.vue';
import participationStorageService from "@/services/ParticipationStorageService";



export default defineComponent({
  name: 'QuestionsManager',
  components: {
    QuestionDisplay,
    Score
  },
  data() {
    return {
      currentQuestionPosition: 1,
      playerName: '',
      currentQuestion: null,
      answersSelected: [],
      goodAnswers: [],
      totalNumberOfQuestions: 0,
      quizEnded: false,
      finalScore: 0,
    };
  },

  async created() {

    const quizInfo = await QuizApiService.getQuizInfo();
    console.log("quiz info :" + quizInfo);
    this.totalNumberOfQuestions = quizInfo.data.size;

    this.currentQuestion = await QuizApiService.getQuestion(this.currentQuestionPosition);

  },


  methods: {



    async answerSelectedHandler(answerId) {
      if (this.currentQuestion) {
        this.answersSelected.push(answerId);
        this.currentQuestionPosition++;

        if (this.currentQuestionPosition <= this.totalNumberOfQuestions) {
          this.currentQuestion = await QuizApiService.getQuestion(this.currentQuestionPosition);
        }
      }

      if (this.currentQuestionPosition > this.totalNumberOfQuestions) {
        this.quizEnded = true;

        await this.scoreHandler();

      }
      if (this.quizEnded == true) {
        const participantData = {
          playerName: participationStorageService.getPlayerName(),
          answers: this.answersSelected,
        };

        const response = await QuizApiService.createParticipant(participantData);


        //this.$router.push('/score');
        this.$router.push({ name: 'Score', params: { playerName: this.playerName, finalScore: this.finalScore } });

      }
    },

    async scoreHandler() {
      this.goodAnswers = await QuizApiService.getGoodAnswers();

      for (let i = 0; i < this.answersSelected.length; i++) {
        const answerSelected = this.answersSelected[i];
        const goodAnswer = this.goodAnswers[i];

        if (answerSelected === goodAnswer) {
          this.finalScore += 1;
        }
      }



    }

  },

});
</script>


<style scoped>
.questions-manager {
  margin-top: 100px;
  padding-bottom: 20px;
  width: 100%;
  /*position: fixed;*/
  top: 100px;
  left: 400px;
  /*overflow-y: auto;*/
}
</style>
