from WMQuality.Emulators.DBSClient.MockDbsApi import MockDbsApi

urlGlobal = "https://cmsweb.cern.ch/dbs/prod/global/DBSReader"

mymock = MockDbsApi(urlGlobal)
results = mymock.listDataTiers()

for result in results:
    print result['data_tier_name']




