
# Script to grab MAO system key table data
# 1. Go to a table page, e.g.
#      https://web.archive.org/web/20180606082838/http://www.umao.ru/system/maosyspics/221-maosyspic25.html
# 2. Open browser devtools (F12)
# 3. Inspect the key table and copy <table> element content
# 4. Past it to html_doc var

from bs4 import BeautifulSoup

html_doc = """
<table cellspacing="4" cellpadding="4" border="0" align="center">
    <tbody>
        <tr align="center" valign="top">
            <td align="center" width="49" valign="middle">номер</td>
            <td align="center" width="80" valign="middle">радикал</td>
            <td align="center" width="82" valign="middle">картинка</td>
            <td bgcolor="#efefef" align="center" width="280" valign="middle">мнемоключик и примеры</td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">241</td>
            <td align="right" width="80" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad17.gif" alt=""></td>
            <td align="right" width="82" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad17a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>ЮБОЧКА </strong><br>
            <br>
            <span style="font-size: x-large;">份</span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">242</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad18.gif" alt=""></td>
            <td align="right" width="82" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad21a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>ГЛАЗКИ, РОЖКИ, УСИКИ </strong><br>
            и тому подобное <br>
            <br>
            <span style="font-size: x-large;">併 兑  </span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">243</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad19.gif" alt=""></td>
            <td align="right" width="82" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad29a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>НОЖКИ, ЛАПКИ, ПАЛЬЧИКИ</strong><br>
            и тому подобное<br>
            <br>
            <span style="font-size: x-large;">帜  </span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">244</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad27.gif" alt=""></td>
            <td align="right" width="82" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad28a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>БУКВА Е </strong><br>
            <br>
            <span style="font-size: x-large;">印  </span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">245</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad20.gif" alt=""></td>
            <td align="right" width="82" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad20a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>СУЧОК, ЧУРКА, ЧУРБАН</strong><br>
            или, на что еще там похоже:)<br>
            <br>
            <span style="font-size: x-large;">扑 </span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">246</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad21.gif" alt=""></td>
            <td align="right" width="82" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad25a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>ЛИСТИК</strong><br>
            <br>
            <span style="font-size: x-large;">乎 币 </span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">247</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad22.gif" alt=""></td>
            <td align="right" width="82" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad22a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>БОГОР</strong><br>
            <br>
            <span style="font-size: x-large;">买  </span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">248</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad23.gif" alt=""></td>
            <td align="right" width="82" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad23a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>ПУЛЕМЕТ</strong><br>
            <br>
            <span style="font-size: x-large;">虍  </span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">249</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad25.gif" alt=""></td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad24a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>ШЛЕМ</strong><br>
            <br>
            <span style="font-size: x-large;">散  </span></td>
        </tr>
        <tr align="center" valign="top">
            <td align="center" valign="middle">250</td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad26.gif" alt=""></td>
            <td align="right" valign="middle"><img height="80" width="80" src="/web/20180606082838im_/http://www.umao.ru/images/stories/cards/ad26a.gif" alt=""></td>
            <td bgcolor="#efefef" align="left" width="280" valign="middle"><strong>РЕШЕТКА</strong><br>
            <br>
            <span style="font-size: x-large;">讲  </span></td>
        </tr>
    </tbody>
</table>
"""


def get_radicals(text):
    soup = BeautifulSoup(text, 'html.parser')

    for tr in soup.table.tbody.find_all('tr')[1:]:
        tds = tr.find_all('td')
        num = int(tds[0].text)
        img = tds[2].img['src'].split('/')[-1]
        text = tds[3].text
        lines = text.split('\n')
        name = lines[0].strip()
        samples = lines[-1].strip()
        comments = '\n'.join(line.strip() for line in lines[1:-1] if line.strip())
        # print(num, img, name, comments, samples)
        yield num, img, name, comments, samples


def generate(text):
    path = 'images/keys'
    for num, img, name, comments, samples in get_radicals(text):
        tr = f"""
        <tr>
		  <td>{num}</td>
		  <td>
		    <span class="fs-1">00K</span>
		  </td>
		  <td><img src="{path}/{img}" /></td>
		  <td>{name}<br>
			 {comments}<br>
			<span class="fs-4">{samples}</span>
		  </td>
		</tr>"""
        print(tr)


generate(html_doc)

