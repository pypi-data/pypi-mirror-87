const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const path = require('path');

module.exports = {
mode: 'development',
entry: {
    'pivot': './src/index.js'
},
output: {
    filename: '[name].js',
    path: path.resolve(__dirname, '../browser/static/pivot'),
},
module: {
    rules: [
        {
            test: /.(js|jsx)$/,
            exclude: /node_modules/,
            use: ['babel-loader']
        },
        {
            test: /.css$/,
            use: ['style-loader', 'css-loader'],
        },
        {
            test: /\.(png|jpe?g|gif)$/,
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
            },
          }
    ]
},
plugins: [
    new HtmlWebpackPlugin({
        filename: 'index.html',
        template: 'src/index.html'
        })
],
devServer: {
    contentBase: path.resolve(__dirname, '../browser/static/pivot'),
    open: true,
    port: 3000
},
};