from vobject import vCard
import yaml
import pandas as pd
import datetime

with open('config.yaml') as file:
    conf = yaml.safe_load(file)

# OH2CH Asterisk IP-PBX domain
domain = conf.get('domain')
vcf_filename = conf.get('output_vcf_file')

sheetDF = pd.read_csv(conf.get('sheet_url'))
phonelist = sheetDF.values.tolist()[3:]

timestamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%SZ')

def csv_to_vcf(phonelist, output_file):
    vcf_file = open(output_file, 'w', encoding='utf-8')
    for row in phonelist:
        card = vCard()
        # Assuming columns: 0 = number, 1 = operator, 2 = extra info
        # Check if row[0] is defined and not NaN
        if row[0] is not None and str(row[0]).lower() != 'nan':
            fn_value = str(row[1])
            # Check if row[2] is defined and not NaN
            if row[2] is not None and str(row[2]).lower() != 'nan':
                fn_value += ", " + str(row[2])
            card.add('fn').value = fn_value
        else:
            continue  # Skip rows without a valid number

        tel = card.add('tel')
        tel.value = "sip:" + row[0] + "@" + domain
        tel.type_param = 'SIP'
        # Add KIND:group
        kind = card.add('kind')
        kind.value = 'group'
        # Add REV:timestamp
        rev = card.add('rev')
        rev.value = timestamp
        vcard_str = card.serialize()
        vcard_lines = vcard_str.splitlines()
        vcf_file.write("\n".join(vcard_lines) + "\n")

if __name__ == "__main__":
    csv_to_vcf(phonelist, vcf_filename)
    print(f"Phone list conversion done, check {vcf_filename}")
