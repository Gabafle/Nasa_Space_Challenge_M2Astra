<template>
  <v-container class="body-upload-pages">
    <div class="excel-container">
      <v-card class="upload-card">
        <v-card-title>Uploader un fichier Excel</v-card-title>
        <v-card-text>
          <v-file-input
            v-model="excelFile"
            label="Choisissez un fichier Excel"
            show-size
            accept=".xlsx, .xls, .csv"
            @change="handleExcelUpload"
          ></v-file-input>

          <div class="file-container" v-if="excelPreview">
            <div class="file-item">
              <v-icon>mdi-file-excel-box</v-icon>
              <span>{{ excelPreview.name }}</span>
              <v-btn icon @click="removeExcelFile">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
          </div>

          <v-alert v-if="uploadError" type="error" class="mt-4" density="compact">
            {{ uploadError }}
          </v-alert>
        </v-card-text>
      </v-card>

      <v-card v-if="excelData.length" class="preview-card">
        <v-infinite-scroll :items="visibleRows" @load="loadMoreRows">
          <v-table fixed-header height="400px">
            <thead>
              <tr>
                <th v-for="(header, index) in excelData[0]" :key="'header-' + index">
                  {{ header }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIndex) in visibleRows" :key="'row-' + rowIndex">
                <td v-for="(cell, colIndex) in row" :key="'cell-' + rowIndex + '-' + colIndex">
                  {{ cell }}
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-infinite-scroll>
      </v-card>

      <v-btn
        class="submit-are"
        color="primary"
        :disabled="!excelFile || isUploading"
        :loading="isUploading"
        @click="submitAnalysis"
      >
        <v-icon class="mr-2">mdi-cube</v-icon>
        Analyser
      </v-btn>
    </div>
  </v-container>
</template>

<script src="./script_upload.js"></script>

<style scoped>
.v-card {
  border-radius: 8px;
}

.body-upload-pages {
  width: 100%;
  min-height: 100vh;
  padding-bottom: 4rem;
}

.excel-container {
  max-width: 100rem;
  margin: 0 auto;
}

.upload-card {
  justify-content: center;
  margin-top: 6rem;
}

.preview-card {
  margin-top: 2rem;
}

.submit-are {
  display: flex;
  margin: 2rem 0 0 auto;
}
</style>

