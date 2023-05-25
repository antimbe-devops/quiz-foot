

<template>
  <div class="question-display" v-if="question">
    <h2>{{ question.data.title }}</h2>
    <p>{{ question.data.text }}</p>
    <img v-if="question.data.image" :src="question.data.image" />

    <div class="answers">
      <div v-for="(answer, index) in question.data.possibleAnswers" :key="index" class="answer">
        <input type="radio" :id="answer.text" :value="answer.text" v-model="selectedAnswer"
          @change="onAnswerSelected(index)" />
        <label :for="answer.text">{{ answer.text }}</label>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "QuestionDisplay",
  emits: ["answer-selected"],
  props: {
    question: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      selectedAnswer: null,
    };
  },
  async created() {

    console.log(this.question);
  },
  methods: {
    onAnswerSelected(answerId) {
      this.selectedAnswer = answerId + 1;
      this.$emit("answer-selected", this.selectedAnswer);
    },
  },
};
</script>

<style>
.question-display {
  margin-top: 100px;
  margin-bottom: 20px;
}

.answers {
  margin-top: 10px;
}

.answer {
  margin-bottom: 5px;
}
</style>
