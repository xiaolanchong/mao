'use strict'

const format = (str, ...args) => {
    return str.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };

export {format}

