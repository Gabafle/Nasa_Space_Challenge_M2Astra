import { computed, reactive } from "vue"

export type AnalysisPrediction = {
  key: string
  label: string
  value: number
}

export type AnalysisFeature = {
  key: string
  value: string | number
}

export type AnalysisResult = {
  id: string
  predictions: AnalysisPrediction[]
  features: AnalysisFeature[]
  shapley_values: AnalysisFeature[]
}

type BackendRow = {
  id?: string
  vals?: Record<string, unknown>
  shapley?: Record<string, unknown>
  softmax_class_1?: unknown
  softmax_class_2?: unknown
  softmax_class_3?: unknown
}

type BackendPayload = {
  dataframe?: BackendRow[]
}

type UploadResponsePayload = {
  filename?: string
  result?: string | BackendPayload
}

interface AnalysisState {
  results: AnalysisResult[]
  metadata: {
    filename: string
    uploadedAt: string
    recordCount: number
  }
}

const STORAGE_KEY = "analysis-results"

const state = reactive<AnalysisState>({
  results: [],
  metadata: {
    filename: "",
    uploadedAt: "",
    recordCount: 0,
  },
})

function toNumber(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value
  }
  if (typeof value === "string") {
    const parsed = Number(value)
    return Number.isFinite(parsed) ? parsed : null
  }
  return null
}

function toDisplayValue(value: unknown): string | number {
  if (value === null || value === undefined) {
    return "-"
  }
  if (typeof value === "number") {
    return Number.isFinite(value) ? value : "-"
  }
  if (typeof value === "string") {
    const trimmed = value.trim()
    return trimmed.length > 0 ? trimmed : "-"
  }
  return String(value)
}

function parseBackendResult(raw: UploadResponsePayload["result"]): BackendRow[] {
  if (!raw) {
    return []
  }

  if (typeof raw === "string") {
    try {
      const parsed = JSON.parse(raw) as BackendPayload
      return Array.isArray(parsed?.dataframe) ? parsed.dataframe : []
    } catch (error) {
      console.error("Unable to parse analysis result payload", error)
      return []
    }
  }

  if (typeof raw === "object") {
    return Array.isArray(raw.dataframe) ? raw.dataframe : []
  }

  return []
}

function normaliseRow(row: BackendRow, index: number): AnalysisResult {
  const features = Object.entries(row.vals ?? {}).map<AnalysisFeature>(([key, value]) => ({
    key,
    value: toDisplayValue(value),
  }))

  const shapleySource = row.shapley ?? {}
  const shapleyValues = features.map<AnalysisFeature>(({ key }) => {
    const value = (shapleySource as Record<string, unknown>)[key]
    const numericValue = toNumber(value)
    return {
      key,
      value: numericValue ?? toDisplayValue(value),
    }
  })

  const predictionEntries: Array<[string, string]> = [
    ["class1", "Classe 1"],
    ["class2", "Classe 2"],
    ["class3", "Classe 3"],
  ]

  const predictions = predictionEntries.map<AnalysisPrediction>(([key, label], idx) => {
    const backendKey = `softmax_class_${idx + 1}` as const
    const rawValue = (row as Record<string, unknown>)[backendKey]
    const numericValue = toNumber(rawValue) ?? 0
    return {
      key,
      label,
      value: numericValue,
    }
  })

  return {
    id: typeof row.id === "string" && row.id.trim().length > 0 ? row.id : `Observation ${index + 1}`,
    predictions,
    features,
    shapley_values: shapleyValues,
  }
}

function normaliseUploadResponse(payload?: UploadResponsePayload): AnalysisResult[] {
  if (!payload) {
    return []
  }

  const rows = parseBackendResult(payload.result)
  return rows.map((row, index) => normaliseRow(row, index))
}

function populateFromSessionStorage(): void {
  if (typeof window === "undefined") {
    return
  }

  try {
    const raw = window.sessionStorage.getItem(STORAGE_KEY)
    if (!raw) {
      return
    }
    const parsed = JSON.parse(raw) as AnalysisState
    if (Array.isArray(parsed?.results)) {
      state.results = parsed.results
    }
    if (parsed?.metadata) {
      state.metadata = parsed.metadata
    }
  } catch (error) {
    console.warn("Unable to read stored analysis results", error)
  }
}

populateFromSessionStorage()

function persistState(): void {
  if (typeof window === "undefined") {
    return
  }

  try {
    const serialized = JSON.stringify({
      results: state.results,
      metadata: state.metadata,
    })
    window.sessionStorage.setItem(STORAGE_KEY, serialized)
  } catch (error) {
    console.warn("Unable to persist analysis results", error)
  }
}

function setAnalysisResultsFromUpload(payload: UploadResponsePayload): void {
  const normalised = normaliseUploadResponse(payload)
  state.results = normalised
  state.metadata = {
    filename: payload?.filename ?? "",
    uploadedAt: new Date().toISOString(),
    recordCount: normalised.length,
  }
  persistState()
}

function clearAnalysisResults(): void {
  state.results = []
  state.metadata = {
    filename: "",
    uploadedAt: "",
    recordCount: 0,
  }
  if (typeof window !== "undefined") {
    window.sessionStorage.removeItem(STORAGE_KEY)
  }
}

const analysisResults = computed(() => state.results)
const analysisMetadata = computed(() => state.metadata)
const hasAnalysisResults = computed(() => state.results.length > 0)

export function useAnalysisResults() {
  return {
    analysisResults,
    analysisMetadata,
    hasAnalysisResults,
    setAnalysisResultsFromUpload,
    clearAnalysisResults,
  }
}
