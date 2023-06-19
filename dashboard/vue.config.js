const { defineConfig } = require('@vue/cli-service')

process.env.NODE_ENV === 'production'

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
     webSocketServer: false
  }
})
