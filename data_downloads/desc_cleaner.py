import re



def description_clean(desc: str) -> str:
        # Empty description
    desc = desc.strip()
    
    if desc == '':
        return ''
    
    # Adding gmail and yahoo
    lowered_desc = desc.lower()
    if 'gmail' in lowered_desc and '@' not in lowered_desc:
        splitted_email = lowered_desc.split('gmail')
        desc = splitted_email[0] + '@gmail' + splitted_email[1]

    if 'yahoo' in lowered_desc and '@' not in lowered_desc:
        splitted_email = lowered_desc.split('yahoo')
        desc = splitted_email[0] + '@yahoo' + splitted_email[1]
    desc = desc.upper()
    
    
    replacements = {
        'EB-':'',
        'EB -':'',
        'MM:':'',
        'MM: ':'',
        '+':'',
        '*':'',
        '%':'',
        'qpay':'',
        '(ГОЛОМТБАНКИКСМЕТАХХК)':''
    }
    
    # CLeaning from outside
    for key in replacements.keys():
        if key in desc:
            desc = desc.replace(key, '')
    
    description = desc.upper()
    data_arr = description.split(' ')

    result = []
    for item in data_arr:
        if item != '':
            result.append(item)
    
    tmp = ''.join(result).strip().lower()

    email = ''
    is_found_invalid = False
    
    for index, ltr in enumerate(tmp):
       if ltr == '@':
           email += tmp[:index]
           sub_email = tmp[index:]
           
           for idx, lt in enumerate(sub_email):
                if lt == '.':
                    email += sub_email[:idx]
                    sub_sub_email = sub_email[idx:]
                    
                    for id, l in enumerate(sub_sub_email):
                        if l == '(' or l == '-' or l == '_' or l == ',':
                            email += sub_sub_email[:id]
                            is_found_invalid = True
                            break
                    if is_found_invalid == False:
                        email += sub_sub_email


    result = re.sub(r'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', email) 
    return result.strip()
