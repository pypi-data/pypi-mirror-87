from .dailycovid import *
if __name__ == '__main__':
    endpoint = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    parser = argparse.ArgumentParser(description='Create a tracker for COVID daily changes')
    parser.add_argument('-getdata',
                       action='store_true',
                       help=f'Download data from New York Times COVID endpoint\n{endpoint}')
    parser.add_argument('-state',
                       default=False,
                       help='U.S state')
    parser.add_argument('-county',
                       default=False,
                       help='County')
    parser.add_argument('-currentdata',
                       action='store_true',
                       help='Uses local us-counties.csv instead of downloading')
    parser.add_argument('-covidupdate',
                       action='store_true',
                       help='Update README\nNot ready')


    args = parser.parse_args()
    dictArgs = vars(args)

    counties = os.path.join(os.getcwd(),'counties','')
    if not os.path.exists(counties):
        os.mkdir(counties)


    if args.getdata: # Used when actually updating, shell online is easier
        # Got rid of curl, requests module now
        print('Downloading NY times COVID-19 CSV\n')
        r = requests.get(endpoint)
        print('http status:', r.status_code)
        endpointTxt = r.text # Writing to disk and keeping in memory
        with open('us-counties.csv', 'w+') as f:
            f.write(r.text)

    if args.state and args.county:
        if not args.getdata:
            endpointTxt = open('us-counties.csv', 'r').read()

        state = states[dictArgs['state'].upper()].lower()
        county = dictArgs['county'].lower()
        query = f',{county},{state},'
        countyStateStr = f'{state},{county}'
        fname = '_'.join(countyStateStr.lower().split(',')) + '.csv'

        stateCountyData = [i for i in endpointTxt.splitlines() if query.lower() in i.lower()]

        main(lines=stateCountyData,
             state=state,
             county=county,
             countiesPath=counties)
