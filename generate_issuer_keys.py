import json
from generate_sig import generate_keys


if __name__ == "__main__":
    issuer_sk, issuer_pk = generate_keys(True) # make random=True

    print("-------------ISSUER KEYS----------------")
    print("-------------PUBLIC KEY-------------")
    print(issuer_pk)
    print("-------------PRIVATE KEY-------------")
    print(issuer_sk)
    print("----------------END-----------------")
    
    # Your dictionary
    dict_obj = {
        'issuer_pk': issuer_pk,
        'issuer_sk': issuer_sk
    }

    # Specify your filename
    filename = 'issuer_keys.json'

    print(f"---------WRITING KEYS TO {filename}------------")

    # Write to file
    with open(filename, 'w') as file:
        json.dump(dict_obj, file)


    print("------------------WRITING COMPLETE-------------------")
