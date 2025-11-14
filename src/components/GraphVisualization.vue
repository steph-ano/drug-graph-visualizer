<template>
  <div class="visualization-container">
    <div class="content-wrapper fade-in">
      <!-- Header -->
      <div class="header">
        <router-link to="/generator" class="back-link">
          <span class="arrow-back">←</span> Volver al Generador
        </router-link>
        <h1 class="page-title">Visualización del Grafo</h1>
        <div v-if="stats" class="stats-bar glass">
          <div class="stat-item">
            <span class="stat-icon">🔵</span>
            <div>
              <div class="stat-value">{{ stats.nodes }}</div>
              <div class="stat-label">Nodos</div>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">🔗</span>
            <div>
              <div class="stat-value">{{ stats.edges }}</div>
              <div class="stat-label">Conexiones</div>
            </div>
          </div>
          <div class="stat-item">
            <span class="stat-icon">📊</span>
            <div>
              <div class="stat-value">{{ density }}</div>
              <div class="stat-label">Densidad</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Controles -->
      <div class="controls glass-dark">
        <button @click="zoomIn" class="btn btn-secondary btn-control">
          <span class="control-icon">🔍+</span> Acercar
        </button>
        <button @click="zoomOut" class="btn btn-secondary btn-control">
          <span class="control-icon">🔍-</span> Alejar
        </button>
        <button @click="resetZoom" class="btn btn-secondary btn-control">
          <span class="control-icon">↺</span> Restaurar
        </button>
        <button @click="downloadImage" class="btn btn-primary btn-control">
          <span class="control-icon">💾</span> Descargar PNG
        </button>
      </div>

      <!-- Área de visualización -->
      <div class="graph-viewer glass-dark" @wheel="handleWheel" @mousedown="startPan" @mousemove="pan" @mouseup="endPan" @mouseleave="endPan">
        <div v-if="!graphImage" class="no-graph">
          <div class="no-graph-icon">📊</div>
          <p>No hay grafo generado</p>
          <router-link to="/generator" class="btn btn-primary">
            Generar Grafo
          </router-link>
        </div>
        <div v-else class="graph-container" :style="containerStyle">
          <img
              ref="graphImg"
              :src="graphImage"
              alt="Grafo de medicamentos"
              :style="imageStyle"
              draggable="false"
          />
        </div>
      </div>

      <!-- Información adicional -->
      <div class="info-section">
        <div class="info-box glass">
          <h3>💡 Información del Grafo</h3>
          <ul>
            <li><strong>Nodos:</strong> Cada nodo representa un medicamento único</li>
            <li><strong>Conexiones:</strong> Las aristas conectan medicamentos que tratan la misma condición médica</li>
            <li><strong>Grosor:</strong> El grosor de las líneas indica la fuerza de la relación</li>
            <li><strong>Algoritmo:</strong> Spring Layout (Force-Directed) con NetworkX</li>
          </ul>
        </div>

        <div class="actions-box glass">
          <h3>🎯 Acciones Rápidas</h3>
          <button @click="generateNew" class="btn btn-secondary btn-block">
            ✨ Generar Nuevo Grafo
          </button>
          <button @click="downloadImage" class="btn btn-primary btn-block">
            💾 Descargar Imagen
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GraphVisualization',
  data() {
    return {
      graphImage: null,
      stats: null,
      zoom: 1,
      panX: 0,
      panY: 0,
      isPanning: false,
      startX: 0,
      startY: 0
    }
  },
  computed: {
    density() {
      if (!this.stats) return '0%'
      const maxEdges = (this.stats.nodes * (this.stats.nodes - 1)) / 2
      const density = (this.stats.edges / maxEdges) * 100
      return density.toFixed(2) + '%'
    },
    imageStyle() {
      return {
        transform: `scale(${this.zoom}) translate(${this.panX}px, ${this.panY}px)`,
        cursor: this.isPanning ? 'grabbing' : 'grab',
        transition: this.isPanning ? 'none' : 'transform 0.2s ease'
      }
    },
    containerStyle() {
      return {
        overflow: 'hidden',
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }
    }
  },
  mounted() {
    this.loadGraph()
  },
  methods: {
    loadGraph() {
      const savedImage = localStorage.getItem('graphImage')
      const savedStats = localStorage.getItem('graphStats')

      if (savedImage) {
        this.graphImage = savedImage
      }

      if (savedStats) {
        this.stats = JSON.parse(savedStats)
      }
    },
    zoomIn() {
      this.zoom = Math.min(this.zoom + 0.2, 3)
    },
    zoomOut() {
      this.zoom = Math.max(this.zoom - 0.2, 0.3)
    },
    resetZoom() {
      this.zoom = 1
      this.panX = 0
      this.panY = 0
    },
    handleWheel(event) {
      event.preventDefault()
      const delta = event.deltaY > 0 ? -0.1 : 0.1
      this.zoom = Math.max(0.3, Math.min(3, this.zoom + delta))
    },
    startPan(event) {
      this.isPanning = true
      this.startX = event.clientX - this.panX
      this.startY = event.clientY - this.panY
    },
    pan(event) {
      if (!this.isPanning) return
      this.panX = event.clientX - this.startX
      this.panY = event.clientY - this.startY
    },
    endPan() {
      this.isPanning = false
    },
    downloadImage() {
      if (!this.graphImage) return

      const link = document.createElement('a')
      link.href = this.graphImage
      link.download = 'grafo_medicamentos.png'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    generateNew() {
      this.$router.push('/generator')
    }
  }
}
</script>

<style scoped>
.visualization-container {
  min-height: 100vh;
  padding: 40px 20px;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.back-link:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(-3px);
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 20px;
}

.stats-bar {
  display: flex;
  justify-content: center;
  gap: 40px;
  padding: 20px;
  margin: 20px auto;
  max-width: 600px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  font-size: 2rem;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--primary);
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.btn-control {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
}

.control-icon {
  font-size: 1.2rem;
}

.graph-viewer {
  min-height: 600px;
  margin-bottom: 30px;
  position: relative;
  user-select: none;
}

.no-graph {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 600px;
  gap: 20px;
}

.no-graph-icon {
  font-size: 5rem;
  opacity: 0.5;
}

.no-graph p {
  font-size: 1.3rem;
  opacity: 0.7;
}

.graph-container {
  width: 100%;
  height: 100%;
  min-height: 600px;
}

.graph-container img {
  max-width: 100%;
  height: auto;
  display: block;
}

.info-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-top: 30px;
}

.info-box,
.actions-box {
  padding: 30px;
}

.info-box h3,
.actions-box h3 {
  font-size: 1.3rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.info-box ul {
  list-style: none;
  padding: 0;
}

.info-box li {
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  line-height: 1.6;
}

.info-box li:last-child {
  border-bottom: none;
}

.btn-block {
  width: 100%;
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .stats-bar {
    flex-direction: column;
    gap: 20px;
  }

  .controls {
    flex-direction: column;
  }

  .btn-control {
    width: 100%;
  }

  .info-section {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 2rem;
  }
}
</style>