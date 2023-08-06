from src.edc_utilities import edcSessionHelper, edcutils

url = "https://infaserveril26zi7vnj4uo.westeurope.cloudapp.azure.com:9085"
resourceName = "demo_custom_lineage"
fileName = "tryout.csv"
fullPath = "/tmp/files/tryout.csv"
scannerId = "LineageScanner"


def upload_csv():

    edc_helper = edcSessionHelper.EDCSession()
    edc_helper.initUrlAndSessionFromEDCSettings()

    url = edc_helper.baseUrl
          #+ "/access/1/catalog/data/objects"
    head = {'Content-Type': 'application/json'}

    edcutils.uploadResourceFileUsingSession(url, edc_helper.session, resourceName, fileName, fullPath, scannerId)

    edcutils.executeResourceLoadUsingSession(url, edc_helper.session, resourceName)

if __name__ == "__main__":
    upload_csv()
