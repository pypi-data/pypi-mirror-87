import platform,socket,re,uuid,json,psutil,getpass,logging,requests

API_URL = 'https://solaris-api-rijk2jvapq-ue.a.run.app/'

COMPANY_CIK_NAME_QUERY = '''
    query {
        companies{
            cik
            name
        }
    }'''

COMPANY_CIK_TICKER_QUERY = '''
    query {
        companies{
            cik
            ticker
        }
    }'''

EQUITIES_MESSAGES_QUERY = '''
    query {
        messages
    }'''

COMPANY_QUERY = lambda cik, api_key : '''
    query {
        company(cik:"%s",apiKey : "%s"){
            name
            ticker
            sic 
            countryba
            cityba
            zipba 
            bas1
            bas2
            baph
            countryma
            stprma
            cityma
            zipma
            mas1
            mas2
            countryinc
            stprinc
            ein
            former
            changed
            income
            cash
            balance
            equity
        }
    }'''%(cik,api_key)

FINANCIAL_STATEMENT_QUERY = lambda cik, kind, api_key :'''
    query {
        company(cik:"%s",apiKey:"%s"){
            %s
        }
    }'''%(cik,api_key,kind)

def LOGIN_MUTATION():
    info = LOGIN_INFO()
    return '''mutation {\
        login(username : "%s",\
            publicIpAddress : "%s",\
            privateIpAddress : "%s",\
            platform : "%s",\
            platformRelease : "%s",\
            platformVersion : "%s",\
            architecture : "%s",\
            hostname : "%s",\
            macAddress : "%s",\
            processor : "%s",\
            ram : "%s"){\
                user{\
                    apiKey\
                }\
        }\
    }'''%(
        info['user'],
        info['puip'],
        info['prip'],
        info['system'],
        info['release'],
        info['version'],
        info['machine'],
        info['host'],
        info['name'],
        info['processor'],
        info['ram'] 
    )

def LOGIN_INFO():
    except_str = 'None'
    info = {}
    try: info['user'] = str(getpass.getuser())
    except: info['user'] = except_str
    try: info['puip'] = str(requests.get('https://api.ipify.org').text)
    except: info['puip'] = except_str
    try: info['prip'] = str(socket.gethostbyname(socket.gethostname()))
    except: info['prip'] = except_str
    try: info['system'] = str(platform.system())
    except: info['system'] = except_str
    try: info['release'] = str(platform.release())
    except: info['release'] = except_str
    try: info['version'] = str(platform.version())
    except: info['version'] = except_str
    try: info['machine'] = str(platform.machine())
    except: info['machine'] = except_str
    try: info['host'] = str(socket.gethostname())
    except: info['host'] = except_str
    try: info['name'] = str(':'.join(re.findall('..', '%012x' % uuid.getnode())))
    except: info['name'] = except_str
    try: info['processor'] = str(platform.processor())
    except: info['processor'] = except_str
    try: info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    except: info['ram'] = except_str
    return info

def take_a_sec():
    print('  - this could take a sec...')

def initialized(verbose):
    if verbose:
        print('> ✨\tApis connected.')

def failed():
    print('> ☠️\tClient failed to connect to api!')

def company(verbose,cik):
    if verbose:
        print('> 📦\tFetching company: %s ...'%cik)
    
def financial_statement(verbose,name,kind):
    if verbose:
        print('> 📦\tFetching financial statement: %s for %s ...'%(kind,name))

COMPANY_SCHEMA = lambda data : {
    'name': data['name'],
    'sic': data['sic'],
    'business_address':
        {
            "country":data['countryba'],
            "city": data['cityba'],
            "zip": data['zipba'],
            "adr1": data['bas1'],
            "adr2": data['bas2'],
        },
    'mailing_address':
        {
            "country":data['countryma'],
            "city": data['cityma'],
            "zip": data['zipma'],
            "adr1": data['mas1'],
            "adr2": data['mas2'],
            "state": data['stprma']
        },
    'phone': data['baph'],
    'country_incorporated': data['countryinc'],
    'state_incorporated' : data['stprinc'],
    'ein' : data['ein'],
    'former_name': data['former'],
    'income':data['income'],
    'balance':data['balance'],
    'cash':data['cash'],
    'equity': data['equity']
}




