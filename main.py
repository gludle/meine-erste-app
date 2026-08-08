import random
import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

leicht_quests = ["Schlage einen Baum", "Crafte eine Werkbank", "Crafte eine Holzspitzhacke", "Baue Stein ab", "Crafte Steinwerkzeuge", "Baue einen Ofen", "Stelle Holzkohle her", "Crafte Fackeln", "Finde Schafe", "Crafte ein Bett", "Finde Kohle", "Baue Eisen ab", "Schmelze Eisen", "Crafte eine Eisenspitzhacke", "Finde Kupfer", "Finde eine Höhle", "Sammle 64 Stein", "Crafte einen Eimer", "Sammle Wasser", "Baue ein Feld", "Ernte Weizen", "Backe Brot", "Pflanze Zuckerrohr", "Finde Kürbisse", "Brate Fleisch", "Finde Beeren", "Baue ein Gehege", "Züchte Kühe", "Züchte Hühner", "Sammle Eier", "Besiege ein Skelett", "Erstelle Knochenmehl", "Finde einen Wolf", "Baue eine Hütte", "Setze eine Tür", "Crafte eine Kiste", "Mache Glas", "Baue Fenster", "Baue einen Weg", "Beschrifte Kisten", "Baue ein Lagerfeuer", "Crafte ein Eisenschwert", "Besiege einen Zombie", "Besiege eine Spinne", "Crafte einen Bogen", "Benutze ein Schild", "Besiege einen Creeper", "Finde ein Dorf", "Handle mit einem Dorfbewohner", "Finde ein Schiffswrack", "Öffne eine Schatztruhe", "Erstelle eine Karte", "Besteige einen Berg", "Finde eine Wüste", "Finde einen Dschungel", "Finde einen Bienenstock", "Überquere einen Ozean", "Baue ein Netherportal", "Betrete den Nether", "Sammle Netherrack", "Finde Seelensand", "Baue Redstone ab", "Crafte eine Lampe", "Crafte einen Kolben", "Baue Schienen", "Fahre mit einer Lore", "Crafte einen Trichter", "Färbe ein Schaf", "Scher ein Schaf", "Ändere die Bettfarbe", "Crafte ein Gemälde", "Erstelle ein Banner", "Crafte eine Jukebox", "Finde eine Musikdisc", "Baue einen Schneegolem", "Benanne ein Tier"]
mittel_quests = ["Finde Diamanten", "Crafte Diamantrüstung", "Baue einen Zaubertisch", "Baue Bücherregale", "Verzaubere ein Werkzeug", "Braue einen Trank", "Finde eine Netherfestung", "Besiege Lohen", "Tausche mit Piglins", "Sammle Enderperlen", "Crafte Enderaugen", "Finde eine Bastion", "Sammle Antiken Schrott", "Crafte Netherit", "Finde eine Stronghold", "Aktiviere das Endportal", "Betrete das Ende", "Besiege den Enderdrachen", "Finde eine Endstadt", "Sammle Elytren", "Baue eine Eisenfarm", "Baue eine Goldfarm", "Finde ein Ozeanmonument", "Besiege Elder Guardians", "Baue eine automatische Farm", "Baue eine Redstone-Maschine", "Finde eine Antike Stadt", "Sammle Sculk", "Baue ein großes Lager", "Erstelle eine Villager-Handelshalle"]
schwer_quests = ["Besiege den Wither", "Baue ein Leuchtfeuer", "Besiege den Warden", "Besiege den Enderdrachen ohne starke Ausrüstung", "Baue eine riesige Basis", "Sammle komplettes Netherit-Equipment", "Baue eine Endermanfarm", "Baue eine Raidfarm", "Baue eine Guardianfarm", "Sammle alle Musikdiscs", "Sammle alle Rüstungsverzierungen", "Baue eine riesige Redstone-Maschine", "Baue eine automatische Sortieranlage", "Baue eine Unterwasserstadt", "Baue eine Nether-Autobahn", "Baue eine riesige Statue", "Sammle seltene Items", "Finde eine Antike Stadt ohne Warden", "Baue eine Shulkerfarm", "Baue eine Ghastfarm", "Sammle 10000 Smaragde", "Höhle einen kompletten Chunk aus", "Baue eine Mega-Farm", "Baue eine riesige Kartenwand", "Schalte alle Fortschritte frei", "Überlebe 500 Minecraft-Tage", "Baue ein Schloss", "Baue eine ganze Stadt", "Erstelle ein Redstone-Spiel", "Baue ein riesiges Museum"]

for i in range(len(leicht_quests), 101): leicht_quests.append(f"Leichte Minecraft Quest Nummer {i}")
for i in range(len(mittel_quests), 101): mittel_quests.append(f"Mittlere Minecraft Quest Nummer {i}")
for i in range(len(schwer_quests), 101): schwer_quests.append(f"Schwere Minecraft Quest Nummer {i}")

class MinecraftQuestApp(App):
    def build(self):
        self.speicher_datei = os.path.join(self.user_data_dir, "minecraft_save.json")
        self.level = 0
        self.xp = 0
        self.aktuelle_quest = None
        self.laden()

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.title_label = Label(text="===================\nMinecraft Quest App\n===================", font_size=20, halign="center")
        self.layout.add_widget(self.title_label)

        self.status_label = Label(text="", font_size=16)
        self.layout.add_widget(self.status_label)

        self.progress_bar = ProgressBar(max=100, value=0)
        self.layout.add_widget(self.progress_bar)

        self.quest_label = Label(text="Klicke auf 'Neue Quest', um zu starten!", font_size=16, halign="center")
        self.layout.add_widget(self.quest_label)

        self.btn_done = Button(text="Quest erledigt (+XP)", background_color=(0.2, 0.8, 0.2, 1))
        self.btn_done.bind(on_press=self.quest_erledigt)
        self.layout.add_widget(self.btn_done)

        self.btn_new = Button(text="Neue Quest generieren", background_color=(0.2, 0.6, 1, 1))
        self.btn_new.bind(on_press=self.neue_quest)
        self.layout.add_widget(self.btn_new)

        self.update_ui()
        return self.layout

    def xp_benoetigt(self):
        return 100 + (self.level * 15)

    def update_ui(self):
        max_xp = self.xp_benoetigt()
        self.status_label.text = f"Level: {self.level}   |   XP: {self.xp} / {max_xp}"
        self.progress_bar.max = max_xp
        self.progress_bar.value = self.xp
        if self.aktuelle_quest:
            self.quest_label.text = f"AKTUELL:\nSchwierigkeit: {self.aktuelle_quest['name']}\nAufgabe: {self.aktuelle_quest['text']}\nBelohnung: {self.aktuelle_quest['xp']} XP"

    def neue_quest(self, instance=None):
        schwierig = random.choice(["Leicht", "Mittel", "Schwer"])
        if schwierig == "Leicht":
            self.aktuelle_quest = {"name": schwierig, "text": random.choice(leicht_quests), "xp": 10}
        elif schwierig == "Mittel":
            self.aktuelle_quest = {"name": schwierig, "text": random.choice(mittel_quests), "xp": 15}
        else:
            self.aktuelle_quest = {"name": schwierig, "text": random.choice(schwer_quests), "xp": 20}
        self.update_ui()

    def quest_erledigt(self, instance):
        if not self.aktuelle_quest: return
        self.xp += self.aktuelle_quest["xp"]
        while self.xp >= self.xp_benoetigt():
            self.xp -= self.xp_benoetigt()
            self.level += 1
        self.speichern()
        self.neue_quest()

    def speichern(self):
        daten = {"level": self.level, "xp": self.xp}
        with open(self.speicher_datei, "w") as datei: json.dump(daten, datei)

    def laden(self):
        if os.path.exists(self.speicher_datei):
            try:
                with open(self.speicher_datei, "r") as datei:
                    daten = json.load(datei)
                    self.level = daten.get("level", 0)
                    self.xp = daten.get("xp", 0)
            except: pass

if __name__ == '__main__':
    MinecraftQuestApp().run()
