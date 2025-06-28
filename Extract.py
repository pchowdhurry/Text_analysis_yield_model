import string 
import re 
import numpy as np


class Extract:

    def __init__(self, text:str):
        self.input = text 

    def remove_punctuation(self):
        result = self.input 
        for el in string.punctuation:
            result.replace(el, "")
        
        result = result.replace('\n',"")
        return result


    def extract_sentences(self)->list[list]:
        cleaned_text = self.input.replace("\n", " ")
        sentences = re.split(r'(?<!\w\.\w)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', cleaned_text)
        all_caps = re.compile(r'\b[A-Z]{2,}\b')
        sentences= [ s for s in sentences if not all_caps.search(s)]
        output = [s for s in sentences if len(s)>0]
        output = [st for st in output if st[0].isupper()]
        st_cancel = ['(', ")", ':', '<', '>', '/','.']
        clean_out = []
        for s in output:
            to_add = s[1:-1]
            add = 0 
            for el in st_cancel:
                if el in to_add:
                    add +=1
            if add == 0 and len(s)>20:
                clean_out.append(s)
        return clean_out
    

class LabelSimilar:
    def __init__(self, key_vecs:list[tuple]):
        self.key_vecs = key_vecs
 
    
    def dot_similarity(self, sentences:list[str]):
        sim_dict = {}
        for i in range(0, len(self.key_vecs)):
            curr_tuple = self.key_vecs[i]
            curr_topic = curr_tuple[0]
            curr_sim_vec = curr_tuple[1]
            dot_product = np.dot(curr_sim_vec,sentences)
            sim_dict[curr_topic] = dot_product
        max = -100000000000
        most_sim_topic = ""
        for topic in sim_dict.keys():
            dot_val = sim_dict[topic]
            if dot_val > max:
                max = dot_val 
                most_sim_topic = topic 
        
        return (most_sim_topic, max)
    
    ## internal function for calculating cosine similarity 
   
    
    def cosine_similarity(self, sentences:list[str]):
        sim_dict = {}
        for i in range(0, len(self.key_vecs)):
            curr_tuple = self.key_vecs[i]
            topic = curr_tuple[0]
            key_vec = curr_tuple[1]

            cos_metric = self.__cos_helper(key_vec, sentences)
            sim_dict[topic] = cos_metric

        ## iterating through dict to find max 
        max = -100000
        ret_topic = ""
        for topic in sim_dict.keys():
            if sim_dict[topic] > max:
                max = sim_dict[topic]
                ret_topic = topic 
        return (ret_topic, max)
    
    def __cos_helper(self,x, y):
        sim_metric = np.dot(x,y)/ (np.linalg.norm(x)*np.linalg.norm(y))
        return sim_metric




    
    
    

    





