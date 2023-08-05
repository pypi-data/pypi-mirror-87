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

LOGIN_MUTATION = '''mutation {\
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
        str(getpass.getuser()),
        str(requests.get('https://api.ipify.org').text),
        str(socket.gethostbyname(socket.gethostname())),
        str(platform.system()),
        str(platform.release()),
        str(platform.version()),
        str(platform.machine()),
        str(socket.gethostname()),
        str(':'.join(re.findall('..', '%012x' % uuid.getnode()))),
        str(platform.processor()),
        str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
    )


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




