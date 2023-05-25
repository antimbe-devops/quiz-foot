<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="header">
    <div class="left">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>

    <div class="center">
      <div class="logo">
        <RouterLink to="/">
          <img src="@/assets/logoesieefc.png" alt="Logo" />
        </RouterLink>
      </div>
    </div>
  </div>

  <RouterView />
</template>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #000000;
  padding: 10px;
  margin-bottom: 200px;
  z-index: 1;
  /* Ajoutez cette ligne */
}


.left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.center {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
}

.logo {
  margin-right: auto;
  margin-left: auto;
  font-size: 24px;
  font-weight: bold;
}

nav {
  flex-shrink: 0;
  font-size: 18px;
  margin-right: 1rem;
}

/*
.content::-webkit-scrollbar {
  width: 8px;
}

.content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.content::-webkit-scrollbar-thumb {
  background: #888;
}

.content::-webkit-scrollbar-thumb:hover {
  background: #555;
}
*/

nav {
  flex: 0;
  font-size: 18px;
  margin-right: 1rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>
