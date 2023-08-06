# Suluoya

### This is a package written by Suluoya not just for fun!

## If pip install Suluoya failed...

```python
pip install --ignore-installed llvmlite
#upgrade Suluoya(not need to uninstall)
import Suluoya as sly
sly.upgrade()
```

## If  this is the first time...

```python
#WELCOME
import Suluoya as sly
sly.welcome()
```

## If you wanna print error prettier

```python
import Suluoya as sly
sly.error()
print(1/0)
```

## If you wanna analyse your dataframe...

```python
import Suluoya as sly
import pandas as pd
df=pd.read_csv('https://sakai.unc.edu/access/content/group/3d1eb92e-7848-4f55-90c3-7c72a54e7e43/public/data/bycatch.csv')
report(df,explorative=False)
#This will make a html,just open it!
```

## If you wanna auto import some packages...

use"import Suluoya.Import as SI" instead of "import pandas as pd,import numpy as np"...

```python

#pass
import pandas as pd
import numpy as np
...
df=pd.Dataframe()
#now
import Suluoya.Import as SI
df=pd.Dataframe()
SI.check()#just to check your import by using SI,can be omitted
#ps.go and see a file named "auto_imports.py"!
```

## If you wanna writer the crawler simper...

```python
import Suluoya as sly
```

### directly get text from an URL

it will return a dictionary which contain title,text,description,keywords,tags,image,infomation and the raw_html

```python
data=sly.get_text(url='https://www.bilibili.com/video/BV1gt411D7gJ?p=29',useragent='',accurate=True)
print(data['title'])
```

### directly get soup from an URL

not need to fill all the blank

url='[https://pypi.org/project/Suluoya](https://pypi.org/project/Suluoya-pkg/)/' in default

encoding='utf8' in defaults

payloads means data in module "requests"

"show=False" means 'print(soup)' instead of 'return soup'

```python
sly.get_soup(url='',encoding='',headers='',params={},payloads={},show=False)
```

### directly get json from an URL

not need to fill all

if url='',Suluoya will go on strike

encoding='utf8' in default

payloads means data in module "requests"

"show=False" means show the json instead of return it

```python
sly.get_json(url='https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoforeignList',encoding='utf8',headers={},params={},payload={},show=False)
```

### directly get tables from an URL

if url='',Suluoya will go on strike

encoding='utf8' in default

header is the header of the table,try "header=0" instead of "header=None" in default

caption is the caption of the table,capture all the tables from the URL in defaults

if "save=True",tables will be saved in "1.xlsx","2.xlsx","3.xlsx"...

```python
sly.get_table(url='https://www.university-list.net/paiming/dx-160001.html',encoding='utf8',header=0,caption='.+',save=False)
```

### directly get links from an URL

if "show=True",return a list of all the URL

```python
sly.get_link(url='https://www.bilibili.com/video/BV1gt411D7gJ?p=29',encoding='utf8',headers={},params={},payload={},show=False)
```

### search question（under  maintenance）

```python
#search question by inputting for only once
sly.search_question()
#search question by inputting for many times
sly.search_question(again=True)
#search question by calling parameters and return answer
print(sly.search_question(question='Besides key points, the other element a summary should include is:'))
#search question by calling parameters and directly print answer 
sly.search_question(question='Besides key points, the other element a summary should include is:',show=True)
```

## If you wanna do something with your texts...

```python
import Suluoya as sly
```

### translate both English and Chinese into each other

if "show=False",return instead of print

```python
sly.translate(text='Welcome to use Suluoya!',show=True)
```

### compare the texts

accurate=True --> accurate match mode

accurate=False --> fuzzy match mode

show=False --> return ratio instead of print

```python
sly.text_compare(text1='Suluoya',text2='suluoya',accurate=True,show=True)
```

### sentiment analysis

language='C'-->Chinese

language='E'-->English

```python
sly.sentiment_analysis(text='',language='C',show=True)
```

### word frequency

count the number of times words appear

```python
sly.word_frequency(key='Suluoya',text='Welcome to use Suluoya!',show=True)
```

### guess gender 

name should be a Chinese name!

show=False --> return instead of print

```python
sly.gender_guess(name='Suluoya',show=True)
```

## If you wanna download something...

```python
import Suluoya as sly
```

### download music

```python
#download music  
sly.download_music()
#download music and play it
sly.download_music(play=True)
```

### download video

```python
sly.download_video(url='https://www.bilibili.com/video/BV1gt411D7gJ?p=29')
```

### download anything you want with an URL

```python
sly.download('http:\www...')
```

### download a big file

```python
sly.download_big_file(url='')
```

## If you wanna make a QRcode...

```python
import Suluoya as sly
```

### make a QRcode

fill in an url or some strings in content

fill in the name of the png in name

```python
sly.QRcode(content='',name='')
```

### contact

If you wanna contact Suluoya...

```python
sly.contact(mode='wechat')
sly.contact(mode='qq')
```

## If you wanna have fun...

```python
import Suluoya as sly
```

### draw a heart

```python
#draw a Suluoya heart
sly.draw_a_heart()
#draw any hearts you want
sly.draw_a_heart(name='any name you like')
```

### xkcd

```python
#you do know what I mean!
sly.xkcd()
```

### standard time

get standard time

show=False --> return instead of print

```python
sly.standard_time(show=True)
```

### voice synthesis

really make a sound

```python
sly.voice_synthesis(text='Welcome to use Suluoya!')
```

