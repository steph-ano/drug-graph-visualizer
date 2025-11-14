<template>
  <div class="team-container">
    <div class="content-wrapper fade-in">
      <!-- Logo/Header -->
      <div class="header">
        <div class="logo-circle glass">
          <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 2v20M2 12h20"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </div>
        <h1 class="main-title">Drug Graph Visualizer</h1>
        <p class="subtitle">Sistema de Visualización de Relaciones entre Medicamentos</p>
      </div>

      <!-- Información académica -->
      <div class="info-card glass-dark">
        <div class="university-logo">🎓</div>
        <h2 class="university-name">UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS</h2>

        <div class="info-grid">
          <div class="info-item">
            <span class="label">CURSO</span>
            <span class="value">Complejidad Algorítmica - 1ACC0184</span>
          </div>

          <div class="info-item">
            <span class="label">CARRERA</span>
            <span class="value">Ingeniería de Software</span>
          </div>

          <div class="info-item">
            <span class="label">SECCIÓN</span>
            <span class="value">12600</span>
          </div>

          <div class="info-item">
            <span class="label">DOCENTE</span>
            <span class="value">José Moisés Cumpa Torres</span>
          </div>
        </div>
      </div>

      <!-- Integrantes -->
      <div class="team-section">
        <h3 class="section-title">INTEGRANTES</h3>
        <div class="team-grid">
          <div class="member-card glass" v-for="member in members" :key="member.code">
            <div class="member-avatar">{{ member.initials }}</div>
            <h4 class="member-name">{{ member.name }}</h4>
            <p class="member-code">{{ member.code }}</p>
          </div>
        </div>
      </div>

      <!-- Botón de navegación -->
      <div class="action-section">
        <router-link to="/generator" class="btn btn-primary btn-large">
          Ir al Generador
          <span class="arrow">→</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TeamPresentation',
  data() {
    return {
      members: [
        {
          name: 'Natalia Bertha Roman Cruz',
          code: 'U202310148',
          initials: 'NR'
        },
        {
          name: 'Stephano Renan Valdivia Quispe',
          code: 'U202311294',
          initials: 'SV'
        },
        {
          name: 'Diego Alejandro Vilca Saboya',
          code: 'U20231A778',
          initials: 'DV'
        }
      ]
    }
  }
}
</script>

<style scoped>
.team-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.content-wrapper {
  max-width: 900px;
  width: 100%;
}

.header {
  text-align: center;
  margin-bottom: 50px;
}

.logo-circle {
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
}

.main-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #fff, #e0e0e0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  font-weight: 300;
}

.info-card {
  padding: 40px;
  margin-bottom: 40px;
}

.university-logo {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 20px;
}

.university-name {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 30px;
  color: var(--primary);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 25px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.7;
  font-weight: 600;
}

.value {
  font-size: 1.1rem;
  font-weight: 500;
}

.team-section {
  margin-bottom: 40px;
}

.section-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 30px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.member-card {
  padding: 30px;
  text-align: center;
  transition: transform 0.3s ease;
}

.member-card:hover {
  transform: translateY(-5px);
}

.member-avatar {
  width: 80px;
  height: 80px;
  margin: 0 auto 15px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 700;
}

.member-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.member-code {
  color: var(--primary);
  font-weight: 500;
  opacity: 0.9;
}

.action-section {
  text-align: center;
  margin-top: 50px;
}

.btn-large {
  font-size: 1.2rem;
  padding: 18px 48px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.arrow {
  font-size: 1.5rem;
  transition: transform 0.3s ease;
}

.btn-large:hover .arrow {
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .team-grid {
    grid-template-columns: 1fr;
  }

  .info-card {
    padding: 25px;
  }
}
</style>