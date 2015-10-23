#!/usr/bin/env python
"""
A set of functions to help clean up messy data in LinkedIn
"""
def normalize_text(list_of_names):
    """ Unidecodes text and get rid of some common 
    """
    # import unidecode
    try:
        from unidecode import unidecode
    except ImportError:
        print("You don't have unidecode;")
        return
    
    # unidecode to begin with.
    decoded = [unidecode(x) for x in list_of_names]

    # Remove periods
    decoded = [x.replace(".","") for x in decoded]

    # List of people who have their first and last names backwards
    except_names = ['Alice','Una', 'John', 'Catherine','Howard Lam','Andy','Laura','Len','Leroy','Dirk','Day','Daniel','Davis','David','Habets']

    # list of titles that can be dropped. post are titles that come after the name, pre are titles that come before a name
    post_titles = ['II','III','MBA','FCMA','CGMA','IX','KBE','FCA','Jr','Sr','CPA','(MBA)','JD','PMP r ','PhD','PMP','MD','ARP','PE','PA','MRICS','DHA','RN-BC','CPHIMS','CENP','FACHE','ABC','PHR','MSC','IV','SRI','OPEN NETWORKER','Open Networker','ACA.HCIB.FICA.','CK','Cert','MBB','BBM PIN-27790699','617  500-3397','AM','CRPC r','FISM','BSc','jr','- Private WiFi','ACAHCIBFICA','CIA- CRMA','CA','ACCA']
    pre_titles = ['Sir','Dr','Prof','CA','CDir','The Honorable']
    normalized = []
    for i,name in enumerate(decoded):
        # Get rid of all parentheses
        for char in ['(',')','"','[',']']:
            name = name.replace(char,' ')
        # Drop everything after a comma
        if name.find(',')>0:
            if any([x in name[name.find(',')+1:] for x in except_names]):
                name = name.split(',')[1]+' '+name.split(',')[0]
            else:
                name = name.split(',')[0]
        # This is one case where it's advertisement
        for char in ['>>',':','|']:
            if name.find(char):
                name = name.split(char)[0]

        # Drop all email addresses
        name = re.sub(r'[(a-zA-Z0-0._%+-]+@.*',"",name).strip()

        # Remove titles
        for pt in post_titles:
            if ' '+pt in name:
                name = name.replace(' '+pt,'')
        for pt in pre_titles:
            if pt+' ' in name:
                name = name.replace(pt+' ','')
                
        # Remove trailing -
        name = re.sub(r'-$','',name).strip()
        
        # Replace all duplicate whitespaces
        name = ' '.join(name.split())
        normalized.append(name)
    
    return
