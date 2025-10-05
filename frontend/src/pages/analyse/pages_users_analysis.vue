<script setup lang="ts">
import { computed, ref, watch } from "vue"
import { useAuth } from "@/composables/useAuth"
import { useAnalysisResults } from "@/composables/useAnalysisResults"
import type { AnalysisResult } from "@/composables/useAnalysisResults"

const { isDoctor } = useAuth()
const { analysisResults, analysisMetadata, hasAnalysisResults } = useAnalysisResults()

const page = ref(1)
const itemsPerPage = ref(10)

watch(
  () => analysisResults.value.length,
  () => {
    page.value = 1
  },
)


const pageCount = computed(() => {
  const total = analysisResults.value.length
  return total > 0 ? Math.ceil(total / itemsPerPage.value) : 1
})

const paginatedResults = computed(() => {
  const start = (page.value - 1) * itemsPerPage.value
  return analysisResults.value.slice(start, start + itemsPerPage.value)
})

function formatDecimal(value: number | undefined): string {
  return typeof value === "number" && Number.isFinite(value) ? value.toFixed(3) : "0.000"
}

function getTopPrediction(result: AnalysisResult) {
  const fallback = { key: "", label: "", value: 0 }
  return result.predictions.reduce(
    (best, current) => (current.value > best.value ? current : best),
    result.predictions[0] ?? fallback,
  )
}

function getShapleyEntry(result: AnalysisResult, featureKey: string) {
  return result.shapley_values.find((entry) => entry.key === featureKey)
}

const hasMetadata = computed(() => {
  const metadata = analysisMetadata.value
  return Boolean(metadata.filename || metadata.uploadedAt)
})

const formattedUploadDate = computed(() => {
  const timestamp = analysisMetadata.value.uploadedAt
  if (!timestamp) {
    return ""
  }
  const parsed = new Date(timestamp)
  return Number.isNaN(parsed.getTime()) ? "" : parsed.toLocaleString()
})
</script>

<template>
  <v-app>
    <v-container class="page-wrapper">
      <v-card class="card-container" elevation="10">
        <v-container class="pa-6">
          <v-card class="table-container" elevation="0">
            <v-card-text class="intro-text">
              Analyse des exoplanetes - Resultats detailles
            </v-card-text>

            <v-alert
              v-if="isDoctor"
              type="success"
              variant="tonal"
              density="comfortable"
              class="mb-4 doctor-alert"
            >
              Mode docteur active : accedez aux outils avances et annotations speciales ci-dessous.
            </v-alert>

            <v-alert
              v-if="!hasAnalysisResults"
              type="info"
              variant="tonal"
              density="comfortable"
              class="empty-state-alert"
            >
              Aucune analyse disponible. Deposez un fichier sur la page d'import pour lancer une nouvelle prediction.
            </v-alert>

            <template v-else>
              <div v-if="hasMetadata" class="analysis-meta">
                <span class="analysis-meta__item">
                  Fichier : <strong>{{ analysisMetadata.filename }}</strong>
                </span>
                <span v-if="formattedUploadDate" class="analysis-meta__item">
                  Analyse du {{ formattedUploadDate }}
                </span>
                <span class="analysis-meta__item">
                  Lignes traitees : {{ analysisMetadata.recordCount }}
                </span>
              </div>

              <div class="table-header">
                <span class="cell cell-id">ID</span>
                <span class="cell">Classe 1</span>
                <span class="cell">Classe 2</span>
                <span class="cell">Classe 3</span>
                <span class="cell">Prediction</span>
              </div>

              <v-expansion-panels class="results-panels" multiple variant="accordion">
                <v-expansion-panel
                  v-for="result in paginatedResults"
                  :key="result.id"
                  class="result-panel"
                >
                  <v-expansion-panel-title class="panel-title">
                    <div class="row-grid">
                      <span class="cell cell-id">{{ result.id }}</span>
                      <span class="cell">
                        {{ formatDecimal(result.predictions.find((p) => p.key === 'class1')?.value) }}
                      </span>
                      <span class="cell">
                        {{ formatDecimal(result.predictions.find((p) => p.key === 'class2')?.value) }}
                      </span>
                      <span class="cell">
                        {{ formatDecimal(result.predictions.find((p) => p.key === 'class3')?.value) }}
                      </span>
                      <span class="cell">{{ formatDecimal(getTopPrediction(result).value) }}</span>
                    </div>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text class="panel-text">
                    <v-table density="compact" class="feature-table">
                      <thead>
                        <tr>
                          <th>Feature</th>
                          <th>Valeur</th>
                          <th>Shapley</th>
                          <th>Valeur</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="feature in result.features"
                          :key="feature.key"
                        >
                          <td>{{ feature.key }}</td>
                          <td>{{ feature.value }}</td>
                          <td>{{ getShapleyEntry(result, feature.key)?.key ?? '-' }}</td>
                          <td>{{ getShapleyEntry(result, feature.key)?.value ?? '-' }}</td>
                        </tr>
                      </tbody>
                    </v-table>

                    <div
                      v-if="isDoctor"
                      class="doctor-actions"
                    >
                    </div>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>

              <div class="table-footer">
                <v-select
                  v-model="itemsPerPage"
                  :items="[5, 10, 15, 20]"
                  label="Lignes par page"
                  density="compact"
                  hide-details
                  class="items-per-page"
                />
                <v-pagination
                  v-model="page"
                  :length="pageCount"
                  total-visible="5"
                />
              </div>
            </template>
          </v-card>
        </v-container>
      </v-card>
      <v-container class="btn-area">
        <v-btn to="/upload_data"> Back</v-btn>
        <v-btn variant="text" class="btn-download">
          <v-icon start>mdi-file-chart</v-icon>
          Exporter le rapport
        </v-btn>
      </v-container>
    </v-container>
  </v-app>
</template>

<style scoped>
.btn-download {
  color: #169976;
  border: 1px solid currentColor;
}

.btn-area {
  display: flex;
  justify-content: space-between;
  margin-top: 2%;
}

.page-wrapper {
  padding-top: 48px;
  width: 100%;
}

.card-container {
  width: 100%;
  background: #1a1a1a;
  border-radius: 16px;
  border: 2px solid #222222;
}

.table-container {
  width: 100%;
  background: transparent;
  padding: 24px;
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

.empty-state-alert {
  margin-top: 16px;
}

.analysis-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #a8a8a8;
  font-size: 0.85rem;
  margin-bottom: 16px;
}

.analysis-meta__item strong {
  color: #e0e0e0;
  font-weight: 600;
}

.table-header {
  display: grid;
  grid-template-columns: 220px repeat(4, minmax(140px, 1fr));
  align-items: center;
  padding: 12px 14px;
  background: #202020;
  color: #e0e0e0;
  border-radius: 12px 12px 0 0;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.6px;
}

.results-panels {
  background: transparent;
}

.result-panel {
  margin-top: 8px;
  border-radius: 12px !important;
  border: 1px solid #2c2c2c !important;
  background: #1a1a1a !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.result-panel:hover {
  border-color: #1dcd9f;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(29, 205, 159, 0.18);
}

.panel-title {
  padding: 0 !important;
}

.row-grid {
  display: grid;
  grid-template-columns: 220px repeat(4, minmax(140px, 1fr));
  align-items: center;
  padding: 16px;
  color: #f5f5f5;
}

.cell {
  font-variant-numeric: tabular-nums;
}

.cell-id {
  text-transform: uppercase;
  font-weight: 600;
}

.panel-text {
  background: #161616;
}

.feature-table {
  background: transparent;
  color: #e0e0e0;
}

.feature-table th,
.feature-table td {
  border-bottom: 1px solid #2a2a2a !important;
}

.feature-table th {
  color: #a0a0a0;
  font-weight: 600;
}

.feature-table td {
  color: #d5d5d5;
}

.doctor-actions {
  margin-top: 16px;
}

.table-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  gap: 12px;
}

.items-per-page {
  max-width: 200px;
}
</style>
