import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

SMTP_SERVER = "127.0.0.1"
SMTP_PORT = 25

def send_test_emails():
    print(f"Подключение к шлюзу {SMTP_SERVER}:{SMTP_PORT}...")
    
    try:
        # Устанавливаем соединение со шлюзом
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        # Раскоментируйте следующую строку, если хотите видеть весь SMTP-диалог в консоли:
        # server.set_debuglevel(1) 
        
        for i in range(1, 11):
            msg = MIMEMultipart()
            msg['From'] = "hacker@bad-guys.net"
            msg['To'] = "admin@your-domain.com"
            msg['Subject'] = f"Тестовое письмо #{i} для Карантина"
            
            # Добавляем наше кодовое слово, на которое сработает Regex правило
            body = f"Привет!\nЭто тестовая рассылка, письмо номер {i}.\nСекретное слово: CASINO_PROMO\nКонец связи."
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Отправка
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            print(f"✅ Письмо #{i} успешно передано на шлюз.")
            
            time.sleep(0.5) # Небольшая пауза между письмами
            
        server.quit()
        print("🎉 Все 10 писем отправлены!")
        
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")

if __name__ == "__main__":
    send_test_emails()