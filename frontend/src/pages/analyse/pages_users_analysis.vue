<script setup lang="ts">
import {computed, ref} from 'vue'
import {useAuth} from '@/composables/useAuth'

type Prediction = {
  key: 'class1' | 'class2' | 'class3'
  label: string
  value: number
}

type FeatureEntry = {
  key: string
  value: string | number
}

type AnalysisResult = {
  id: string
  predictions: Prediction[]
  features: FeatureEntry[]
}
const {isDoctor} = useAuth()

const analysisResults = ref<AnalysisResult[]>([
  {
    id: 'EXO-0001',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.873},
      {key: 'class2', label: 'Classe 2', value: 0.412},
      {key: 'class3', label: 'Classe 3', value: 0.321},
    ],

    features: [
      {key: 'Température', value: '521 K'},
      {key: 'Masse', value: '1.2 M⊕'},
      {key: 'Rayon', value: '0.96 R⊕'},
      {key: 'Gravité', value: '9.8 m/s²'},
    ],
  },
  {
    id: 'EXO-0002',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.241},
      {key: 'class2', label: 'Classe 2', value: 0.622},
      {key: 'class3', label: 'Classe 3', value: 0.137},
    ],

    features: [
      {key: 'Température', value: '392 K'},
      {key: 'Masse', value: '0.8 M⊕'},
      {key: 'Rayon', value: '1.10 R⊕'},
      {key: 'Gravité', value: '7.1 m/s²'},
    ],
  },
  {
    id: 'EXO-0003',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.388},
      {key: 'class2', label: 'Classe 2', value: 0.255},
      {key: 'class3', label: 'Classe 3', value: 0.781},
    ],

    features: [
      {key: 'Température', value: '218 K'},
      {key: 'Masse', value: '2.4 M⊕'},
      {key: 'Rayon', value: '1.45 R⊕'},
      {key: 'Gravité', value: '14.3 m/s²'},
    ],
  },
  {
    id: 'EXO-0004',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.559},
      {key: 'class2', label: 'Classe 2', value: 0.603},
      {key: 'class3', label: 'Classe 3', value: 0.421},
    ],
    shapley: 0.22,
    features: [
      {key: 'Température', value: '677 K'},
      {key: 'Masse', value: '1.9 M⊕'},
      {key: 'Rayon', value: '1.02 R⊕'},
      {key: 'Gravité', value: '11.2 m/s²'},
    ],
  },
  {
    id: 'EXO-0005',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.324},
      {key: 'class2', label: 'Classe 2', value: 0.451},
      {key: 'class3', label: 'Classe 3', value: 0.612},
    ],
    features: [
      {key: 'Température', value: '495 K'},
      {key: 'Masse', value: '3.1 M⊕'},
      {key: 'Rayon', value: '1.65 R⊕'},
      {key: 'Gravité', value: '13.4 m/s²'},
    ],
  },
  {
    id: 'EXO-0006',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.487},
      {key: 'class2', label: 'Classe 2', value: 0.522},
      {key: 'class3', label: 'Classe 3', value: 0.198},
    ],

    features: [
      {key: 'Température', value: '311 K'},
      {key: 'Masse', value: '0.9 M⊕'},
      {key: 'Rayon', value: '0.88 R⊕'},
      {key: 'Gravité', value: '8.4 m/s²'},
    ],
  },
  {
    id: 'EXO-0007',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.693},
      {key: 'class2', label: 'Classe 2', value: 0.512},
      {key: 'class3', label: 'Classe 3', value: 0.302},
    ],
    features: [
      {key: 'Température', value: '430 K'},
      {key: 'Masse', value: '1.3 M⊕'},
      {key: 'Rayon', value: '1.05 R⊕'},
      {key: 'Gravité', value: '10.2 m/s²'},
    ],
  },
  {
    id: 'EXO-0008',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.334},
      {key: 'class2', label: 'Classe 2', value: 0.879},
      {key: 'class3', label: 'Classe 3', value: 0.256},
    ],
    features: [
      {key: 'Température', value: '268 K'},
      {key: 'Masse', value: '0.6 M⊕'},
      {key: 'Rayon', value: '0.77 R⊕'},
      {key: 'Gravité', value: '6.9 m/s²'},
    ],
  },
  {
    id: 'EXO-0009',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.612},
      {key: 'class2', label: 'Classe 2', value: 0.165},
      {key: 'class3', label: 'Classe 3', value: 0.565},
    ],
    features: [
      {key: 'Température', value: '358 K'},
      {key: 'Masse', value: '1.1 M⊕'},
      {key: 'Rayon', value: '0.99 R⊕'},
      {key: 'Gravité', value: '9.4 m/s²'},
      {key: 'Shapley', value: '11.6'}
    ],
  },
  {
    id: 'EXO-0010',
    predictions: [
      {key: 'class1', label: 'Classe 1', value: 0.457},
      {key: 'class2', label: 'Classe 2', value: 0.774},
      {key: 'class3', label: 'Classe 3', value: 0.274},
    ],
    features: [
      {key: 'Température', value: '402 K'},
      {key: 'Masse', value: '1.5 M⊕'},
      {key: 'Rayon', value: '1.21 R⊕'},
      {key: 'Gravité', value: '11.6 m/s²'},
      {key: 'Shapley', value: '11.6'},
    ],
  },
])

const itemsPerPage = ref(5)
const page = ref(1)

const pageCount = computed(() => Math.ceil(analysisResults.value.length / itemsPerPage.value) || 1)

const paginatedResults = computed(() => {
  const start = (page.value - 1) * itemsPerPage.value
  return analysisResults.value.slice(start, start + itemsPerPage.value)
})

function formatDecimal(value: number) {
  return value.toFixed(3)
}

function getTopPrediction(result: AnalysisResult) {
  return result.predictions.reduce((best, current) => (current.value > best.value ? current : best))
}
</script>

<template>
  <v-app>
    <v-container class="page-wrapper">
      <v-card class="card-container" elevation="10">
        <v-container class="pa-6">
          <v-card class="table-container" elevation="0">
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

            <div class="table-header">
              <span class="cell cell-id">ID</span>
              <span class="cell">Classe 1</span>
              <span class="cell">Classe 2</span>
              <span class="cell">Classe 3</span>
              <span class="cell">Classe dominante</span>
              <span class="cell">Shapley</span>
              <span class="cell cell-actions">Détails</span>
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
                    <span class="cell">{{
                        formatDecimal(result.predictions.find((p) => p.key === 'class1')?.value ?? 0)
                      }}</span>
                    <span class="cell">{{
                        formatDecimal(result.predictions.find((p) => p.key === 'class2')?.value ?? 0)
                      }}</span>
                    <span class="cell">{{
                        formatDecimal(result.predictions.find((p) => p.key === 'class3')?.value ?? 0)
                      }}</span>
                    <span class="cell">{{ formatDecimal(getTopPrediction(result).value) }}</span>
                    <span class="cell">{{ result.shapeley }}</span>
                  </div>
                </v-expansion-panel-title>
                <v-expansion-panel-text class="panel-text">
                  <v-table density="compact" class="feature-table">
                    <thead>
                    <tr>
                      <th>Feature</th>
                      <th>Valeur</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="feature in result.features" :key="feature.key">
                      <td>{{ feature.key }}</td>
                      <td>{{ feature.value }}</td>
                    </tr>
                    </tbody>
                  </v-table>

                  <div
                    v-if="isDoctor"
                    class="doctor-actions"
                  >
                    <v-btn size="small" color="primary" variant="tonal">
                      <v-icon start>mdi-flask-outline</v-icon>
                      Ajouter une note clinique
                    </v-btn>
                    <v-btn size="small" color="secondary" variant="text">
                      <v-icon start>mdi-file-chart</v-icon>
                      Exporter le rapport
                    </v-btn>
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
          </v-card>
        </v-container>
      </v-card>
    </v-container>
  </v-app>
</template>

<style scoped>
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

.table-header {
  display: flex;
  justify-content: space-around;
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
  grid-template-columns: 190px repeat(4, minmax(170px, 1fr)) 140px 1px;
  align-items: center;
  padding: 16px;
  color: #f5f5f5;
}

.cell {
  font-variant-numeric: tabular-nums;
}

.cell-id {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  color: #c2f7e6;
}

.cell-actions {
  display: flex;
  justify-content: center;

  color: #1dcd9f;
}

.panel-text {
  background: #191919 !important;
  padding: 16px 24px !important;
  color: #e0e0e0;
}

.feature-table {
  background: #1f1f1f;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
}

.feature-table thead {
  background: rgba(29, 205, 159, 0.12);
  color: #ffffff;
}

.feature-table td,
.feature-table th {
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.doctor-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.table-footer {
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.items-per-page {
  max-width: 160px;
}

@media (max-width: 1024px) {
  .table-header,
  .row-grid {
    grid-template-columns: 120px repeat(4, minmax(90px, 1fr)) 140px 60px;
  }
}

@media (max-width: 768px) {
  .table-container {
    padding: 16px;
  }

  .table-header,
  .row-grid {
    grid-template-columns: repeat(3, minmax(100px, 1fr));
    grid-template-areas:
      'id id id'
      'c1 c2 c3'
      'top top score'
      'actions actions actions';
  }

  .cell-id {
    grid-area: id;
  }

  .row-grid .cell:nth-child(2) {
    grid-area: c1;
  }

  .row-grid .cell:nth-child(3) {
    grid-area: c2;
  }

  .row-grid .cell:nth-child(4) {
    grid-area: c3;
  }

  .row-grid .cell:nth-child(5) {
    grid-area: top;
  }

  .row-grid .cell:nth-child(6) {
    grid-area: score;
  }

  .row-grid .cell-actions {
    grid-area: actions;
    justify-content: flex-start;
  }

  .table-header {
    display: none;
  }
}

@media (max-width: 768px) {
  .table-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .items-per-page {
    max-width: 100%;
  }
}
</style>
