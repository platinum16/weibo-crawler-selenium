from selenium.webdriver import Chrome
import time
import datetime
import pandas as pd
from random import randint 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# 无头模式
chrome_options = Options()
chrome_options.add_argument("--headless")
web = webdriver.Chrome(options=chrome_options)

# web=Chrome()
# web.maximize_window()
web.get('https://weibo.com/')
time.sleep(10)
# print('login')

# 目标feature信息
# user_id_list=[]
# check_time_list=[]
create_time_list = []
name_list=[]
description_list=[]
gender_list=[]
following_list=[]
follower_list=[]
post_count_list=[]
reply_count_list=[]
friend_count_list=[]
follower_count_list=[]
following_count_list=[]
have_verification_list=[]
ip_list = []

df = pd.read_csv('context_weibo1.csv', low_memory=False)

# user_name = df['user_id'].drop_duplicates().iloc[:50000]
user_name = df['user_id'].drop_duplicates()
print(len(user_name))
# 20409

j=0
# 搜索信息
for keyword in user_name:
    # time.sleep(randint(0,1))
    try:
        url = f"https://s.weibo.com/user?q={keyword}&Refer=weibo_user"    
        web.get(url)
    except:
        continue

    # 计数器
    print(j)
    j+=1

    # 进入账户主页
    try:
        # 进入账户主页
        button = web.find_element_by_xpath('//*[@id="pl_user_feedList"]/div[1]/div[2]/div/a')
        button.click()
        web.switch_to.window(web.window_handles[1])
    except:
        continue


    time.sleep(randint(1,2))



    found=False
    count = 0
    while not found and count<3:
    # while not found:
        try:
            # 点开详细信息
            detail = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div/div/div[2]')
            detail.click()
            found = True
        except NoSuchElementException:
            web.refresh()
            time.sleep(randint(1, 2))
            count += 1
    if not found:
        # 返回原窗口
        web.close()
        web.switch_to.window(web.window_handles[0])
        continue
    


    try:
        id = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div')
        name_list.append(id.text)
        print(id.text)
    except NoSuchElementException:
        name_list.append('')

    try:
        createtime = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[3]/div[1]/div/div[2]')
        create_time_list.append(createtime.text[:-5])
    except NoSuchElementException:
        create_time_list.append('')


    try:
        description = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[2]')
        description_list.append(description.text)
    except NoSuchElementException:
        description_list.append('')



    male_elements = web.find_elements_by_xpath('//*[@class="woo-icon-main woo-icon--male"]')
    female_elements = web.find_elements_by_xpath('//*[@class="woo-icon-main woo-icon--female"]')
    if len(male_elements) > 0:
        gender_list.append('male')
    elif len(female_elements) > 0:
        gender_list.append('female')
    else:
        gender_list.append('')




    try:
        postcount = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[2]/div[1]/div')
        post_count_list.append(postcount.text[5:-1])
    except NoSuchElementException:
        post_count_list.append('')



    # try:
    #     reply = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[1]/div[1]/div/div/div[2]/span')
    #     reply_count_list.append(reply.text[-4:])
    # except NoSuchElementException:
    #     reply_count_list.append('')



    try:
        follower = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/a[1]/span/span')
        follower_count_list.append(follower.text)
    except NoSuchElementException:
        follower_count_list.append('')


    try:
        following = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/a[2]/span/span')
        following_count_list.append(following.text)
    except NoSuchElementException:
        following_count_list.append('')


    try:
        verify = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/div[1]/span')
        have_verification_list.append('verified')
    except NoSuchElementException:
        have_verification_list.append('unverified')



    elements = web.find_elements_by_css_selector('.woo-box-item-flex.ProfileHeader_con3_Bg19p')
    has_ip=False
    for element in elements:
        try:
            if 'IP属地：' in element.text or '北京' in element.text or '天津' in element.text or '河北' in element.text or '山西' in element.text or '内蒙古' in element.text or '辽宁' in element.text or '吉林' in element.text or '黑龙江' in element.text or '上海' in element.text or '江苏' in element.text or '浙江' in element.text or '安徽' in element.text or '福建' in element.text or '江西' in element.text or '山东' in element.text or '河南' in element.text or '湖北' in element.text or '湖南' in element.text or '广东' in element.text or '广西' in element.text or '海南' in element.text or '重庆' in element.text or '四川' in element.text or '贵州' in element.text or '云南' in element.text or '西藏' in element.text or '陕西' in element.text or '甘肃' in element.text or '青海' in element.text or '宁夏' in element.text or '台湾' in element.text or '澳门' in element.text or '香港' in element.text or '新疆' in element.text:
                if not has_ip:
                    print(element.text)
                    ip_list.append(element.text)
                    has_ip=True
        except:
            pass
    if not has_ip:
        ip_list.append('')



    # following_link = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/a[2]')
    # following_link.click()
    # following_name = []

    # # 下滑到底部
    # last_height = web.execute_script("return document.body.scrollHeight")
    # while True:
    #     web.execute_script("window.scrollBy(0, 950);")

    #     time.sleep(randint(1,2))


    #     # 获取用户名信息
    #     name = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/a/div/div[2]/div[1]/span')
   
    #     for element in name:
    #         try:
    #             following_name.append(element.text)

    #         except StaleElementReferenceException:
    #             continue    

    # # 继续下滑----------------------------------------------------------
    #     new_height = web.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         following_name = list(set(following_name))
    #         following_list.append(','.join(following_name))
    #         break
    #     last_height = new_height

    # web.back()

    # time.sleep(2)


    # follower_link = web.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/a[1]')
    # follower_link.click()
    # follower_name = []

    # # 下滑到底部
    # last_height = web.execute_script("return document.body.scrollHeight")
    # while True:
    #     web.execute_script("window.scrollBy(0, 950);")

    #     time.sleep(randint(1,2))

    #     # 获取用户名信息
    #     name = web.find_elements_by_xpath('//*[@id="scroller"]/div[1]/div/div/div/div/a/div/div[2]/div[1]/span')
    #     for element in name:
    #         try:
    #             follower_name.append(element.text)
    #         except StaleElementReferenceException:
    #     # 如果出现异常，跳过
    #             continue    
    # # 继续下滑----------------------------------------------------------
    #     new_height = web.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         follower_name = list(set(follower_name))
    #         follower_list.append( ','.join(follower_name))
    #         break
    #     last_height = new_height







    # 返回原窗口
    web.close()
    web.switch_to.window(web.window_handles[0])


# 保存信息
df=pd.DataFrame()
# user_id=[]
df['create_time'] = create_time_list
df['check_time']=datetime.date.today()
df['name']=name_list
df['description']=description_list
df['gender']=gender_list
# df['following']=following_list
# df['follower']=follower_list
df['post_count']=post_count_list
# df['reply_count']=reply_count_list
# friend_count=[]
df['follower_count']=follower_count_list
df['following_count']=following_count_list
df['have_verification']=have_verification_list
df['ip']=ip_list

  
df.to_csv('useraddition-1.csv', index=False, encoding="utf_8_sig")

print('end')
