from selenium.webdriver import Chrome
import time
import datetime
import pandas as pd
from random import randint 
from selenium.common.exceptions import NoSuchElementException
import jieba
import jieba.analyse


# 帖子和评论信息
def scrape_page():

    time.sleep(randint(1,2))

    # try:
    #     pt_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/header/div[1]/div/div[2]/a')
    # except NoSuchElementException:
    #     web.refresh()
    #     time.sleep(1)

    found=False
    count = 0
    while not found and count<5:
    # while not found:
        try:
            pt_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/header/div[1]/div/div[2]/a')
            found = True
        except NoSuchElementException:
            web.refresh()
            time.sleep(randint(1, 2))
            count += 1
            # pt_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/header/div[1]/div/div[2]/a')
    if not found:
        return
    
    news_id.append(titleid)
    # context_id
    tgt_id.append('')
    publish_time.append(pt_posts.text[:-5])
    type.append('posts')
    ui_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/header/div[1]/div/div[1]/a/span')
    user_id.append(ui_posts.text)
    tgt_user_id.append('')
    content_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/div/div/div')
    content.append(content_posts.text)

    try:
        pic_url_posts = web.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/div/div[2]//img').get_attribute('src')
        pic_url.append(pic_url_posts)
    except NoSuchElementException:
        pic_url.append(None)
    try:
        video_url_posts = web.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/div/div[1]//a[@target="_blank"][starts-with(@href, "https://video")]').get_attribute('href')
        video_url.append(video_url_posts)
    except NoSuchElementException:
        video_url.append(None)
    try:
        at_user_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/div/div/div/a[starts-with(text(), "@")]')
        at_user.append(at_user_posts.text)
    except NoSuchElementException:
        at_user.append(None)
    try:
        hashtag_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/div/div/div/a[starts-with(text(), "#")]')
        hashtag.append(hashtag_posts.text)
    except NoSuchElementException:
        hashtag.append(None)
    try:
        view_count_posts=web.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/main/div/div/div[2]/article/div[2]/div/div[2]/div/div/div[3]')
        view_count.append(view_count_posts.text)
    except NoSuchElementException:
        view_count.append('')


    like_count_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/footer/div/div[1]/div/div[3]/div/button/span[2]')
    # like_count_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/footer/div/div[3]/div/button/span[2]')
    if '赞' in like_count_posts.text:
        like_count.append('')
    else:
        like_count.append(like_count_posts.text)

    dislike_count.append('')

    cmt_count_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/footer/div/div[1]/div/div[2]/div/span')
    # cmt_count_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/footer/div/div[2]/div/span')
    if '评论' in cmt_count_posts.text:
        cmt_count.append('')
    else:
        cmt_count.append(cmt_count_posts.text)

    repost_count_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/footer/div/div[1]/div/div[1]/div/div/span/div/span')
    # repost_count_posts = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/article/footer/div/div[1]/div/div/span/div/span')
    if '转发' in repost_count_posts.text:
        repost_count.append('')
    else:
        repost_count.append(repost_count_posts.text)


    # 下滑至底部
    last_height = web.execute_script("return document.body.scrollHeight")
    while True:
        # web.execute_script("window.scrollTo(0, document.body.scrollHeight)/5;")
        web.execute_script("window.scrollBy(0, 950);")

        # time.sleep(randint(2,3))
        time.sleep(randint(1,2))

        # 评论信息-------------------------------------

        pt_cmts = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div[1]')
        ui_comts = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/div[1]/div[2]/div[1]/a[1]')
        content_cmts = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/div[1]/div/div[1]/span')
        like_count_cmts = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/div[1]/div[2]/div[2]/div[2]')
        
        if len(pt_cmts)==len(like_count_cmts) and len(ui_comts)==len(like_count_cmts) and len(like_count_cmts)==len(content_cmts):

            for element in pt_cmts:       
                publish_time.append((element.text).split(' ')[0])
                tgt_id.append(None)
                type.append('comments')
                news_id.append(titleid)

            for ui in ui_comts:
                user_id.append(ui.text)
                tgt_user_id.append(ui_posts.text)

            for element in content_cmts:
                content.append(element.text)
                video_url.append(None)
                hashtag.append(None)
                view_count.append(None)

                dislike_count.append(None)
                cmt_count.append(None)
                repost_count.append(None)        

                img_elements = element.find_elements_by_xpath('.//img')
                if img_elements:
                    img_url = img_elements[0].get_attribute('src')
                    pic_url.append(img_url)
                else:
                    pic_url.append(None)

                if element.text.startswith("@"):
                    at_user.append(element.text)
                else:
                    at_user.append(None)
                                                                                                
            for element in like_count_cmts:    
                like_count.append(element.text)
                # dislike_count.append('')
                # cmt_count.append('')
                # repost_count.append('')
# --------------------------------------------------第二部分---------------------
        
        pt_cmts1 = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[1]')
        ui_comts1 = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/div[2]/div/div/div[1]/a')
        content_cmts1 = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/div[2]/div/div/div[1]/span')

        if len(pt_cmts1)==len(ui_comts1) and len(ui_comts1)==len(content_cmts1):
            for element in pt_cmts1:       
                publish_time.append((element.text).split(' ')[0])
                tgt_id.append(None)
                type.append('comments')
                news_id.append(titleid)


            for ui in ui_comts1:
                user_id.append(ui.text)
                tgt_user_id.append(ui_posts.text)

            for element in content_cmts1:
                content.append(element.text)
                video_url.append(None)
                hashtag.append(None)
                view_count.append(None)
                like_count.append(None)
                dislike_count.append(None)
                cmt_count.append(None)
                repost_count.append(None)        

                img_elements = element.find_elements_by_xpath('.//img')
                if img_elements:
                    img_url = img_elements[0].get_attribute('src')
                    pic_url.append(img_url)
                else:
                    pic_url.append(None)

                if element.text.startswith("@"):
                    at_user.append(element.text)
                else:
                    at_user.append(None)
                                                                                            

    # 继续下滑----------------------------------------------------------
        new_height = web.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# ----------------------------------------------------------------
# 目标feature信息
news_id=[]
# context_id=[]
tgt_id = []
publish_time =[]
type=[]
user_id=[]
tgt_user_id=[]
content=[]
pic_url=[]
video_url=[]
at_user=[]
hashtag=[]
view_count=[]
like_count=[]
dislike_count=[]
cmt_count=[]
repost_count=[]
web=Chrome()
web.maximize_window()
web.get('https://weibo.com/')

time.sleep(20)

print('login')

df = pd.read_csv('news.csv')

# 24362
df = df.iloc[23500:24000].reset_index(drop=True)


title = df['content']

title_id =df['news_id']
i=0


# 搜索信息
for keyword in title:
    titleid = title_id[i]
    i=i+1
    print(titleid)
    # 提词搜索引擎模式

    seg_list = jieba.cut(keyword,use_paddle=True)
    result = ", ".join(seg_list)
    keywords = jieba.analyse.extract_tags(result, topK=5)
    if len(keywords) < 5:
        keywords = keyword

    try:
        url = f"https://s.weibo.com/weibo?q={keywords}&page=1"    

        web.get(url)

    except:
        continue

    # 翻页
    page=0



    while True:
        # 遍历对应话题下的微博
        box = web.find_elements_by_xpath('//*[@id="pl_feedlist_index"]/div[2]/div/div/div[1]/div[2]/div[2]/a[1]')

        for link_element in box:
            # 打开评论详情的新窗口
            try:
                link = link_element.get_attribute('href')
            
                web.execute_script(f"window.open('{link}', '_blank')")
                web.switch_to.window(web.window_handles[1])

            except:
                break


            # 获取帖子和评论信息
            try:
                scrape_page()
            except:
                # 返回原窗口
                web.close()
                web.switch_to.window(web.window_handles[0])
                break

            # 返回原窗口
            web.close()
            web.switch_to.window(web.window_handles[0])

        # 翻页

        try:
            
            next_button = web.find_element_by_xpath("//a[contains(text(), '下一页')]")
            next_button.click()
            time.sleep(randint(0,1))
            page = page+1
            if page==5:
                break

        except:
            break
            


web.close()



# 储存
min_length = min(len(news_id), len(publish_time), len(tgt_id), len(type), len(user_id), len(tgt_user_id), len(content), len(pic_url), len(video_url), len(at_user), len(hashtag), len(view_count), len(like_count), len(dislike_count), len(cmt_count), len(repost_count))
news_id = news_id[:min_length]
publish_time = publish_time[:min_length]
tgt_id = tgt_id[:min_length]
type = type[:min_length]
user_id = user_id[:min_length]
tgt_user_id = tgt_user_id[:min_length]
content = content[:min_length]
pic_url = pic_url[:min_length]
video_url = video_url[:min_length]
at_user = at_user[:min_length]
hashtag = hashtag[:min_length]
view_count = view_count[:min_length]
like_count = like_count[:min_length]
dislike_count = dislike_count[:min_length]
cmt_count = cmt_count[:min_length]
repost_count = repost_count[:min_length]

lengths = [len(news_id), len(publish_time), len(tgt_id), len(type), len(user_id), len(tgt_user_id), len(content), len(pic_url), len(video_url), len(at_user), len(hashtag), len(view_count), len(like_count), len(dislike_count), len(cmt_count), len(repost_count)]
if len(set(lengths)) > 1:
    print("序列长度不匹配")
    for i, length in enumerate(lengths):
        print(f"序列 {i} 长度: {length}")

df=pd.DataFrame()
df['news_id']=news_id
# df['context_id']=[]
df['publish_time'] =publish_time
df['tgt_id'] = tgt_id
df['check_time']=datetime.date.today()
df['type']=type
df['user_id']=user_id
df['tgt_user_id']=tgt_user_id
df['content']=content
df['pic_url']=pic_url
df['video_url']=video_url
df['at_user']=at_user
df['hashtag']=hashtag
df['view_count']=view_count
df['like_count']=like_count
df['dislike_count']=dislike_count
df['cmt_count']=cmt_count
df['repost_count']=repost_count



# df.to_csv('social_context3-300.csv',index=False,encoding="utf_8_sig")
try:
    df.to_csv('context-weibo23500.csv', index=False, encoding="utf_8_sig")
except ValueError as e:
    if 'Length of values' in str(e):
        min_length = min(df.shape[0], len(news_id), len(publish_time), len(tgt_id), len(type), len(user_id), len(tgt_user_id), len(content), len(pic_url), len(video_url), len(at_user), len(hashtag), len(view_count), len(like_count), len(dislike_count), len(cmt_count), len(repost_count))
        df = df.iloc[:min_length]
        df.to_csv('context—weibo.csv', index=False, encoding="utf_8_sig")
    else:
        raise e

print('end')

