'use strict'

import $ from 'jquery'
import data from './key_list.yaml';
import './styles.scss'

const imagePath = "images/keys/new2";
const radicalPath = "images/keys";

const addSymbols = (tr, sym) => {
	const td = $("<td/>");
	if (sym instanceof Array) {
		let firstSym = true;
		for (const indivSym of sym) {
			const span = $("<span/>");
			if (indivSym.char.rad !== undefined) {
				span.text(indivSym.char.rad);
				if (indivSym.char.lang !== undefined) {
					span.attr('lang', indivSym.char.lang);
				}
				if (firstSym) {
					span.addClass("fs-1");
				} else {
					span.addClass("fs-2 text-body-secondary");
				}
			}
			else if (indivSym.char.rad_img !== undefined) {
				const img = createImage(radicalPath, indivSym.char.rad_img);
				img.attr('width', '40');
				span.append(img);
			}
			
			firstSym = false;
			td.append(span);
		}
	} else {
		console.error('Not array')
	}
	tr.append(td);
	return td;
}

const createImage = (parentDir, imgName) => $("<img/>").attr("src", `${parentDir}/${imgName}`);

const addImages = (tr, images) => {
	const td = $("<td/>");
	
	if (images instanceof Array) {
		for (const indivImg of images) {
			const tdImg = createImage(imagePath, indivImg);
			td.append($("<div/>").append(tdImg));
		}
	} else {
		const tdImg = createImage(imagePath, images);
		td.append(tdImg);
	}
	tr.append(td);
	return td;
}

function addKeyList() {
  const table = $("#key_table");
  if (!table)
    return;
  const tbody = $("tbody", table);
  let index = 0;
  for (const item of data) {
	++index;
	const tr = $("<tr/>");
	const tdNum = $("<td/>").text(index.toString());
	tr.append(tdNum);
	
	addSymbols(tr, item.key.sym);
	addImages(tr, item.key.images);
	
	const tdText = $("<td/>")
	if (item.key.id === undefined)
		console.warn(`No id for ${item.key}`);
	else
		tr.attr('id', item.key.id);
	tdText.append($("<div/>").text(item.key.name))
	tdText.append($("<div/>").text(item.key.text))
	tdText.append($("<div/>").text(item.key.examples).addClass("example"))
	tr.append(tdText);
	
    tbody.append(tr);
  }
}

export {addKeyList}
