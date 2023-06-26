import { fileURLToPath, URL } from 'node:url'


import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Bloglite',
        short_name: 'Blog',
        theme_color: '#ffffff',
        description: 'My Progressive Web App',
        icons: [
          {
            src: '/icons/image.png',
            sizes: '256x256',
            type: 'image/png'
          },
        ]
      },
      workbox: {
        cleanupOutdatedCaches: true,
      }
    })
  ],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
