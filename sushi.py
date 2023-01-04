import os
import cv2
import numpy as np

class CreationImagette:
    def __init__(self, image_path : str, size: tuple = (100, 100)):
        image = cv2.imread(image_path)
        self.taille_image_originale=image.shape
        self.image_path = image_path
        self.output_dir = os.path.basename(image_path).split('.')[0]
        self.size = size
    
    def decoupe(self):
        # On charge l'image
        image = cv2.imread(self.image_path)
        
        # On récupère le nom de l'image sans l'extension
        image_name = os.path.splitext(os.path.basename(self.image_path))[0]
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # On itère sur chaque ligne et chaque colonne de l'image
        for i in range(0, image.shape[0], self.size[0]):
            for j in range(0, image.shape[1], self.size[1]):
                # On découpe l'imagette
                imagette = image[i:i+self.size[0], j:j+self.size[1]]
                # Si l'image est trop petite on ajoute une bordure noire
                if imagette.shape[0]<image.shape[0] or imagette.shape[1]<image.shape[1]:
                    imagette = cv2.copyMakeBorder(imagette, 0, self.size[0]-imagette.shape[0], 0, self.size[1]-imagette.shape[1], cv2.BORDER_CONSTANT, value=0)
                # On génère le nom de l'imagette en incluant ses coordonnées par rapport à l'image d'origine
                imagette_name = f"{image_name}_{i}_{j}.jpg"
                
                # On enregistre l'imagette
                cv2.imwrite(os.path.join(self.output_dir, imagette_name), imagette)
                
    def reconstruction(self,prefixe : str = ""):
        #on prends la liste des images
        liste_path=os.listdir(self.output_dir)
        liste_path=[prefixe+x for x in liste_path]
        
        #on récupère la taille de l'image à construire
        nombre_imagette_x=int(self.taille_image_originale[0]/self.size[0])
        nombre_imagette_y=int(self.taille_image_originale[1]/self.size[1])
        longueur_image=nombre_imagette_x*self.size[0]
        hauteur_image=nombre_imagette_y*self.size[1]
        #On construit une matrice vide de taille (nombre_imagette_x,nombre_imagette_y,3)
        matrice_image=np.zeros((nombre_imagette_x,nombre_imagette_y,3),dtype=np.uint8)
        #On remplit cette matrice avec les valeurs des fichiers correspondants
        for fichier in liste_path:
            imagette=cv2.imread(self.output_dir+"/"+fichier)
            print(imagette.shape)
            nom_fichier=os.path.splitext(os.path.basename(fichier))[0]
            xstart=int(nom_fichier.split('_')[-1])
            ystart=int(nom_fichier.split('_')[-2])
            xend=xstart+self.size[0]
            yend=ystart+self.size[1]
            print(xstart,ystart,xend,yend)
            print(matrice_image[ystart:yend,xstart:xend])
            matrice_image[:,ystart:yend,xstart:xend]=imagette
        cv2.imwrite(self.output_dir+f"{prefixe}reconstruction.jpg",matrice_image)
        return matrice_image


if __name__=="__main__":
    sushi = CreationImagette("DJI_0202.JPG", size=(100, 100))
    sushi.decoupe()
    sushi.reconstruction()
    print(len(sushi.reconstruction(".jpg")))
    

