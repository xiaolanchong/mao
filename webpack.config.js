'use strict'

const path = require('path');
const yaml = require('yamljs');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer')
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const devMode = process.env.NODE_ENV !== "production";

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  devtool: devMode ? 'source-map' : 'none',
  devServer: {
    static: '.',
    client: {
      overlay: {
        errors: true,
        warnings: false,
        runtimeErrors: true,
      },
    },
  },
  output: {
    filename: 'bundle.js',
   // path: path.resolve(__dirname, 'dist'),
    path: __dirname,
  },
  module: {
    rules: [
	  {
        test: /\.yaml$/i,
        type: 'json',
        parser: {
          parse: yaml.parse,
        },
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(scss)$/,
        use: [
          {
            // Adds CSS to the DOM by injecting a `<style>` tag
            loader: 'style-loader'
          },
          {
            // Interprets `@import` and `url()` like `import/require()` and will resolve them
            loader: 'css-loader'
          },
          {
            // Loader for webpack to process CSS with PostCSS
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  autoprefixer
                ]
              }
            }
          },
          {
            // Loads a SASS/SCSS file and compiles it to CSS
            loader: 'sass-loader',
			options: {
			  sassOptions: {
				quietDeps: true,
				//silenceDeprecations: ['import', 'global-builtin', 'mixed-decls'],
			  }
			}
          }
        ]
      },	  
    ],
	
  },
  plugins: [
    // Provides jQuery for other JS bundled with Webpack
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    }),
	//new BundleAnalyzerPlugin(),
  ],
  externals: {
    jquery: 'jQuery',
	bootstrap: 'bootstrap',
  },
};