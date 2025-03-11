'use strict'

import $ from 'jquery'
import jun_da from 'jun_da_3000.txt';
import { getStoryDb } from './char_db';

function addHanziList() {
	//console.log(data0);
	const storyDb = getStoryDb();
	//console.log(map);
	
	const listEl = $('#hanzi_list');
	if (listEl[0] === undefined)
		return;
	
	const lines = jun_da.split('\n');
	for(const line of lines.slice(0, 40)) {
		for(const sym of line) {
			const span = $("<span/>");
			if (storyDb.has(sym)) {
				const link = $("<a/>");
				link.attr('href', `char.html?ch=${sym}`).text(sym);
				span.append(link);
			}
			else {
				span.text(sym);
			}
			span.addClass("m-1");
			listEl.append(span);
		}
		listEl.append($("<br>"));
	}
}

export {addHanziList}
