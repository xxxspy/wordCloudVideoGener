from ddparser import DDParser
ddp = DDParser()
txt = '因子分析是一种统计技术，旨在研究变量群中提取共性因子。它通过研究众多变量之间的内部依赖关系，探求观测数据中的基本结构，并用少数几个假想变量来表示其基本的数据结构。这几个假想变量能够反映原来众多变量的主要信息。原始的变量是可观测的显在变量，而假想变量是不可观测的潜在变量，称为因子。'

splitors = '。，！？，'
# for seg in  '。，！？，':
#     txt = txt.replace(seg, '\n')
# sentences = txt.split('\n')


r=ddp.parse(txt)
print(r)

nodes = []
links =[]

group = 0
nid = 0
for word,head in zip(r[0]['word'], r[0]['head']):
    nid += 1
    if word in splitors:
        group += 1
    if nid > 1:
        links.append({
            'source': nid -1,
            'target': nid,
            'curve': 0,
        })
    nodes.append({
        'id': nid, 
        'group': group,
        'label': word,
    })
    if head > 0:
        links.append({
            'source': head,
            'target': nid,
            'curve': 0.6
        })

data = {
    'nodes': nodes, 'links': links,
}

import json
with open('word_cloud_video/testnetwork/data.json', 'w', encoding='utf8') as f:
    data = json.dumps(data)
    f.write(data)
