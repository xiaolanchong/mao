
# Система МАО

МАО - мнемонические ассоциации иероглифов.

Проект изучения китайский иероглифов через мнемоники.

## Сборка

npm run build
git commit -m "Comment"

## Структура

-- chars
  |_ dictNNNN.yaml  статьи толкового словаря
  |_ storyNNNN.yaml мнемоистории иероглифофв
  |_ \*.txt  списки иероглифов

-- css
  |_ \*.css  файлы стилей

-- images
   |_ headers  заголовки страниц 
   |_ keys     изображение ключей
   |_ stories  изображения для историй
   
-- scripts    Python script
-- site       html static pages
-- src        Javascript files
-- video      Original MAO system animated stories
-- video_gen  Neuronet generated stories


## Формат файла ключей иероглифов (key_list.yaml)

  - id: bee         текстовый идентификатор: a-z, 0-9 и _
    sym:
      - char:       массив (1 и более)
          rad: ⼂   компонент иероглифов, если есть в таблице Уникода
		   или
		  rad_img: blaster-rad.svg    изображение в папке images/keys/sym, если компонента нет в таблице Уникода
    name: ПЧЕЛКА    русское имя
    images: bee.png   изображение в папке images/keys
    text: В зависимости от создаваемой мнемосценки ее можно заменять на другие мелкие
      предметы.
    examples: 义 忍    примеры

## Формат storyNNNN.yaml файла


## Формат dictNNNN.yaml файла


## Как исправить описание ключа (mao/site/key_list.html)

1. Открыть src/key_list.yaml
2. Найти ключ и исправить (см. формат)
3. npm run build
4. git commit -m "Edited xxx key"
5. git push

## Как создать историю

1. Открыть chars/storyNNNN.yaml
2. Добавить иероглиф (см. формат)
3. npm run build
4. git commit -m "Added xxx characterd"
5. git push

