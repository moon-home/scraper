import time, csv, random, requests, re, os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

DRIVER_PATH = '/Users/moonma/Downloads/chromedriver-mac-x64/chromedriver'
MIN_PAUSE_TIME = 80
MAX_PAUSE_TIME = 250
URL_FNAME = 'test_urls.csv'
POST_FNAME = URL_FNAME[:-4] + "_output.csv"

service = Service(executable_path=DRIVER_PATH)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.skool.com/community/about')

loginXPath = '//*[@id="__next"]/div/div/div[1]/div/div/div[3]/div/button[2]/span[1]/p'
login = driver.find_element(By.XPATH, loginXPath)
print(login.text)

driver.find_element(By.XPATH, loginXPath).click()
formXPath = '//*[@id="__next"]/div[2]/div[2]/div[2]/div/form/div'
form = driver.find_element(By.XPATH, formXPath)
print(form.text)

emailXPath = '//*[@id="email"]/input'
email = driver.find_element(By.XPATH, emailXPath).send_keys("put your email here")

passwordXPath = '//*[@id="password"]/input'
password = driver.find_element(By.XPATH, passwordXPath).send_keys("put your password here")

submitXPath = '//*[@id="__next"]/div[2]/div[2]/div[2]/div/form/button[2]/span'
submit = driver.find_element(By.XPATH, submitXPath).click()

time.sleep(5)

with open(URL_FNAME, 'r', newline='') as infile, open(POST_FNAME, 'a', newline='') as outfile:
    csvreader = csv.reader(infile, delimiter=',') 
    next(csvreader, None)
    csvwriter = csv.writer(outfile, delimiter=',')
    csvwriter.writerow(["URL", "Title", "AuthorLevel", "AuthorName", "PublishTime", "Category", "WacthCount", \
                        "ContentLinesCount", "Content", "CommentsCount", "AllComments"])
    random.seed(a=33, version=2)
    row_ct = 0
    for row in csvreader:
        title, url = row[0], row[1]
        print(f"Row #{row_ct} started: {title}, url: {url}")
        driver.get(url)

        # make sure post isn't deleted by the time of scraping
        try:
            titleXPath = '//*[@id="__next"]/div/div/div[3]/div/div[1]/div/div/div[1]/div/div[1]/div/div[2]/div/div/span'
            driver.find_element(By.XPATH, titleXPath).click()
        except Exception:
            url_status = requests.get(url).status_code
            print("   ", url_status, url, "→ NOT WORKING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            continue

        time_pause = random.randint(MIN_PAUSE_TIME, MAX_PAUSE_TIME)/100
        time.sleep(time_pause)
        row_ct += 1

        # expand all "View x more reply", there may be nested cases
        while True:
            morereplies = driver.find_elements(By.CSS_SELECTOR, ".styled__ExpandRepliesLabel-sc-1lql1qn-8.cEAa-dK")
            if morereplies == []: break
            print(f"    'more replies' found: {len(morereplies)}")
            for mr in morereplies: 
                driver.execute_script("arguments[0].click();", mr)
                time.sleep(1.5)

        # expand all "See more", there shouldn't be any nested case
        seemores =  driver.find_elements(By.CLASS_NAME, "jss62")
        print(f"    'See more' found: {len(seemores)}")
        for sm in seemores: 
            try:
                sm.click()
                time.sleep(1.5)
            except Exception:
                os.system('say "See more click failed"')
                print('-------------------------------------See more click failed:\n', Exception)
        
        # parsing post
        postXPath = '//*[@id="__next"]/div/div/div[3]/div/div[1]/div/div/div[1]/div/div[1]/div'
        post_elements = driver.find_element(By.XPATH, postXPath).text.splitlines()
        author_level = post_elements[0]
        author_name = post_elements[1]
        splitIndex = post_elements[2].index("in")
        publish_time = ''.join(post_elements[2][:splitIndex])
        category = ''.join(post_elements[2][splitIndex+3:])
        watch_ct = re.findall("\d+", post_elements[3])
        if watch_ct: watch_ct = int(watch_ct[0]) # edge case where there is no number
        content_lines_ct = len(post_elements) - 5 # each line in the content of the post is a single element in post_elements
        print(f"    content_lines_ct: {content_lines_ct}")
        post_content = ''
        for i in range(5, len(post_elements)): # edge case where the post doesn't have text content
            if i != len(post_elements) - 1:
                post_content += post_elements[i] + "\n\n"
            else:
                post_content += post_elements[i]

        # parsing comments
        commentsXPath = '//*[@id="__next"]/div/div/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div[2]/div[1]'
        comments_elements = driver.find_element(By.XPATH, commentsXPath).text.splitlines()
        comments_ct, all_comments, comment = 0, '', []
        for i, el in enumerate(comments_elements): 
            comment.append(el)
            if el == "Reply":
                if i != len(comments_elements) - 1:
                    all_comments += ' '.join(comment) + "\n\n"
                else:
                    all_comments += ' '.join(comment)
                comment = []
                comments_ct += 1

        csvwriter.writerow([url, title, author_level, author_name, publish_time, category, watch_ct, content_lines_ct, post_content, comments_ct, all_comments])
        print('    completed')
driver.quit()