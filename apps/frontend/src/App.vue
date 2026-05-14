<template>
  <div id="app" class="app">
    <header class="navbar">
      <div class="navbar-brand">
        <h1>📊 Data Pipeline Monitor</h1>
      </div>
      <nav class="navbar-menu">
        <router-link to="/">Home</router-link>
        <router-link to="/datasets">Datasets</router-link>
      </nav>
    </header>

    <main class="container">
      <router-view />
    </main>

    <footer class="footer">
      <p>&copy; 2026 Data Pipeline Monitor - Learning Project</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { defineComponent } from 'vue'
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand h1 {
  margin: 0;
  font-size: 1.5rem;
}

.navbar-menu {
  display: flex;
  gap: 2rem;
}

.navbar-menu a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.navbar-menu a:hover,
.navbar-menu a.router-link-active {
  background: #34495e;
}

.container {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 2rem;
  margin-top: auto;
}

.footer p {
  margin: 0;
}
</style>
