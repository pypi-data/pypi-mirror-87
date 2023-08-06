#analyze
def report(df,explorative=False):
    import pandas_profiling
    a=pandas_profiling.ProfileReport(df,title='Suluoya',explorative=explorative)
    a.to_file('report.html')
#download
def download_big_file(url):
    import requests
    from tqdm import tqdm
    import re
    a=re.findall('/(.*)/',url)[0]
    b=re.findall(f'{a}/(.*)',url)[0]
    try:
        res=requests.get(url,stream=True)
        with open(r'{}'.format(b),'wb') as f:
            for chunk in tqdm(res.iter_content(chunk_size=1024)):
                if chunk:
                    f.write(chunk)
    except:
        print('Something went wrong!')
def download(url):
    import wget
    import ssl
    try:
        ssl._creat_default_https_context=ssl._create_unverified_context
        wget.download(url)
    except:
        print('Something went wrong!')
def download_music(play=False):
    import requests
    import urllib.parse as parse
    from urllib.request import urlretrieve
    import json
    import urllib.request
    w=parse.urlencode({'w':input('请输入歌名:')})
    url='https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=63229658163010696&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&%s&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'%(w)
    content=requests.get(url=url)
    str_1=content.text
    dict_1=json.loads(str_1)
    song_list=dict_1['data']['song']['list']
    str_3='''https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey5559460738919986&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"1825194589","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"1825194589","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'''
    url_list=[]
    music_name=[]
    for i in range(len(song_list)):
        music_name.append(song_list[i]['name']+'-'+song_list[i]['singer'][0]['name'])
        print('{}.{}-{}'.format(i+1,song_list[i]['name'],song_list[i]['singer'][0]['name']))
        url_list.append(str_3 % (song_list[i]['mid']))
    id=int(input('请输入你想下载的音乐序号:'))
    content_json=requests.get(url=url_list[id-1])
    dict_2=json.loads(content_json.text)
    url_ip=dict_2['req']['data']['freeflowsip'][1]
    purl=dict_2['req_0']['data']['midurlinfo'][0]['purl']
    downlad=url_ip+purl    
    try:
        print('开始下载...')
        urlretrieve(url=downlad,filename='{}.mp3'.format(music_name[id-1]))
        print('{}.mp3下载完成!'.format(music_name[id-1]))
    except Exception as e:
        print('没有{}的版权'.format(music_name[id-1]))
    if play == True:
        import time
        time.sleep(2)
        import pyglet
        music = pyglet.resource.media('{}.mp3'.format(music_name[id-1]))
        music.play()
        pyglet.app.run()
def download_video(url):
    import os
    try:
        os.system(f'you-get {url}')
    except:
        print('Something went wrong!')
#fun
def error():
    import pretty_errors

def draw_a_heart(name='Suluoya'):
    try:
        print('\n'.join([''.join([(name[(x-y)%len(list(name))]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))
    except:
        print('请输入字符串！')
def standard_time(show=True):
    import time
    t=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if show == True:
        print(t)
    return t
def xkcd():
    import antigravity
def syy():
    draw_a_heart('syy')
def hqy():
    draw_a_heart('hqy')
def wyx():
    draw_a_heart('wyx')
def lsf():
    print('SB')
#QRcode
def QRcode(content='I Love Suluoya!',name='QRcode'):
    from MyQR import myqr
    myqr.run(words=content,save_name=name+'.png')
def contact(mode='qq'):
    qq='https://qm.qq.com/cgi-bin/qm/qr?k=SQEky7p_hr1bclCGYHLO9YHGEV2SCcg1&noverify=0'    
    wechat='https://u.wechat.com/ELmeETBV3ihbSWAoJogLLp0'
    from MyQR import myqr
    print('Thanks for your support!\nMy contact code is already created!\nPlease search for QRcode.png in the current directory!\nThanks again! ')
    if mode=='qq':
        myqr.run(words=qq,save_name='qq_QRcode.png')
    elif mode == 'wechat':
        myqr.run(words=wechat,save_name='wechat_QRcode.png')
    else:
        print('Please choose the a mode:\nqq in default or wechat instead')
#spider
def search_question(question='',again=False,show=False):
    #http://tiku.71kpay.com/api/dj.html
    #https://wangke.vvhan.com/
    #http://free.han8.net/?ti=题目
    import requests
    import json
    if question !='':
        url='http://api.xmlm8.com/tk.php?t={}'.format(question)
        response = requests.request("GET", url)
        data=json.loads(response.text)
        if show == True:
            print(data['tm']+'\n'+data['da']+'\n')
        else:
            return(data['tm']+'\n'+data['da']+'\n')
    else:
        if again == False:        
            timu=input('Please input the question:')
            url='http://api.xmlm8.com/tk.php?t={}'.format(timu)
            try:
                response = requests.request("GET", url)
                data=json.loads(response.text)
                print(data['tm']+'\n'+data['da']+'\n')
            except:
                mistake='Could not find the answer!'
                print(mistake) 
        else:
            while 1:
                timu=input('请输入题目：')
                url='http://api.xmlm8.com/tk.php?t={}'.format(timu)
                try:
                    response = requests.request("GET", url)
                    data=json.loads(response.text)
                    print(data['tm']+'\n'+data['da']+'\n')                
                except:
                    mistake='Could not find the answer!'
                    print(mistake)
def get_link(url='https://pypi.org/project/Suluoya/',encoding='utf8',headers={},params={},payload={},show=False):
    import requests
    import re
    html = requests.request("GET", url, headers=headers, data = payload, params = params).text
    links = re.findall('"((http|ftp)s?://.*?)"', html)
    lists=[]
    for i in links:
        lists.append(i[0])
    if show==True:
        for i in lists:
            print(i)
    else:
        return lists
def get_table(url,encoding='utf8',header=None,caption='.+',save=False):
    import pandas as pd
    try:
        dfs=pd.read_html(io=url,encoding=encoding,header=header,match=caption)
        if len(dfs)>1:
            print('='*13)
            print(f'Get {len(dfs)} tables.')
            print('='*13)
            print('\n')
        elif len(dfs)==1:
            pass
        lists=[]
        for df in dfs:
            df.dropna(how='all',inplace=True)
            lists.append(df)
        if save == True:
            k=0
            for i in lists:
                k+=1
                i.to_excel(f'{k}.xlsx',index=False)
        return lists 
    except:
        print('No tables found!')
def get_soup(url='https://pypi.org/project/Suluoya/',encoding='utf8',headers={},params={},payload={},show=False):
    import requests
    from bs4 import BeautifulSoup
    try:
        response = requests.request("GET", url, headers=headers, data = payload, params = params)
        response.encoding=encoding
        soup = BeautifulSoup(response.text,'html.parser')
        if show == True:
            print(soup)
        return(soup)
    except:
        try:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            if show == True:
                num=str(response)[-5:-2]
                print('HTTP Status Code ='+num)
                print('Please access https://www.cnblogs.com/hao-1234-1234/p/8940079.html')                
        except:
            print('Something went wrong!')    
def get_json(url='',encoding='utf8',headers={},params={},payload={},show=False):
    import json
    import requests
    try:
        if url == '':
            print('Please add an url!')
        else:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            response.encoding=encoding
            data=json.loads(response.text)
            if show==True:
                print(data)
            return(data)
    except:
        try:
            response = requests.request("GET", url, headers=headers, data = payload, params = params)
            num=str(response)[-5:-2]
            print('HTTP Status Code ='+num)
            print('Please access https://www.cnblogs.com/hao-1234-1234/p/8940079.html')
        except:
            print('Something went wrong!')
def get_text(url='',useragent='',accurate=True):
    try:    
        from goose3 import Goose
        if accurate == True:
            from goose3.text import StopWordsChinese
            g = Goose({'stopwords_class': StopWordsChinese,
                    'browser_user_agent': useragent
                    })
        else:
            g = Goose({'browser_user_agent': useragent
                    })
        url = url
        article=g.extract(url=url)
        dic={
        'title':article.title,#标题
        'text':article.cleaned_text,#正文
        'description':article.meta_description,#摘要
        'keywords':article.meta_keywords,#关键词
        'tags':article.tags,#标签
        'image':article.top_image,#主要图片
        'infomation':article.infos,#包含所有信息的 dict
        'raw_html':article.raw_html#原始 HTML 文本
        }
        return dic
    except:
        print('Something went wrong!')
#voice
def voice_synthesis(text='Welcome to use Suluoya!'):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
#upgrade
def upgrade():
    try:
        import os
        os.system('pip install --upgrade Suluoya')
    except:
        print('Something went wrong!')
#text
def translate(text='Welcome to use " sly.apy () "function to make a donation!',show=True):
    import translators as ts
    if text=='Welcome to use "sly.apy ()" to make a donation!':
        print(text)
    else:
        if show==True:
            try:
                print(ts.baidu(text, professional_field='common'))
            except:
                print('Something went wrong!')
        else:
            try:
                return(ts.baidu(text, professional_field='common'))
            except:
                print('Something went wrong!')
def text_compare(text1='suluoya',text2='Suluoya',accurate=True,show=True):
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    if show == True:
        if accurate == True:
            print(f'The similarity of {text1} and {text2} is '+str(fuzz.ratio(text1,text2))+'%.')
        else:
            print(f'The similarity of {text1} and {text2} is '+str(fuzz.partial_ratio(text1,text2))+'%.')
    else:
        if accurate == True:
            return fuzz.ratio(text1,text2)/100
        else:
            return fuzz.partial_ratio(text1,text2)/100
def gender_guess(name='苏洛雅',show=True):
    import ngender as nd
    try:
        if show==True:
            print(f'{round(nd.guess(name)[1]*100,2)}% could be a {nd.guess(name)[0]}.')
        else:
            return nd.guess(name)
    except:
        print('The name should be Chinese!')
def word_frequency(key='',text='',show=True):
    from flashtext import KeywordProcessor
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keyword(key)
    keywords_found = keyword_processor.extract_keywords(text)
    if show==True:
        print(len(keywords_found))
    else:
        return len(keywords_found)
def sentiment_analysis(text='',language='C',show=True):
    try:
        if language=='E':
            from textblob import TextBlob
            blob = TextBlob(text)
            if show == True:
                print(f'The probability of postive emotion is {blob.sentiment[0]}')
            else:
                return blob.sentiment[0]
        elif language == 'C':
            from snownlp import SnowNLP
            s = SnowNLP(text)
            if show == True:
                print(f'The probability of postive emotion is {s.sentiments}')
            else:
                return s.sentiments
        else:
            print('Please choose a correct languge!')
    except:
        print('Something went wrong!')