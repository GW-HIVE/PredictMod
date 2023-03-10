module.exports = {
    // devServer: {
    //     proxy: "http://localhost:3344"
    // },
    outputDir: "dist/",
    publicPath: "./",
    pluginOptions: {
      vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		},
    filenameHashing: false,
    configureWebpack: {
      devServer: {
        devMiddleware: {
          writeToDisk: true
        }
      }
    }
  }
}
