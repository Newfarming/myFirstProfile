'use strict';
var fs = require('fs');
exports.fileExists = function(filePath) {
    try {
        return fs.statSync(filePath).isFile();
    } catch (err) {
        return false;
    }
};