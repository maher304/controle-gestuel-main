import cv2
import webbrowser
import datetime

def perform_action(fingers, roi):
    font = cv2.FONT_HERSHEY_SIMPLEX
    action_text = ""

    if fingers == 0:
        action_text = "0 doigt : Capture d'écran enregistrée"
        # Enregistrer la capture d'écran de la ROI avec horodatage
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"
        cv2.imwrite(filename, roi)
        print(f"Capture enregistrée sous {filename}")

    elif fingers == 1:
        action_text = "1 doigt : Afficher une image"
        img = cv2.imread("assets/image1.jpg")
        if img is not None:
            img = cv2.resize(img, (roi.shape[1], roi.shape[0]))
            roi[:] = img
        else:
            action_text = "Image non trouvée."

    elif fingers == 2:
        action_text = "2 doigts : Couleur de fond = bleu"
        roi[:] = (255, 0, 0)

    elif fingers == 3:
        action_text = "3 doigts : Action spéciale !"
        # Action spéciale à définir

    elif fingers == 4:
        action_text = "4 doigts : Fermer toutes les fenêtres"
        cv2.destroyAllWindows()

    elif fingers == 5:
        action_text = "5 doigts : Ouvrir un site web"
        webbrowser.open("https://www.example.com")  # Remplace par ton lien ou un chemin de fichier PDF
        print("Ouverture d'un site web...")

    else:
        action_text = f"{fingers} doigts détectés"

    # Affichage du texte dans la ROI
    cv2.putText(roi, action_text, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
