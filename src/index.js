'use strict'

import $ from 'jquery'

import {addKeyList as addKeyListInt} from './key_list'
import {addHanziList as addHanziListInt} from './hanzi_list'
import {addHanziStories as addHanziStoriesInt} from './hanzi_story'

/*
$(function(){ 
  addKeyList();
  addHanziList();
})
*/

export function addKeyList() {
	$(function(){ 
	  addKeyListInt();
	})
}

export function addHanziList() {
	$(function(){ 
	  addHanziListInt();
	})
}

export function addHanziStories(crumbElId, storyElId) {
	$(function(){ 
	  addHanziStoriesInt(crumbElId, storyElId);
	})
}