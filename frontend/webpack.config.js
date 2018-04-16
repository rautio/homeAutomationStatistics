// Webpack Config
const BabiliPlugin = require('babili-webpack-plugin');
const path = require('path');
const { env } = require('yargs').argv;

const plugins = [];
let devServer = {};
let devtool = '';
//For build mode we output a minified file. This is what will be published to npm.
//Otherwise we can use the unminified version for development and debugging.
if (env === 'build') {
  plugins.push(new BabiliPlugin());
  // This is where we could distinguish a .min.js version for build
  // But I'm keeping both versions as .js for now for ease of development
} else {
  devServer = {
    port: 8080,
    index: './index.html',
  };
  devtool = 'source-map';
}
module.exports = {
  entry: path.resolve(__dirname, './src/index.js'),
  plugins,
  target: 'web',
  output: {
    path: path.resolve('dist'),
    filename: 'bundle.js',
    publicPath: 'dist',
  },
  devtool,
  devServer,
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.(js|jsx)$/,
        loader: "eslint-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.scss$|\.css$/,
        loader: 'style-loader!css-loader!scss-loader!resolve-url',
      },
    ],
  },
};
