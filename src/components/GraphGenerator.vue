<template>
  <div class="generator-container">
    <div class="content-wrapper fade-in">
      <!-- Header con navegación -->
      <div class="header">
        <router-link to="/" class="back-link">
          <span class="arrow-back">←</span> Volver
        </router-link>
        <h1 class="page-title">Generador de Grafos</h1>
        <p class="page-subtitle">Configura los parámetros para visualizar las relaciones entre medicamentos</p>
      </div>

      <!-- Formulario de parámetros -->
      <div class="form-card glass-dark">
        <div class="form-grid">
          <!-- Número máximo de nodos -->
          <div class="form-group">
            <label for="maxNodes">
              <span class="label-icon">🔢</span>
              Número máximo de nodos
            </label>
            <input
                type="number"
                id="maxNodes"
                v-model.number="params.maxNodes"
                placeholder="Dejar vacío para usar todos"
                min="10"
                max="10000"
            />
            <small class="help-text">Opcional: limita la cantidad de medicamentos a visualizar</small>
          </div>

          <!-- Velocidad de layout -->
          <div class="form-group">
            <label for="layoutSpeed">
              <span class="label-icon">⚡</span>
              Velocidad de generación
            </label>
            <select id="layoutSpeed" v-model="params.layoutSpeed">
              <option value="fast">Rápido (30 iteraciones)</option>
              <option value="complete">Completo (70 iteraciones)</option>
            </select>
            <small class="help-text">El modo completo genera un layout más optimizado</small>
          </div>

          <!-- Dataset completo -->
          <div class="form-group full-width">
            <label class="checkbox-wrapper">
              <input
                  type="checkbox"
                  v-model="params.useFullDataset"
              />
              <span class="checkbox-label">
                <span class="label-icon">📊</span>
                Usar dataset completo
              </span>
            </label>
            <small class="help-text">Procesar todos los datos disponibles en el CSV</small>
          </div>
        </div>

        <!-- Botón de generación -->
        <div class="action-area">
          <button
              @click="generateGraph"
              :disabled="loading"
              class="btn btn-primary btn-generate"
          >
            <span v-if="!loading">
              <span class="btn-icon">✨</span>
              Generar Grafo
            </span>
            <span v-else class="loading-content">
              <div class="spinner"></div>
              Generando...
            </span>
          </button>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error" class="error-message glass">
          <span class="error-icon">⚠️</span>
          {{ error }}
        </div>

        <!-- Preview de parámetros -->
        <div class="params-preview glass">
          <h4 class="preview-title">Configuración actual:</h4>
          <div class="preview-grid">
            <div class="preview-item">
              <span class="preview-label">Nodos:</span>
              <span class="preview-value">{{ params.maxNodes || 'Todos' }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">Velocidad:</span>
              <span class="preview-value">{{ params.layoutSpeed === 'fast' ? 'Rápida' : 'Completa' }}</span>
            </div>
            <div class="preview-item">
              <span class="preview-label">Dataset:</span>
              <span class="preview-value">{{ params.useFullDataset ? 'Completo' : 'Parcial' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Información adicional -->
      <div class="info-cards">
        <div class="info-card-small glass">
          <div class="card-icon">🔬</div>
          <h4>Análisis de Red</h4>
          <p>Visualiza conexiones entre medicamentos basadas en condiciones médicas compartidas</p>
        </div>
        <div class="info-card-small glass">
          <div class="card-icon">📈</div>
          <h4>Algoritmos</h4>
          <p>Utiliza NetworkX y Spring Layout para la distribución óptima de nodos</p>
        </div>
        <div class="info-card-small glass">
          <div class="card-icon">💊</div>
          <h4>Dataset</h4>
          <p>Datos de medicamentos y efectos secundarios de Drugs.com</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GraphGenerator',
  data() {
    return {
      params: {
        maxNodes: null,
        layoutSpeed: 'complete',
        useFullDataset: true
      },
      loading: false,
      error: null
    }
  },
  methods: {
    async generateGraph() {
      this.loading = true
      this.error = null

      try {
        const response = await axios.post('http://localhost:8000/generar-grafo', {
          max_nodes: this.params.maxNodes,
          layout_speed: this.params.layoutSpeed,
          use_full_dataset: this.params.useFullDataset
        })

        if (response.data.success) {
          // Guardar imagen y estadísticas en localStorage para la siguiente vista
          localStorage.setItem('graphImage', response.data.image)
          localStorage.setItem('graphStats', JSON.stringify(response.data.stats))

          // Navegar a la visualización
          this.$router.push('/visualization')
        }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al generar el grafo. Verifica que el backend esté corriendo.'
        console.error('Error:', err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.generator-container {
  min-height: 100vh;
  padding: 40px 20px;
}

.content-wrapper {
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 40px;
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

.arrow-back {
  font-size: 1.2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 10px;
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  font-weight: 300;
}

.form-card {
  padding: 40px;
  margin-bottom: 30px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.full-width {
  grid-column: 1 / -1;
}

label {
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.label-icon {
  font-size: 1.2rem;
}

.help-text {
  font-size: 0.85rem;
  opacity: 0.7;
  font-style: italic;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.action-area {
  text-align: center;
  margin: 40px 0 30px;
}

.btn-generate {
  font-size: 1.3rem;
  padding: 20px 60px;
}

.btn-icon {
  font-size: 1.5rem;
  margin-right: 8px;
}

.loading-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.error-message {
  background: rgba(255, 107, 107, 0.2);
  border: 2px solid rgba(255, 107, 107, 0.5);
  padding: 15px 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.error-icon {
  font-size: 1.5rem;
}

.params-preview {
  background: rgba(0, 174, 239, 0.1);
  border: 1px solid rgba(0, 174, 239, 0.3);
  padding: 20px;
  margin-top: 20px;
}

.preview-title {
  font-size: 1rem;
  margin-bottom: 15px;
  opacity: 0.9;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.preview-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.preview-label {
  font-size: 0.85rem;
  opacity: 0.7;
}

.preview-value {
  font-weight: 600;
  color: var(--primary);
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-card-small {
  padding: 25px;
  text-align: center;
  transition: transform 0.3s ease;
}

.info-card-small:hover {
  transform: translateY(-5px);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.info-card-small h4 {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.info-card-small p {
  font-size: 0.95rem;
  opacity: 0.85;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-card {
    padding: 25px;
  }

  .btn-generate {
    font-size: 1.1rem;
    padding: 16px 40px;
  }

  .page-title {
    font-size: 2rem;
  }
}
</style>