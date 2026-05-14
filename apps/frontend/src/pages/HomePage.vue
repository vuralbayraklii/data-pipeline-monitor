"""Home page component."""
<template>
  <div class="home">
    <h2>Welcome to Data Pipeline Monitor</h2>
    <p>A full-stack learning project for data platform architecture.</p>
    
    <section class="info-grid">
      <div class="info-card">
        <h3>📚 Learn</h3>
        <p>Understand full-stack development, GitHub workflows, and data platforms.</p>
      </div>
      <div class="info-card">
        <h3>🚀 Build</h3>
        <p>Create modules through realistic development scenarios.</p>
      </div>
      <div class="info-card">
        <h3>🤝 Collaborate</h3>
        <p>Practice proper versioning, issues, PRs, and CI/CD.</p>
      </div>
    </section>

    <section class="quick-links">
      <h3>Quick Start</h3>
      <ul>
        <li><router-link to="/datasets">View Datasets</router-link></li>
        <li><a href="https://github.com" target="_blank">GitHub Repository</a></li>
        <li><a href="/docs/architecture/">Architecture Docs</a></li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home {
  padding: 2rem 0;
}

h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
}

.info-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.info-card h3 {
  margin-top: 0;
  color: #2c3e50;
}

.quick-links {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-links ul {
  list-style: none;
  padding: 0;
}

.quick-links li {
  padding: 0.5rem 0;
}

.quick-links a {
  color: #0066cc;
  text-decoration: none;
}

.quick-links a:hover {
  text-decoration: underline;
}
</style>
