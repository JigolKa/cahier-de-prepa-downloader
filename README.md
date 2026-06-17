# cahier-de-prepa-downloader

Télécharge tous les fichiers d'un site Cahier de Prépa.

### Installation

```bash
git clone https://github.com/JigolKa/cahier-de-prepa-downloader
cd cahier-de-prepa-downloader
pip install -r requirements.txt
```

### Utilisation

exemple:
```bash
> python main.py 
Entrez l'url du site sous la forme: https://cahier-de-prepa.fr/<lycée>/
URL: https://cahier-de-prepa.fr/mp2i-fermat/
```

### Connexion

(Optionnel) <br/>

Pour télécharger les fichiers contenus dans des dossiers verrouillés, créez un fichier `.env` et remplissez le de telle sorte:

```
LOGIN=true
UTILISATEUR=<votre nom d'utilisateur>
MOT_DE_PASSE=<votre mot de passe>
```
