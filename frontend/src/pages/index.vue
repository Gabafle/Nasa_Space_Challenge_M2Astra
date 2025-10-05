<template>
  <v-app>

    <v-main class="main">
      <canvas ref="starsCanvas" class="background-canvas"></canvas>
      <v-container
        fluid
        class="cover-container d-flex flex-column align-center justify-center"
      >
        <div class="card-menu-container">
          <v-img
            src="@/assets/logo_app_head.png"
            class="logo"
            contain
          ></v-img>

          <h1 class="title mt-4">AstroMetric</h1>
          <p class="subtitle">
            Analyse intelligente des données d’exoplanètes — Powered by M2Astro
          </p>

          <div class="btn-container">
            <v-btn to="/upload_data"
              class="btn-analyse"
              elevation="4">
              Commencer l’analyse
              <v-icon end>mdi-google-analytics</v-icon>
            </v-btn>

          </div>


        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import Header from '@/components/Header.vue'
import { onMounted, ref } from 'vue'

const starsCanvas = ref<HTMLCanvasElement | null>(null)

onMounted(() => {
  const canvas = starsCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')!
  let stars: { x: number; y: number; size: number; speed: number }[] = []
  const nbStars = 120

  const resize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    stars = Array.from({ length: nbStars }).map(() => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 1.5 + 0.5,
      speed: Math.random() * 0.3 + 0.1
    }))
  }

  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = 'white'
    for (const star of stars) {
      ctx.beginPath()
      ctx.arc(star.x, star.y, star.size, 0, 2 * Math.PI)
      ctx.fill()
      star.y += star.speed
      if (star.y > canvas.height) star.y = 0
    }
    requestAnimationFrame(animate)
  }

  resize()
  animate()
  window.addEventListener('resize', resize)
})
</script>

<style scoped>

.background-canvas {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 0;
  width: 100%;
  height: 100%;;
}


/* ================================
   STRUCTURE
   ================================ */


.cover-container {
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  color: #fff;
  overflow: hidden;
}

/* ================================
   LOGO & TITRE
   ================================ */
.logo {
  width: 120px;
  height: 120px;
  filter: drop-shadow(0px 0px 12px rgba(255, 255, 255, 0.4));
}

.title {
  font-family: "Arial Black";
  font-size: 3rem;
  font-weight: 700;
  color: #48f1af;
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
  letter-spacing: 2px;
}

.subtitle {
  font-family: "Arial",serif;
  font-size: 1.2rem;
  color: #e0f6f0;
  margin-top: 0.5rem;
  letter-spacing: 1px;

}

/* ================================
   BOUTON
   ================================ */
.btn-container{
  width: 100%;
  margin-top: 3rem;
  display: flex;
  justify-content:space-around;
}
.btn-analyse {
  background: linear-gradient(30deg, #169976, #1DCD9F);
  color: white;
  transition: all 0.3s ease;
}

.btn-analyse:hover {
  transform: scale(1.05);
  background: linear-gradient(30deg, #169976, #1DCD9F);
}


/* ================================
   ANIMATIONS
   ================================ */
.fade-in {
  animation: fadeIn 1.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-menu-container {
  align-items: center;
  text-align: center;
  display: flex;
  flex-direction: column;

}
</style>
