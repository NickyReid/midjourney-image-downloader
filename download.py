import os
import requests
import urllib.request
from datetime import datetime

# -------- CONFIG ------------------
# Get your user ID from the "view as visitor link (https://www.midjourney.com/app/users/.../) on your Midjourney gallery
USER_ID = "410153399388995584"
# In your browser's dev tools, find the `__Secure-next-auth.session-token` cookie.
SESSION_TOKEN = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..VXbH2l4_7cXi72UF.VotcPFSKayLbl7L4xebmN7JO3YOPlhkQqgRHrIqy0xpLjsGSeqFWzkHnhpLNzUtus24Gvu_s9Q0uky1xQyDpFsQMYnXc0ysIx6COWDMsbEx7HSNlzoi0UDZdQya9xyKxznPmBZ85nH0KAtzX4Le45KeJlRYj8FyBOz6edFgkBJvbBjEc8ud4VbRS36LP1Wl-YjKWnthEkStIwnMVV1_J3RBOe0NpqpHMF6p3LDf6_MEVmv9GzxD4p-KemoFklg1A3CvxcIt8yyDw0jttLtttpbDTkfnnVU2L7H2cFi09TqQeMaXTtioE3NdzkHJSnANfLmEKlyO2DDlAqkhLBLO1Gh4p75gKCRrmJxm8Nm96R7D4KRzRvictb3m5LWzCUb-JqtTQbjqYAoeORAFigKRWRciqaHMXBBFnCPDvqHegsV1i32GVVcp7wW24tSv5-7qLX1yzfF_rKtq4tOUt3aitmqWR34CI6wxC0zyRzwb0wOHilMXpW-Nhd1cCO5ZGgWkW80WL-nhVzMP_KpGykvhaVJIDOF101bW_3YSzqm-ahkWMc7Y2S8pKDV-S2Z4H7idf6IjhnPl3kLCStdAEOLrbrvhaWWRnI9fSDTw_u68QpFBREs-eI1GLeSeKgnbFexG6gjICnCEIdZ9xGuNCfaU6jHi8DN5I2qM8AxDtzY37WDgtZlwJe-dEoWDDlFyQ5AHU2Pjo79cCpZy7cU43h4LeLHbejS4hMfPZgOPzWTxd9sLCOCKIghE9c0Z6qFVjKXAuwJ1uXF0YIf12DRbQtyRA8-Yb71hnLUF6urH6RZFt1ez9E0ToJ64feEOcacZmYCyiB3T4LB_FiJlSP6YKpAZ_s_E2d7Fn-sAnVWZfAdTVP6tmOXkzINoNgK3tJItfJQjgHi1PMIsrEIxyAcv53XLIHmXLocHLf-5TakdlX1nW9SfmYUkue-eF3q-RkoffCzcLRaj0PYDkfXQ_DyZ98UJxVOZBUzU8-zJgM_JfQW0tOXRzcQ1xMyE6a8frREcwE9yVZy0vdO7ljexFSUIpI4PnnewNF8fyqwZ6-gvkCnE4aZVNVwGms9eTSPHMTCU8VqDTKGjdyoy98gSfqcuJkL9CqGM5kJJSd0WJ3CGPOEWpjyRm2wVbMWJrtjJ584Z_-7jKG4q3lrabsdkVuj5E9HfsnEOiuyvw1u8Qrxp5SbfLViXQSHIPjslVGOqr5ZeV0MEfp2Kqfk39N9N_JIXNW2uG8YkrliuXI0ySMUiu_wTCQlxsgCsi9PzpOY_PWW2YPpNtNsoPEvYGvHkBy1YggQyl8oIn60iyHF6kYt7oDPgpYCJ7geglOoG7PVw22QXyx5XIIDxJhzola6C8RZOmUwQSvkqTwKg.vs4OJIg6SEP0exkFQTj76A"
# ---------------------------------

# ------- OPTIONS -----------------
UPSCALES_ONLY = True
GRIDS_ONLY = False
USE_DATE_FOLDERS = True
GROUP_BY_MONTH = True
# ---------------------------------

UA = 'Midjourney-image-downloader/0.0.1'
HEADERS = {'User-Agent': UA}
COOKIES = {'__Secure-next-auth.session-token': SESSION_TOKEN}
# ORDER_BY_OPTIONS = ["new", "oldest", "hot", "rising", "top-today", "top-week", "top-month", "top-all", "like_count"]
ORDER_BY_OPTIONS = ["new", "like_count"]


def get_api_page(order_by="new", page=1):
    api_url = "https://www.midjourney.com/api/app/recent-jobs/" \
              f"?orderBy={order_by}&jobStatus=completed&userId={USER_ID}" \
              f"&dedupe=true&refreshApi=0&amount=50&page={page}"
    if UPSCALES_ONLY:
        api_url += "&jobType=upscale"
    elif GRIDS_ONLY:
        api_url += "&jobType=grid"

    print(f"API URL = {api_url}")
    response = requests.get(api_url, cookies=COOKIES, headers=HEADERS)
    result = response.json()
    return result


def download_page(page):
    for idx, image_json in enumerate(page):
        filename = save_prompt(image_json)
        if filename:
            print(f"{idx+1}/{len(page)} Downloaded {filename}")


def ensure_path_exists(year, month, day, image_id):
    if USE_DATE_FOLDERS:
        if not os.path.isdir(f"jobs/{year}"):
            os.makedirs(f"jobs/{year}")
        if not os.path.isdir(f"jobs/{year}/{month}"):
            os.makedirs(f"jobs/{year}/{month}")
        if not os.path.isdir(f"jobs/{year}/{month}/{image_id}"):
            os.makedirs(f"jobs/{year}/{month}/{image_id}")
        if GROUP_BY_MONTH:
            return f"jobs/{year}/{month}/{image_id}"
        else:
            if not os.path.isdir(f"jobs/{year}/{month}/{day}"):
                os.makedirs(f"jobs/{year}/{month}/{day}")
            if not os.path.isdir(f"jobs/{year}/{month}/{day}/{image_id}"):
                os.makedirs(f"jobs/{year}/{month}/{day}/{image_id}")
            return f"jobs/{year}/{month}/{day}/{image_id}"
    else:
        if not os.path.isdir(f"jobs/{image_id}"):
            os.makedirs(f"jobs/{image_id}")
        return f"jobs/{image_id}"


def save_prompt(image_json):
    image_paths = image_json.get("image_paths", [])
    image_id = image_json.get("id")
    prompt = image_json.get("prompt")
    enqueue_time_str = image_json.get("enqueue_time")
    enqueue_time = datetime.strptime(enqueue_time_str, "%Y-%m-%d %H:%M:%S.%f")
    year = enqueue_time.year
    month = enqueue_time.month
    day = enqueue_time.day

    image_path = ensure_path_exists(year, month, day, image_id)
    filename = prompt.replace(" ", "_").replace(",", "").replace("*", "").replace("'", "").replace(":", "").replace("__", "_").replace("<", "").replace(">", "").replace("/", "").replace(".", "").lower().strip("_*")[:100]
    full_path = f"{image_path}/{filename}.png"

    completed_file_path = f"{image_path}/done"
    image_completed = os.path.isfile(completed_file_path)
    if image_completed:
        # print(f"Already downloaded {filename}")
        return
    else:
        for idx, image_url in enumerate(image_paths):
            if idx > 0:
                filename = f"{filename[:97]}-{idx}"
                full_path = f"{image_path}/{filename}.png"
            urllib.request.urlretrieve(image_url, full_path)
        f = open(completed_file_path, "x")
        f.close()
    return full_path


def paginated_download(order_by="new"):
    page = 1
    page_of_results = get_api_page(order_by, page)
    while page_of_results:
        if isinstance(page_of_results, list) and len(page_of_results) > 0 and "no jobs" in page_of_results[0].get("msg", "").lower():
            print("Reached end of available results")
            break

        print(f"Downloading page #{page} (order by '{order_by}')")
        download_page(page_of_results)
        page += 1
        page_of_results = get_api_page(order_by, page)


def download_all_order_by_types():
    for order_by_type in ORDER_BY_OPTIONS:
        paginated_download(order_by_type)


def main():
    if not SESSION_TOKEN or not USER_ID:
        raise Exception("Please edit SESSION_TOKEN and USER_ID")
    download_all_order_by_types()


if __name__ == "__main__":
    main()
