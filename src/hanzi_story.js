'use strict'

import $ from 'jquery'
import { getStoryDb, getDictDb } from './char_db'
import {format} from './format'
import storyTmpl from './story.pug'
//import pug from "pug"

const noHanziInDictMsg = "对不起, в словаре нет иероглифа {0}";
//const noHanziInStoryDbMsg = "对不起, нет мнемофраз для иероглифа {0}";

function addHanziStories(crumbElId, storyElId) {
	storyElId;
	const searchParams = new URLSearchParams(window.location.search);
	const hanzi = searchParams.get('ch')
	if (hanzi === undefined)
		return;
	$(`#${crumbElId}`).text(hanzi);
	$("h1").text( $("h1").first().text() + ' ' + hanzi  );
	
	const dictDb = getDictDb();
	if (!dictDb.has(hanzi)) {
		const noHanzi = $("<div/>").text(format(noHanziInDictMsg, hanzi));
		noHanzi.addClass("text-danger").addClass("fs-1");
		$(`#${storyElId}`).append(noHanzi);
		return;
	}
	const storyDb = getStoryDb();
	if (!storyDb.has(hanzi)) {
		console.warn('No story')
	}

	const PINYIN 		= 1
	const DEFINITION 	= 2
	const EXAMPLE	 	= 3
	const compiled = storyTmpl(
		{ 'entries': 
			[	{ 'type': PINYIN, 'text': 'de' }, 
				{ 'type': DEFINITION, 'text': '-ный (суффикс, чей, 红的 hóngd), точный, цель' }, 
				{ 'type': EXAMPLE, 'text': 'very glad that you like my sentence' }, 
			],
		  'hanzi': hanzi,	
	})
	$(`#${storyElId}`).html(compiled);
}

export { addHanziStories };
