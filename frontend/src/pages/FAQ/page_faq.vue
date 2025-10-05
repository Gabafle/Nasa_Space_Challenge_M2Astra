<script lang="js">
export default {
  data() {
    return {
      expandedItems: []
    }
  },
  methods: {
    onScroll(event) {
      const target = event.target;
      console.log('Position scroll Top:', target.scrollTop);
    },
    toggleItem(index) {
      const idx = this.expandedItems.indexOf(index);
      if (idx > -1) {
        this.expandedItems.splice(idx, 1);
      } else {
        this.expandedItems.push(index);
      }
    },
    isExpanded(index) {
      return this.expandedItems.includes(index);
    }
  }
}
</script>

<template>
  <v-app>
    <v-container>
      <v-card class="card-container" elevation="10">
        <v-card-title class="headline">
          <span class="faq-title">Questions Fréquentes</span>
        </v-card-title>

        <v-container class="pa-6">
          <v-card
            class="scroll-container"
            v-scroll.self="onScroll"
            elevation="0"
          >
            <v-card-text class="intro-text">
              Trouvez rapidement les réponses à vos questions
            </v-card-text>

            <v-expansion-panels
              v-model="expandedItems"
              multiple
              variant="accordion"
            >
              <v-expansion-panel
                v-for="i in 10"
                :key="i"
                class="faq-item"
              >
                <v-expansion-panel-title class="faq-question">
                  <div class="question-content">
                    <v-icon class="question-icon" size="24">mdi-help-circle</v-icon>
                    <span class="question-text">Question {{ i }} - Comment puis-je obtenir de l'aide ?</span>
                  </div>
                </v-expansion-panel-title>

                <v-expansion-panel-text class="faq-answer">
                  Lorem ipsum dolor sit amet, consectetur adipisicing elit. Deserunt, dolorem esse et eum fuga fugiat iste laboriosam neque officia quos reiciendis rerum similique tempora veritatis voluptatibus! Ad deleniti ipsum recusandae! Consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-container>
      </v-card>
    </v-container>
  </v-app>
</template>

<style scoped>
.card-container {
  margin-top: 5%;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  background: #1a1a1a;
  border-radius: 16px;
  overflow: hidden;
  border: 2px solid #222222;
}

.headline {
  background: linear-gradient(135deg, #1DCD9F 0%, #169976 100%);
  padding: 32px 24px;
  justify-content: center;
}

.faq-title {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.scroll-container {
  height: 600px;
  overflow-y: auto;
  background: transparent;
  padding: 0;
}

.scroll-container::-webkit-scrollbar {
  width: 10px;
}

.scroll-container::-webkit-scrollbar-track {
  background: #222222;
  border-radius: 10px;
}

.scroll-container::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #1DCD9F 0%, #169976 100%);
  border-radius: 10px;
}

.scroll-container::-webkit-scrollbar-thumb:hover {
  background: #1DCD9F;
}

.intro-text {
  text-align: center;
  color: #1DCD9F;
  font-size: 1.1rem;
  padding: 24px 16px;
  margin-bottom: 16px;
}

.faq-item {
  margin-bottom: 16px;
  background: #222222 !important;
  border-radius: 12px !important;
  border: 1px solid #333333;
  transition: all 0.3s ease;
}

.faq-item:hover {
  border-color: #1DCD9F;
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(29, 205, 159, 0.2);
}

.faq-question {
  background: #222222 !important;
  color: #ffffff !important;
  padding: 20px 24px;
  font-weight: 600;
  border-radius: 12px;
}

.question-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.question-icon {
  color: #1DCD9F;
  flex-shrink: 0;
}

.question-text {
  font-size: 1.1rem;
  line-height: 1.5;
}

.faq-answer {
  background: #2a2a2a !important;
  color: #e0e0e0 !important;
  padding: 24px !important;
  line-height: 1.8;
  border-top: 2px solid #169976;
}

/* Animation pour l'expansion */
:deep(.v-expansion-panel-text__wrapper) {
  padding: 0 !important;
}

:deep(.v-expansion-panel-title__icon) {
  color: #1DCD9F !important;
}

/* Responsive */
@media (max-width: 768px) {
  .card-container {
    margin-top: 2%;
  }

  .faq-title {
    font-size: 1.5rem;
  }

  .question-text {
    font-size: 1rem;
  }

  .scroll-container {
    height: 500px;
  }
}
</style>
