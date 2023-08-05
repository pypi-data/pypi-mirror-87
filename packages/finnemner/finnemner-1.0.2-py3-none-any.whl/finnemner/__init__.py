# -*- coding: utf-8 -*-
"""
@author: WuYR
@Time    : 2020/11/19 19:47
"""

# class Tokenizer(object):

import requests
import traceback
import time
import json,re
from itertools import combinations
from multiprocessing.dummy import Pool

cities = ['克孜勒苏柯尔克孜', '巴音郭楞蒙古', '博尔塔拉蒙古', '鄂托克前旗', '伊金霍洛旗', '伊犁哈萨克', '康巴什区', '达拉特旗', '准格尔旗', '鄂托克旗', '伊金霍洛', '呼和浩特', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '锡林郭勒', '齐齐哈尔', '大兴安岭', '西双版纳', '乌鲁木齐', '克拉玛依', '连云港', '石家庄', '秦皇岛', '张家口', '东胜区', '杭锦旗', '乌审旗', '康巴什', '达拉特', '准格尔', '鄂托克', '阿拉善', '内蒙古', '葫芦岛', '黑龙江', '哈尔滨', '双鸭山', '佳木斯', '七台河', '牡丹江', '马鞍山', '南昌县', '景德镇', '平顶山', '三门峡', '驻马店', '张家界', '防城港', '攀枝花', '六盘水', '黔西南', '黔东南', '日喀则', '嘉峪关', '石嘴山', '吐鲁番', '阿克苏', '阿勒泰', '中国', '北京', '上海', '天津', '重庆', '香港', '澳门', '江苏', '南京', '无锡', '徐州', '常州', '苏州', '南通', '淮安', '盐城', '扬州', '镇江', '河北', '浙江', '长兴', '杭州', '宁波', '温州', '嘉兴', '广东', '龙岗', '广州', '深圳', '珠海', '汕头', '韶关', '佛山', '江门', '湛江', '湖州', '绍兴', '唐山', '邯郸', '邢台', '山东', '济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '威海', '保定', '承德', '沧州', '廊坊', '衡水', '山西', '太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁', '东胜', '杭锦', '乌审', '包头', '乌海', '赤峰', '通辽', '兴安', '辽宁', '沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '吉林', '长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延边', '鸡西', '鹤岗', '大庆', '伊春', '黑河', '绥化', '常熟', '泰州', '宿迁', '金华', '衢州', '舟山', '台州', '丽水', '安徽', '合肥', '芜湖', '蚌埠', '淮南', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '巢湖', '六安', '亳州', '池州', '宣城', '福建', '福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德', '江西', '南昌', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶', '济宁', '泰安', '日照', '莱芜', '临沂', '德州', '聊城', '滨州', '菏泽', '河南', '郑州', '开封', '洛阳', '焦作', '鹤壁', '新乡', '安阳', '濮阳', '许昌', '漯河', '南阳', '商丘', '信阳', '周口', '湖北', '武汉', '黄石', '襄樊', '十堰', '荆州', '宜昌', '荆门', '鄂州', '孝感', '黄冈', '咸宁', '随州', '恩施', '湖南', '长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '益阳', '郴州', '永州', '怀化', '娄底', '湘西', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮', '广西', '南宁', '柳州', '桂林', '梧州', '北海', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左', '海南', '海口', '三亚', '四川', '成都', '自贡', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '宜宾', '广安', '达州', '眉山', '雅安', '巴中', '资阳', '阿坝', '甘孜', '凉山', '贵州', '顺竹', '桐梓', '务川', '贵阳', '遵义', '安顺', '铜仁', '毕节', '黔南', '云南', '昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '文山', '红河', '楚雄', '大理', '德宏', '怒江', '迪庆', '西藏', '拉萨', '昌都', '山南', '那曲', '阿里', '林芝', '陕西', '西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛', '甘肃', '静宁', '兰州', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '定西', '陇南', '临夏', '甘南', '青海', '西宁', '海东', '海北', '黄南', '海南', '果洛', '玉树', '海西', '宁夏', '银川', '吴忠', '固原', '中卫', '新疆', '哈密', '和田', '喀什', '昌吉', '塔城', '台湾', '台北', '高雄', '基隆', '台中', '台南', '新竹', '嘉义']

def __init__(self):

    self = self


def load_config(config_path):
    '''
    :param config_path: 参数配置
    :return: 服务参数字典
    '''
    profile = open(config_path, 'r', encoding='utf-8').readlines()[1]
    pro = profile.replace('\ufeff', '')
    entity_config = json.loads(pro)
    return entity_config


def load_text(file_path):
    '''
    :param file_path: 读取的文件路径，utf8格式，逐行读取
    :return: 去重空格的内容降序的lst
    '''
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    file_list = []
    for line in lines:
        file_list.append(line.strip().replace('\ufeff', ''))
    file_list = sorted(file_list, key=lambda x: len(x), reverse=True)
    return file_list

def load_text_NoSort(file_path):
    '''
    :param file_path: 读取的文件路径，utf8格式，逐行读取
    :return: 去重空格且长度不为零的内容lst
    '''
    file_list = [word.strip().replace('\ufeff', '') for word in open(file_path, 'r', encoding='utf-8').readlines()
                 if len(word.strip().replace('\ufeff', '')) > 0]
    return file_list


'''实体识别'''
def getnerweb(sen,ner_url_lst):
    '''
    :param sen: 待识别文本
    :param ner_url_lst: 服务地址端口组，list格式
    :return: 字典json串
    '''
    results = ''
    sessweb = requests.Session()
    try:
        # 连接命名实体的connect,检查服务地址是否能有效，链接
        Live_url = []
        for url in ner_url_lst:
            try:
                html = requests.get(url, timeout=3)
                Live_url.append(url)
            except requests.exceptions.RequestException as e:
                e = e
                # print(e)   #此代码开服务则写入日志，封装则不做处理
        if len(Live_url) > 0:
            req = requests.Request('POST', Live_url[0], data=sen.encode("utf-8"))
            prep = sessweb.prepare_request(req)
            res_temp = sessweb.send(prep, stream=False).text

            ners_lable = ['loc','per','org']
            ners = []
            if res_temp:
                loc = res_temp.split(';\n')[0].split(':')[1]
                loc1 = loc.split(',')
                loc1 = list(set(loc1))
                if len(loc1) > 0:
                    loc1 = [i for i in loc1 if len(i) > 0]
                    ners.append(loc1)

                per = res_temp.split(';\n')[1].split(':')[1]
                per1 = per.split(',')
                per1 = list(set(per1))
                if len(per1) > 0:
                    per1 = [i for i in per1 if len(i) > 0]
                    ners.append(per1)

                org = res_temp.split(';\n')[2].split(':')[1]
                org1 = org.split(',')
                org1 = list(set(org1))
                if len(org1) > 0:
                    org1 = [i for i in org1 if len(i) > 0]
                    ners.append(org1)
            else:
                ners = [[], [], []]
            results_dict = dict(zip(ners_lable, ners))
            results = json.dumps(results_dict, ensure_ascii=False)
        else:
            results = '【错误】实体识别服务异常!'

    except Exception as e:
        results = '【错误】实体识别服务异常!'
    sessweb.close()
    return results


'''机构匹配'''
HEADERS = {'Content-Type': 'application/soap+xml; charset=utf-8'}
pool = Pool(3)


#实体匹配，接口返回值为list，函数返回值list
def get_org_wcf_lst(url, text):
    sesswcf = requests.Session()
    data = """<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing"><s:Header><a:Action s:mustUnderstand="1">http://tempuri.org/IService1/Ind2</a:Action><a:MessageID>urn:uuid:e9f70a27-bfd3-4b52-89d3-80f1f36f9d0d</a:MessageID><a:ReplyTo><a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address></a:ReplyTo><a:To s:mustUnderstand="1">""" + url +  """</a:To></s:Header><s:Body><Ind2 xmlns="http://tempuri.org/"><content>"""+ text + """</content></Ind2></s:Body></s:Envelope>"""
    userInfo = data.encode("utf-8").decode("latin1")
    # 请求方式
    contentwcf = ''
    try:
        req = requests.Request('POST', url=url, headers=HEADERS, data=userInfo)
        prep = sesswcf.prepare_request(req)
        contentwcf = sesswcf.send(prep, stream=False, timeout=3).text
    except Exception as ex:
        contentwcf = ''
    sesswcf.close()
    content = re.findall("(?<=<Ind2Result>)[\s\S]*?(?=</Ind2Result>)", contentwcf)
    return content

#实体匹配，接口返回值为json,服务返回值list
def get_org_wcf_json(url, text):
    data = """<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing"><s:Header><a:Action s:mustUnderstand="1">http://tempuri.org/IService1/Ind2</a:Action><a:MessageID>urn:uuid:e9f70a27-bfd3-4b52-89d3-80f1f36f9d0d</a:MessageID><a:ReplyTo><a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address></a:ReplyTo><a:To s:mustUnderstand="1">""" + url +  """</a:To></s:Header><s:Body><Ind2 xmlns="http://tempuri.org/"><content>"""+ text + """</content></Ind2></s:Body></s:Envelope>"""
    data = data.encode("utf-8").decode("latin1")
    # 请求方式
    contentwcf = ''
    try:
        sesswcf = requests.Session()
        req = requests.Request('POST', url=url, headers=HEADERS, data=data)
        prep = sesswcf.prepare_request(req)
        contentwcf = sesswcf.send(prep, stream=False).text
    except Exception as ex:
        contentwcf = ''

    content = re.findall("(?<=<Ind2Result>)[\s\S]*?(?=</Ind2Result>)", contentwcf)
    res = []
    if len(content) > 0:
        for cell in json.loads(content[0]):
            res.append(cell['key'])

    return res


#加括号自定义词
save_key = ['特殊的普通合伙企业', '特殊普通合伙企业', '普通合伙分支机构', '特殊普通合伙', '普通合伙企业', '有限合伙', '普通合伙', '特殊合伙', '集团', '筹', '株']

#自定义词加括号
def shiti_words(text, shiti, words):
    '''有限合伙等字眼'''
    for word in words:
        word_chi = '（' + word + '）'
        word_eng = '(' + word + ')'
        if shiti.endswith(word) or (word in shiti and not shiti.startswith(word)):
            shiti_1 = shiti.replace(word, word_chi)
            shiti_2 = shiti.replace(word, word_eng)
            if shiti_1 in text:
                shiti = shiti_1
                break
            elif shiti_2 in text:
                shiti = shiti_2
                break
    return shiti

#城市加括号
def shiti_cities(text, shiti, cities):
    '''各种城市字样'''
    for city in cities:
        if city in shiti:
            if not shiti.startswith(city) and not shiti.endswith(city):
                if shiti not in text:
                    shiti_1 = shiti.replace(city, '（' + city + '）')
                    shiti_2 = shiti.replace(city, '(' + city + ')')
                    if shiti_1 in text:
                        shiti = shiti_1
                        break
                    elif shiti_2 in text:
                        shiti = shiti_2
                        break
                else:
                    shiti = shiti
                    break
        else:
            shiti = shiti
    return shiti


#自定义词和城市加括号，查找实体索引
def text_list_shiti_word(text_list, shitis, words, cities):
    '''
    :param text_list:待识别的所有文本，list
    :param shitis:所有实体词
    :param words:自定义加括号的词
    :param cities:城市名称
    :return:元素为索引+实体词的tuple组成的list
    '''
    res = []
    for shiti in shitis:
        for text in text_list:
            shiti = shiti_words(text, shiti, words)  #自定义词加括号，是save_key,后期加入导入自定义词，类似于自定义词典
            shiti = shiti_cities(text, shiti, cities) #城市加括号
            if shiti in text:
                if re.findall('[省市县]$', shiti):
                    continue
                else:
                    res.append((text.index(shiti), shiti))
                break
    return res


#整合实体匹配和括号处理,返回机构
# cities = load_text(r'./regions.txt')
def get_org_pp_thread(contents, cities,nem_url_lst,nerswitch):
    texts = contents
    # 或者采用分割的方式去处理
    org_res = []

    #有效服务
    Live_nemurl = []
    for url in nem_url_lst:
        try:
            html = requests.get(url, timeout=3)
            Live_nemurl.append(url)
        except requests.exceptions.RequestException as e:
            print(e)  # 此代码开服务则写入日志，封装则不做处理

    if len(Live_nemurl) > 0:
        strhh = ""
        li = Live_nemurl[0]
        result = []
        if nerswitch == 'lst':
            result = get_org_wcf_lst(li, texts)
        elif nerswitch == 'jon':
            result = get_org_wcf_json(li, texts)
        if len(result) > 0:
            # 去除包含关系与长度降序排列
            # msg_pp_list = list(set(re.split("\n", strhh)[:-1]))
            msg_pp_list = sorted(result, key=lambda x: len(x), reverse=True)

            text_list = texts.split('。')
            words = save_key
            res_org = text_list_shiti_word(text_list, msg_pp_list, words, cities)

            res_org_final = []
            for res in res_org:
                shiti = res[1]
                if shiti in texts:
                    texts = texts.replace(shiti, '@' * len(shiti))
                    res_org_final.append(res)

            if len(res_org_final) > 0:
                for i in res_org_final:
                    org_res.append(i[1])
    elif len(Live_nemurl) == 0:
        org_res.append('【错误】：实体匹配或实体识别接口参数有误！')
    return org_res

'''
后处理三剑客：地址、机构实体合并；自定义词典删除；自定义模式删除。
'''

#实体合并
def hebing_shiti(res_list, text):

    def combine(temp_list, n):
        '''根据n获得列表中的所有可能组合（n个元素为一组）'''
        temp_list2 = []
        for c in combinations(temp_list, n):
            c = ''.join(c)
            temp_list2.append(c)
        return temp_list2

    '''实体列表：res_list, text：文本'''
    res_list = list(set(res_list))

    res_list_sort = []
    for i in res_list:
        ind = text.index(i)
        tpu = []
        tpu.append(i)
        tpu.append(ind)
        res_list_sort.append(tpu)
    res_list_sort = sorted(res_list_sort, key=lambda cell: cell[1])
    res_list = [cell[0] for cell in res_list_sort]


    end_list = []
    for i in range(1, 4):
        temp_list = combine(res_list, 4 - i)
        temp_list = sorted(temp_list, key=lambda x: len(x), reverse=True)
        end_list.extend(temp_list)
    res_final = []
    for item in end_list:
        if item in text:
            res_final.append(item)
            text = text.replace(item, '*'*len(item))
    return res_final


#词典剔除
del_words = ['公司','上市公司']

def del_word(path):
    '''
    :param path: 自定义删除词典路径
    :return: 长度降序排序后的lst
    '''
    del_words.extend(load_text(path))

    return del_words

#模式剔除
del_rulers_lst = ['adhdufhggsdioeh']
def del_ruler(path):
    del_rulers_lst.extend(load_text_NoSort(path))
    return del_rulers_lst


def EntityCapture(sen,entity_config,nemswitch,*args):
    '''
    :param sen: 识别语句
    :param entity_config: 接口字典
    :param nemswitch: 匹配lst和json选择开关
    :param args:
    :return:
    '''
    try:
        waring = '【错误】：实体匹配或实体识别接口参数有误！'
        entity_res = ''
        if len(args) == 0:
            return waring
        elif len(args) > 0:
            args = list(set(args))
            if len(args) == 1:
                if args[0] == 'nem' and len(entity_config['nem']) > 0:
                    nem_res = get_org_pp_thread(sen,cities,entity_config['nem'],nemswitch)
                    if len(re.findall('【错误】', ''.join(entity_res))) == 0:
                        org_delwords = list(set(nem_res).difference(set(del_words)))
                        results_dict = {}
                        results_dict['org'] = org_delwords
                        results_dict['per'] = []
                        results_dict['loc'] = []
                        entity_res = json.dumps(results_dict, ensure_ascii=False)
                    else:
                        entity_res = waring

                elif args[0] == 'ner' and len(entity_config['ner']) > 0:
                    ner_res = getnerweb(sen,entity_config['ner'])
                    if len(re.findall('【错误】', ner_res)) == 0:
                        ner_dict = json.loads(ner_res)
                        org_lst = ner_dict['org']
                        loc_lst = ner_dict['loc']
                        org_loc = loc_lst + org_lst
                        orgHBloc = hebing_shiti(org_loc,sen)
                        org_delloc = list(set(orgHBloc).difference(set(loc_lst)))  # 去除loc
                        org_delwords = list(set(org_delloc).difference(set(del_words)))
                        ner_dict['org'] = org_delwords
                        entity_res = json.dumps(ner_dict, ensure_ascii=False)
                    else:
                        entity_res = waring
                else:
                    entity_res = waring
            elif len(args) == 2:
                if 'nem' in args and 'ner' in args and len(entity_config['nem']) > 0 and len(entity_config['ner']) > 0:
                    nem_res = get_org_pp_thread(sen, cities,entity_config['nem'],nemswitch)
                    ner_res = getnerweb(sen, entity_config['ner'])

                    if len(re.findall('【错误】',''.join(nem_res) + ner_res)) == 0:
                        ner_dict = json.loads(ner_res)
                        org_lst = ner_dict['org']
                        loc_lst = ner_dict['loc']

                        org_loc = loc_lst + org_lst + nem_res
                        orgHBloc = hebing_shiti(org_loc, sen)
                        org_delloc = list(set(orgHBloc).difference(set(loc_lst)))  #去除loc
                        org_delwords = list(set(org_delloc).difference(set(del_words)))  #去除loc
                        ner_dict['org'] = org_delwords
                        entity_res = json.dumps(ner_dict, ensure_ascii=False)
                    else:
                        entity_res = waring
                else:
                    entity_res = waring
            else:
                entity_res = waring

        #检测是否导入了自定义规则
        if len(del_rulers_lst) > 1 and len(re.findall('【错误】',entity_res)) == 0:
            del_rulers = '|'.join(del_rulers_lst[1:])
            entity_dict = json.loads(entity_res)
            results_dict = {}
            org_t = entity_dict['org']
            per_t = entity_dict['per']
            loc_t = entity_dict['loc']
            if len(org_t) > 0:
                org_t = [i for i in org_t if len(re.findall(del_rulers,i)) == 0]
            if len(per_t) > 0:
                per_t = [i for i in per_t if len(re.findall(del_rulers,i)) == 0]
            if len(loc_t) > 0:
                loc_t = [i for i in loc_t if len(re.findall(del_rulers,i)) == 0]

            results_dict['org'] = org_t
            results_dict['per'] = per_t
            results_dict['loc'] = loc_t
            entity_res = json.dumps(results_dict, ensure_ascii=False)

    except BaseException as e:
        errors = str(traceback.format_exc()).split('\n')
        if len(errors) > 0:
            errors = [i for i in errors if len(i) > 1]
            if len(errors) > 0:
                entity_res = errors[-1]
            else:
                entity_res = e
        else:
            entity_res = e
    return entity_res



# dt = Tokenizer()
# redd = dt.load_text
