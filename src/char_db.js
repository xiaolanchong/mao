'use strict'

import dict0 from 'dict0001.yaml';

import story0 from 'story0001.yaml';


function getDictDb() {
	const map = new Map();
	console.debug(dict0);
	for (const entry of dict0) {
		let key = entry['ch']
		map.set(key, entry)
	}
	//console.debug(map);
	return map;
}

function getStoryDb() {
	const map = new Map();
	console.debug(story0);
	for (const entry of story0) {
		let key = entry['ch']
		map.set(key, entry)
	}
	return map;
}

export { getDictDb, getStoryDb };
