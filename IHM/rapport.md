## IMH

### Technologie
Pour l'IHM, j'ai choisi d'utiliser Angular. Je me suis assurée d'utiliser la dernière version. J'ai également utilisé la librairie Angular Material.

### Méthodes mises en place pour sécuriser l'application :

#### 1 - Implémentation d'un Auth Guard pour gérer l'accès aux pages
J'ai d'abord commencé par ajouter un Auth Guard, nouvelle fonctionnalité d'Angular qui permet de superviser l'accès aux routes choisi. L'application étant assez simple (elle ne contient que deux pages : la page de connexion et la page principale du site), j'ai supervisé l'accès à la route '/'.
L'auth guard permet d'effectuer des actions avant de permettre l'accès à une route, j'ai donc vérifié si l'utilisation est authentifié. On vérifie cela grace à l'access token, s'il y en a bien un, on peut accéder à la page principale de site, sinon on est redirigé automatiquement vers la page de connexion.
Cela permet aussi à un utilisateur déjà connecté d'accéder au site directement s'il est déjà authentifié.

#### 2 - Token JWT
L'API a implémenté l'authentification avec JWT, j'ai donc pris en charge l'access token et le refresh token. J'ai créé un service pour les appels à l'api, qui garde l'access token.
// A compléter

#### 3 - Gestion des inputs
L'application ayant plusieurs formulaires (notamment sur la page de connexion), j'ai essayé de nettoyer au mieux les données entrées par l'utilisateur. our ça, j'ai mis un place des Validators sur les données du formulaire de connexion/d'inscription. Ils permettent de valider l'entrée utilisateur et empèchent de pouvoir envoyer le formulaire si les données ne sont pas conformes aux spécifications souhaitées :

screens 


Une fois le formulaire envoyé, je sanitize les données avant de les traiter pour ne pas envoyer des données problématiques à l'api. Angular sanitize déjà automatiquement les url pasées en paramètre (comme les images par exemple).

#### 4 - 