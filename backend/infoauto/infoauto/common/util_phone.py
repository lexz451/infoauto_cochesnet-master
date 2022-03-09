def normalize_phone(phone):
    if not phone or phone == 'anonymous':
        return phone
    if phone[:2] == '00':
        return '+' + phone[2:]
    if len(phone) == 9:
        return '+34' + phone
    if phone[:1] != '+':
        return '+' + phone

    return phone
