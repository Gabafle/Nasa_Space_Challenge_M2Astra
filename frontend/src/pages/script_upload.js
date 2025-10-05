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

      if (file) {
        this.excelPreview = {
          name: file.name,
          type: 'excel',
        }

        const reader = new FileReader()
        reader.onload = (e) => {
          const data = new Uint8Array(e.target.result)
          const workbook = XLSX.read(data, { type: 'array' })
          const firstSheet = workbook.Sheets[workbook.SheetNames[0]]
          const sheetData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 })

          this.excelData = sheetData
          this.resetVisibleRows()
        }
        reader.readAsArrayBuffer(file)
      } else {
        this.removeExcelFile()
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
        print()
        this.$router.push('/analyse/pages_users_analysis')
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
