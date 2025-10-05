import * as XLSX from 'xlsx'
import api from '../../api/api-config'

export default {
  data() {
    return {
      excelFile: null,
      excelPreview: null,
      excelData: [],
      visibleRows: [],
      currentIndex: 1,
      chunkSize: 50,
      isUploading: false,
      uploadError: null,
    }
  },
  methods: {
    handleExcelUpload() {
      const file = Array.isArray(this.excelFile) ? this.excelFile[0] : this.excelFile
      this.uploadError = null

      if (!file) {
        this.removeExcelFile()
        return
      }

      this.excelPreview = {
        name: file.name,
        type: 'table',
      }

      const reader = new FileReader()
      const extension = file.name.split('.').pop()?.toLowerCase()

      reader.onload = (event) => {
        const result = event?.target?.result
        if (!result) {
          this.uploadError = 'Aucun contenu detecte dans le fichier.'
          this.removeExcelFile()
          return
        }

        try {
          let workbook
          if (extension === 'csv') {
            const text = typeof result === 'string' ? result : new TextDecoder().decode(result)
            workbook = XLSX.read(text, { type: 'string' })
          } else {
            const buffer = result instanceof ArrayBuffer ? result : new ArrayBuffer(0)
            const data = new Uint8Array(buffer)
            workbook = XLSX.read(data, { type: 'array' })
          }

          const firstSheet = workbook.Sheets[workbook.SheetNames[0]]
          const sheetData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 })

          this.excelData = sheetData
          this.resetVisibleRows()
        } catch (err) {
          console.error('Erreur lors de l\'analyse du fichier', err)
          this.uploadError = 'Impossible de lire le fichier fourni.'
          this.removeExcelFile()
        }
      }

      if (extension === 'csv') {
        reader.readAsText(file)
      } else {
        reader.readAsArrayBuffer(file)
      }
    },

    async submitAnalysis() {
      const file = Array.isArray(this.excelFile) ? this.excelFile[0] : this.excelFile
      if (!file || this.isUploading) {
        return
      }

      const formData = new FormData()
      formData.append('file', file)

      this.isUploading = true
      this.uploadError = null

      try {
        await api.post('/upload-excel', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })

        this.$router.push('/analyser')
      } catch (error) {
        console.error('Upload Excel error', error)
        this.uploadError = error?.response?.data?.detail || "Erreur lors de l'envoi du fichier."
      } finally {
        this.isUploading = false
      }
    },

    resetVisibleRows() {
      this.currentIndex = 1
      this.visibleRows = []
      this.loadMoreRows({ done: () => {} })
    },

    loadMoreRows({ done }) {
      const nextRows = this.excelData.slice(this.currentIndex, this.currentIndex + this.chunkSize)
      if (nextRows.length > 0) {
        this.visibleRows.push(...nextRows)
        this.currentIndex += this.chunkSize
        done('ok')
      } else {
        done('empty')
      }
    },

    removeExcelFile() {
      this.excelFile = null
      this.excelPreview = null
      this.excelData = []
      this.visibleRows = []
      this.uploadError = null
    },
  },
}

