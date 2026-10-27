'use strict';
const characterIndex = JSON.parse(document.getElementById('character-index').textContent);
const keys = JSON.parse(document.getElementById('key-data').textContent);
const characterOrder = JSON.parse(document.getElementById('character-order').textContent);
const el = id => document.getElementById(id);
function renderCharacterBand(char) {
  const band = el('character-band');
  band.replaceChildren();
  const current = characterOrder.indexOf(char);
  band.hidden = current < 0;
  if (current < 0) return;
  characterOrder.slice(Math.max(0, current - 5), current + 6).forEach(neighbor => {
    const active = neighbor === char;
    const item = document.createElement(active ? 'span' : 'a');
    item.textContent = neighbor;
    item.className = active ? 'text-body fw-bold px-2' : 'text-decoration-none px-1';
    if (active) item.setAttribute('aria-current', 'page');
    else item.href = `?h=${encodeURIComponent(neighbor)}`;
    band.append(item);
  });
}
function toneMarks(value) {
  return value.replace(/([a-züÜvV:]+)([0-5])/gi, (_, raw, tone) => {
    const syllable = raw.toLowerCase().replace(/u:|v/g, 'ü');
    if (+tone === 0 || +tone === 5) return syllable;
    let index = syllable.indexOf('a');
    if (index < 0) index = syllable.indexOf('e');
    if (index < 0 && syllable.includes('ou')) index = syllable.indexOf('o');
    if (index < 0) {
      for (let i = syllable.length - 1; i >= 0; i--) {
        if ('iouü'.includes(syllable[i])) { index = i; break; }
      }
    }
    if (index < 0) return syllable;
    const marks = {a:'āáǎà',e:'ēéěè',i:'īíǐì',o:'ōóǒò',u:'ūúǔù',ü:'ǖǘǚǜ'};
    return syllable.slice(0,index) + marks[syllable[index]][+tone-1] + syllable.slice(index+1);
  });
}
function keyLink(text, id) {
  const link = document.createElement('a');
  link.textContent = text;
  link.href = 'key_list.html#' + encodeURIComponent(id);
  return link;
}
function render(data) {
  document.title = `${data.character} — МАО`;
  el('character').textContent = data.character;
  const ranking = data.ranking;
  const frequency = el('frequency');
  frequency.hidden = !Number.isInteger(ranking) || ranking < 1;
  if (!frequency.hidden) {
    const level = ranking <= 1000 ? 3 : ranking <= 2000 ? 2 : ranking <= 3000 ? 1 : 0;
    const category = ['Редкие', 'Менее частые', 'Частые', 'Очень частые'][level];
    frequency.dataset.level = level;
    frequency.title = `Частотный ранг: ${ranking} — ${category}`;
    frequency.setAttribute('aria-label', frequency.title);
  }
  const encodedCharacter = encodeURIComponent(data.character);
  el('dictionary-bkrs').href = `https://bkrs.info/slovo.php?ch=${encodedCharacter}`;
  el('dictionary-mdbg').href = `https://www.mdbg.net/chinese/dictionary?page=chardict&cdcanoce=0&cdqchi=${encodedCharacter}`;
  const unicodeCode = data.character.codePointAt(0).toString(16).toUpperCase();
  el('dictionary-gxdq').href = `https://www.gxdq.com/zidian/${unicodeCode}.html`;
  el('pinyin').replaceChildren();
  data.pinyin.forEach((reading, index) => {
    if (index) el('pinyin').append(' / ');
    const span = document.createElement('span');
    span.textContent = toneMarks(reading);
    const tone = reading.match(/([1-5])$/)?.[1];
    span.className = `tone-${tone || 'neutral'}`;
    el('pinyin').append(span);
  });
  el('meaning').textContent = data.meaning.join('; ');
  const components = data.components || [];
  components.forEach((component, index) => {
    if (index) el('components').append(', ');
    if (component.character && !component.ad_hoc) {
      const link = document.createElement('a');
      link.textContent = component.key;
      link.href = 'hanzi.html?h=' + encodeURIComponent(component.character);
      el('components').append(link);
      return;
    }
    const target = component.target ?? component.key;
    const match = component.ad_hoc ? undefined : Object.entries(keys).find(([id, key]) => id === target || key.name.toLocaleLowerCase('ru') === target.toLocaleLowerCase('ru') || key.name.toLocaleLowerCase('ru').split(/[,;]/).some(name => name.trim() === target.toLocaleLowerCase('ru')));
    el('components').append(match ? keyLink(component.key, match[0]) : document.createTextNode(component.key));
  });
  if (!components.length) el('components').textContent = 'Не указаны.';
  const once = data.structure?.once || [];
  const displayParts = parts => parts.map(part => part ?? '□').join(' + ');
  el('structure').textContent = displayParts(once) || 'Не указана в базе.';
  (data.mnemonic || []).forEach(([text, type, id]) => {
    let node;
    if (type === 0) node = keyLink(text, id);
    else {
      node = document.createElement(type === 1 ? 'mark' : 'span');
      node.textContent = text;
      if (type === 3) { node.className = 'compound'; node.title = `Составной элемент: ${id}`; }
    }
    el('mnemonic').append(node);
  });
  if (!data.mnemonic?.length) el('mnemonic').textContent = 'История пока не добавлена.';
  if (data.video) {
    const url = new URL(data.video, new URL('../', document.baseURI));
    if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Некорректный адрес видео.');
    const video = document.createElement('video');
    video.controls = true; video.preload = 'metadata'; video.className = 'w-100 rounded';
    video.setAttribute('aria-label', `Мнемоническая история: ${data.character}`);
    video.src = url.href;
    video.append('Ваш браузер не поддерживает видео.');
    video.addEventListener('error', () => { el('video').textContent = 'Видео недоступно.'; });
    el('video').append(video);
  } else el('video').textContent = 'Видео пока не добавлено.';
  el('status').hidden = true;
  el('content').hidden = false;
}
async function loadCharacter() {
  const char = new URLSearchParams(location.search).get('h')?.trim();
  if (!char) return;
  el('query').value = char;
  renderCharacterBand(char);
  if (!Object.hasOwn(characterIndex, char)) {
    el('status').textContent = `Иероглиф «${char}» пока отсутствует в базе.`;
    return;
  }
  el('status').textContent = 'Загрузка…';
  try {
    const folder = characterIndex[char];
    const response = await fetch(`../cdb/${encodeURIComponent(folder)}/${encodeURIComponent(char)}.json`);
    if (!response.ok) throw new Error(`Ошибка загрузки (${response.status}).`);
    const data = await response.json();
    if (data.character !== char) throw new Error('Данные не соответствуют иероглифу.');
    render(data);
  } catch (error) {
    el('status').textContent = `Не удалось открыть иероглиф. ${error.message}`;
  }
}
loadCharacter();
