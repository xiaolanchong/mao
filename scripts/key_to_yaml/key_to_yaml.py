import typing

from bs4 import BeautifulSoup
import yaml


def read_keys():
    key_list = []
    with open("../../key_list.html", encoding='utf8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        # Find all td elements
        for tr in soup.find_all('tr')[1:]:
            td_tags = tr.find_all('td')
            #print(td_tags)
            number, keys, images, desc = td_tags
            keys =[span.text for span in keys.find_all('span')]
            image_srcs = [img['src'].split('/')[-1] for img in images.find_all('img')]
            parts = desc.text.split('\n')

            def splitp():
                for part in parts:
                    if len(part.strip()):
                        yield part.strip()
            lines = list(splitp())
            rus_name, text, examples = lines[0], lines[1:-1], lines[-1]
            if desc is None:
                print(number, keys, images, desc)
            key_list.append({
                'key': dict([
                          ('id', image_srcs[0].split('.')[0]),
                          ('sym', [('char', {'rad': key}) for key in keys]),
                          ('name', rus_name),
                          ('images', image_srcs[0] if len(image_srcs) == 1 else image_srcs),
                          ('text', ' '.join(text)),
                          ('examples', examples)
                       ])
            })
    import pprint
    #pprint.pprint(key_list)
    return key_list


keys = read_keys()

class IndentSafeDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentSafeDumper, self).increase_indent(flow, False)

#print(result)
with open('key_list_v3.yaml', mode='w', encoding='utf-8') as f:
    # safe_dump
    yaml.dump(keys, stream=f, Dumper=IndentSafeDumper, allow_unicode=True, sort_keys=False,
              canonical=False,
              explicit_start=False, explicit_end=False, version=(1,2))
