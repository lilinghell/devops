const path = require('path');
const apiMocker = require('mocker-api');

module.exports = {
  lintOnSave: process.env.NODE_ENV !== 'production',
  pluginOptions: {
    quasar: {
      theme: 'mat',
      importAll: true
    }
  },
  transpileDependencies: [
    'vue-echarts',
    'resize-detector',
    /[\\/]node_modules[\\/]quasar[\\/]/
  ],
  devServer: {
    overlay: {
      errors: true
    },
    /*before(app) {
      // unnecessary fill in all mock files
      apiMocker(app, path.resolve('./mock/index.js'));
    }*/
    proxy: "http://127.0.0.1:8000/",
  },
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  css: {
    loaderOptions: {
      stylus: {
        import: ['~quasar-variables', '~quasar-variables-styl']
      }
    }
  }
};
