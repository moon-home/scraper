*Please don't judge the engineering practice you see here ...*

*Use this to make money and have fun!*

# Manual

- This scraper is specifically designed to scrape posts on [skool](https://www.skool.com/). You will need to create an account there and update the code with your credentials
- This code doesn't include the preparation of those URLs. You can use [Bardeen.ai](https://www.bardeen.ai/) to do that for free without coding.
- The sample URLs in `test_urls.csv` are posts in a [public community](https://www.skool.com/community) of skool. You may need to join that group first. It's free.

# High Level Steps

**(URLs →) Auth → Check URL → Expand → Read, Parse, Store**

1. Load a list of urls from CSV (I used the free feature of Bardeen.ai to perpare this)
2. Authentificate the access to the page you gonna scrape using Selenium
3. Check if the url still exists, they may get deleted by the time of scraping
4. Expand all the nested data on the page
5. Read and parse the data into a structure easy to retrieve and digest


# Technical Lessons

> *Warning, this is boring ...*

> - If you ask how engineers learn coding, this is how. ¯\\\_(ツ)_/¯
> - Trial and error, until you are frustrated enough to ask for help ಠ_ಠ
> - (even though humans tend to be very annoying because they never have a stable API with documentation! 😂)

1. Selenium 
    - It is the solution to solve the authentification issue. Initially, I tried using Python request directly and include the header and cookies, but that didn't work because of this AWSALBCORS thing. 
    - BTW, I have a certification of AWS Solution Architect Associate, but, no, that didn't help. No certification can increase my patience.
2. Page Status
    - I encoutered this page displaying 404, so I was looking for 404 in the request status to handle it, but couldn't capture it, until I realized that that's just the UI, the actual code still returend 200. 
    - I found it funny because it's like the page lied to you.
3. XPath
    - It is the easiest way to select an element
    - Here is how to get it in Chrome
4. chromedriver 
    - It is the tool to interact with the elements on the page
    - but still need request to check status code
5. Nested Content
    - there may be nested content on a page, we need to check and expand all of them if there are
    - after the code clicks open a page, it may take a while to load, so set some sleep time as safety after `click()` so won’t throw error at you
6. Compoud Class
    - XPath is not convienient since you can only target a specific element on the page. If you want to find all elements that satisify certain criteria, you may try `find_elements_by_class_name()`
    - Then the problem is that a class name may have multiple elements in it, which is called compound class name, then you need to use a css selector
7. CSV reader is an iterator
    - so you just use next() to skip the header
8. CSV multi-line cell
    - to my surprise, it’s actually pretty easy to write multiple lines in single cell in csv. the new line character `\n` is interpreted as expected.
8. Edge Case
    - just like in LeetCode, some post only have title, no content, some watch doesn't have number in it, this messes up data parsing. The page doesn't have placeholder for values expected but don't actually exist.
    - you need large enough data to encounter those edge cases
9. Test For POC 
    - make sure start with small tasks and have tests in place, I scraped these 10k entires twice because I didn't realize those "nested data" issue the first time until I started eyeballing and reading the output data
10. Money!
    - pretty happy overall. This would have cost me $3,000 otherwise using tools like Bardeen. OK, this isn't technical, but it's the WHY! leadership is about the WHY! life is about the WHY! or is it...
    - maybe we can just have fun..
