import re
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
        idseg = self.fix_polite_type(zhseg, idseg)
        idseg = self.fix_negation_type(zhseg, idseg)
        idseg = self.fix_state_sentence_type(zhseg, idseg)
        idseg = self.fix_conjunection_type(zhseg, idseg)
        idseg = self.fix_predicate_type(zhseg, idseg)
        idseg = self.fix_question_type(zhseg, idseg)
        idseg = self.fix_question_case_by_case(zhseg, idseg)
        idseg = self.fix_time_type(zhseg, idseg)
        return " ".join(idseg)
        
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
                result = "bagi" + resList[1].strip() + " , " + resList[0].strip()
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
                result = result.replace(" hingga ", "sehingga")
        
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
            elif "tolong" not in result and "silahkan" not in result:
                result = "silahkan " + result
        # 麻煩你 ...
        elif "麻煩你" in ref or "麻煩" == ref[:2]:
            if "silahkan" in result:
                result = result.replace("silahkan", "tolong")
            elif "tolong" not in result and "silahkan" not in result:
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


        
        return result

    def fix_question_case_by_case(self, zhseg: list, idseg: list) -> list:
        
        result: str = " ".join(idseg)
        ref: str = "".join(zhseg)
        # 處理 在哪裡的問題
        if "在哪裡" in ref:
            if "mana" in result and "dimana" not in result and "di mana" not in result:
                result = result.replace("mana", "di mana")
            if "di mana" not in result and "dimana" not in result:
                result = result + " di mana"
                
        # 處理 "為甚麼"
        elif "為甚麼" in ref or "為什麼" in ref:
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
            if "berapa" not in result:
                result = "berapa " + result
            if "berapa" in result:
                if "panjang" not in result:
                    result = result.replace("berapa", "jam berapa")
        
        return result.split(" ")
    
    def fix_time_type(self, zhseg: list, idseg: list) -> list:
        
        result: str = " ".join(idseg)
        ref: str = "".join(zhseg)
        if idseg.count("hari") >= 2:
            result = result.replace("hari", "", 1)
    
        return result.split(" ")
        
if __name__ == "__main__":
    correct = IndoSyntaxPostCorrection()
    zhseg = " 不好意思 ， 今天 星期幾".split()
    idseg = "segelas air ini sangat besar".split()
    
    res = correct.correction_main(zhseg, idseg)
    print(res)