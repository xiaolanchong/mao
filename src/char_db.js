'use strict'

import dict0 from 'dict0001.yaml';

import story0 from 'story0001.yaml';


function getDictDb() {
	const map = new Map();
	for (const entry of dict0) {
		let key;
		for (const prop in entry) {
			key = prop;
			break;
		}
		map.set(key, entry[key])
	}
	return map;
}

function getStoryDb() {
	const map = new Map();
	for (const entry of story0) {
		let key;
		for (const prop in entry) {
			key = prop;
			break;
		}
		map.set(key, entry[key])
	}
	return map;
}

export { getDictDb, getStoryDb };
