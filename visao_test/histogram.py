import cv2
import numpy as np

# Função para calcular o histograma
def calculate_histogram(image):
    # Converter a imagem para tons de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calcular o histograma
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    # Normalizar o histograma
    hist /= hist.sum()
    return hist

# Função para comparar histogramas
def compare_histograms(hist1, hist2):
    # Calcular a correlação entre os dois histogramas
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return correlation

# Capturar vídeo da câmera
cap = cv2.VideoCapture(0)

# Carregar a imagem de referência
reference_image_red = cv2.imread('visao/vermelho_foto.jpeg')
reference_hist_red = calculate_histogram(reference_image_red)

reference_image_black = cv2.imread('visao/preto_foto.jpeg')
reference_hist_black = calculate_histogram(reference_image_black)

while True:
    # Capturar frame a frame
    ret, frame = cap.read()

    # Calcular o histograma do frame em tempo real
    real_time_hist = calculate_histogram(frame)

    # Mostra a correlação para o preto
    #print(compare_histograms(real_time_hist, reference_hist_black))

    
    # Comparar o histograma em tempo real com o histograma de referência
    if compare_histograms(real_time_hist, reference_hist_red) >= 0.75:
        cv2.putText(frame, 'Histograms Match!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        x = "0010" #vermelha

    if compare_histograms(real_time_hist,reference_hist_black) >= 0.75:
        cv2.putText(frame, 'Histograms Match!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        x = "0001" #Preta
        ativa_robo = True
        

    # Mostrar o frame
    cv2.imshow('Real-time Histogram Comparison', frame)

    # Sair do loop se 'q' for pressionado
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura e fechar todas as janelas
cap.release()
cv2.destroyAllWindows()