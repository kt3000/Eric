# coding:utf8

from bs4 import BeautifulSoup
import requests
import os
import re
import tools.utils as utils
import tools.io as io


class WebParser:

    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}

    @staticmethod
    def html_filter(soup):
        # Remove irrelevant tags to increase speed
        [s.extract() for s in soup(['script', 'style', 'img', 'sup', 'b'])]
        return soup

    def get_html_zhidao(self, url):
        # Get HTML from baidu zhidao
        soup_zhidao = BeautifulSoup(requests.get(url=url, headers=self.headers).content, "lxml")
        return WebParser.html_filter(soup_zhidao)

    def get_html_baike(self, url):
        # Get HTML from baidu baike
        soup_baike = BeautifulSoup(requests.get(url=url, headers=self.headers).content, "lxml")
        return WebParser.html_filter(soup_baike)

    def get_html_bingkg(self, url):
        # Get HTML from bing knowledge graph
        soup_bingwd = BeautifulSoup(requests.get(url=url, headers=self.headers).content, "lxml")
        return WebParser.html_filter(soup_bingwd)

    def get_html_baidu(self, url):
        # Get HTML from baidu search
        soup_baidu = BeautifulSoup(requests.get(url=url, headers=self.headers).content.decode('utf-8'), "lxml")
        return WebParser.html_filter(soup_baidu)

    def get_html_bing(self, url):
        # Get HTML from bing search
        soup_bing = BeautifulSoup(requests.get(url=url, headers=self.headers).content.decode('utf-8'), "lxml")
        return WebParser.html_filter(soup_bing)

    def get_baike_info(self,basicInfo_block):
        info = {}
        for bI_LR in basicInfo_block.contents[1:3]:
            for bI in bI_LR:
                if bI.name == None:
                    continue
                if bI.name == 'dt':
                    tempName = ''
                    for bi in bI.contents:
                        tempName += bi.string.strip().replace(u" ", u"")
                elif bI.name == 'dd':
                    info[tempName] = bI.contents
        return info


    def baike_query(self, entity, attr):
        soup = self.get_html_baidu("http://baike.baidu.com/item/" + entity)
        basic_info_block = soup.find(class_='basic-info cmn-clearfix')
        if basic_info_block == None:
            return attr + "::Can not be found"
        else:
            info = self.get_baike_info(basic_info_block)
            if info.has_key(attr.decode('utf8')):
                return info[attr.decode('utf8')]
            else:
                # 同义词判断
                attr_list = io.load_baike_attr_name(
                    os.path.dirname(os.path.split(os.path.realpath(__file__))[0]) + '/resources/Attribute_name.txt')
                attr = io.load_synonyms_word_in_attr(attr, os.path.dirname(
                    os.path.split(os.path.realpath(__file__))[0]) + '/resources/SynonDic.txt', attr_list)
                if info.has_key(attr.decode('utf8')):
                    return info[attr.decode('utf8')]
                else:
                    return attr + "::Can not be found"

    def ptr_answer(self, ans, is_html):
        result = ''
        for answer in ans:
            if is_html:
                print answer
            else:
                if answer == u'\n':
                    continue
                p = re.compile('<[^>]+>')
                result += p.sub("", answer.string).encode('utf8')
        return result

    def kw_query(self, query):
        answer = []
        text = ''
        flag = 0
        keywords = utils.get_noun(query)

        # 抓取百度前10条的摘要
        soup_baidu = self.get_html_baidu('https://www.baidu.com/s?wd=' + query)
        for i in range(1, 10):
            if soup_baidu == None:
                break
            results = soup_baidu.find(id=i)
            if results == None:
                break

            if results.attrs.has_key('mu') and i == 1:
                r = results.find(class_='op_exactqa_s_answer')
                if r == None:
                    pass
                else:
                    # 百度知识图谱找到答案
                    answer.append(r.get_text().strip())
                    flag = 1
                    break

            # 古诗词判断
            if results.attrs.has_key('mu') and i == 1:
                r = results.find(class_="op_exactqa_detail_s_answer")
                if r == None:
                    pass
                else:
                    # 百度诗词找到答案
                    answer.append(r.get_text().strip())
                    flag = 1
                    break

            # 万年历 & 日期
            if results.attrs.has_key('mu') and i == 1 and results.attrs['mu'].__contains__(
                    'http://open.baidu.com/calendar'):
                r = results.find(class_="op-calendar-content")
                if r == None:
                    pass
                else:
                    # 百度万年历找到答案
                    answer.append(r.get_text().strip().replace("\n", "").replace(" ", ""))
                    flag = 1
                    break

            if results.attrs.has_key('tpl') and i == 1 and results.attrs['tpl'].__contains__('calendar_new'):
                r = results.attrs['fk'].replace("6018_", "")
                print r

                if r == None:
                    pass
                else:
                    # 百度万年历新版找到答案
                    answer.append(r)
                    flag = 1
                    break

            # 计算器
            if results.attrs.has_key('mu') and i == 1 and results.attrs['mu'].__contains__(
                    'http://open.baidu.com/static/calculator/calculator.html'):
                # r = results.find('div').find_all('td')[1].find_all('div')[1]
                r = results.find(class_="op_new_val_screen_result")
                if r == None:
                    pass
                else:
                    # 计算器找到答案
                    answer.append(r.get_text().strip())
                    flag = 1
                    break

            # 百度知道答案
            if results.attrs.has_key('mu') and i == 1:
                r = results.find(class_='op_best_answer_question_link')
                if r == None:
                    pass
                else:
                    # 百度知道图谱找到答案
                    url = r['href']
                    zhidao_soup = self.get_html_zhidao(url)
                    r = zhidao_soup.find(class_='bd answer').find('pre')
                    if r == None:
                        r = zhidao_soup.find(class_='bd answer').find(class_='line content')

                    answer.append(r.get_text())
                    flag = 1
                    break

            if results.find("h3") != None:
                # 百度知道
                if results.find("h3").find("a").get_text().__contains__(u"百度知道") and (i == 1 or i == 2):
                    url = results.find("h3").find("a")['href']
                    if url == None:
                        continue
                    else:
                        # 百度知道图谱找到答案
                        zhidao_soup = self.get_html_zhidao(url)

                        r = zhidao_soup.find(class_='bd answer')
                        if r == None:
                            continue
                        else:
                            r = r.find('pre')
                            if r == None:
                                r = zhidao_soup.find(class_='bd answer').find(class_='line content')
                        answer.append(r.get_text().strip())
                        flag = 1
                        break

                # 百度百科
                if results.find("h3").find("a").get_text().__contains__(u"百度百科") and (i == 1 or i == 2):
                    url = results.find("h3").find("a")['href']
                    if url == None:
                        continue
                    else:
                        # 百度百科找到答案
                        baike_soup = self.get_html_baike(url)

                        r = baike_soup.find(class_='lemma-summary')
                        if r == None:
                            continue
                        else:
                            r = r.get_text().replace("\n", "").strip()
                        answer.append(r)
                        flag = 1
                        break
            text += results.get_text()

        if flag == 1:
            return answer

        # 获取bing的摘要
        soup_bing = self.get_html_bing('https://www.bing.com/search?q=' + query)
        # 判断是否在Bing的知识图谱中
        bingbaike = soup_bing.find(class_="bm_box")

        if bingbaike != None:
            if bingbaike.find_all(class_="b_vList")[1] != None:
                if bingbaike.find_all(class_="b_vList")[1].find("li") != None:
                    # Bing知识图谱找到答案
                    flag = 1
                    answer.append(bingbaike.get_text())
                    return answer
        else:
            results = soup_bing.find(id="b_results")
            bing_list = results.find_all('li')
            for bl in bing_list:
                temp = bl.get_text()
                if temp.__contains__(u" - 必应网典"):
                    # 查找Bing网典
                    url = bl.find("h2").find("a")['href']
                    if url == None:
                        continue
                    else:
                        # Bing网典找到答案
                        bingwd_soup = self.get_html_bingwd(url)

                        r = bingwd_soup.find(class_='bk_card_desc').find("p")
                        if r == None:
                            continue
                        else:
                            r = r.get_text().replace("\n", "").strip()
                        answer.append(r)
                        flag = 1
                        break

            if flag == 1:
                return answer

            text += results.get_text()

        # print text


        # 如果再两家搜索引擎的知识图谱中都没找到答案，那么就分析摘要
        if flag == 0:
            # 分句
            cutlist = [u"。", u"?", u".", u"_", u"-", u":", u"！", u"？"]
            temp = ''
            sentences = []
            for i in range(0, len(text)):
                if text[i] in cutlist:
                    if temp == '':
                        continue
                    else:
                        # print temp
                        sentences.append(temp)
                    temp = ''
                else:
                    temp += text[i]

            # 找到含有关键词的句子,去除无关的句子
            key_sentences = {}
            for s in sentences:
                for k in keywords:
                    if k in s:
                        key_sentences[s] = 1

            # 根据问题制定规则

            # 识别人名
            target_list = {}
            for ks in key_sentences:
                # print ks
                words = utils.pos_tag(ks)
                for w in words:
                    if w.flag == ("nr"):
                        if target_list.has_key(w.word):
                            target_list[w.word] += 1
                        else:
                            target_list[w.word] = 1

            # 找出最大词频
            sorted_lists = sorted(target_list.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
            # print len(target_list)
            # 去除问句中的关键词
            sorted_lists2 = []
            # 候选队列
            for i, st in enumerate(sorted_lists):
                # print st[0]
                if st[0] in keywords:
                    continue
                else:
                    sorted_lists2.append(st)

            # print "返回前n个词频"
            answer = []
            for i, st in enumerate(sorted_lists2):
                if i < 3:
                    answer.append(st[0])

        return answer

    def get_pairs(self, aiml_resp):
        res = aiml_resp.split(':')
        entity = str(res[1]).replace(" ", "")
        attr = str(res[2]).replace(" ", "")
        return entity, attr

    def web_process(self, aiml_resp, msg, mybot):
        if aiml_resp.__contains__("searchbaike"):
            entity, attr = self.get_pairs(aiml_resp)
            ans = self.baike_query(entity, attr)
            if type(ans) == list and len(ans) > 0:
                return self.ptr_answer(ans, False)
            elif ans.decode('utf-8').__contains__(u'::Can not be found'):
                ans = self.kw_query(msg)

        # 匹配不到模版，通用查询
        elif aiml_resp.__contains__("NoMatchingTemplate"):
            ans = self.kw_query(msg)

        if len(ans) == 0:
            ans = mybot.respond('找不到答案')

        if type(ans) == list:
            return "".join(ans)
        else:
            return ans