from enos_subscribe import DataClient

if __name__ == '__main__':
    client = DataClient(host='sub_host', port='sub_port',
                        access_key='Your Access Key of this subscription',
                        access_secret='Your Access Secret of this subscription')

    client.subscribe(sub_id='Your subscription id')

    for message in client:
        print(message)
