<template>
  <div class="container">
    <div class="card">
      <h1>Prédiction Espèce de Manchot</h1>
      <p class="subtitle">
        Entrez les caractéristiques morphologiques pour obtenir une prédiction.
      </p>

      <form @submit.prevent="predict">
        <div class="grid">
          <div class="form-group">
            <label for="bill_length_mm">Longueur du bec (mm)</label>
            <input
              id="bill_length_mm"
              v-model.number="features.bill_length_mm"
              type="number"
              step="any"
            />
          </div>

          <div class="form-group">
            <label for="bill_depth_mm">Profondeur du bec (mm)</label>
            <input
              id="bill_depth_mm"
              v-model.number="features.bill_depth_mm"
              type="number"
              step="any"
            />
          </div>

          <div class="form-group">
            <label for="flipper_length_mm">Longueur des nageoires (mm)</label>
            <input
              id="flipper_length_mm"
              v-model.number="features.flipper_length_mm"
              type="number"
              step="any"
            />
          </div>

          <div class="form-group">
            <label for="body_mass_g">Masse corporelle (g)</label>
            <input
              id="body_mass_g"
              v-model.number="features.body_mass_g"
              type="number"
              step="any"
            />
          </div>
        </div>

        <button :disabled="loading">
          {{ loading ? "Analyse en cours..." : "Lancer la prédiction" }}
        </button>
      </form>

      <div v-if="result !== null" class="result">
        Résultat :
        <strong>{{ result }}</strong>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      features: {
        bill_length_mm: 0,
        bill_depth_mm: 0,
        flipper_length_mm: 0,
        body_mass_g: 0
      },
      result: null,
      loading: false
    }
  },
  methods: {
    async predict() {
      this.loading = true
      try {
        /*const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

        const res = await axios.post(`${API_BASE_URL}/predict`, {
          features: Object.values(this.features)
        })*/

       const res = await axios.post("/api/predict", {
          features: Object.values(this.features)
        })

        this.result = res.data.prediction
        
      } catch (err) {
        alert("Erreur lors de la prédiction: " + (err.response?.data?.detail || err.message))
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.card {
  background: #ffffff;
  max-width: 900px;
  width: 100%;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

h1 {
  text-align: center;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: #555;
  margin-bottom: 25px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}

input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
}

button {
  margin-top: 20px;
  width: 100%;
  padding: 14px;
  font-size: 16px;
  border: none;
  border-radius: 10px;
  background: #1e88e5;
  color: white;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #1565c0;
}

button:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.result {
  margin-top: 25px;
  padding: 15px;
  border-radius: 10px;
  font-size: 18px;
  text-align: center;
  background: #e8f5e9;
  color: #2e7d32;
}
</style>
