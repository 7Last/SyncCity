import requests


def deploy() -> None:
    # parse args received from command line
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--jar', type=str, required=True)
    jar = '/home/elena/docs/uni/swe/poc/flink/flink-job.jar'
    jobmanager_url = 'http://localhost:9001/jars/upload'

    headers = {
        'Content-Type': 'application/java-archive',
        'Content-Disposition': 'form-data; name="jarfile"; filename="flink-job.jar"',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    with open(jar, 'rb') as f:
        jar_content = f.read()

    response = requests.post(
        jobmanager_url,
        files={'jarfile': (jar, jar_content)},
        headers=headers,
    )

    if response.status_code == 200:
        print('Job deployed successfully')
    else:
        print('Job deployment failed, status code:', response.status_code)
        print('Response:', response.text)


if __name__ == '__main__':
    deploy()
