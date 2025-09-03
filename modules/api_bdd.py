from loguru import logger
from tools.mysql import Mysql



class TableStories(Mysql):
    def __init__(self, table=None, configClass=None):   
        self._table = table
        super().__init__(create_script=self.create_script(), configClass=configClass)
          
    def create(self, datas):
        return self.insert_auto(table=self._table, datas=self.format_for_db(datas))
              
    def update(self, id, datas):
        return self.update_auto(table=self._table, id=id, datas=self.format_for_db(datas))      

    def delete(self, indice):    
        query = f"DELETE FROM `{self._table}` WHERE `{self._table}`.indice = {indice}"
        rs = self.query(query)
        return rs
    
    def create_script(self):
        return f"""
        CREATE TABLE `{self._table}` (
            `indice` INT(10) UNSIGNED,
            `event` LONGTEXT NOT NULL,
            `indices` LONGTEXT NULL,
            PRIMARY KEY (`indice`) USING BTREE
        )
        COLLATE='utf8mb4_unicode_ci'
        ENGINE=InnoDB
        AUTO_INCREMENT=81
        ;

        """
    def get(self):
        query = f"SELECT * FROM `{self._table}`"
        rs = self.fetch(query)
        if rs:
            return rs
        return False
    
    def get_event(self, indice):
        query = f"SELECT * FROM `{self._table}` WHERE `{self._table}`.indice = '{indice}'"
        rs = self.fetch(query)
        if rs:
            return self.format_from_db(rs[0])
        return False
    
    def get_stories(self):
        query = "SHOW TABLES FROM rpg_games"
        rs = self.fetch(query)
        if rs:
            stories = []
            for elem in rs:
                story = elem['Tables_in_rpg_games']
                stories.append(story)
        return stories

    
    def format_for_db(self, datas):
        if 'indices' in datas:
            if len(datas['indices']) == 0: #liste vide
               datas['indices'] = None
            else:
                datas['indices'] = ",".join(datas['indices']) # Convertit la liste en chaîne
        return datas
    
    def format_from_db(self, datas):
        if datas['indices'] is not None and len(datas['indices']) > 0:
            datas['indices'] = [int(x.strip()) for x in datas['indices'].split(',')]

        return datas
    
    def get_story(self):
        query = f"SELECT * FROM `{self._table}` ORDER BY `{self._table}`.indice ASC"
        rs = self.fetch(query)
        if rs:
            for elem in rs:
                elem = self.format_from_db(elem)
            return rs
        return False