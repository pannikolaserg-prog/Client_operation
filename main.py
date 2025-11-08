from src.mask import get_mask_account
from src.mask import get_mask_card_number

if __name__ == '__main__':
    print(get_mask_card_number("1234567890123456"))
    print(get_mask_account("1234567890123456"))