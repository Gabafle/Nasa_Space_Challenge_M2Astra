<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'

type AnalysisResult = {
  id: string
  score: number
  prediction: number
}

const { isDoctor } = useAuth()

const chunkSize = 8
const analysisResults = ref<AnalysisResult[]>([
  { id: 'EXO-0001', score: 0.873, prediction: 0.912 },
  { id: 'EXO-0002', score: 0.642, prediction: 0.731 },
  { id: 'EXO-0003', score: 0.781, prediction: 0.854 },
  { id: 'EXO-0004', score: 0.559, prediction: 0.603 },
  { id: 'EXO-0005', score: 0.924, prediction: 0.951 },
  { id: 'EXO-0006', score: 0.487, prediction: 0.522 },
  { id: 'EXO-0007', score: 0.693, prediction: 0.744 },
  { id: 'EXO-0008', score: 0.834, prediction: 0.879 },
  { id: 'EXO-0009', score: 0.612, prediction: 0.665 },
  { id: 'EXO-0010', score: 0.957, prediction: 0.974 },
  { id: 'EXO-0011', score: 0.415, prediction: 0.463 },
  { id: 'EXO-0012', score: 0.522, prediction: 0.561 },
  { id: 'EXO-0013', score: 0.738, prediction: 0.793 },
  { id: 'EXO-0014', score: 0.861, prediction: 0.905 },
  { id: 'EXO-0015', score: 0.694, prediction: 0.741 },
  { id: 'EXO-0016', score: 0.358, prediction: 0.402 },
  { id: 'EXO-0017', score: 0.805, prediction: 0.842 },
  { id: 'EXO-0018', score: 0.629, prediction: 0.701 },
  { id: 'EXO-0019', score: 0.912, prediction: 0.946 },
  { id: 'EXO-0020', score: 0.733, prediction: 0.781 },
  { id: 'EXO-0021', score: 0.564, prediction: 0.612 },
  { id: 'EXO-0022', score: 0.816, prediction: 0.864 },
  { id: 'EXO-0023', score: 0.672, prediction: 0.725 },
  { id: 'EXO-0024', score: 0.787, prediction: 0.836 },
  { id: 'EXO-0025', score: 0.948, prediction: 0.966 },
  { id: 'EXO-0026', score: 0.503, prediction: 0.549 },
  { id: 'EXO-0027', score: 0.688, prediction: 0.733 },
  { id: 'EXO-0028', score: 0.829, prediction: 0.872 },
  { id: 'EXO-0029', score: 0.921, prediction: 0.953 },
  { id: 'EXO-0030', score: 0.612, prediction: 0.659 },
])

const visibleResults = ref<AnalysisResult[]>(analysisResults.value.slice(0, chunkSize))
const currentIndex = ref(chunkSize)

function loadMoreResults({ done }: { done: (status: 'ok' | 'empty') => void }) {
  if (currentIndex.value >= analysisResults.value.length) {
    done('empty')
    return
  }

  const nextItems = analysisResults.value.slice(currentIndex.value, currentIndex.value + chunkSize)
  if (nextItems.length) {
    visibleResults.value.push(...nextItems)
    currentIndex.value += nextItems.length
    done('ok')
  } else {
    done('empty')
  }
}

function formatDecimal(value: number) {
  return value.toFixed(3)
}

function formatPercent(value: number) {
  return `${Math.round(value * 100)}%`
}
</script>

<template>
  <v-app>
    <v-container class="page-wrapper">
      <v-card class="card-container" elevation="10">
        <v-container class="pa-6">
          <v-card class="scroll-container" elevation="0">
            <v-card-text class="intro-text">
              Analyse des Exoplanètes — Résultats détaillés
            </v-card-text>

            <v-alert
              v-if="isDoctor"
              type="success"
              variant="tonal"
              density="comfortable"
              class="mb-4 doctor-alert"
            >
              Mode docteur activé : accédez aux outils avancés et annotations spécialisées ci-dessous.
            </v-alert>

            <v-infinite-scroll :items="visibleResults" @load="loadMoreResults">
              <template #default>
                <div class="results-grid">
                  <v-card
                    v-for="item in visibleResults"
                    :key="item.id"
                    class="result-card"
                    elevation="4"
                  >
                    <div class="result-content">
                      <div class="result-info">
                        <div class="result-header">
                          <v-icon>mdi-planet</v-icon>
                          <span class="result-id">{{ item.id }}</span>
                        </div>

                        <v-table density="compact" class="score-table">
                          <thead>
                            <tr>
                              <th>Métrique</th>
                              <th>Valeur</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td>Score</td>
                              <td>{{ formatDecimal(item.score) }}</td>
                            </tr>
                            <tr>
                              <td>Score (%)</td>
                              <td>{{ formatPercent(item.score) }}</td>
                            </tr>
                          </tbody>
                        </v-table>
                      </div>

                      <v-sheet class="prediction-badge" elevation="2">
                        <span class="badge-label">Prédiction</span>
                        <span class="badge-value">{{ formatPercent(item.prediction) }}</span>
                      </v-sheet>
                    </div>

                    <div
                      v-if="isDoctor"
                      class="result-footer"
                    >
                      <v-btn
                        size="small"
                        color="primary"
                        variant="tonal"
                        class="doctor-action"
                      >
                        <v-icon start>mdi-flask-outline</v-icon>
                        Ajouter une note clinique
                      </v-btn>
                      <v-btn
                        size="small"
                        color="secondary"
                        variant="text"
                        class="doctor-action"
                      >
                        <v-icon start>mdi-file-chart</v-icon>
                        Exporter le rapport
                      </v-btn>
                    </div>
                  </v-card>
                </div>
              </template>
            </v-infinite-scroll>
          </v-card>
        </v-container>
      </v-card>
    </v-container>
  </v-app>
</template>

<style scoped>
.page-wrapper {
  padding-top: 48px;
}

.card-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  background: #1a1a1a;
  border-radius: 16px;
  overflow: hidden;
  border: 2px solid #222222;
}

.scroll-container {
  max-height: 640px;
  overflow-y: auto;
  background: transparent;
  padding: 24px;
}

.scroll-container::-webkit-scrollbar {
  width: 10px;
}

.scroll-container::-webkit-scrollbar-track {
  background: #222222;
  border-radius: 10px;
}

.scroll-container::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #1dcd9f 0%, #169976 100%);
  border-radius: 10px;
}

.scroll-container::-webkit-scrollbar-thumb:hover {
  background: #1dcd9f;
}

.intro-text {
  text-align: center;
  color: #1dcd9f;
  font-size: 1.1rem;
  padding-bottom: 24px;
}

.doctor-alert {
  color: #0f5132;
}

.results-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-card {
  background: #222222;
  border: 1px solid #333333;
  border-radius: 12px;
  padding: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.result-card:hover {
  border-color: #1dcd9f;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(29, 205, 159, 0.25);
}

.result-content {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 24px;
}

.result-info {
  flex: 1;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  color: #1dcd9f;
  font-weight: 600;
  text-transform: uppercase;
}

.result-id {
  letter-spacing: 1px;
}

.score-table {
  background: #1f1f1f;
  border-radius: 8px;
  overflow: hidden;
}

.score-table thead {
  background: rgba(29, 205, 159, 0.12);
  color: #ffffff;
}

.score-table tbody tr td {
  color: #e0e0e0;
}

.prediction-badge {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-width: 120px;
  background: linear-gradient(180deg, rgba(29, 205, 159, 0.15) 0%, rgba(22, 153, 118, 0.25) 100%);
  border: 1px solid #1dcd9f;
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  gap: 6px;
}

.badge-label {
  font-size: 0.85rem;
  color: #c2f7e6;
}

.badge-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
}

.result-footer {
  margin-top: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.doctor-action {
  text-transform: none;
}

@media (max-width: 900px) {
  .result-content {
    flex-direction: column;
    align-items: stretch;
  }

  .prediction-badge {
    flex-direction: row;
    justify-content: space-between;
    min-width: auto;
  }
}

@media (max-width: 600px) {
  .scroll-container {
    max-height: none;
    padding: 16px;
  }

  .result-footer {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
