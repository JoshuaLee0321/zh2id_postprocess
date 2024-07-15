import re
# from scripts.statics import *
from statics import *

class IndoSyntaxPostCorrection():
    def __init__(self) -> None:
        pass
    def get_position(self, zhstr: str, idstr: str):
        pass
    
    def correction_main(self, zhseg: list, idseg: list) -> str:
        
        # 先修正問題
        # 再修正再問題中的分類
        
        # 修正直述句
        try:
            idseg = [x.replace("Anda", "anda").
                     replace("aku", "saya").
                     replace("Aku", "saya").
                     replace("Apa", "apa")
                     for x in idseg]
            
            idseg = self.fix_impolite_type(idseg)
            idseg = self.fix_polite_type(zhseg, idseg)
            idseg = self.fix_negation_type(zhseg, idseg)
            idseg = self.fix_state_sentence_type(zhseg, idseg)
            idseg = self.fix_conjunection_type(zhseg, idseg)
            idseg = self.fix_predicate_type(zhseg, idseg)
            idseg = self.fix_question_type(zhseg, idseg)
            idseg = self.fix_question_case_by_case(zhseg, idseg)
            idseg = self.fix_time_type(zhseg, idseg)
            # 整理用
            for i in range(len(idseg)):
                if idseg[i] == "&quot;":
                    idseg[i] = '\"'
                if idseg[i] == "&apos;":
                    idseg[i] = "\'"
       
            if idseg[-1] == ",":
                idseg = idseg[:-1]
            if idseg[-1] == "\"":
                idseg = idseg[:-1]
            if idseg[-1] == ";":
                idseg = idseg[:-1]
        except Exception as e:
            print(e)
            return ""
        
        result = " ".join(idseg).strip()
        return result
    
    def fix_special_and_replica_type(self, zhseg: list, idseg: list) -> list:
        ref: str = "".join(zhseg)
        result: str = " ".join(idseg)
        
        if "老闆娘" in ref:
            if "bos bos" in result:
                result = result.replace("bos bos", "bos")
            if "bos" in result and "ibu bos" not in result:
                result = result.replace("bos")
        
        if "apakah bisakah" in result:
            result = result.replace("apakah bisakah", "apakah")
        return result.split(" ")
        
    def fix_impolite_type(self, idseg: list) -> list:
        
        for i in range(len(idseg)):
            if idseg[i] == "aku":
                idseg[i] = "saya"
            if idseg[i] == "kau":
                idseg[i] = "anda"
           # add more implite rules here...    

        return idseg
    
    def fix_polite_type(self, zhseg: list, idseg: list) -> list:
        ref: str = "".join(zhseg)
        result: str = " ".join(idseg)
        
        # 不好意思 ...
        if "不好意思" == ref[:4]:
            if "maaf" in result:
                result = result.replace("maaf", "permisi")
                
            if "permisi" not in result:
                result = "permisi , " + result
        # 對不起
        elif "對不起" == ref[:3]:
            if "maafkan aku" in result or "maafkan saya" in result:
                result = result.replace("maafkan aku", "maaf")
                result = result.replace("maafkan saya", "maaf")

            if "maaf" not in result:
                result = "maaf , " + result
        # 沒關係
        elif "沒關係" == ref[:3]:
            result = result.replace("tidak apa-apa", "gapapa")
            result = result.replace("tak apa-apa", "gapapa")
            result = result.replace("tak apa", "gapapa")
        
        # 謝謝 不用做
        
        return result.split(" ")
        
    def fix_negation_type(self, zhseg: list, idseg: list) -> list:
        ref: str = "".join(zhseg)
        result: str = " ".join(idseg)
        # 別 XXX
        if "別" == ref[0]:
            if "jangan" not in result:
                result = "jangan " + result
        # 不可以 XX
        elif "不可以" in ref:
            if "tidak boleh" not in result:
                result = result.replace("tidak bisa", "tidak boleh")
                result = result.replace("tak bisa", "tidak boleh")
        # 禁止 XX
        elif "禁止" == ref[:2]:
            if "dilarang" not in result:
                result = "dilarang " + result
        # 不
        elif "不" in ref:
            result = result.replace("nggak", 'tidak')
            result = result.replace(" gak ", ' tidak ')
            result = result.replace(" ga ", ' tidak ')
            result = result.replace(" tak ", ' tidak ')
        
        # elif re.search("今天")    
        return result.split(" ")
            
    def fix_state_sentence_type(self, zhseg: list, idseg: list) -> list:
        ref: str = "".join(zhseg)
        result: str = " ".join(idseg)
    
        # 越來越 XX 
        if "越來越" in ref:
            if idseg.count("semakin") == 1 and "lama" not in result:
                result = result.replace("semakin", "semakin lama semakin")
        # 有一點 ... 
        elif "有一點" in ref:
            if "sesuatu" in result:
                result = result.replace("sesuatu", "sedikit")
        # XX 很 XX
        elif re.search(".*很.*", ref) or re.search(".*蠻.*", ref):
            if "這" in ref and "sangat" not in result:
                result = result.replace("ini", "ini sangat", 1)
            elif "那" in ref and "sangat" not in result:
                result = result.replace("itu", "itu sangat", 1)
        # XX 蠻 XX
        elif re.search(".*蠻.*", ref):
            if "sangat" in result:
                result = result.replace("sangat", "terlalu")
            if "這" in ref and "terlalu" not in result:
                result = result.replace("ini", "ini terlalu", 1)
            elif "那" in ref and "terlalu" not in result:
                result = result.replace("itu", "itu terlalu", 1)
        # 最 XXX
        elif re.search("最.*", ref):
            if "paling" not in result and "yang" in result:
                result = result.replace("yang", "yang paling")
        return result.split(" ")
                
    def fix_conjunection_type(self, zhseg: list, idseg: list) -> list:
        ref: str = "".join(zhseg)
        result: str = " ".join(idseg)
        
        # 雖然 A, 但是 B
        if re.search("雖然.*但是", ref):
            if "meskipun" in result:
                result = result.replace("meskipun", "meski")
            if "meski" not in result:
                result = "meski " + result
                
        # 對 A 來說, B ...
        elif re.search("對.*來說", ref):
            # 代表在中間
            if "bagi" in result and "bagi" != result[:4]:
                resList = result.split("bagi")
                result = "bagi " + resList[1].strip() + " , " + resList[0].strip()
            elif "bagi" not in result:
                result = "bagi " + result
                
        # 因為 A，所以 B
        elif re.search("因為.*所以", ref):
            if "karena" not in result:
                result = "karena " + result
                
        # 我以為 A，原來 B
        elif re.search("以為.*[,|，]原來.*", ref):
            if "," in result:
                resList = result.split(",")
                if "kukira" in resList[0]:
                    resList[0] = resList[0].replace("kukira", "saya kira")
                    
                if "kira" not in resList[0] and "mengira" in resList[0]:
                    resList[0] = resList[0].replace("mengira", "kira")
                    
                if "ternyata" not in resList[1]:
                    resList[1] = "ternyata " + resList[1]
                result = resList[0].strip() + " , " + resList[1].strip()
                result = result.replace("  ", " ")
        # 越 A 越 B
        elif re.search("越.*越", ref):
            if "semakin" not in result:
                result = "Semakin " + result
        
        # 自從 ...
        elif "自從" == ref[:2]:
            if "sejak" not in result:
                result = "sejak " + result
        
        # 在 XX 過程中
        elif re.search("在.*過程中", ref):
            if "saat" in result and "selama" not in result:
                result = result.replace("saat", "selama")

            if "selama" not in result:
                result = "selama " + result
        # xx, 儘管 xx
        elif re.search(".*[,|，]儘管.*", ref):
            if " meski " in result:
                resList = result.split("meski")
                result = resList[0].strip() + " meskipun " + resList[1].strip()
        # 以至於
        elif "以至於" in ref:
            if " hingga " in result:
                result = result.replace(" hingga ", " sehingga ")
        
        # 要是 XX(原因)，就 XX(結果)
        elif re.search("要是.*", ref):
            if "jika" in result:
                result = result.replace("jika", "kalo")
                
            if "kalau" not in result or "kalo" not in result:
                result = "kalo " + result
                
                
                
        return result.split(" ")
    
    def fix_predicate_type(self, zhseg: list, idseg: list) -> list:
        ref: str = "".join(zhseg)
        result: str = " ".join(idseg)
        
        if re.search('接近.*的時候', ref):
            if "menjelang" not in result:
                result  = "menjelang " + result
                
        elif "所以" in ref:
            if "jadi" not in result:
                result = "jadi " + result
        # 這 ... 沒有 ..
        elif re.search('這.*沒有.*', ref):
            result = result.replace("tak", "tidak ada")
                
        elif "要一個" in ref:
            if "mau" not in result:
                result = result.replace("satu", "mau tambah satu")
            else:
                result = result.replace("satu", "tambah satu")
        # 請 ..
        elif "請" in ref:
            if "tolong" in result:
                result = result.replace("tolong", "silahkan")
            elif "tolong" not in result and "silahkan" not in result and "silakan" not in result:
                result = "silahkan " + result
        # 麻煩你 ...
        elif "麻煩你" in ref or "麻煩" == ref[:2]:
            if "silahkan" in result:
                result = result.replace("silahkan", "tolong")
            elif "tolong" not in result and "silahkan" not in result and "silakan" not in result:
                result = "tolong " + result
                
        return result.split(" ")  

    def fix_question_type(self, zhseg: list, idseg: list) -> list:
        '''
            # 修正問題 type\n
            1. 5w1h 沒有修正的問題在這邊修正\n
            2. y/n 問題 在這邊修正\n
            3. 特殊問句在這邊修正
        '''
        questionType = None
        for char in zhseg:
            if char in QUESTION_TYPE.keys():
                questionType = QUESTION_TYPE[char]
                break
        # 檢查是否為問句並判斷問句類型
        questionType = None
        questionContent = []
        
        for char in zhseg:
            if char in QUESTION_TYPE:
                questionType = QUESTION_TYPE[char]
                questionContent.append(char)
                
        # # 若沒有問題則跳過
        if questionType == None:
            return idseg
        result: list = idseg.copy()
        for i in range(len(result)):
            if "apa" == result[i] or "apakah" == result[i]:
                result[i] = INDONESIAN_QUESTION_WORDS[questionType] 
        
        result = " ".join(result)
        # print(result)
        # 最後如果沒有 apa ，則根據要問的問題，家在最前面
        if "apa" not in result and "mana" not in result and "apakah" not in result:
            result = INDONESIAN_QUESTION_WORDS[questionType] + " " + result
        
        # 处理包含“你”或“妳”的情况
        if "妳" in zhseg or "你" in zhseg:
            if "kau" not in result and "anda" not in result and "Anda" not in result:
                result = result.replace(INDONESIAN_QUESTION_WORDS[questionType], INDONESIAN_QUESTION_WORDS[questionType] + " anda")


        
        return result.split(' ')

    def fix_question_case_by_case(self, zhseg: list, idseg: list) -> list:
        
        result: str = " ".join(idseg)
        ref: str = "".join(zhseg)
        # 處理 在哪裡的問題
        if "在哪裡" in ref:
            if "Dimana" in result:
                result = result.replace("Dimana", "di mana")
            if "mana" in result and "dimana" not in result and "di mana" not in result:
                result = result.replace("mana", "di mana")
            if "di mana" not in result and "dimana" not in result:
                result = result + " di mana"
                
        # 處理 "為甚麼"
        elif "為甚麼" in ref or "為什麼" in ref:
            if "kenapa" in result:
                result = result.replace("kenapa", "mengapa")
            if "mengapa" not in result:
                if "apa" in result:
                    result = result.replace("apa", "mengapa")
                elif "apa" not in result:
                    result = "mengapa " + result    
        # 處理問售價
        elif "多少錢" in ref or "賣多少" in ref:
            if "berapa" in result:
                if "harga" not in result:
                    result = result.replace("berapa", "harga berapa")
        # 處理問身高
        elif "多高" in ref or "身高多高" in ref:
            if "berapa" in result:
                if "tinggi" not in result:
                    result = result.replace("berapa", "berapa tinggi")
        # 處理問長度、距離
        elif "多遠" in ref or "多長" in ref:
            if "berapa" in result:
                if "panjang" not in result:
                    result = result.replace("berapa", "berapa panjang")
                    
        # 處理問大小
        elif "什麼時候" in ref or "幾點" in ref:
            if "berapa" not in result and "kapan" not in result:
                result = "berapa " + result
            if "berapa" in result:
                if "panjang" not in result and "jam berapa" not in result:
                    result = result.replace("berapa", "jam berapa")
        # 處理 何時
        elif "何時" in ref or "幾時" in ref:
            if "jam berapa" not in result and "kapan" not in result:
                result = "jam berapa " + result
            elif "jam" in result and "jam berapa" not in result and "berapa" not in result:
                result = result.replace("jam", "jam berapa")
                
        return result.split(" ")
    
    def fix_time_type(self, zhseg: list, idseg: list) -> list:
        
        result: str = " ".join(idseg)
        ref: str = "".join(zhseg)
        if idseg.count("hari") >= 2:
            result = result.replace("hari", "", 1)
    
        return result.split(" ")

class IndoSyntaxPostCorrectionPlus(IndoSyntaxPostCorrection):
    '''
    第二度更改
    '''
    def __init__(self) -> None:
        pass
    def correct_over_translation(self, zhstr: str, idseg: list) -> list:
        if "我們家住" in zhstr:
            if idseg[0] == "rumah":
                idseg[0] = ""
            
        if "TIME" in zhstr:
            if "這TIME" in zhstr:
                pass
            elif idseg[-1] == "ini" or idseg[-1] == "hari" and idseg[-2] == "TIME":
                idseg = idseg[:-1]
        
        if "這" not in zhstr and "這個" not in zhstr:
            idseg = " ".join(idseg).replace("ini", "itu").replace("  ", " ").strip().split()
            if "那" in zhstr or "那個" in zhstr:
                pass
            else:
                idseg = " ".join(idseg).replace("itu", "").replace("  ", " ").strip().split()

        if "那" not in zhstr and "那個" not in zhstr:
            idseg = " ".join(idseg).replace("itu", "ini").replace("  ", " ").strip().split()
            if "這" in zhstr or "這個" in zhstr:
                pass
            else:
                idseg = " ".join(idseg).replace("ini", "").replace("  ", " ").strip().split()
        
        if re.search("奶奶.*常常", zhstr):
            idseg = [x.replace("terbangun", "bangun") for x in idseg]
        
        if "回來" == zhstr[-2:]:
            idstr = " ".join(idseg)
            if "dan kembali" in idstr or "kembali" in idstr:
                idseg = idstr.replace("dan kembali", "").replace("kembali", "").replace("  ", "").strip().split()
        
        
        if re.search("洗一下.*[手|腳|身體|頭]。", zhstr):
            if idseg[-2] == "anda":
                idseg[-2] = ""
        if re.search("洗一下.*[手|腳|身體|頭]", zhstr):
            if idseg[-1] == "anda":
                idseg[-1] = ""    

        return " ".join(idseg).replace("  ", "").strip().split()
    
    def correct_under_translation(self, zhstr: str, idseg: list) -> list:
        
        if re.search("他是.*", zhstr):
            idstr = " ".join(idseg)
            if "dia adalah" not in idstr:
                idseg = idstr.replace("dia","dia adalah",1).split()
            
        if re.search("我是.*", zhstr):
            idstr = " ".join(idseg)
            if "saya adalah" not in idstr:
                idseg = idstr.replace("saya","saya adalah",1).split()
        
        ## pada 介係詞少翻譯問題
        if "DATE" in zhstr:
            idstr = " ".join(idseg)
            if "pada DATE" not in idstr:
                idseg = idstr.replace("DATE","pada DATE",1).split()
                
        if "TIME" in zhstr:
            idstr = " ".join(idseg)
            if "pada TIME" not in idstr:
                idseg = idstr.replace("TIME","pada TIME",1).split()
                
                
        ## sudah 少譯問題
        if re.search("[我|你|他].*了", zhstr):
            idstr = " ".join(idseg)
            if "saya sudah" not in idstr:
                idseg = idstr.replace("saya","saya sudah",1).split()
            elif "dia sudah" not in idstr:
                idseg = idstr.replace("dia","dia sudah",1).split()
            elif "anda sudah" not in idstr:
                idseg = idstr.replace("anda","saya sudah",1).split()
        sudahReString = "|".join(INDONESIAN_SUDAH_ERROR_WORDS.keys())
        matches = f".*[{sudahReString}].*了"

        if re.search("那個.*了", zhstr):
            idstr = " ".join(idseg)
            if "itu sudah" not in idstr:
                idseg = idstr.replace("itu","itu sudah").split()
        elif re.search(matches, zhstr):
            for i in range(len(idseg)):
                for k, v in INDONESIAN_SUDAH_ERROR_WORDS.items():
                    if idseg[i] == v and idseg[i - 1] != "sudah":
                        idseg[i] = "  sudah " +  v 

        
        # location 菜品問題
        if re.search(".*LOCATION.*[菜|食物]", zhstr): 
            for i in range(len(idseg)):
                if idseg[i] == "LOCATION" and idseg[i - 1] != "makanan":
                    idseg[i] = "  makanan " + idseg[i]
            pass
        # 吃／喝 少譯問題
        if re.search(".*吃FOOD", zhstr):
            for i in range(len(idseg)):
                if idseg[i] == "FOOD" and idseg[i - 1] != "makan":
                    idseg[i] = "  makan " + idseg[i]
        if re.search(".*喝", zhstr):
            for i in range(len(idseg)):
                for k, v in INDONESIAN_MINUM_UNDERCASE.items():
                    if idseg[i] == v and idseg[i - 1] != "minum":
                        idseg[i] = "  minum " +  v 
        
        # 副詞少譯情況
        if re.search(".*很.*", zhstr):
            for i in range(len(idseg)):
                for k, v in INDONESIAN_MINUM_UNDERCASE.items():
                    if idseg[i] == v and idseg[i - 1] != "sangat":
                        idseg[i] = "  sangat " +  v 
                    
        return " ".join(idseg).replace("  ", "").strip().split()
  
    def correct_grammar_mistake(self, zhstr: str, idseg: list) -> list:
        idstr = " ".join(idseg)
        if re.search(".*好朋友.*", zhstr):
            idstr = idstr.replace("temanku yang baik", "teman baikku")
        
        # 動詞片語錯誤
        if "沒吃完" in zhstr:
            idstr = idstr.replace("belum selesai makan", "tidak menghabiskan makannanya")
            idstr = idstr.replace("tidak selesai makan", "tidak menghabiskan makannanya")
            
        if re.search("請[你|我|他|她]", zhstr):
            idstr = idstr.replace("silakan", "tolong")
            idstr = idstr.replace("silahkan", "tolong")
        
        if "煮甚麼" in zhstr or "煮什麼" in zhstr:
            if "masak apa" not in idstr:
                if "apa" in idstr:
                    idstr = idstr.replace("apa", "").strip()
                idstr = idstr.replace("masak", "masak apa")
            if "TIME" in idstr:
                idstr = "TIME " + idstr.replace("TIME", "").strip()
                
        if "陪伴" in zhstr:
            if "bersama" in idstr:
                idstr = idstr.replace("bersama", "dengan")
                
        if re.search("[我|你|您]幫[我|你|您]洗澡", zhstr):
            idstr = idstr.replace("mandi untuk anda", "membantu anda mandi")
            
        return idstr.replace("  ", "").strip().split()    
    
    def correct_error_translation(self, zhstr: str, idseg: list) -> list:
        idstr = " ".join(idseg)
        
        # 兄弟姊妹稱謂
        if "姐姐" in zhstr or "姊姊" in zhstr or "哥哥" in zhstr:
            if "adik" in idstr:
                idstr = idstr.replace("adik", "kakak", 1) # replace first encounter
        if "妹妹" in zhstr or "弟弟" in zhstr:
            if "kakak" in idstr:
                idstr = idstr.replace("kakak", "adik", 1) # replace first encounter
            if "saudara perempuan" in idstr:
                idstr = idstr.replace("saudara perempuan", "adik")
        
        if re.search("整理.*[床|沙發|衣服|地板|陽台|盆栽]", zhstr):
            if "mengatur" in idstr:
                idstr = idstr.replace("mengatur", "merapikan")

        if "TIME" in zhstr or "DATE" in zhstr:
            if "di pada" in idstr:
                idstr = idstr.replace("di pada", "pada")
        
        # 等等
        if "等等" in zhstr or "等一下" in zhstr or "等一等" in zhstr:
            if "menunggu" in idstr:
                idstr = idstr.replace("menunggu", "nanti akan", 1)
            elif "tunggu" in idstr:
                idstr = idstr.replace("tunggu", "nanti akan", 1)
        
        # 代名詞翻譯錯誤
        if "你" in zhstr and "你們" not in zhstr:
            idstr = idstr.replace("kalian", "kamu")
            
        if "不舒服" in zhstr and "這裡" not in zhstr:
            idstr = idstr.replace("nyaman", "enak")
            
        if "神經痛" in zhstr:
            if "linu" in idstr:
                idstr = idstr.replace("linu", "sakit saraf")
                
        return idstr.replace("  ", "").strip().split() 
    def correction_main(self, zhseg: list, idseg: list) -> str:
        zhstr = "".join(zhseg)
        idseg = super().correction_main(zhseg, idseg).split()
        
        idseg = self.correct_over_translation(zhstr, idseg)
        idseg = self.correct_under_translation(zhstr, idseg)
        idseg = self.correct_grammar_mistake(zhstr, idseg)
        idseg = self.correct_error_translation(zhstr, idseg)
        
        return " ".join(idseg).replace("  ", "").strip()

if __name__ == "__main__":
    correct = IndoSyntaxPostCorrectionPlus()
    zhseg = "神經 痛".split()
    idseg = "linu".split()
    # zhseg = "這橘子 很 甜".split()
    # idseg = "jeruk itu manis".split()
    # zhseg = "物理 治療師 TIME 評估 ， 奶奶 的 午餐 準備 了 嗎 ？".split()
    # idseg = "ahli terapi fisik menilai TIME ini , apakah nenek siap makan siang ?".split()
    # zhseg = "奶奶 的 飯 為什麼 沒 吃 完".split()
    # idseg = "mengapa nenek belum selesai makan ?".split()
    # zhseg = "TIME 煮 什麼".split()
    # idseg = "masak TIME ini Apa".split()
    # zhseg = "TIME 時 記得 去 LOCATION".split()
    # idseg = "ingatlah untuk pergi ke LOCATION TIME ini".split()
    # zhseg = "您 需要 我 幫 您 洗澡 嗎 ？".split()
    # idseg = "apakah Anda membutuhkan saya untuk mandi untuk Anda ?".split()
    res = correct.correction_main(zhseg, idseg)
    print(res)