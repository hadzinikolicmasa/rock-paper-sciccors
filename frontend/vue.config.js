const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    proxy: {
      '/choices': {
        target: 'http://backend:5000',
        changeOrigin: true
      },
      '/play': {
        target: 'http://backend:5000',
        changeOrigin: true
      },
      '/results/reset': {
        target: 'http://backend:5000',
        changeOrigin: true
      },
       '/results': {
        target: 'http://backend:5000',
        changeOrigin: true
      },
       '/register': {
        target: 'http://backend:5000',
        changeOrigin: true
      },
        '/multi/play': {
        target: 'http://backend:5000',
        changeOrigin: true
      },
        '/multi/status': {
        target: 'http://backend:5000',
        changeOrigin: true
      }
    }
  }
}
