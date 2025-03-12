'use strict'

import $ from 'jquery'
import { getStoryDb, getDictDb } from './char_db'
import {format} from './format'
import definitionTmpl from './definition.pug'
//import pug from "pug"

const noHanziInDictMsg = "对不起, в словаре нет иероглифа {0}";
//const noHanziInStoryDbMsg = "对不起, нет мнемофраз для иероглифа {0}";
const imagePath = '../images/stories'

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

	const dictEntry = dictDb.get(hanzi);
	const storyEntry = storyDb.get(hanzi);

	const PINYIN 		= 1
	const MEANING	 	= 2
	const EXAMPLE	 	= 3
	const tmplDictEntities = new Array()
	const addItem = (type, text) => tmplDictEntities.push({'type': type, 'text': text})
	for (const entity of dictEntry.def)
	{
		if(entity['py'] !== undefined)
			addItem(PINYIN, entity['py']);
		else if (entity['mn'] !== undefined)
			addItem(MEANING, entity['mn']);
		else if (entity['ex'] !== undefined) {
			for (const ex of entity['ex']) {
				addItem(EXAMPLE, ex)
			}
		}
	}

	const compiled = definitionTmpl({ 
		'hanzi': hanzi,
		'dict': tmplDictEntities,
		'story': storyEntry !== undefined ? {
			'keys': storyEntry.keys,
			'image': storyEntry.image !== undefined ? `${imagePath}/${storyEntry.image}` : undefined,
			'text': storyEntry.story,
		} : undefined,
	})
	$(`#${storyElId}`).html(compiled);
}

export { addHanziStories };
