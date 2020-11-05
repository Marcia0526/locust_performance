import os
import pandas as pd
import queue
from locust import HttpUser, TaskSet, between, task
from common.auth import dso_authorization_header

env = os.environ.get('env') or 'dev'
api_authorization_header = dso_authorization_header(env)
es_queue = queue.Queue()
opp_queue = queue.Queue()


class UserBehavior(TaskSet):

    def on_start(self):
        df = pd.read_csv('../input/parameters_input.csv')
        for item in df.values:
            es_queue.put(item[0])
            opp_queue.put(item[1])

    @task(2)
    def search_es(self):
        key = es_queue.get()
        with self.client.get("/search?name=" + key, name="/search", headers=api_authorization_header,
                             catch_response=True) as response:
            es_queue.put_nowait(key)
            result_status = key in response.text
            if response.status_code == 200 and result_status:
                response.success()
            else:
                response.failure('Failed')

    @task(1)
    def opp_detail(self):
        opp_id = opp_queue.get()
        with self.client.get("/opportunities/%d" % opp_id, name="/opp_detail", headers=api_authorization_header,
                             catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                opp_queue.put(opp_id)
                # print(response.status_code)
            opp_queue.put(opp_id)


class EsUser(HttpUser):
    tasks = [UserBehavior]
    # tasks = {UserBehavior: 3, OtherBehavior: 1}
    wait_time = between(0, 1)
    # host = "https://dso-api-test-dot-days-sales-outstanding-265916.appspot.com"

if __name__ == "__main__":
    # import os
    os.system("locust -f ../locustfiles/es_test.py -H https://dso-api-test-dot-days-sales-outstanding-265916.appspot.com -u 100 -r 10 --headless")


