import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget

from ui_MeteoF import Ui_Dialog
from meteo import meteo
from geocodage_IGN import trait_request

import pandas as pd


from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar


from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
from qt_material import apply_stylesheet



class MeteoWindow(QWidget):
    def __init__(self, message):
        # Message = liste contenant [localisation, duree]
        #     localisation = dictionnaire key = ville, value = list[X, Y]
        #     duree = nombre entier de jours

        localisation = message[0]
        duree = message [1]

        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        
        #fig = export_figure(5)
        fig = meteo (localisation, duree)
        canvas = FigureCanvas(fig) # create canvas
        layout.addWidget(canvas)   # add canvas to layout
 
        # Create and add toolbar
        toolbar = NavigationToolbar(canvas, self)
        layout.addWidget(toolbar)



class MyWindow(QWidget, Ui_Dialog):

    
    def __init__(self):
        
        super().__init__()
                
        self.setupUi(self)
        
        self.localisations_fav=None
        self.locations_search=None
        
        ######## Favoris

        # initialise la combobox
        #populate combo box
        self.populate_fav()

        # connect OK_fav button
        
        ###### ACTION FERMER
        self.btnClose.clicked.connect(self.btnCloseClicked)

        ######¸ ACTIONS FAVORIS
        # prévisions favori selectionné
        self.listFav.doubleClicked.connect(self.listFavDblClicked)
        self.btnRemoveFav.clicked.connect(self.btnRemoveFavClicked)
        
        # ajouter aux favoris
        #self.btnAddFav.clicked.connect(self.btnAddFavClicked)

        ###### ACTION RECHERCHE

        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.btnOkSearch.clicked.connect(self.btnOKSearchClicked)
        self.btnAddFav.clicked.connect(self.btnAddFavClicked)


    ###### METHODES FAVORIS
    def populate_fav(self): 
        try : 
            
            df_fav = pd.read_csv("localisation.txt", sep= ",", header = None)
            df_fav.columns = ['VILLE', 'X', 'Y']
            df_fav = df_fav.set_index('VILLE')
            self.localisations_fav={}

            
            for row in df_fav.iterrows() :
                ville = row[0]
                x = row[1]['X']
                y = row[1]['Y']
                self.localisations_fav.update({ville : [x,y]})
            l_villes = list(self.localisations_fav)
            
            self.listFav.clear()
            
            for ville in l_villes :
                self.listFav.addItem(ville)
        except:
            pass

    
    def btnRemoveFavClicked(self) :
        
        try :

            if self.listFav.currentItem().isSelected():
                ville = self.listFav.currentItem().text()

                print (f'le favori à supprimer est {ville}')
            
                eff = None
                with open("localisation.txt", "r", encoding='utf-8') as f :
                    lignes = f.readlines()  # Retourne une liste
                    
                    for i, ligne in enumerate(lignes):
                        print(ligne)
                        if ville in ligne :
                            print(f'{ville} est dans {ligne}   ---- {i}')
                            eff = i
                            break
                    f.close()

                if not(eff is None) :
                    del lignes[eff]
                    if len(lignes)!=0 :
                        if lignes[-1][-1] == '\n' :
                            lignes[-1] = lignes[-1][0:-1]
                
                    with open("localisation.txt", "w") as f :

                        f.writelines(lignes)
                    
                        f.close() 
                self.listFav.clear()
                self.populate_fav()

        except:
            pass
  

    ###### METHODES RECHERCHE

    def btnSearchClicked(self) :
        loc = self.lineLoc.text()
        self.locations_search = trait_request(loc) #geocode_city_france(loc)

        if not(self.locations_search is None) :

            self.comboSearch.clear()
            
            for i, (k, v) in enumerate(self.locations_search.items()) :
                #print (f'{k} ----> {v}')
                self.comboSearch.addItem(k)

    
               
    def btnOKSearchClicked(self) :
        if not(self.locations_search is None) :
            ville = self.comboSearch.currentText()
            
            XY = self.locations_search[ville]
            locals={ville : XY}
            
            # récupère la durée
            duree = self.spnDuree.value()
            #appelle la fonction 

            print (f'Meteo pour {ville} sur {duree} jours.')
            self.w = MeteoWindow([locals, duree])
            self.w.show()

    
    def btnAddFavClicked(self) :
        if not(self.locations_search is None) :
            with open("localisation.txt", "a", encoding = "utf8") as f :
                
                #ceriture dans le fichier
                ville = self.comboSearch.currentText()
                XY = self.locations_search[ville]
                locals=f'{ville},{XY[0]},{XY[1]}'

                f.write("\n")
                f.write(locals)
                
                f.close()

                # mise à jour liste combobox

                self.populate_fav()

    ###### METHODES FERMER

    def btnCloseClicked(self):
        
        myWindow.close()

     ###### METHODES FAVORIS METEO



    def listFavDblClicked(self):

        # récupère l'élément sélectionné de la combobox ou a défaut le premier élement
        ville = self.listFav.currentItem().text()
        
        self.localisation_fav = {k: v for k, v in self.localisations_fav.items() if ville == k}
      
        # récupère la durée
        self.duree = self.spnDuree.value()

        print (f'Meteo pour {ville} sur {self.duree} jours.')

        self.w = MeteoWindow([self.localisation_fav, self.duree])
        self.w.show()




if __name__ == "__main__":
    # On crée l'instance d'application en lui passant le tableau des arguments.


    app = QApplication(sys.argv)

    theme ='dark_pink.xml'
    apply_stylesheet(app, theme=theme)
    # On instancie une fenêtre graphique et l'affiche.
    myWindow = MyWindow()
    myWindow.show()

    # On démarre la boucle de gestion des événements.
    sys.exit(app.exec())