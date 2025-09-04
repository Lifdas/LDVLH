from pathlib import Path
from loguru import logger
import webview
from modules.api_bdd import TableStories
class API():
    def __init__(self, config=None):
        self.config = config
        self._user_id = 0
        # self.child_windows = []  # Stocker les références des fenêtres enfants
         
    # def get_version(self):
    #     return __version__

    # def fetch_latest(self):
    #     """Récupère latest.json depuis ton serveur de mises à jour."""
    #     url = 'http://217.154.121.75/updates/latest.json'
    #     session = requests.Session()
    #     retries = Retry(
    #         total=2,
    #         backoff_factor=0.3,
    #         status_forcelist=[502, 503, 504],
    #         raise_on_status=False
    #     )
    #     session.mount('http://', HTTPAdapter(max_retries=retries))

    #     try:
    #         res = session.get(url, timeout=(5, 10))
    #         res.raise_for_status()
    #         return res.json()
    #     except Exception as e:
    #         # On renvoie une structure uniforme en cas d’erreur
    #         return {'error': str(e)}
        


    # création d'une fenêtre enfant
    def open_story_window(self, story):
        project_root = Path(__file__).resolve().parents[1]
        story_html = project_root / "frontend" / "pages" / "story.html"
        file_uri = story_html.resolve().as_uri()
        url      = f"{file_uri}#story={story}"

        webview.create_window(
            title=f"{story}",
            url=url,
            js_api=self,
            width=600,
            height=765,
            resizable=False
        )

    def _get_main_window(self):
        """Trouve la fenêtre principale de manière dynamique"""
        try:
            for window in webview.windows:
                if "Rpg games" in window.title:
                    return window
        except Exception as e:
            print(f"Erreur lors de la recherche de la fenêtre principale: {e}")
        return None
    
    def create_title(self, data):
        """ Crée une nouvelle histoire """
        db = TableStories(table=data, configClass=self.config)
        creation = db.create_table()
        if creation:
            return True
        return False
    
    def get_stories(self):
        db = TableStories(configClass=self.config)
        rs = db.get_stories()
        if rs:
            return rs
        
    def create_event(self, table, data):
        db = TableStories(table=table, configClass=self.config)
        if data['indice'] != '' or data['indice'] != 0:
            creation = db.create(data)
            if creation:
                return True
            return False
    
    def createHero(self, table, data):
        db = TableStories(table=table, configClass=self.config)
        rs = db.get_event(9999)
        if rs and data['name'] != '' and data['skills'] != '':
            liste_de_heros = rs['indices']
            liste_de_heros.append(data)
            rs['indices'] = liste_de_heros
            update = db.update(9999, rs)

            if update:
                return True
            return False
        else:
            if data['name'] != '' and data['skills'] != '':
                hero_data = {
                    'indice': 9999,
                    'event': f"Veuillez sélectionner un héros.",
                    'indices': [data]
                }
                creation = db.create(hero_data)

                if creation:
                    return True
                return False
    
    def update_event(self, table, data):
        db = TableStories(table=table, configClass=self.config)
        if id != '' or id != 0:
            update = db.update(data['indice'], data)
            if update:
                return True
            return False
    
    def get_event(self, table, indice = False):
        db = TableStories(table=table, configClass=self.config)
        if indice:
            event = db.get_event(indice)
            if event:
                return event
            return False
        else:
            event = db.get_event(1)
            if event:
                return event
            return False
    
    def get_story(self, table):
        db = TableStories(table=table, configClass=self.config)
        story = db.get_story()
        if story:
            return story    
        return False
    
    def delete_event(self, table, id):
        db = TableStories(table=table, configClass=self.config)
        deletion = db.delete(id)
        if deletion:
            return True
        return False