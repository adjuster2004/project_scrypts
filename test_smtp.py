import smtplib

def test_hopedb():
    print("Подключаемся к HopeDB MSG на порт 2525...")
    try:
        with smtplib.SMTP('127.0.0.1', 2525) as server:
            server.set_debuglevel(1) 
            
            raw_email = """From: sender@external.com
To: alice@hope.local
Subject: Test Policy
Content-Disposition: attachment; filename="virus.exe"

Это тело письма. Сервер должен оборвать нас, как только увидит заголовок вложения!
"""
            # Исправлено: принудительно кодируем в UTF-8
            server.sendmail('sender@external.com', 'alice@hope.local', raw_email.encode('utf-8'))
            
    except smtplib.SMTPResponseException as e:
        print(f"\n✅ ОТЛИЧНО! Сервер заблокировал письмо. Код: {e.smtp_code}, Ошибка: {e.smtp_error.decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"\n❌ Что-то пошло не так: {e}")

if __name__ == "__main__":
    test_hopedb()