module.exports = {
    devServer: {
        proxy: "http://localhost:3344"
    },
    publicPath: "./",
    pluginOptions: {
      vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
    }
};
