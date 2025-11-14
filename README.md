# Drug Graph Visualizer 💊📊

Sistema de visualización de relaciones entre medicamentos basado en condiciones médicas compartidas.

**Universidad Peruana de Ciencias Aplicadas**  
Complejidad Algorítmica - 1ACC0184  
Ingeniería de Software - Sección 12600

---

## 👥 Integrantes

- Natalia Bertha Roman Cruz (U202310148)
- Stephano Renan Valdivia Quispe (U202311294)
- Diego Alejandro Vilca Saboya (U20231A778)

**Docente:** José Moisés Cumpa Torres

---

## 🏗️ Estructura del Proyecto

```
drug-graph-visualizer/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── drugs_side_effects_drugs_com.csv
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── router/
    │   ├── App.vue
    │   ├── main.js
    │   └── style.css
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 🚀 Instalación y Ejecución

### 📦 Requisitos Previos

- Python 3.8 o superior
- Node.js 16 o superior
- npm o yarn

---

### 🔧 Backend (FastAPI)

1. **Navegar a la carpeta backend:**
```bash
cd backend
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Colocar el archivo CSV:**
    - Asegúrate de tener el archivo `drugs_side_effects_drugs_com.csv` en la carpeta `backend/`

5. **Ejecutar el servidor:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará corriendo en: `http://localhost:8000`

---

### 🎨 Frontend (Vue 3 + Vite)

1. **Abrir una nueva terminal y navegar a la carpeta frontend:**
```bash
cd frontend
```

2. **Instalar dependencias:**
```bash
npm install
```

3. **Ejecutar el servidor de desarrollo:**
```bash
npm run dev
```

El frontend estará corriendo en: `http://localhost:5173`

---

## 🌐 Uso de la Aplicación

### 1. Pantalla de Presentación
- Visualiza la información del equipo y del proyecto
- Click en "Ir al Generador" para continuar

### 2. Generador de Grafos
Configura los parámetros:
- **Número máximo de nodos:** Limita la cantidad de medicamentos (opcional)
- **Velocidad de generación:**
    - Rápido (30 iteraciones)
    - Completo (70 iteraciones - recomendado)
- **Dataset completo:** Procesar todos los datos del CSV

Click en "Generar Grafo" y espera el procesamiento

### 3. Visualización
- **Zoom:** Usa la rueda del mouse o los botones
- **Pan:** Arrastra la imagen con el mouse
- **Descargar:** Guarda el grafo como PNG
- **Estadísticas:** Visualiza nodos, conexiones y densidad del grafo

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI:** Framework web moderno y rápido
- **Pandas:** Procesamiento de datos CSV
- **NetworkX:** Generación y análisis de grafos
- **Matplotlib:** Visualización de grafos

### Frontend
- **Vue 3:** Framework progresivo de JavaScript
- **Vite:** Build tool ultrarrápido
- **Vue Router:** Navegación entre páginas
- **Axios:** Cliente HTTP para APIs

---

## 📊 Características del Grafo

- **Nodos:** Cada medicamento es representado como un nodo
- **Aristas:** Conectan medicamentos que tratan la misma condición médica
- **Peso de aristas:** Mayor grosor indica más condiciones compartidas
- **Layout:** Spring Layout (Force-Directed) optimizado
- **Colores:** Azul (#00AEEF) para nodos, gris para conexiones

---

## 🎨 Diseño

- Tema oscuro con gradientes vibrantes
- Glassmorphism en cards y controles
- Totalmente responsive
- Tipografía moderna (Inter)
- Animaciones suaves

---

## 🐛 Solución de Problemas

### El backend no inicia:
- Verifica que el archivo CSV esté en la carpeta correcta
- Asegúrate de haber instalado todas las dependencias
- Revisa que el puerto 8000 no esté ocupado

### El frontend no se conecta al backend:
- Verifica que el backend esté corriendo
- Revisa la URL de la API en `GraphGenerator.vue` (línea 122)
- Desactiva temporalmente CORS en el navegador si es necesario

### Error al generar el grafo:
- Verifica que el archivo CSV tenga las columnas `drug_name` y `medical_condition`
- Asegúrate de que el dataset no esté vacío
- Revisa los logs del backend para más detalles

---

## 📝 Comandos Útiles

### Backend
```bash
# Instalar dependencias
pip install -r requirements.txt

# Correr servidor
uvicorn main:app --reload

# Ver documentación API
http://localhost:8000/docs
```

### Frontend
```bash
# Instalar dependencias
npm install

# Desarrollo
npm run dev

# Build para producción
npm run build

# Preview de producción
npm run preview
```

---

## 📄 Licencia

Proyecto académico - Universidad Peruana de Ciencias Aplicadas (UPC)

---

## 🤝 Contribuciones

Este es un proyecto académico. Para sugerencias o mejoras, contacta a los integrantes del equipo.

---

**Desarrollado con ❤️ por el equipo de Ingeniería de Software**