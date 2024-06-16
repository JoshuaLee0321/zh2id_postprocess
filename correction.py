import re
from statics import *

class IndoSyntaxPostCorrection():
    def __init__(self) -> None:
        pass
    def get_position(self, zhstr: str, idstr: str):
        pass
    
    def correction_main(self, zhseg: list, idseg: list) -> list:
        
        result: list = []
        # 先修正問題
        # 再修正再問題中的分類
        
        # 修正直述句
        
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
    

    def fix_():
        pass
        
        
        
    
        

if __name__ == "__main__":
    correct = IndoSyntaxPostCorrection()
    zhseg = "他 要 一 個 天花".split()
    idseg = "dia ingin satu penyakit ku tik".split()
    
    res = correct.fix_predicate_type(zhseg, idseg)
    print(res)