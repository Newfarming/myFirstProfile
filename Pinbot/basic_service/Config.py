# encoding: utf-8
# 读取学校(985,211 and other)  读取索引(倒排) 
import codecs
import pymongo
import ConfigParser

class Config:
    config = None
    properties_path = ''
    
    def __init__(self, properties_path):
        self.config = ConfigParser.ConfigParser()
        self.properties_path = properties_path
        # self.config.read(properties_path)        
        
    def get_prop_value(self, section, key):
        self.config.read(self.properties_path) 
        sections = self.config.sections()
        context1 = self.config.get(section, key)
        return context1
    
    def read_school(self, school_file_path):
        school_dict = dict()
        lines = codecs.open(school_file_path, "r", 'utf-8').readlines()  
        for line in lines:
            if ',' in line:
                line = line.split(',')
                key = line[0].strip() 
                value = line[1].strip()
                school_dict[key] = value 
        return school_dict
    
    def read_company(self, company_file_path):   
        company_dict = dict()     
        company_file = open(company_file_path, "r")  
        for line in company_file:
            line = line.decode("utf-8").split()
            company_dict[line[0].strip()] = '' 
        company_file.close()
        return company_dict
    
    def read_skill_file(self, skill_file_path):
        skill_dict = dict()
        skill_file = open(skill_file_path, "r")  
        for line in skill_file:
            line = line.decode("utf-8").split()
            skill_dict[line[0].strip()] = ''
        skill_file.close()
        return skill_dict
    
    def read_keywords_file(self, keywords_file_path):
        keywords_dict = dict()
        keywords_file = open(keywords_file_path, "r")
        for line in keywords_file:
            line = line.decode("utf-8").split()
            keywords_dict[line[0].strip()] = ''
        keywords_file.close()
        return keywords_dict
    
    def read_city_file(self, city_file_path):
        city_dict = dict()
       
        keywords_file = open(city_file_path, "r")
        for line in keywords_file:
            line = line.decode("utf-8").split()
            city_dict[line[0].strip()] = ''
        return city_dict
    
    def read_common_csv(self, common_csv_file_path):
        common_dict = dict()
        common_max = float(0)
        common_min = float(1)
        common_csv_file = open(common_csv_file_path, 'r')
        line = common_csv_file.readline().decode("utf-8")  # 调用文件的 readline()方法
        while line:
            line = line.decode("utf-8")
            keyword = line.split(',')[0].strip()
            
            sequence = float(line.split(',')[1])
            if sequence > common_max:
                common_max = sequence
            if sequence < common_min:
                common_min = sequence
            common_dict[keyword] = sequence  # 后面跟 ',' 将忽略换行符
            line = common_csv_file.readline()
        
        common_dict['common_max'] = common_max
        common_dict['common_min'] = common_min
        common_csv_file.close() 
        return common_dict
    
    def read_resume_csv(self, common_csv_file_path):
        common_dict = dict()
        common_max = float(0)
        common_min = float(1)
        common_csv_file = open(common_csv_file_path, 'r')
        line = common_csv_file.readline().decode("utf-8")  # 调用文件的 readline()方法
        while line:
            line = line.decode("utf-8")
            
            keyword = line.split(' ')[1].strip()
            sequence = float(line.split(' ')[0])
            if sequence > common_max:
                common_max = sequence
            if sequence < common_min:
                common_min = sequence
            common_dict[keyword] = sequence  # 后面跟 ',' 将忽略换行符
        # print(line, end = '')　　　# 在 Python 3中使用
            line = common_csv_file.readline()
        common_csv_file.close() 
        return common_dict
        
    def read_skill_csv(self, skill_csv_file_path):
        skill_dict = dict()
        skill_max = float(0)
        skill_min = float(1)
        skill_csv_file = open(skill_csv_file_path, 'r')
        line = skill_csv_file.readline().decode("utf-8")  # 调用文件的 readline()方法
        while line:
            line = line.decode("utf-8")
            keyword = line.split(',')[0].strip()
            sequence = float(line.split(',')[1])
            if sequence > skill_max:
                skill_max = sequence
            if sequence < skill_min:
                skill_min = sequence        
            skill_dict[keyword] = sequence  # 后面跟 ',' 将忽略换行符
        # print(line, end = '')　　　# 在 Python 3中使用
            line = skill_csv_file.readline()
            
        skill_dict['skill_max'] = skill_max
        skill_dict['skill_min'] = skill_min
        skill_csv_file.close()
        return skill_dict

    def get_colleciton(self, conn, db, collection):
        return conn.db.collection

