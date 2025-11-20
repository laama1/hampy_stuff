import csv
from vobject import vCard
import sys
import os
import datetime

# OH2CH Asterisk IP-PBX 
domain = "@haloo.oh2ch.fi"
phone_prefix = "sip:"
timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%SZ')
# Input CSV and output VCF filenames
csv_filename = "puhelinluettelo.csv"
vcf_filename = "puhelinluettelo.vcf"

def csv_to_vcf(csv_path, vcf_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(vcf_path, 'w', encoding='utf-8') as vcf_file:
            
            for row in reader:
                card = vCard()
                # Assuming columns: Callsign, Phone, Description
                if 'Callsign' in row:
                    card.add('fn').value = row['Callsign'] + ", "  + row['Description']
                if 'Phone' in row:
                    tel = card.add('tel')
                    tel.value = phone_prefix + row['Phone'] + domain
                    tel.type_param = 'SIP'
                # Add KIND:group
                kind = card.add('kind')
                kind.value = 'group'
                # Add REV:timestamp
                rev = card.add('rev')
                rev.value = timestamp
                vcard_str = card.serialize()
                # Insert VERSION:4.0 after BEGIN:VCARD
                vcard_lines = vcard_str.splitlines()
                if vcard_lines and vcard_lines[0].strip() == 'BEGIN:VCARD':
                    vcard_lines.insert(1, 'VERSION:4.0')
                vcf_file.write("\n".join(vcard_lines) + "\n")

if __name__ == "__main__":
    csv_to_vcf(csv_filename, vcf_filename)
    print(f"Converted {csv_filename} to {vcf_filename}")
