#!/usr/bin/python3
from stem.descriptor import DocumentHandler
from stem.descriptor.remote import DescriptorDownloader
import linecache, os


#go to /var/spool/cron
#run crontab -e
#add these two lines. This will delete the consensus_dump file at first minute of every hour. Then download the Tor consensus file, save it to ~/Desktop/collection folder.
#01 * * * * rm /tmp/consensus_dump
#02 * * * * cd ~/Desktop && ./consensus_update.py

def download_consensus():
    downloader = DescriptorDownloader()
    consensus = downloader.get_consensus(document_handler = DocumentHandler.DOCUMENT).run()[0]

    with open('/tmp/consensus_dump', 'w') as descriptor_file:
        descriptor_file.write(str(consensus))

def filecopy():
    fifth_line = linecache.getline('/tmp/consensus_dump',4).split()
    commd = "cp /tmp/consensus_dump ./collection/"+fifth_line[1]+"_"+fifth_line[2]
    os.system(commd)

def main():
    try:
        download_consensus()
        filecopy()
    except Exception:
        try:
            download_consensus()
            filecopy()
        except Exception:
            try:
                download_consensus()
                filecopy()
            except Exception:
                pass
if __name__ == "__main__":
    main()
