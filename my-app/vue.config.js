const { defineConfig } = require('@vue/cli-service', 'vue-csv-import')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  publicPath: process.env.NODE_ENV === 'development' ? '/vue-csv-import/' : './'
}
