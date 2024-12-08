from requests import RequestException

from core.regex_service import RegexService
from core.repositories import JsonResultRepository


def main():
    repository = JsonResultRepository()
    service = RegexService(repository)

    while True:
        print("\nВыберите действие:")
        print("1. Получить ссылки из файла")
        print("2. Получить ссылки с веб-страницы")
        print("3. Найти ссылки в тексте")
        print("4. Выход")

        try:
            user_input = input("Введите номер действия: ").strip().lower()
            choice = int(user_input)

            match choice:
                case 1:
                    result = service.get_urls_in_file()
                        
                    print(f"Результат из файла: {result.urls}")

                case 2:
                    url = input("Введите URL веб-страницы: ")
                    result = service.get_urls_in_web(url)

                    print(f"Результат с веб-страницы: {result.urls}")

                case 3:
                    text = input("Введите текст: ")
                    urls_list = service.get_urls_in_text(text)

                    print(f"Результат из текста: {urls_list}")

                case 4:
                    print("Выход из программы.")
                    break

                case _:
                    print("Ошибка: выбрано недопустимое действие. Попробуйте снова.")

        except RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()