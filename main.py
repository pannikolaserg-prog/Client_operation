from src.mask import get_mask_account, get_mask_card_number
from src.widget import get_date, mask_account_card

if __name__ == "__main__":
    print(get_mask_card_number("1234567890123456"))
    print(get_mask_account("1234567890123456"))
    # Тестирование
    print(mask_account_card("Visa Platinum 7000792289606361"))
    # Visa Platinum 7000 79** **** 6361

    print(mask_account_card("Счет 73654108430135874305"))
    # Счет **4305

    print(mask_account_card("MasterCard Gold 5500000000000004"))
    # MasterCard Gold 5500 00** **** 0004

    # Тестирование
    print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
    print(get_date("2024-12-01T15:30:45.123456"))  # 01.12.2024
